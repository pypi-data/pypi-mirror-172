# THIS FILE HAS BEEN GENERATED AUTOMATICALLY BY capnpy
# do not edit by hand
# generated on 2022-10-20 01:46
# cython: language_level=2

from capnpy cimport ptr as _ptr
from capnpy.struct_ cimport Struct as _Struct
from capnpy.struct_ cimport check_tag as _check_tag
from capnpy.struct_ import undefined as _undefined
from capnpy.enum import enum as _enum, fill_enum as _fill_enum
from capnpy.enum cimport BaseEnum as _BaseEnum
from capnpy.type import Types as _Types
from capnpy.segment.segment cimport Segment as _Segment
from capnpy.segment.segment cimport MultiSegment as _MultiSegment
from capnpy.segment.builder cimport SegmentBuilder as _SegmentBuilder
from capnpy.list cimport List as _List
from capnpy.list cimport PrimitiveItemType as _PrimitiveItemType
from capnpy.list cimport BoolItemType as _BoolItemType
from capnpy.list cimport TextItemType as _TextItemType
from capnpy.list cimport TextUnicodeItemType as _TextUnicodeItemType
from capnpy.list cimport StructItemType as _StructItemType
from capnpy.list cimport EnumItemType as _EnumItemType
from capnpy.list cimport VoidItemType as _VoidItemType
from capnpy.list cimport ListItemType as _ListItemType
from capnpy.anypointer import AnyPointer as _AnyPointer
from capnpy.util import text_bytes_repr as _text_bytes_repr
from capnpy.util import text_unicode_repr as _text_unicode_repr
from capnpy.util import data_repr as _data_repr
from capnpy.util import float32_repr as _float32_repr
from capnpy.util import float64_repr as _float64_repr
from capnpy.util import extend_module_maybe as _extend_module_maybe
from capnpy.util import check_version as _check_version
from capnpy.util import encode_maybe as _encode_maybe
from capnpy cimport _hash
from capnpy.list cimport void_list_item_type as _void_list_item_type
from capnpy.list cimport bool_list_item_type as _bool_list_item_type
from capnpy.list cimport int8_list_item_type as _int8_list_item_type
from capnpy.list cimport uint8_list_item_type as _uint8_list_item_type
from capnpy.list cimport int16_list_item_type as _int16_list_item_type
from capnpy.list cimport uint16_list_item_type as _uint16_list_item_type
from capnpy.list cimport int32_list_item_type as _int32_list_item_type
from capnpy.list cimport uint32_list_item_type as _uint32_list_item_type
from capnpy.list cimport int64_list_item_type as _int64_list_item_type
from capnpy.list cimport uint64_list_item_type as _uint64_list_item_type
from capnpy.list cimport float32_list_item_type as _float32_list_item_type
from capnpy.list cimport float64_list_item_type as _float64_list_item_type
from capnpy.list cimport data_list_item_type as _data_list_item_type
from capnpy.list cimport text_bytes_list_item_type as _text_bytes_list_item_type
from capnpy.list cimport text_unicode_list_item_type as _text_unicode_list_item_type
__capnpy_id__ = 0xb8641e621253ede2
__capnpy_version__ = '0.9.0'
__capnproto_version__ = '0.9.1'
# schema compiled with --no-version-check, skipping the call to _check_version
from capnpy.schema import CodeGeneratorRequest as _CodeGeneratorRequest
from capnpy.annotate import Options as _Options
from capnpy.reflection import ReflectionData as _ReflectionData
class _plexo_promise_ReflectionData(_ReflectionData):
    request = _CodeGeneratorRequest.from_buffer(_Segment(b'\x00\x00\x00\x00\x00\x00\x04\x00\x11\x00\x00\x00\xb7\x00\x00\x00u\x02\x00\x00\x1f\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x005\x02\x00\x007\x00\x00\x00\x00\x00\t\x01\x00\x00\x00\x00\x08\x00\x00\x00\x05\x00\x06\x00\xe2\xedS\x12b\x1ed\xb8\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x00\x00\x00*\x01\x00\x00Q\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x14\x15\x04\xfd\xe8\xdc\xe7%\x00\x00\x00\x01\x00\x04\x00\xe2\xedS\x12b\x1ed\xb8\x02\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00=\x00\x00\x00\x92\x01\x00\x00U\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Q\x00\x00\x00W\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00src/plexo/schema/plexo_promise.capnp\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x01\x00\xf0\x14\x15\x04\xfd\xe8\xdc\xe7\x01\x00\x00\x00j\x00\x00\x00PlexoPromise\x00\x00\x00\x00src/plexo/schema/plexo_promise.capnp:PlexoPromise\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x18\x00\x00\x00\x03\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\x00\x00\x00\x03\x00\x01\x00\xa4\x00\x00\x00\x02\x00\x01\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa1\x00\x00\x00Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0\x00\x00\x00\x03\x00\x01\x00\xac\x00\x00\x00\x02\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa9\x00\x00\x00J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa8\x00\x00\x00\x03\x00\x01\x00\xb4\x00\x00\x00\x02\x00\x01\x00\x03\x00\x00\x00\x02\x00\x00\x00\x00\x00\x01\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb1\x00\x00\x00\x9a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x00\x00\x00\x03\x00\x01\x00\xc0\x00\x00\x00\x02\x00\x01\x00\x04\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xbd\x00\x00\x00\x9a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x03\x00\x01\x00\xcc\x00\x00\x00\x02\x00\x01\x00\x05\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x00\x00\x00b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8\x00\x00\x00\x03\x00\x01\x00\xd4\x00\x00\x00\x02\x00\x01\x00instanceId\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00proposalId\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00typeName\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00acceptedInstanceId\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00acceptedProposalId\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00multicastIp\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x01\x00\x02\x00\xf0\x14\x15\x04\xfd\xe8\xdc\xe7\x00\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x007\x00\x00\x00\xe2\xedS\x12b\x1ed\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\xe2\xedS\x12b\x1ed\xb8\x05\x00\x00\x00*\x01\x00\x00\x15\x00\x00\x00\x07\x00\x00\x00src/plexo/schema/plexo_promise.capnp\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00'), 8, 0, 4)
    default_options = _Options.from_buffer(_Segment(b'\x02\x00\x03\x00\x01\x00\x03\x00'), 0, 1, 0)
    pyx = True
