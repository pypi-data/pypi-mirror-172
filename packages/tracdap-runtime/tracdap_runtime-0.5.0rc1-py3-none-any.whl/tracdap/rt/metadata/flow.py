# Code generated by TRAC

from __future__ import annotations
import typing as _tp  # noqa
import dataclasses as _dc  # noqa
import enum as _enum  # noqa

from .type import *  # noqa
from .model import *  # noqa
from .search import *  # noqa


class FlowNodeType(_enum.Enum):

    NODE_TYPE_NOT_SET = 0, 

    INPUT_NODE = 1, 

    OUTPUT_NODE = 2, 

    MODEL_NODE = 3, 


@_dc.dataclass
class FlowModelStub:

    parameters: _tp.Dict[str, TypeDescriptor] = _dc.field(default_factory=dict)

    inputs: _tp.List[str] = _dc.field(default_factory=list)

    outputs: _tp.List[str] = _dc.field(default_factory=list)


@_dc.dataclass
class FlowNode:

    nodeType: FlowNodeType = FlowNodeType.NODE_TYPE_NOT_SET

    modelStub: FlowModelStub = None

    nodeSearch: SearchExpression = None


@_dc.dataclass
class FlowSocket:

    node: str = None

    socket: str = None


@_dc.dataclass
class FlowEdge:

    source: FlowSocket = None

    target: FlowSocket = None


@_dc.dataclass
class FlowDefinition:

    nodes: _tp.Dict[str, FlowNode] = _dc.field(default_factory=dict)

    edges: _tp.List[FlowEdge] = _dc.field(default_factory=list)

    parameters: _tp.Dict[str, ModelParameter] = _dc.field(default_factory=dict)

    inputs: _tp.Dict[str, ModelInputSchema] = _dc.field(default_factory=dict)

    outputs: _tp.Dict[str, ModelOutputSchema] = _dc.field(default_factory=dict)
