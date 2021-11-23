import importlib.util
import json
import logging
import os.path
import sys
import typing
import click
from google.protobuf.descriptor import Descriptor, FieldDescriptor


class SchemaConvertor:
    def __init__(self, pb2_path: str, avro_path: str):
        self.pb2_path = pb2_path
        self.avro_path = avro_path
        self.type_to_convertor = {
            FieldDescriptor.TYPE_DOUBLE: {"type": "float", "method": self.__read_through},
            FieldDescriptor.TYPE_FLOAT: {"type": "float", "method": self.__read_through},
            FieldDescriptor.TYPE_INT64: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_UINT64: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_INT32: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_FIXED64: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_FIXED32: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_BOOL: {"type": "boolean", "method": self.__read_through},
            FieldDescriptor.TYPE_STRING: {"type": "string", "method": self.__read_through},
            FieldDescriptor.TYPE_GROUP: {"method": self.__not_readable},
            FieldDescriptor.TYPE_MESSAGE: {"method": self.__convert_message_type},
            FieldDescriptor.TYPE_BYTES: {"type": "string", "method": self.__read_through},
            FieldDescriptor.TYPE_UINT32: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_ENUM: {"method": self.__not_readable},
            FieldDescriptor.TYPE_SFIXED32: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_SFIXED64: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_SINT32: {"type": "int", "method": self.__read_through},
            FieldDescriptor.TYPE_SINT64: {"type": "int", "method": self.__read_through},
        } 
    
    # Many of these methods are private methods and not static methods
    def __import_pb2_module(self, root: str, compiled_proto: str) -> str:
        module_basename = os.path.basename(root)
        module_path = f"{module_basename}/{compiled_proto}.py"
        spec = importlib.util.spec_from_file_location(
            name=compiled_proto, location=module_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[compiled_proto] = module
        spec.loader.exec_module(module)
        return importlib.import_module(name=compiled_proto)

    def __fix_import_error(self, root: str, filename: str) -> None:
        filepath = f"{root}/{filename}"
        with open(filepath, "r+") as f:
            content = f.read()
            new_content = content.replace(
                "from types import", "from dwh.domain.pb2.types import"
            )
            f.truncate(0)
            f.seek(0)
            f.write(new_content)

    def __read_through(self, field_name: str, field_type: str) -> typing.Dict[str, str]:
        """
        system default is used: zero for numeric types, the empty string for strings, false for bools
        """
        return {"name": field_name, "type": ["null", field_type], "default": None}

    def __not_readable(self, field_name: str, field_type: str):
        raise TypeError(f"Type {field_type} not supported")
    
    def __convert_message_type(self, field: FieldDescriptor) -> typing.Dict[str, str]:
        message_type_dict = field.message_type.file.message_types_by_name
        
        if len(message_type_dict) == 1:
            if field.message_type.full_name == "google.protobuf.Timestamp":
                avro_field = {
                    "name": field.name,
                    "type": ["null", "float"],
                    "logicalType": "timestamp-micros",
                    "default": None,
                }
            elif field.message_type.full_name == "Decimal":
                avro_field = {
                    "name": field.name,
                    "type": ["null", "bytes"],
                    "logicalType": "decimal",
                    "precision": 38,
                    "scale": 9,
                    "default": None,
                }
            else:
                self.__not_readable(
                    field_name=field.name, field_type=field.message_type.full_name
                )
        
        return avro_field
    
    def __event_class_from_filename(self, root: str, filename: str):
        compiled_proto = filename.rpartition(".")[0]
        try:
            pb2_module = self.__import_pb2_module(root, compiled_proto)
        except ImportError:
            self.__fix_import_error(root, filename)
            pb2_module = self.__import_pb2_module(root, compiled_proto)

        proto_message = pb2_module.DESCRIPTOR.message_types_by_name  # noqa

        if len(proto_message.keys()) != 1:
            raise ValueError("Each proto file must contain only one message")

        # _, proto_message_descriptor = proto_message.popitem()
        return proto_message.values()[0]

    def __avro_schema_from_event_class(
        self, event_class: Descriptor
    ) -> typing.OrderedDict[str, typing.Any]:
        fields = []
        for field in event_class.fields_by_name.values():
            
            if not field.message_type:
                convert_method = self.type_to_convertor[field.type]["method"]
                avro_field = convert_method(
                    field_name=field.name,
                    field_type=self.type_to_convertor[field.type]["type"],
                )
                fields.append(avro_field)
            else:
                convert_method = self.type_to_convertor[field.type]["method"]
                avro_field = convert_method(field=field)
                fields.append(avro_field)

        return self.__avro_schema(name=event_class.name, fields=fields)

    def __avro_schema(
            self, name: str, fields: typing.List[typing.Dict[str, str]]
        ) -> typing.OrderedDict[str, typing.Any]:
            return typing.OrderedDict(  # noqa
                [
                    ("type", "record"),
                    ("name", name),
                    ("fields", fields),
                ]
            )
    
    def __write_avro_file(self, root: str, filename: str) -> None:
        event_class = self.__event_class_from_filename(root, filename)
        avro_schema = self.__avro_schema_from_event_class(event_class)

        os.makedirs(self.avro_path, exist_ok=True)
        avro_file_path = f"{self.avro_path}/{event_class.name}.avsc"
        
        logging.info(f"Writing {avro_file_path}")
        with open(avro_file_path, "w") as f:
            f.write(json.dumps(avro_schema, indent=2))

#public method
    def convert_protobuf_to_avro(self) -> None:
        """
        This is an alpha batch convert process
        Converts the *_pb2.py files to *.avro and writes them to disk
        """
        for root, _, files in os.walk(self.pb2_path):
            if not files:
                continue

            for filename in files:
                if filename in {"__init__.py"} or "cpython" in filename:
                    continue

                self.__write_avro_file(root, filename)

@click.command()
@click.option("--pb2_path", required=True, help="Location of the pb2 files sources")
@click.option("--avro_path", required=True, help="Output location for the generated avro schemas")

def main(pb2_path, avro_path):
    schema_convertor = SchemaConvertor(pb2_path, avro_path)
    schema_convertor.convert_protobuf_to_avro()

if __name__ == "__main__":
    main()