_reflection_data = _plexo_promise_ReflectionData()

#### FORWARD DECLARATIONS ####

cdef class PlexoPromise(_Struct)


#### DEFINITIONS ####

cdef class PlexoPromise(_Struct):
    __capnpy_id__ = 0xe7dce8fd041514f0
    __static_data_size__ = 4
    __static_ptrs_size__ = 2
    
    
    property instance_id:
        def __get__(self):
            # no union check
            value = self._read_primitive(0, ord(b'Q'))
            if 0 != 0:
                value = value ^ 0
            return value
    
    property proposal_id:
        def __get__(self):
            # no union check
            value = self._read_primitive(8, ord(b'Q'))
            if 0 != 0:
                value = value ^ 0
            return value
    
    property type_name:
        def __get__(self):
            # no union check
            return self._read_text_bytes(0)
    
    cpdef get_type_name(self):
        return self._read_text_bytes(0, default_=b"")
    
    cpdef has_type_name(self):
        ptr = self._read_fast_ptr(0)
        return ptr != 0
    
    property accepted_instance_id:
        def __get__(self):
            # no union check
            value = self._read_primitive(16, ord(b'Q'))
            if 0 != 0:
                value = value ^ 0
            return value
    
    property accepted_proposal_id:
        def __get__(self):
            # no union check
            value = self._read_primitive(24, ord(b'Q'))
            if 0 != 0:
                value = value ^ 0
            return value
    
    property multicast_ip:
        def __get__(self):
            # no union check
            return self._read_data(8)
    
    cpdef get_multicast_ip(self):
        return self._read_data(8, default_=b"")
    
    cpdef has_multicast_ip(self):
        ptr = self._read_fast_ptr(8)
        return ptr != 0
    
    @staticmethod
    cdef __new(object instance_id=0, object proposal_id=0, object type_name=None, object accepted_instance_id=0, object accepted_proposal_id=0, object multicast_ip=None):
        cdef _SegmentBuilder builder
        cdef long pos
        builder = _SegmentBuilder()
        pos = builder.allocate(48)
        builder.write_uint64(pos + 0, instance_id)
        builder.write_uint64(pos + 8, proposal_id)
        builder.alloc_text(pos + 32, type_name)
        builder.write_uint64(pos + 16, accepted_instance_id)
        builder.write_uint64(pos + 24, accepted_proposal_id)
        builder.alloc_data(pos + 40, multicast_ip)
        return builder.as_string()
    
    def __init__(object self, object instance_id=0, object proposal_id=0, object type_name=None, object accepted_instance_id=0, object accepted_proposal_id=0, object multicast_ip=None):
        _buf = PlexoPromise.__new(instance_id, proposal_id, type_name, accepted_instance_id, accepted_proposal_id, multicast_ip)
        self._init_from_buffer(_buf, 0, 4, 2)
    
    cpdef shortrepr(self):
        parts = []
        parts.append("instanceId = %s" % self.instance_id)
        parts.append("proposalId = %s" % self.proposal_id)
        if self.has_type_name(): parts.append("typeName = %s" % _text_bytes_repr(self.get_type_name()))
        parts.append("acceptedInstanceId = %s" % self.accepted_instance_id)
        parts.append("acceptedProposalId = %s" % self.accepted_proposal_id)
        if self.has_multicast_ip(): parts.append("multicastIp = %s" % _data_repr(self.get_multicast_ip()))
        return "(%s)" % ", ".join(parts)

cdef _StructItemType _PlexoPromise_list_item_type = _StructItemType(PlexoPromise)


_extend_module_maybe(globals(), modname=__name__)