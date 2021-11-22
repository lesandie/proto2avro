# Google Protobuffer to AVRO

## Rationale

Fix and Refactor the current ``proto_to_avro.py``` tool

## Compile protobuffer

Reference (gist)[https://gist.github.com/txomon/5c8eb8402989a26a016265009dc51e67]

To compile protobuffer with a docker container:

```bash
$ docker run --rm -ti -v $(pwd)/proto:/defs -v $(pwd)/tmp:/mnt namely/protoc-all -d /defs/ -l python -o /mnt
```

* Create a Python virtualenv (3.8 or 3.9), you can use pyenv.

* Install the requirements:

```bash
(virtualenv)$ pip install -r requirements.txt
```
