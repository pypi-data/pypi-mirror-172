# Code generated by TRAC

from __future__ import annotations
import typing as _tp  # noqa
import dataclasses as _dc  # noqa
import enum as _enum  # noqa

from .type import *  # noqa
from .object_id import *  # noqa


class SchemaType(_enum.Enum):

    """
    Enumeration of the available types of data schema
    
    Currently only table schemas are supported, other schema types may be added later.
    
    .. seealso::
        :class:`SchemaDefinition <SchemaDefinition>`
    """

    SCHEMA_TYPE_NOT_SET = 0, 

    TABLE = 1, 


class PartType(_enum.Enum):

    PART_ROOT = 0, 

    PART_BY_RANGE = 1, 

    PART_BY_VALUE = 2, 


@_dc.dataclass
class FieldSchema:

    fieldName: str = None

    fieldOrder: int = None

    fieldType: BasicType = BasicType.BASIC_TYPE_NOT_SET

    label: str = None

    businessKey: bool = None

    categorical: bool = None

    formatCode: _tp.Optional[str] = None


@_dc.dataclass
class TableSchema:

    fields: _tp.List[FieldSchema] = _dc.field(default_factory=list)


@_dc.dataclass
class SchemaDefinition:

    """
    A schema definition describes the schema of a dataset
    
    Schema definitions can be top level objects (a type of object definition),
    in which case they can be referred to by multiple data definitions. Alternatively
    they can be embedded in a data definition to create datasets with one-off schemas.
    
    A table schema describes the schema of a tabular data set. Other schema types may
    be added later, e.g. for matrices, tensors, curves, surfaces and structured datasets.
    
    .. seealso::
        :class:`DataDefinition <DataDefinition>`
    """

    schemaType: SchemaType = SchemaType.SCHEMA_TYPE_NOT_SET

    partType: PartType = PartType.PART_ROOT

    table: _tp.Optional[TableSchema] = None


@_dc.dataclass
class PartKey:

    opaqueKey: str = None

    partType: PartType = PartType.PART_ROOT

    partValues: _tp.List[Value] = _dc.field(default_factory=list)

    partRangeMin: _tp.Optional[Value] = None

    partRangeMax: _tp.Optional[Value] = None


@_dc.dataclass
class DataDefinition:

    @_dc.dataclass
    class Delta:

        deltaIndex: int = None

        dataItem: str = None

    @_dc.dataclass
    class Snap:

        snapIndex: int = None

        deltas: _tp.List[DataDefinition.Delta] = _dc.field(default_factory=list)

    @_dc.dataclass
    class Part:

        partKey: PartKey = None

        snap: DataDefinition.Snap = None

    schemaId: _tp.Optional[TagSelector] = None

    schema: _tp.Optional[SchemaDefinition] = None

    parts: _tp.Dict[str, DataDefinition.Part] = _dc.field(default_factory=dict)

    storageId: TagSelector = None
