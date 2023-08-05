# Code generated by TRAC

from __future__ import annotations
import typing as _tp  # noqa
import dataclasses as _dc  # noqa
import enum as _enum  # noqa

from .object_id import *  # noqa
from .data import *  # noqa
from .model import *  # noqa
from .flow import *  # noqa
from .job import *  # noqa
from .file import *  # noqa
from .custom import *  # noqa
from .stoarge import *  # noqa



@_dc.dataclass
class ObjectDefinition:

    """
    Object definitions are the core structural element of TRAC's metadata model
    
    Definitions describe every object that is stored in the TRAC platform and there
    is a one-to-one relation between definitions and objects. I.e. every dataset
    has its own data definition, every model has its own model definition and so
    on. Definitions also describe actions that take place on the platform by way of
    job definitions, so a "job" is just another type of object. Each type of object
    has its own definition and definitions can be added or extended as the platform
    evolves.
    
    The object definition container class allows different types of objects to be
    stored, indexed and accessed in the same way. Every object has a standard
    object header which contains enough information to identify the object.
    
    TRAC object definitions can be versioned. In order to use versioning the
    semantics of versioning must be defined and those vary depending on the object
    type. Currently these semantics are defined for DATA objects, see
    DataDefinition for details. Versioning is also allowed for CUSTOM objects, in
    this case it is the responsibility of the application to define versioning
    semantics. Versioning is not currently permitted for other object types.
    
    Object definitions are intended for storing structural data necessary to access
    data and run jobs on the TRAC platform. Informational data to catalogue and
    describe objects is stored in tags. Tags are a lot more flexible than object
    definitions, so applications built on the TRAC platform may choose to store
    structural information in tags where their required structure is not supported
    by TRAC's core object definitions.
    
    .. seealso::
        :class:`Tag <Tag>`
    """

    objectType: ObjectType = ObjectType.OBJECT_TYPE_NOT_SET

    data: _tp.Optional[DataDefinition] = None

    model: _tp.Optional[ModelDefinition] = None

    flow: _tp.Optional[FlowDefinition] = None

    job: _tp.Optional[JobDefinition] = None

    file: _tp.Optional[FileDefinition] = None

    custom: _tp.Optional[CustomDefinition] = None

    storage: _tp.Optional[StorageDefinition] = None

    schema: _tp.Optional[SchemaDefinition] = None
