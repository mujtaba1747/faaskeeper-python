from abc import ABC, abstractmethod
from typing import List, Optional

from faaskeeper.config import Config
from faaskeeper.node import Node
from faaskeeper.operations import (
    DirectOperation,
    ExistsNode,
    GetChildren,
    GetData,
    RegisterSession,
)


class ProviderClient(ABC):
    def __init__(self, cfg: Config):
        self._config = cfg

    @abstractmethod
    def get_data(self, path: str) -> Node:
        pass

    @abstractmethod
    def exists(self, path: str) -> Optional[Node]:
        pass

    @abstractmethod
    def get_children(self, path: str, include_data: bool) -> List[Node]:
        pass

    @abstractmethod
    def register_session(self, session_id: str, sourceAddr: str, heartbeat: bool):
        pass

    def execute_request(self, op: DirectOperation):
        if isinstance(op, GetData):
            return self.get_data(op.path)
        elif isinstance(op, ExistsNode):
            return self.exists(op.path)
        elif isinstance(op, GetChildren):
            return self.get_children(op.path, op.include_data)
        elif isinstance(op, RegisterSession):
            return self.register_session(op.session_id, op.source_addr, op.heartbeat)
        else:
            raise NotImplementedError()
