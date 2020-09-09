from typing import *

from abc import ABC, abstractmethod

class BaseModel(ABC):
    #initialize model state
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def infer_shape(self) -> Iterable[int]:
        pass


    @abstractmethod
    def preprocess(self, batch:dict) -> dict:
        pass

    @abstractmethod
    def batch_size(self) -> int:
        pass

    @abstractmethod
    def __call__(self, **kwargs) -> dict:
        pass
