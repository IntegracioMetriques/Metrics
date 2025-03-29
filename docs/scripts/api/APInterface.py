from abc import ABC, abstractmethod

class APInterface(ABC):
    @abstractmethod
    def execute(self, owner_name ,repo_name,headers, data: dict) -> dict:
        pass