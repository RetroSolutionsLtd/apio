
# pylint: disable=C0114, C0115, C0301, C0303, C0411
# pylint: disable=E0245, E0602, E1139
# pylint: disable=R0913, R0801, R0917
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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\napio.proto\x12\x11\x61pio.common.proto\"+\n\rIce40FpgaInfo\x12\x0c\n\x04type\x18\x01 \x02(\t\x12\x0c\n\x04pack\x18\x02 \x02(\t\"9\n\x0c\x45\x63p5FpgaInfo\x12\x0c\n\x04type\x18\x04 \x02(\t\x12\x0c\n\x04pack\x18\x05 \x02(\t\x12\r\n\x05speed\x18\x06 \x02(\t\"\x1f\n\rGowinFpgaInfo\x12\x0e\n\x06\x66\x61mily\x18\x04 \x02(\t\"\xda\x01\n\x08\x46pgaInfo\x12\x0f\n\x07\x66pga_id\x18\x01 \x02(\t\x12\x10\n\x08part_num\x18\x02 \x02(\t\x12\x0c\n\x04size\x18\x03 \x02(\t\x12\x31\n\x05ice40\x18\n \x01(\x0b\x32 .apio.common.proto.Ice40FpgaInfoH\x00\x12/\n\x04\x65\x63p5\x18\x0b \x01(\x0b\x32\x1f.apio.common.proto.Ecp5FpgaInfoH\x00\x12\x31\n\x05gowin\x18\x0c \x01(\x0b\x32 .apio.common.proto.GowinFpgaInfoH\x00\x42\x06\n\x04\x61rch\"I\n\tVerbosity\x12\x12\n\x03\x61ll\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x14\n\x05synth\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x12\n\x03pnr\x18\x03 \x01(\x08:\x05\x66\x61lse\"\xc5\x01\n\x0b\x45nvironment\x12\x13\n\x0bplatform_id\x18\x01 \x02(\t\x12\x12\n\nis_windows\x18\x02 \x02(\x08\x12\x36\n\rterminal_mode\x18\x03 \x02(\x0e\x32\x1f.apio.common.proto.TerminalMode\x12\x12\n\ntheme_name\x18\x04 \x02(\t\x12\x17\n\x08is_debug\x18\x05 \x01(\x08:\x05\x66\x61lse\x12\x12\n\nyosys_path\x18\x06 \x02(\t\x12\x14\n\x0ctrellis_path\x18\x07 \x02(\t\"T\n\x07Project\x12\x10\n\x08\x62oard_id\x18\x01 \x02(\t\x12\x12\n\ntop_module\x18\x02 \x02(\t\x12#\n\x19yosys_synth_extra_options\x18\x03 \x01(\t:\x00\"\x98\x01\n\nLintParams\x12\x14\n\ntop_module\x18\x01 \x01(\t:\x00\x12\x1c\n\rverilator_all\x18\x02 \x01(\x08:\x05\x66\x61lse\x12!\n\x12verilator_no_style\x18\x03 \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x12verilator_no_warns\x18\x04 \x03(\t\x12\x17\n\x0fverilator_warns\x18\x05 \x03(\t\"Z\n\x0bGraphParams\x12\x37\n\x0boutput_type\x18\x01 \x02(\x0e\x32\".apio.common.proto.GraphOutputType\x12\x12\n\ntop_module\x18\x02 \x01(\t\"3\n\tSimParams\x12\x13\n\ttestbench\x18\x01 \x01(\t:\x00\x12\x11\n\tforce_sim\x18\x02 \x02(\x08\"%\n\x0e\x41pioTestParams\x12\x13\n\ttestbench\x18\x01 \x01(\t:\x00\"&\n\x0cUploadParams\x12\x16\n\x0eprogrammer_cmd\x18\x01 \x01(\t\"\x8b\x02\n\x0cTargetParams\x12-\n\x04lint\x18\n \x01(\x0b\x32\x1d.apio.common.proto.LintParamsH\x00\x12/\n\x05graph\x18\x0b \x01(\x0b\x32\x1e.apio.common.proto.GraphParamsH\x00\x12+\n\x03sim\x18\x0c \x01(\x0b\x32\x1c.apio.common.proto.SimParamsH\x00\x12\x31\n\x04test\x18\r \x01(\x0b\x32!.apio.common.proto.ApioTestParamsH\x00\x12\x31\n\x06upload\x18\x0e \x01(\x0b\x32\x1f.apio.common.proto.UploadParamsH\x00\x42\x08\n\x06target\"N\n\x14RichLibWindowsParams\x12\x17\n\x0fstdout_encoding\x18\x01 \x02(\t\x12\n\n\x02vt\x18\x02 \x02(\x08\x12\x11\n\ttruecolor\x18\x03 \x02(\x08\"\x89\x03\n\x0bSconsParams\x12\x11\n\ttimestamp\x18\x01 \x02(\t\x12)\n\x04\x61rch\x18\x02 \x02(\x0e\x32\x1b.apio.common.proto.ApioArch\x12.\n\tfpga_info\x18\x03 \x02(\x0b\x32\x1b.apio.common.proto.FpgaInfo\x12/\n\tverbosity\x18\x04 \x01(\x0b\x32\x1c.apio.common.proto.Verbosity\x12\x33\n\x0b\x65nvironment\x18\x05 \x02(\x0b\x32\x1e.apio.common.proto.Environment\x12+\n\x07project\x18\x06 \x02(\x0b\x32\x1a.apio.common.proto.Project\x12/\n\x06target\x18\x07 \x01(\x0b\x32\x1f.apio.common.proto.TargetParams\x12H\n\x17rich_lib_windows_params\x18\x08 \x01(\x0b\x32\'.apio.common.proto.RichLibWindowsParams*@\n\x08\x41pioArch\x12\x14\n\x10\x41RCH_UNSPECIFIED\x10\x00\x12\t\n\x05ICE40\x10\x01\x12\x08\n\x04\x45\x43P5\x10\x02\x12\t\n\x05GOWIN\x10\x03*_\n\x0cTerminalMode\x12\x18\n\x14TERMINAL_UNSPECIFIED\x10\x00\x12\x11\n\rAUTO_TERMINAL\x10\x01\x12\x12\n\x0e\x46ORCE_TERMINAL\x10\x02\x12\x0e\n\nFORCE_PIPE\x10\x03*B\n\x0fGraphOutputType\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x07\n\x03SVG\x10\x01\x12\x07\n\x03PNG\x10\x02\x12\x07\n\x03PDF\x10\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'apio_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_APIOARCH']._serialized_start=1877
  _globals['_APIOARCH']._serialized_end=1941
  _globals['_TERMINALMODE']._serialized_start=1943
  _globals['_TERMINALMODE']._serialized_end=2038
  _globals['_GRAPHOUTPUTTYPE']._serialized_start=2040
  _globals['_GRAPHOUTPUTTYPE']._serialized_end=2106
  _globals['_ICE40FPGAINFO']._serialized_start=33
  _globals['_ICE40FPGAINFO']._serialized_end=76
  _globals['_ECP5FPGAINFO']._serialized_start=78
  _globals['_ECP5FPGAINFO']._serialized_end=135
  _globals['_GOWINFPGAINFO']._serialized_start=137
  _globals['_GOWINFPGAINFO']._serialized_end=168
  _globals['_FPGAINFO']._serialized_start=171
  _globals['_FPGAINFO']._serialized_end=389
  _globals['_VERBOSITY']._serialized_start=391
  _globals['_VERBOSITY']._serialized_end=464
  _globals['_ENVIRONMENT']._serialized_start=467
  _globals['_ENVIRONMENT']._serialized_end=664
  _globals['_PROJECT']._serialized_start=666
  _globals['_PROJECT']._serialized_end=750
  _globals['_LINTPARAMS']._serialized_start=753
  _globals['_LINTPARAMS']._serialized_end=905
  _globals['_GRAPHPARAMS']._serialized_start=907
  _globals['_GRAPHPARAMS']._serialized_end=997
  _globals['_SIMPARAMS']._serialized_start=999
  _globals['_SIMPARAMS']._serialized_end=1050
  _globals['_APIOTESTPARAMS']._serialized_start=1052
  _globals['_APIOTESTPARAMS']._serialized_end=1089
  _globals['_UPLOADPARAMS']._serialized_start=1091
  _globals['_UPLOADPARAMS']._serialized_end=1129
  _globals['_TARGETPARAMS']._serialized_start=1132
  _globals['_TARGETPARAMS']._serialized_end=1399
  _globals['_RICHLIBWINDOWSPARAMS']._serialized_start=1401
  _globals['_RICHLIBWINDOWSPARAMS']._serialized_end=1479
  _globals['_SCONSPARAMS']._serialized_start=1482
  _globals['_SCONSPARAMS']._serialized_end=1875
# @@protoc_insertion_point(module_scope)
