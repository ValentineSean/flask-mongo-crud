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
- ROOT_URL can be configured in application's configurations and it is *optional*.
- If configured, it is used by all generated endpoints.
- Code snippet in **Basic Application** section shows how to configure ROOT_URL.
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
        - *collection_name* is the actual name of the collection in MongoDB.
        - *model_url_prefix* allows to have unique URLs for each and every model.
        - If these configurations are not defined, default configurations will be used.
    - Model Class Code Snippet:
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
    app.config["MODELS_DIRECTORY"] = "<CUSTOM_NAME>"
    # If root URL is not defined, generated endpoints will not have a root URL
    app.config["ROOT_URL"] = "/flask-mongo-crud/v1"

    mongo = PyMongo()

    app.config["MONGO_URI"] = "mongodb://<DB_HOST>:<DB_PORT>/<DB_NAME>"

    flask_crud = FlaskMongoCrud()
    flask_crud.init_app(app, request, mongo)

    if __name__ == "__main__":
        app.run(debug=True)
    ```

## Generated Endpoints Examples and HTTP Methods:
- HTTP Methods supported are POST, GET, PUT, PATCH and DELETE.
- The following generated endpoints will be using model snippet defined earlier in **Configuration** as well **Basic Application** sections.
- These endpoints are after application base URL:
    `<IP_ADDRESS>:<PORT_NUMBER>`
- Basic complete URL looks like:
    
    `<IP_ADDRESS>:<PORT_NUMBER>/<ROOT_URL>/<MODEL_URL_PREFIX>/<RESOURCE_NAME>`

    or

    `<IP_ADDRESS>:<PORT_NUMBER>/<ROOT_URL>/<MODEL_URL_PREFIX>/<RESOURCE_NAME>/<RESOURCE_IDENTIFIER>`
- RESOURCE_NAME is automatically generated, and a developer can not customize it.
- RESOURCE_IDENTIFIER should be the document ID.
- Given the generated URL:
    `localhost:5000/flask-mongo-crud/v1/professor-subject-test/professor-subject/66c40a7d1e7029dbdf77df02`:
    - "/professor-subject" is the RESOURCE_NAME.
    - "/66c40a7d1e7029dbdf77df02" is the RESOURCE_IDENTIFIER.
    - In case ROOT_URL is not specified:
        - In the above URL, ROOT_URL is `/flask-mongo-crud/v1`.
        - The URL without ROOT_URL is `/professor-subject-test/professor-subject`
    - In case MODEL_URL_PREFIX is not specified:
        - In the above URL, MODEL_URL_PREFIX is `/professor-subject-test`
        - The URL without MODEL_URL_PREFIX is `/flask-mongo-crud/v1/professor-subject`
    - In case both ROOT_URL and MODEL_URL_PREFIX are not specified:
        - The URL without both is `/professor-subject`
        - It contains only the RESOURCE_NAME.

#### POST
- Saves new document into the database
- Only saves one document at a time.
- Supports only JSON data.
- Fields can be None (null).

- JSON Payload Example:
    ```json
    {
        "professor_first_name": "Foo",
        "professor_last_name": "Bar",
        "subject_name": "Comp Science"
    }
    ```

#### GET
- Retrieves documents from the database.
- Can retrieve only one document or a list of documents.
- To retrieve only one document, include RESOURCE_IDENTIFIER in the URL.
- This RESOURCE_IDENTIFIER will be used to identify that one document.
- If RESOURCE_IDENTIFIER is not provided, list of documents will be retrieved.
- Developer can opt for pagination when retrieving many documents.

    ##### Pagination:
        - To paginate, provide the following query parameters:
            - **pagination** = *true*
            - **limit** = "number of documents" per page. Should be integer greater than 0
            - **page** = "page number". Should be integer greater than 0

#### PUT
- Updates one document at a time.
- That document is identified by RESOURCE_IDENTIFIER in the URL.
- If there is no such document in the database, a new document will be created.

#### PATCH
- Updates one document at a time.
- That document is identified by RESOURCE_IDENTIFIER in the URL.
- If there is no such document in the database, the endpoint will return a payload:
    ```json
    {
        "message": "<RESOURCE_NAME> not found"
    }
    ```

#### DELETE
- Deletes one document at a time.
- That document is identified by RESOURCE_IDENTIFIER in the URL.
- If there is no such document in the database, the endpoint will return a payload:
    ```json
    {
        "message": "<RESOURCE_NAME> not found"
    }
    ```