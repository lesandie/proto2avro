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
            FieldDescriptor.TYPE_DOUBLE: {"type": "float", "method": self.read_through},
            FieldDescriptor.TYPE_FLOAT: {"type": "float", "method": self.read_through},
            FieldDescriptor.TYPE_INT64: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_UINT64: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_INT32: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_FIXED64: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_FIXED32: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_BOOL: {"type": "boolean", "method": self.read_through},
            FieldDescriptor.TYPE_STRING: {
                "type": "string",
                "method": self.read_through,
            },
            FieldDescriptor.TYPE_GROUP: {"method": self.not_readable},
            FieldDescriptor.TYPE_MESSAGE: {"method": self.convert_message_type},
            FieldDescriptor.TYPE_BYTES: {"type": "string", "method": self.read_through},
            FieldDescriptor.TYPE_UINT32: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_ENUM: {"method": self.not_readable},
            FieldDescriptor.TYPE_SFIXED32: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_SFIXED64: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_SINT32: {"type": "int", "method": self.read_through},
            FieldDescriptor.TYPE_SINT64: {"type": "int", "method": self.read_through},
        }

    @staticmethod
    def avro_schema(
        name: str, fields: typing.List[typing.Dict[str, str]]
    ) -> typing.OrderedDict[str, typing.Any]:
        return typing.OrderedDict(  # noqa
            [
                ("type", "record"),
                ("name", name),
                ("fields", fields),
            ]
        )

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

                self._write_avro_file(root=root, filename=filename)

    def _write_avro_file(self, root: str, filename: str) -> None:
        event_class = self.event_class_from_filename(root=root, filename=filename)
        avro_schema = self.avro_schema_from_event_class(event_class=event_class)

        os.makedirs(self.avro_path, exist_ok=True)

        avro_file_path = f"{self.avro_path}/{event_class.name}.avsc"
        logging.info("Writing %s", avro_file_path)
        with open(avro_file_path, "w") as f:
            f.write(json.dumps(avro_schema, indent=2))

    @staticmethod
    def import_pb2_module(root: str, compiled_proto: str):
        module_basename = os.path.basename(root)
        module_path = f"./avro/{module_basename}/{compiled_proto}.py"
        spec = importlib.util.spec_from_file_location(
            name=compiled_proto, location=module_path
        )
        module = importlib.util.module_from_spec(spec=spec)
        sys.modules[compiled_proto] = module
        spec.loader.exec_module(module)
        return importlib.import_module(name=compiled_proto)

    def event_class_from_filename(self, root: str, filename: str):
        compiled_proto = str(filename).rpartition(".")[0]
        try:
            pb2_module = self.import_pb2_module(
                root=root, compiled_proto=compiled_proto
            )
        except ImportError:
            self._fix_import_error(root=root, filename=filename)
            pb2_module = self.import_pb2_module(
                root=root, compiled_proto=compiled_proto
            )

        proto_message = pb2_module.DESCRIPTOR.message_types_by_name  # noqa

        if len(proto_message.keys()) != 1:
            raise ValueError("Each proto file must contain only one message")

        # _, proto_message_descriptor = proto_message.popitem()
        return proto_message.values()[0]

    @staticmethod
    def _fix_import_error(root: str, filename: str) -> None:
        filepath = f"{root}/{filename}"
        with open(filepath, "r+") as f:
            content = f.read()
            new_content = content.replace(
                "from types import", "from dwh.domain.pb2.types import"
            )
            f.truncate(0)
            f.seek(0)
            f.write(new_content)

    @staticmethod
    def read_through(field_name: str, field_type: str) -> typing.Dict[str, str]:
        """
        system default is used: zero for numeric types, the empty string for strings, false for bools
        """
        return {"name": field_name, "type": ["null", field_type], "default": None}

    def convert_message_type(self, field: FieldDescriptor) -> typing.Dict[str, str]:
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

                self.not_readable(
                    field_name=field.name, field_type=field.message_type.full_name
                )

        return avro_field

    @staticmethod
    def not_readable(field_name: str, field_type: str):
        raise TypeError("Type %s not supported", field_type)

    def avro_schema_from_event_class(
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

        return self.avro_schema(name=event_class.name, fields=fields)


@click.command()
@click.option("--pb2_path", required=True, help="Root of the pb2 files sources")
@click.option("--avro_path", required=True, help="Output of the generated avro schemas")
def main(pb2_path, avro_path):
    schema_convertor = SchemaConvertor(pb2_path=pb2_path, avro_path=avro_path)
    schema_convertor.convert_protobuf_to_avro()


if __name__ == "__main__":
    main()
