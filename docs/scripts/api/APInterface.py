from abc import ABC, abstractmethod

class APInterface(ABC):
    @abstractmethod
    def execute(self, owner_name ,repo_name,headers, members, data: dict) -> dict:
        pass