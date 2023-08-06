import os
import json
from datetime import datetime
from zipfile import ZipFile
from pbu import default_options, list_to_json
from flask import jsonify, request, send_file, abort


class _DummyUser:
    def __init__(self, permissions):
        self.email = "anonymous"
        self.permissions = permissions


_DEFAULT_OPTIONS = {
    "api_prefix": "/api/impex",
    "permission": "admin",
    "logic_check_function": None,
    "temp_folder": "_temp",
}


def register_endpoints(app, stores: dict, options={}):
    final_options = default_options(_DEFAULT_OPTIONS, options)

    api_prefix = final_options["api_prefix"]
    permission = final_options["permission"]
    login_check_function = final_options["login_check_function"]
    temp_folder = final_options["temp_folder"]

    # check if temp folder exists, if not attempt to create it
    if not os.path.isdir(temp_folder):
        try:
            os.mkdir(temp_folder)
        except BaseException as be:
            print(f"Cannot create 'temp_folder': {temp_folder}. Please check the parent directory exists and your app "
                  f"has sufficient permissions")
            raise be  # ensure app crashes

    # clean up any previous export files
    for file_name in os.listdir(temp_folder):
        os.remove(os.path.join(temp_folder, file_name))

    def _check_login_state(_permission=None):
        if login_check_function is not None:
            return login_check_function(_permission)
        return _DummyUser([_permission])

    @app.route(api_prefix, methods=["GET"])
    def get_data_base_store_list():
        _check_login_state(permission)
        result = {}
        for store_key in stores:
            result[store_key] = [stores[store_key].__class__.__name__,
                                 stores[store_key].collection.estimated_document_count()]
        return jsonify(result)

    @app.route(f"{api_prefix}/<store_key>", methods=["GET"])
    def export_database_store_by_store_key(store_key: str):
        _check_login_state(permission)
        if store_key not in stores:
            abort(400, description=f"Store with store key {store_key} does not exist.")

        # fetch all documents
        all_docs = stores[store_key].get_all()
        if isinstance(all_docs, tuple):
            # in case the get_all returns the number of docs as well
            all_docs = all_docs[0]

        # prepare json file
        json_file = f"export_{store_key}.json"
        json_path = os.path.join(temp_folder, json_file)
        if os.path.exists(json_path):
            os.remove(json_path)

        # write json file
        fp = open(json_path, "w")
        json.dump(list_to_json(all_docs), fp)
        fp.close()

        # zip json file
        zip_path = os.path.join(temp_folder, f"export_{store_key}.zip")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        with ZipFile(zip_path, "w") as zip_file:
            zip_file.write(json_path, json_file)

        # clean up json file
        os.remove(json_path)

        # send zip file
        return send_file(zip_path, mimetype="application/zip",
                         download_name=f"export_{store_key}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.zip")

    @app.route(f"{api_prefix}/<store_key>", methods=["POST"])
    def import_database_store_by_store_key(store_key: str):
        _check_login_state(permission)
        if store_key not in stores:
            abort(400, description=f"Store with store key {store_key} does not exist.")
        store = stores[store_key]

        # prepare upload path
        upload_path = os.path.join(temp_folder, f"import_{store_key}.zip")
        if os.path.exists(upload_path):
            os.remove(upload_path)

        # save zip file
        upload_file = request.files.get("file")
        upload_file.save(upload_path)

        # prepare extraction of json file
        json_file_name = f"export_{store_key}.json"
        json_path = os.path.join(temp_folder, f"import_{store_key}.json")
        if os.path.exists(json_path):
            os.remove(json_path)

        # extract zip file
        with ZipFile(upload_path, "r") as zip_file:
            extracted = zip_file.extract(json_file_name, temp_folder)
            os.rename(extracted, json_path)

        # clean up zip file
        os.remove(upload_path)

        # parse json file
        fp = open(json_path, "r")
        json_docs = json.load(fp)
        fp.close()
        # clean up json file
        os.remove(json_path)

        parsed_docs = list(map(lambda doc: store.object_class.from_json(doc), json_docs))

        # read import options submitted via request
        request_options = json.loads(request.form["options"])
        truncate_before_import = request_options.get("truncate", True)

        # delete old / existing documents before import
        if truncate_before_import:
            store.collection.delete_many({})

        # insert new documents
        for obj in parsed_docs:
            store.create(obj)

        return jsonify({
            "status": True,
            "count": len(parsed_docs),
        })
