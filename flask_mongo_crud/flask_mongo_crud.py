import os
import re
import inspect
import importlib
import json
import traceback

from bson.json_util import dumps
from bson.objectid import ObjectId

# Provides a CRUD System Integrated to Flask
class FlaskMongoCrud(object):
    def __init__(self, app=None, mongo=None) -> None:
        self.app = None
        self.mongo = None

        if app:
            self.init_app(app)


    # Initialize the CRUD System with a Flask application, Flask request & mongo instances.
    def init_app(self, app, request, mongo):
        self.app = app
        self.app.flask_crud = self
        self.request = request
        self.mongo = mongo

        app_configs = self._load_config()

        app.config["MONGO_URI"] = f"mongodb://{app_configs['db_host']}/{app_configs['database_name']}"

        mongo.init_app(app)

        """
            Get Caller Absolute Path
            But Need to figure out how to accommodate other OS (MacOS, Linux, etc)
        """
        callee_abs_path = os.path.abspath((inspect.stack()[0])[1]) # No use at the moment
        abs_path = os.path.abspath((inspect.stack()[1])[1])
        caller_directory = os.path.dirname(abs_path)
        project_root = caller_directory.split("\\")[-1]

        # -------------------------------------------------------------------------------

        url_prefix = app_configs["url_prefix"]
        models = self.get_models(project_root=project_root)

        for model in models:
            app.route(f"{url_prefix}/{model.get('route_model_name')}", methods=["GET", "POST"])(self.db_interface(
                self.request,
                self.mongo,
                model.get('route_model_name'),
                model.get("collection_name"),
                model.get("model_class"),
                id=None
            ))
            app.route(f"{url_prefix}/{model.get('route_model_name')}/<id>", methods=["GET", "PUT", "PATCH", "DELETE"])(self.db_interface(
                self.request,
                self.mongo,
                model.get('route_model_name'),
                model.get("collection_name"),
                model.get("model_class"),
                id
            ))


    # Load the configurations from the Flask configuration
    def _load_config(self):
        options = dict()

        db_username = self.app.config.get("DB_USERNAME")
        if db_username:
            options["db_username"] = db_username

        db_password = self.app.config.get("DB_PASSWORD")
        if db_password:
            options["db_password"] = db_password

        db_host = self.app.config.get("DB_HOST")
        if db_host:
            options["db_host"] = db_host

        database_name = self.app.config.get("DATABASE_NAME")
        if database_name:
            options["database_name"] = database_name

        url_prefix = self.app.config.get("URL_PREFIX")
        if url_prefix:
            options["url_prefix"] = url_prefix


        return options
    

    # GET MODELS
    def get_models(self, project_root):
        package_name = "models"

        files = os.listdir(package_name)

        models = list()

        for file in files:
            if file not in ["__init__.py", "__pycache__"]:
                if file[-3:] != ".py":
                    continue

                file_name = file[:-3]

                module_name = ".." + package_name + "." + file_name
                
                for name, cls, in inspect.getmembers(importlib.import_module(module_name, package=f"{project_root}.models"), inspect.isclass):
                    split = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()

                    route_model_name = split[0].lower()
                    db_model_name = split[0].lower()

                    x = 1

                    if len(split) > 1:
                        while x < len(split):
                            route_model_name = route_model_name + f"-{split[x].lower()}"
                            db_model_name = db_model_name + f"_{split[x].lower()}"
                            x = x + 1

                    custom_name = None
                    if hasattr(cls, "collection_name"):
                        custom_name = cls.collection_name

                    else:
                        custom_name = db_model_name

                    
                    models.append({
                        "route_model_name": route_model_name,
                        "collection_name": custom_name,
                        "model_class": cls,
                    })

        return models

    # DB INTERFACE
    def db_interface(self, request, mongo, route_model_name, collection_name, model_class, id):
        if id == None:
            def _dynamic_function():
                if request.method == "POST":
                    entity = request.json

                    model_attributes_list = list(inspect.signature(model_class).parameters)

                    new_entity = {}

                    for z in model_attributes_list:
                        new_entity[z] = entity[z]

                    # Add Data to DB
                    new_entity_id = mongo.db[collection_name].insert_one(new_entity).inserted_id

                    new_entity = mongo.db[collection_name].find_one({"_id": ObjectId(new_entity_id)})
                    new_entity = json.loads(dumps(new_entity))
                    
                    return new_entity
                    

                elif request.method == "GET":
                    # Some logic here...
                    try:
                        entities =  mongo.db[collection_name].find()

                        if entities:
                            entities = json.loads(dumps(entities))

                        else:
                            entities = []

                    except:
                        traceback.print_exc()
                        entities = []

                    return entities
            
            _dynamic_function.__name__ = route_model_name

            return _dynamic_function

        else:
            def _dynamic_function(id):

                if request.method == "GET":
                    # Some logic here...
                    try:
                        entity =  mongo.db[collection_name].find_one({"_id": ObjectId(id)})

                        if entity:
                            entity = json.loads(dumps(entity))

                        else:
                            entity = {}

                    except:
                        traceback.print_exc()
                        entity = {}

                    return entity

                elif request.method == "PUT":
                    entity = request.json

                    model_attributes_list = list(inspect.signature(model_class).parameters)

                    new_entity = {}

                    for z in model_attributes_list:
                        if entity.get(z) is None:
                            new_entity[z] = None
                            continue
                        new_entity[z] = entity[z]

                    # Add Data to DB
                    # old_entity = mongo.db[collection_name].find_one({"_id": ObjectId(id)})

                    mongo.db[collection_name].update_one(
                        {"_id": ObjectId(id)},
                        {"$set": new_entity},
                        upsert=True
                    )

                    new_entity = mongo.db[collection_name].find_one({"_id": ObjectId(id)})
                    new_entity = json.loads(dumps(new_entity))
                    
                    return new_entity

                elif request.method == "PATCH":
                    entity = request.json
                    
                    model_attributes_list = list(inspect.signature(model_class).parameters)

                    new_entity = {}

                    for z in model_attributes_list:
                        if entity.get(z) is None:
                            continue
                        new_entity[z] = entity[z]

                    # Add Data to DB
                    old_entity = mongo.db[collection_name].find_one({"_id": ObjectId(id)})
                    if old_entity == None:
                        return {
                            "message": f"{route_model_name} not found"
                        }

                    mongo.db[collection_name].update_one(
                        {"_id": ObjectId(id)},
                        {"$set": new_entity},
                    )

                    new_entity = mongo.db[collection_name].find_one({"_id": ObjectId(id)})
                    new_entity = json.loads(dumps(new_entity))
                    
                    return new_entity

                elif request.method == "DELETE":
                    old_entity = mongo.db[collection_name].find_one({"_id": ObjectId(id)})
                    if old_entity == None:
                        return {
                            "message": f"{route_model_name} not found"
                        }

                    mongo.db[collection_name].delete_one({"_id": ObjectId(id)})
                    return {
                        "message": f"{route_model_name} deleted successfully"
                    }
                
            _dynamic_function.__name__ = route_model_name + "-one"

            return _dynamic_function