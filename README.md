# Google Protobuffer to AVRO

## Rationale

Fix and Refactor the current ``proto_to_avro.py``` tool

## Compile protobuffer

Reference (gist)[https://gist.github.com/txomon/5c8eb8402989a26a016265009dc51e67]

To compile protobuffer with a docker container:

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

## Refactoring

I think the main structure of the code is OK. Every function executes a different task, and probably some tasks could be joined to optimize the code, but the main idea, in my opinion is ok.

The problem was in the coding/execution. There were many basic OOP principles "raped", like encapsulation (using staticmethods and not understanding what they are), confusing private and public methods... Also the distribution (order) of functions was totally wrong if you want to facilitate somebody to read the code and understand what is going on, it is a good practice to align the order of the definition of methods with their calls (IMHO). Also the type hints were badly managed and some functions that returned something din't have a type hint but others did. If you use type hinting then use it in a homogeneus manner all over the codebase.