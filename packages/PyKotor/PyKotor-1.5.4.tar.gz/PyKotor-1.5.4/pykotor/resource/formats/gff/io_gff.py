from typing import Optional, List, Any

from pykotor.common.misc import ResRef
from pykotor.common.stream import BinaryWriter
from pykotor.resource.formats.gff import GFF, GFFContent, GFFFieldType, GFFStruct, GFFList
from pykotor.resource.type import SOURCE_TYPES, ResourceReader, ResourceWriter, TARGET_TYPES, autoclose


_COMPLEX_FIELD = {GFFFieldType.UInt64, GFFFieldType.Int64, GFFFieldType.Double, GFFFieldType.String,
                  GFFFieldType.ResRef, GFFFieldType.LocalizedString, GFFFieldType.Binary, GFFFieldType.Vector3,
                  GFFFieldType.Vector4}


class GFFBinaryReader(ResourceReader):
    def __init__(
            self,
            source: SOURCE_TYPES,
            offset: int = 0,
            size: int = 0
    ):
        super().__init__(source, offset, size)
        self._gff: Optional[GFF] = None

        self._labels: List[str] = []
        self._field_data_offset = 0
        self._field_indices_offset = 0
        self._list_indices_offset = 0
        self._struct_offset = 0
        self._field_offset = 0

    @autoclose
    def load(
            self,
            auto_close: bool = True
    ) -> GFF:
        self._gff = GFF()

        file_type = self._reader.read_string(4)
        file_version = self._reader.read_string(4)

        if not any(x for x in GFFContent if x.value == file_type):
            raise ValueError("Not a valid binary GFF file.")

        if file_version != "V3.2":
            raise ValueError("The GFF version of the file is unsupported.")

        self._gff.content = GFFContent(file_type)

        self._struct_offset = self._reader.read_uint32()
        struct_count = self._reader.read_uint32()
        self._field_offset = self._reader.read_uint32()
        field_count = self._reader.read_uint32()
        label_offset = self._reader.read_uint32()
        label_count = self._reader.read_uint32()
        self._field_data_offset = self._reader.read_uint32()
        field_data_count = self._reader.read_uint32()
        self._field_indices_offset = self._reader.read_uint32()
        field_indices_count = self._reader.read_uint32()
        self._list_indices_offset = self._reader.read_uint32()
        list_indices_count = self._reader.read_uint32()

        self._labels = []
        self._reader.seek(label_offset)
        for i in range(label_count):
            self._labels.append(self._reader.read_string(16))

        self._load_struct(self._gff.root, 0)

        return self._gff

    def _load_struct(
            self,
            gff_struct: GFFStruct,
            struct_index: int
    ):
        self._reader.seek(self._struct_offset + struct_index * 12)
        struct_id, data, field_count = self._reader.read_uint32(), self._reader.read_uint32(), self._reader.read_uint32()

        gff_struct.struct_id = struct_id

        if field_count == 1:
            self._load_field(gff_struct, data)
        elif field_count > 1:
            self._reader.seek(self._field_indices_offset + data)
            indices = []
            for i in range(field_count):
                indices.append(self._reader.read_uint32())
            for index in indices:
                self._load_field(gff_struct, index)

    def _load_field(
            self,
            gff_struct: GFFStruct,
            field_index: int
    ):
        self._reader.seek(self._field_offset + field_index * 12)
        field_type_id = self._reader.read_uint32()
        label_id = self._reader.read_uint32()

        field_type = GFFFieldType(field_type_id)
        label = self._labels[label_id]

        if field_type in _COMPLEX_FIELD:
            offset = self._reader.read_uint32()  # relative to field data
            self._reader.seek(self._field_data_offset + offset)
            if field_type is GFFFieldType.UInt64:
                gff_struct.set_uint64(label, self._reader.read_uint64())
            elif field_type is GFFFieldType.Int64:
                gff_struct.set_int64(label, self._reader.read_int64())
            elif field_type is GFFFieldType.Double:
                gff_struct.set_double(label, self._reader.read_double())
            elif field_type is GFFFieldType.String:
                length = self._reader.read_uint32()
                gff_struct.set_string(label, self._reader.read_string(length))
            elif field_type is GFFFieldType.ResRef:
                length = self._reader.read_uint8()
                value = ResRef(self._reader.read_string(length))
                gff_struct.set_resref(label, value)
            elif field_type is GFFFieldType.LocalizedString:
                gff_struct.set_locstring(label, self._reader.read_locstring())
            elif field_type is GFFFieldType.Binary:
                length = self._reader.read_uint32()
                gff_struct.set_binary(label, self._reader.read_bytes(length))
            elif field_type is GFFFieldType.Vector3:
                gff_struct.set_vector3(label, self._reader.read_vector3())
            elif field_type is GFFFieldType.Vector4:
                gff_struct.set_vector4(label, self._reader.read_vector4())
        elif field_type is GFFFieldType.Struct:
            struct_index = self._reader.read_uint32()
            value = GFFStruct()
            self._load_struct(value, struct_index)
            gff_struct.set_struct(label, value)
        elif field_type is GFFFieldType.List:
            offset = self._reader.read_uint32()  # relative to list indices
            self._reader.seek(self._list_indices_offset + offset)
            value = GFFList()
            count = self._reader.read_uint32()
            list_indices = []
            for i in range(count):
                struct_index = self._reader.read_uint32()
                list_indices.append(struct_index)
            for struct_index in list_indices:
                value.add(0)
                child = value.at(len(value) - 1)
                self._load_struct(child, struct_index)
            gff_struct.set_list(label, value)
        else:
            if field_type is GFFFieldType.UInt8:
                gff_struct.set_uint8(label, self._reader.read_uint8())
            elif field_type is GFFFieldType.Int8:
                gff_struct.set_int8(label, self._reader.read_int8())
            elif field_type is GFFFieldType.UInt16:
                gff_struct.set_uint16(label, self._reader.read_uint16())
            elif field_type is GFFFieldType.Int16:
                gff_struct.set_int16(label, self._reader.read_int16())
            elif field_type is GFFFieldType.UInt32:
                gff_struct.set_uint32(label, self._reader.read_uint32())
            elif field_type is GFFFieldType.Int32:
                gff_struct.set_int32(label, self._reader.read_int32())
            elif field_type is GFFFieldType.Single:
                gff_struct.set_single(label, self._reader.read_single())


