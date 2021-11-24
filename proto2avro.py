import importlib.util
import json
import os.path
import sys
import click
from typing import OrderedDict, Any, Dict
from google.protobuf.descriptor import Descriptor, FieldDescriptor


class SchemaConvertor:
    def __init__(self, pb2_path: str, avro_path: str):
        self._pb2_path = pb2_path
        self._avro_path = avro_path
        self._type_to_convertor = {
            FieldDescriptor.TYPE_DOUBLE: {"type": "float", "method": self._read_through},
            FieldDescriptor.TYPE_FLOAT: {"type": "float", "method": self._read_through},
            FieldDescriptor.TYPE_INT64: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_UINT64: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_INT32: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_FIXED64: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_FIXED32: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_BOOL: {"type": "boolean", "method": self._read_through},
            FieldDescriptor.TYPE_STRING: {"type": "string", "method": self._read_through},
            FieldDescriptor.TYPE_GROUP: {"method": self._not_readable},
            FieldDescriptor.TYPE_MESSAGE: {"method": self._convert_message_type},
            FieldDescriptor.TYPE_BYTES: {"type": "string", "method": self._read_through},
            FieldDescriptor.TYPE_UINT32: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_ENUM: {"method": self._not_readable},
            FieldDescriptor.TYPE_SFIXED32: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_SFIXED64: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_SINT32: {"type": "int", "method": self._read_through},
            FieldDescriptor.TYPE_SINT64: {"type": "int", "method": self._read_through},
        } 
    
    # These methods are private methods and not static methods
    def _import_pb2_module(self, root: str, compiled_proto: str) -> str:
        """
        Import the pb2 module files
        """
        module_basename = os.path.basename(root)
        module_path = f"{module_basename}/{compiled_proto}.py"
        spec = importlib.util.spec_from_file_location(
            name=compiled_proto, location=module_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[compiled_proto] = module
        spec.loader.exec_module(module)
        return importlib.import_module(name=compiled_proto)

    def _fix_import_error(self, root: str, filename: str) -> None:
        """
        Hardcoded fix when an import error occurs because of an incorrect format
        """
        filepath = f"{root}/{filename}"
        with open(filepath, 'r+') as f:
            content = f.read()
            new_content = content.replace(
                "from types import", "from dwh.domain.pb2.types import"
            )
            f.truncate(0)
            f.seek(0)
            f.write(new_content)

    def _read_through(self, field_name: str, field_type: str) -> Dict[str, str]:
        """
        system default is used: zero for numeric types, the empty string for strings, false for bools
        """
        return {"name": field_name, "type": ["null", field_type], "default": None}

    def _not_readable(self, field_name: str, field_type: str):
        """
        When the Field type is nor supported raise an exception
        """
        raise TypeError(f"Type {field_type} with name {field_name} not supported")
    
    def _convert_message_type(self, field: FieldDescriptor) -> Dict[str, str]:
        """
        Converts the proto field type Decimal and Timestamp to avro types
        """
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
                self._not_readable(field_name=field.name, field_type=field.message_type.full_name)

        return avro_field
    
    def _event_class_from_filename(self, root: str, filename: str) -> Descriptor:
        """
        Returns a proto Descriptor object with all the parsed fields from the pb2 module files
        """
        # Read the files and import the modules
        compiled_proto = filename.rpartition(".")[0]
        try:
            pb2_module = self._import_pb2_module(root, compiled_proto)
        except ImportError(f"Import error detected: applying fix and reimporting {compiled_proto}"):
            self.__fix_import_error(root, filename)
            pb2_module = self._import_pb2_module(root, compiled_proto)

        # Creates a Descriptor type object and returns the object
        proto_message = pb2_module.DESCRIPTOR.message_types_by_name
        if len(proto_message.keys()) != 1:
            raise ValueError("Each proto file must contain only one message")

        return proto_message.values()[0]

    def _avro_schema_from_event_class(self, event_class: Descriptor) -> OrderedDict[str, Any]:
        """
        From a Descriptor object returns an avro schema
        """
        # Convert the proto fields to avro fields
        fields = []
        for field in event_class.fields_by_name.values():
            if not field.message_type:
                convert_method = self._type_to_convertor[field.type]["method"]
                avro_field = convert_method(
                    field_name=field.name,
                    field_type=self._type_to_convertor[field.type]["type"],
                )
                fields.append(avro_field)
            else:
                convert_method = self._type_to_convertor[field.type]["method"]
                avro_field = convert_method(field)
                fields.append(avro_field)

        #returns the avro schema
        return OrderedDict(
                [
                    ("type", "record"),
                    ("name", event_class.name),
                    ("fields", fields),
                ]
            )
    
    def _write_avro_file(self, root: str, filename: str) -> None:
        """
        Writes the converted avro schema from a proto message into an avsc file
        """
        # filename (pb2) -> event_class (proto) -> avro_schema
        event_class = self._event_class_from_filename(root, filename)
        avro_schema = self._avro_schema_from_event_class(event_class)

        os.makedirs(self._avro_path, exist_ok=True)
        avro_file_path = f"{self._avro_path}/{event_class.name}.avsc"
        
        # Writes the avsc files
        print(f"Writing {event_class.name}.avsc in {self._avro_path}")
        with open(avro_file_path, 'w') as f:
            f.write(json.dumps(avro_schema, indent=2))

#Public method
    def convert_protobuf_to_avro(self) -> None:
        """
        This is an alpha batch convert process
        Converts the *_pb2.py files to *.avro and writes them to disk
        It ignores the __pycache__ directory and the __init__ constructor
        """
        for root, _, files in os.walk(self._pb2_path):
            if "__pycache__" not in root:
                for filename in files:
                    if "__init__" not in filename:
                        self._write_avro_file(root, filename)

@click.command()
@click.option("--pb2_path", required=True, help="Input location of the pb2 files sources")
@click.option("--avro_path", required=True, help="Output location for the generated avro schemas")

def main(pb2_path, avro_path):
    schema_convertor = SchemaConvertor(pb2_path, avro_path)
    schema_convertor.convert_protobuf_to_avro()

if __name__ == "__main__":
    main()
