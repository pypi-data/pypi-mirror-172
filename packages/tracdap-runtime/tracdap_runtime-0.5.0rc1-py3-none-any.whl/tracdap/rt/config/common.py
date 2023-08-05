# Code generated by TRAC

from __future__ import annotations
import typing as _tp  # noqa
import dataclasses as _dc  # noqa
import enum as _enum  # noqa

class ConfigFormat(_enum.Enum):

    CONFIG_FORMAT_NOT_SET = 0, 

    YAML = 1, 

    JSON = 2, 

    PROTO = 3, 


@_dc.dataclass
class _ConfigFile:

    config: _tp.Dict[str, str] = _dc.field(default_factory=dict)
