# Flask Import/Export

Database import/export functionality for database stores under Flask

1. [Example Usage](#example-usage)
2. [Options](#options)

## Example Usage

```python
from frappyflaskauth import check_login_state
from frappyflaskimpex import register_endpoints
from flask import Flask

app = Flask(__name__)
# create a dictionary of stores (key > AbstractMongoStore subclass)
stores = {}  
# register the endpoints
register_endpoints(app, stores, options={
    "permission": "impex",
    "login_check_function": check_login_state,
    "temp_folder": "_data/temp",
})
```

## Options

Options for the `register_endpoints` function are:

- `api_prefix` - default `/api/impex` - is the prefix under which the endpoints will be registered. This should
 match the prefix used in the front-end.
- `permission` - default `None` - the permission required to manage imports and exports, if `None` is provided the user 
  just needs to be logged in.  
- `login_check_function` - default `None` - provide a function that performs authentication and uses Flask's `abort` in
 case the login / permission check fails. The function has 1 parameter for the required permission. You can use
 `check_login_state` from the `frappyflaskauth` package.
- `temp_folder` - default `_temp` - a folder path which will be used to temporarily store zip/json files used for import
  and export.
