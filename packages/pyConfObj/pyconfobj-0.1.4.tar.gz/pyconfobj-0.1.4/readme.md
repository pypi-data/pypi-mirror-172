#pyConfObject

Define configuration files from classes and its relations

It allows to load/export configuration from classes to json/yaml files easily
It allows to have code completion on your configuration objects and not depend on dictionaries


# Example 

```python
from numbers import Number
from confObj import ConfObj

class PgServerConf(ConfObj):
    ip: str = ""
    port: Number = 5432
    username:str = ""
    password:str = ""

class MainConf(ConfObj):
    pgconf: PgServerConf = PgServerConf()
    timezone:str = "UTC"


if __name__ == "__main__":
    conf = MainConf()
    print("Default configuration:")
    print(conf.as_json())
    conf.pgconf.username = "admin"
    print("Modified configuration for pg: ")
    print(conf.pgconf.as_json())
```

# Usage

The idea behind this module is to create a configuration object that can be organized as a tree and IDE's code completion features can be used. 

It should be used as:
 - Define the structure of the whole configuration defining classes that inherit from `confObj``
 - [optional] Assign default values to configuration items on code
 - Output the defined configuration tree as a file (either yaml or json)
   - [optional] Fix default values on the generated file
 - On runtime, either load configuration or use default hardcoded values.
   - [optional] On runtime, values can be changed and saved to file if necessary
