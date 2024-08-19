# Flask Mongo CRUD Docs

## Features
- Automatically generates CRUD endpoints from defined model.
- Allows to specify custom MongoDB collection name of each model.
- Allows to customize app base URL as well as each model's url prefix.
- Allows to paginate when getting many documents from collection. ***TO BE IMPROVED***
- Allows documents sorting (Ascending or Descending order). ***COMING SOON***

## Installation
```bash
pip install flask-mongo-crud
```

## Configuration
- Empty __init__.py file required in project root directory.
- Models:
    - Models directory is required in the project root directory:
    - If custom name Models directory is not defined, as:
        ~~~python
        app.config[MODELS_DIRECTORY] = "<CUSTOM_NAME>"
        ~~~
        - then, default “models” directory will be used.
        - This is where models files are defined.
        - Inside these files declare models classes and their configurations such as:
            - *collection_name [OPTIONAL]*
            - *model_url_prefix [OPTIONAL]*
        - If these configurations are not defined, default configurations will be used.
    - Model Code Snippet:
        ```python
        class ProfessorSubject:
            collection_name = "professor_subjects"
            model_url_prefix = "/professor-subject-test"

            # These are document fields
            def __init__(self, professor_first_name, professor_last_name, subject_name):
                self.professor_first_name = professor_first_name
                self.professor_last_name = professor_last_name
                self.subject_name = subject_name
        ```

## Basic Application
- Code Snippet:
    ```python
    from flask import Flask, request
    from flask_pymongo import PyMongo
    from flask_mongo_crud import FlaskMongoCrud

    app = Flask(__name__)
    # If models directory is not defined, default "models" directory will be used
    app.config["MODELS_DIRECTORY"] = "db_classes"
    # If root URL is not defined, generated endpoints will not have a root URL
    app.config["ROOT_URL"] = "/flask-mongo-crud/v1"

    mongo = PyMongo()

    app.config["MONGO_URI"] = "mongodb://<DB_HOST>:<DB_PORT>/<DB_NAME>"

    flask_crud = FlaskMongoCrud()
    flask_crud.init_app(app, request, mongo)

    if __name__ == "__main__":
        app.run(debug=True)
    ```

## API / HTTP Methods / Endpoints

## Examples

This is a Flask Library that enables a developer to define database models, and the library will automatically generate CRUD endpoints. ;)