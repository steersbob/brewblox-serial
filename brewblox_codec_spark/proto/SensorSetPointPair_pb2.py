# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SensorSetPointPair.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import brewblox_pb2 as brewblox__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='SensorSetPointPair.proto',
  package='blox',
  syntax='proto3',
  serialized_pb=_b('\n\x18SensorSetPointPair.proto\x12\x04\x62lox\x1a\x0e\x62rewblox.proto\"n\n\x12SensorSetPointPair\x12-\n\x05links\x18\x03 \x01(\x0b\x32\x1e.blox.SensorSetPointPair.Links\x1a)\n\x05Links\x12\x0e\n\x06sensor\x18\x01 \x01(\x0c\x12\x10\n\x08setpoint\x18\x02 \x01(\x0c\"M\n\x1cSensorSetPointPair_Persisted\x12-\n\x05links\x18\x03 \x01(\x0b\x32\x1e.blox.SensorSetPointPair.Linksb\x06proto3')
  ,
  dependencies=[brewblox__pb2.DESCRIPTOR,])




_SENSORSETPOINTPAIR_LINKS = _descriptor.Descriptor(
  name='Links',
  full_name='blox.SensorSetPointPair.Links',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sensor', full_name='blox.SensorSetPointPair.Links.sensor', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='setpoint', full_name='blox.SensorSetPointPair.Links.setpoint', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=160,
)

_SENSORSETPOINTPAIR = _descriptor.Descriptor(
  name='SensorSetPointPair',
  full_name='blox.SensorSetPointPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='links', full_name='blox.SensorSetPointPair.links', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SENSORSETPOINTPAIR_LINKS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=160,
)


_SENSORSETPOINTPAIR_PERSISTED = _descriptor.Descriptor(
  name='SensorSetPointPair_Persisted',
  full_name='blox.SensorSetPointPair_Persisted',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='links', full_name='blox.SensorSetPointPair_Persisted.links', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=239,
)

_SENSORSETPOINTPAIR_LINKS.containing_type = _SENSORSETPOINTPAIR
_SENSORSETPOINTPAIR.fields_by_name['links'].message_type = _SENSORSETPOINTPAIR_LINKS
_SENSORSETPOINTPAIR_PERSISTED.fields_by_name['links'].message_type = _SENSORSETPOINTPAIR_LINKS
DESCRIPTOR.message_types_by_name['SensorSetPointPair'] = _SENSORSETPOINTPAIR
DESCRIPTOR.message_types_by_name['SensorSetPointPair_Persisted'] = _SENSORSETPOINTPAIR_PERSISTED
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SensorSetPointPair = _reflection.GeneratedProtocolMessageType('SensorSetPointPair', (_message.Message,), dict(

  Links = _reflection.GeneratedProtocolMessageType('Links', (_message.Message,), dict(
    DESCRIPTOR = _SENSORSETPOINTPAIR_LINKS,
    __module__ = 'SensorSetPointPair_pb2'
    # @@protoc_insertion_point(class_scope:blox.SensorSetPointPair.Links)
    ))
  ,
  DESCRIPTOR = _SENSORSETPOINTPAIR,
  __module__ = 'SensorSetPointPair_pb2'
  # @@protoc_insertion_point(class_scope:blox.SensorSetPointPair)
  ))
_sym_db.RegisterMessage(SensorSetPointPair)
_sym_db.RegisterMessage(SensorSetPointPair.Links)

SensorSetPointPair_Persisted = _reflection.GeneratedProtocolMessageType('SensorSetPointPair_Persisted', (_message.Message,), dict(
  DESCRIPTOR = _SENSORSETPOINTPAIR_PERSISTED,
  __module__ = 'SensorSetPointPair_pb2'
  # @@protoc_insertion_point(class_scope:blox.SensorSetPointPair_Persisted)
  ))
_sym_db.RegisterMessage(SensorSetPointPair_Persisted)


# @@protoc_insertion_point(module_scope)