from abc import ABC, abstractmethod


class Wallet(ABC):

    @abstractmethod
    def __init__(self, path:str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def set_key_slot(self) -> None:
        raise NotImplemented

    @abstractmethod
    def get_public_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def sign(self, payload:str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def verify(self, signature:str, public_key:str=None) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def path(self) -> str:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def key_slot(self) -> int:
        raise NotImplementedError