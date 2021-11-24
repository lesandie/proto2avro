# Google Protobuffer to AVRO

## Rationale

Fix and Refactor the current ```proto_to_avro.py``` tool

## Compile protobuffer

Reference [gist](https://gist.github.com/txomon/5c8eb8402989a26a016265009dc51e67)

Compile .proto files using the protobuffer compiler provided in a docker container:

```bash
$ docker run --rm -ti -v $(pwd)/proto:/defs -v $(pwd)/tmp:/mnt namely/protoc-all -d /defs/ -l python -o /mnt
```

This compilation process generates various files in tmp and the *grpc* ones are to be discarded, because the script will
generate this error:

```bash
AttributeError: module 'Decimal_pb2_grpc' has no attribute 'DESCRIPTOR'
```

* Create a Python virtualenv (3.8 or 3.9), you can use pyenv.

* Install the requirements:

```bash
(virtualenv)$ pip install -r requirements.txt
```


## Usage

```bash
$ python proto2avro.py --pb2_path ./tmp --avro_path ./avro
```

## Refactoring

I think the main structure of the code is OK. Every function seems to solve a different problem/task, but there are some that can be joined to optimize the code and avoid extra calls (done). If some SOLID principles would have been applied, the code would look much better.

Problems in the coding/execution that has been corrected:

* There were some basic OOP patterns "raped", like encapsulation (using Python static methods and not understanding what they are).
* Regarding public and private methods (and properties), although in Python privates are accessible, it is a good pattern to signal that a method or property is private to avoid other users to mess with the values of the properties or call unecessary methods. In this case both paths should be private and cannot be changed once you executed the script. The same for the types_conversion. 
* The distribution (order) of functions was wrong, if you want to facilitate somebody to read the code and understand what is going on, it is a good practice to align the order of the functions definition with their calls (IMHO).
* Default parameters usage was very confusing (params=params).
* Some functions were not documented properly, and there were few comments in the code.
* The type hints were badly managed and some functions that returned something din't have a type hint but others did. Using type hinting improves the readability but it has to be used in a homogeneus manner all over the codebase.
* Some functions were refactored/deleted:
  * Using ```continue``` or ```break``` is not a good practice.
  * Some functions were unnecessary

