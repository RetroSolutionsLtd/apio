
# pylint: disable=C0114, C0115, C0301, C0303, C0411
# pylint: disable=E0245, E0602, E1139
# pylint: disable=R0913, R0917
# pylint: disable=W0212, W0223, W0311, W0613, W0622

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: apio.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'apio.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\napio.proto\x12\napio.proto\"+\n\rIce40FpgaInfo\x12\x0c\n\x04type\x18\x01 \x02(\t\x12\x0c\n\x04pack\x18\x02 \x02(\t\"9\n\x0c\x45\x63p5FpgaInfo\x12\x0c\n\x04type\x18\x04 \x02(\t\x12\x0c\n\x04pack\x18\x05 \x02(\t\x12\r\n\x05speed\x18\x06 \x02(\r\"\x1f\n\rGowinFpgaInfo\x12\x0e\n\x06\x66\x61mily\x18\x04 \x02(\t\"\xc5\x01\n\x08\x46pgaInfo\x12\x0f\n\x07\x66pga_id\x18\x01 \x02(\t\x12\x10\n\x08part_num\x18\x02 \x02(\t\x12\x0c\n\x04size\x18\x03 \x02(\t\x12*\n\x05ice40\x18\n \x01(\x0b\x32\x19.apio.proto.Ice40FpgaInfoH\x00\x12(\n\x04\x65\x63p5\x18\x0b \x01(\x0b\x32\x18.apio.proto.Ecp5FpgaInfoH\x00\x12*\n\x05gowin\x18\x0c \x01(\x0b\x32\x19.apio.proto.GowinFpgaInfoH\x00\x42\x06\n\x04\x61rch\"I\n\tVerbosity\x12\x12\n\x03\x61ll\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x14\n\x05synth\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x12\n\x03pnr\x18\x03 \x01(\x08:\x05\x66\x61lse\"e\n\x0b\x45nvrionment\x12\x13\n\x0bplatform_id\x18\x01 \x02(\t\x12\x17\n\x08is_debug\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x12\n\nyosys_path\x18\x03 \x02(\t\x12\x14\n\x0ctrellis_path\x18\x04 \x02(\t\"/\n\x07Project\x12\x10\n\x08\x62oard_id\x18\x01 \x02(\t\x12\x12\n\ntop_module\x18\x02 \x02(\t\"\x99\x01\n\x0b\x43mdLintInfo\x12\x14\n\ntop_module\x18\x01 \x01(\t:\x00\x12\x1c\n\rverilator_all\x18\x02 \x01(\x08:\x05\x66\x61lse\x12!\n\x12verilator_no_style\x18\x03 \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x12verilator_no_warns\x18\x04 \x03(\t\x12\x17\n\x0fverilator_warns\x18\x05 \x03(\t\"T\n\x0c\x43mdGraphInfo\x12\x30\n\x0boutput_type\x18\x01 \x02(\x0e\x32\x1b.apio.proto.GraphOutputType\x12\x12\n\ntop_module\x18\x02 \x01(\t\"9\n\nCmdSimInfo\x12\x11\n\ttestbench\x18\x01 \x02(\t\x12\x18\n\tforce_sim\x18\x02 \x01(\x08:\x05\x66\x61lse\"\"\n\x0b\x43mdTestInfo\x12\x13\n\ttestbench\x18\x01 \x01(\t:\x00\"\'\n\rCmdUploadInfo\x12\x16\n\x0eprogrammer_cmd\x18\x01 \x01(\t\"\xe5\x01\n\x0b\x43ommandInfo\x12\'\n\x04lint\x18\n \x01(\x0b\x32\x17.apio.proto.CmdLintInfoH\x00\x12)\n\x05graph\x18\x0b \x01(\x0b\x32\x18.apio.proto.CmdGraphInfoH\x00\x12%\n\x03sim\x18\x0c \x01(\x0b\x32\x16.apio.proto.CmdSimInfoH\x00\x12\'\n\x04test\x18\r \x01(\x0b\x32\x17.apio.proto.CmdTestInfoH\x00\x12+\n\x06upload\x18\x0e \x01(\x0b\x32\x19.apio.proto.CmdUploadInfoH\x00\x42\x05\n\x03\x63md\"\x92\x02\n\x0bSconsParams\x12\x11\n\ttimestamp\x18\x01 \x02(\t\x12\"\n\x04\x61rch\x18\x02 \x02(\x0e\x32\x14.apio.proto.ApioArch\x12\'\n\tfpga_info\x18\x03 \x02(\x0b\x32\x14.apio.proto.FpgaInfo\x12(\n\tverbosity\x18\x04 \x01(\x0b\x32\x15.apio.proto.Verbosity\x12,\n\x0b\x65nvrionment\x18\x05 \x02(\x0b\x32\x17.apio.proto.Envrionment\x12$\n\x07project\x18\x06 \x02(\x0b\x32\x13.apio.proto.Project\x12%\n\x04\x63mds\x18\x07 \x01(\x0b\x32\x17.apio.proto.CommandInfo*@\n\x08\x41pioArch\x12\x14\n\x10\x41RCH_UNSPECIFIED\x10\x00\x12\t\n\x05ICE40\x10\x01\x12\x08\n\x04\x45\x43P5\x10\x02\x12\t\n\x05GOWIN\x10\x03*B\n\x0fGraphOutputType\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x07\n\x03SVG\x10\x01\x12\x07\n\x03PNG\x10\x02\x12\x07\n\x03PDF\x10\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'apio_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_APIOARCH']._serialized_start=1477
  _globals['_APIOARCH']._serialized_end=1541
  _globals['_GRAPHOUTPUTTYPE']._serialized_start=1543
  _globals['_GRAPHOUTPUTTYPE']._serialized_end=1609
  _globals['_ICE40FPGAINFO']._serialized_start=26
  _globals['_ICE40FPGAINFO']._serialized_end=69
  _globals['_ECP5FPGAINFO']._serialized_start=71
  _globals['_ECP5FPGAINFO']._serialized_end=128
  _globals['_GOWINFPGAINFO']._serialized_start=130
  _globals['_GOWINFPGAINFO']._serialized_end=161
  _globals['_FPGAINFO']._serialized_start=164
  _globals['_FPGAINFO']._serialized_end=361
  _globals['_VERBOSITY']._serialized_start=363
  _globals['_VERBOSITY']._serialized_end=436
  _globals['_ENVRIONMENT']._serialized_start=438
  _globals['_ENVRIONMENT']._serialized_end=539
  _globals['_PROJECT']._serialized_start=541
  _globals['_PROJECT']._serialized_end=588
  _globals['_CMDLINTINFO']._serialized_start=591
  _globals['_CMDLINTINFO']._serialized_end=744
  _globals['_CMDGRAPHINFO']._serialized_start=746
  _globals['_CMDGRAPHINFO']._serialized_end=830
  _globals['_CMDSIMINFO']._serialized_start=832
  _globals['_CMDSIMINFO']._serialized_end=889
  _globals['_CMDTESTINFO']._serialized_start=891
  _globals['_CMDTESTINFO']._serialized_end=925
  _globals['_CMDUPLOADINFO']._serialized_start=927
  _globals['_CMDUPLOADINFO']._serialized_end=966
  _globals['_COMMANDINFO']._serialized_start=969
  _globals['_COMMANDINFO']._serialized_end=1198
  _globals['_SCONSPARAMS']._serialized_start=1201
  _globals['_SCONSPARAMS']._serialized_end=1475
# @@protoc_insertion_point(module_scope)