class GFFBinaryWriter(ResourceWriter):
    def __init__(
            self,
            gff: GFF,
            target: TARGET_TYPES
    ):
        super().__init__(target)
        self._gff = gff

        self._struct_writer: BinaryWriter = BinaryWriter.to_bytearray()
        self._field_writer: BinaryWriter = BinaryWriter.to_bytearray()
        self._field_data_writer: BinaryWriter = BinaryWriter.to_bytearray()
        self._field_indices_writer: BinaryWriter = BinaryWriter.to_bytearray()
        self._list_indices_writer: BinaryWriter = BinaryWriter.to_bytearray()

        self._labels: List[str] = []

        self._struct_count: int = 0
        self._field_count: int = 0

    @autoclose
    def write(
            self,
            auto_close: bool = True
    ) -> None:
        self._build_struct(self._gff.root)

        struct_offset = 56
        struct_count = self._struct_writer.size() // 12
        field_offset = struct_offset + self._struct_writer.size()
        field_count = self._field_writer.size() // 12
        label_offset = field_offset + self._field_writer.size()
        label_count = len(self._labels)
        field_data_offset = label_offset + len(self._labels) * 16
        field_data_count = self._field_data_writer.size()
        field_indices_offset = field_data_offset + self._field_data_writer.size()
        field_indices_count = self._field_indices_writer.size()
        list_indices_offset = field_indices_offset + self._field_indices_writer.size()
        list_indices_count = self._list_indices_writer.size()

        self._writer.write_string(self._gff.content.value)
        self._writer.write_string("V3.2")
        self._writer.write_uint32(struct_offset)
        self._writer.write_uint32(struct_count)
        self._writer.write_uint32(field_offset)
        self._writer.write_uint32(field_count)
        self._writer.write_uint32(label_offset)
        self._writer.write_uint32(label_count)
        self._writer.write_uint32(field_data_offset)
        self._writer.write_uint32(field_data_count)
        self._writer.write_uint32(field_indices_offset)
        self._writer.write_uint32(field_indices_count)
        self._writer.write_uint32(list_indices_offset)
        self._writer.write_uint32(list_indices_count)

        self._writer.write_bytes(self._struct_writer.data())
        self._writer.write_bytes(self._field_writer.data())
        for label in self._labels:
            self._writer.write_string(label, string_length=16)
        self._writer.write_bytes(self._field_data_writer.data())
        self._writer.write_bytes(self._field_indices_writer.data())
        self._writer.write_bytes(self._list_indices_writer.data())

    def _build_struct(
            self,
            gff_struct: GFFStruct
    ):
        self._struct_count += 1
        struct_id = gff_struct.struct_id
        field_count = len(gff_struct)

        self._struct_writer.write_uint32(struct_id, max_neg1=True)

        if len(gff_struct) == 0:
            self._struct_writer.write_uint32(0xFFFFFFFF)
            self._struct_writer.write_uint32(0)
        elif len(gff_struct) == 1:
            self._struct_writer.write_uint32(self._field_count)
            self._struct_writer.write_uint32(field_count)

            for label, field_type, value in gff_struct:
                self._build_field(label, value, field_type)
        elif len(gff_struct) > 1:
            self._struct_writer.write_uint32(self._field_indices_writer.size())
            self._struct_writer.write_uint32(field_count)

            self._field_indices_writer.end()
            pos = self._field_indices_writer.position()
            self._field_indices_writer.write_bytes(b'\x00\x00\x00\x00' * field_count)

            i = 0
            for label, field_type, value in gff_struct:
                self._field_indices_writer.seek(pos + i * 4)
                self._field_indices_writer.write_uint32(self._field_count)
                self._build_field(label, value, field_type)
                i += 1

    def _build_list(
            self,
            gff_list: GFFList
    ):
        self._list_indices_writer.end()
        self._list_indices_writer.write_uint32(len(gff_list))
        pos = self._list_indices_writer.position()
        self._list_indices_writer.write_bytes(b'\x00\x00\x00\x00' * len(gff_list))
        for i, gff_struct in enumerate(gff_list):
            self._list_indices_writer.seek(pos + i * 4)
            self._list_indices_writer.write_uint32(self._struct_count)
            self._build_struct(gff_struct)

    def _build_field(
            self,
            label: str,
            value: Any,
            field_type: GFFFieldType
    ):
        self._field_count += 1
        field_type_id = field_type.value
        label_index = self._label_index(label)

        self._field_writer.write_uint32(field_type_id)
        self._field_writer.write_uint32(label_index)

        if field_type in _COMPLEX_FIELD:
            self._field_writer.write_uint32(self._field_data_writer.size())

            self._field_data_writer.end()
            if field_type is GFFFieldType.UInt64:
                self._field_data_writer.write_uint64(value)
            elif field_type is GFFFieldType.Int64:
                self._field_data_writer.write_int64(value)
            elif field_type is GFFFieldType.Double:
                self._field_data_writer.write_double(value)
            elif field_type is GFFFieldType.String:
                self._field_data_writer.write_string(value, prefix_length=4)
            elif field_type is GFFFieldType.ResRef:
                self._field_data_writer.write_string(value.get(), prefix_length=1)
            elif field_type is GFFFieldType.LocalizedString:
                self._field_data_writer.write_locstring(value)
            elif field_type is GFFFieldType.Binary:
                self._field_data_writer.write_uint32(len(value))
                self._field_data_writer.write_bytes(value)
            elif field_type is GFFFieldType.Vector4:
                self._field_data_writer.write_vector4(value)
            elif field_type is GFFFieldType.Vector3:
                self._field_data_writer.write_vector3(value)
        elif field_type is GFFFieldType.Struct:
            self._field_writer.write_uint32(self._struct_count)
            self._build_struct(value)
        elif field_type is GFFFieldType.List:
            self._field_writer.write_uint32(self._list_indices_writer.size())
            self._build_list(value)
        else:
            if field_type is GFFFieldType.UInt8:
                self._field_writer.write_uint32(value, max_neg1=True)
            elif field_type is GFFFieldType.Int8:
                self._field_writer.write_int32(value)
            elif field_type is GFFFieldType.UInt16:
                self._field_writer.write_uint32(value, max_neg1=True)
            elif field_type is GFFFieldType.Int16:
                self._field_writer.write_int32(value)
            elif field_type is GFFFieldType.UInt32:
                self._field_writer.write_uint32(value, max_neg1=True)
            elif field_type is GFFFieldType.Int32:
                self._field_writer.write_int32(value)
            elif field_type is GFFFieldType.Single:
                self._field_writer.write_single(value)
            else:
                raise ValueError("Unknown field type")

    def _label_index(
            self,
            label: str
    ) -> int:
        if label in self._labels:
            return self._labels.index(label)
        else:
            self._labels.append(label)
            return len(self._labels) - 1
