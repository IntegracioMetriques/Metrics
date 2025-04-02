from abc import ABC, abstractmethod

class collectorBase(ABC):
    @abstractmethod
    def execute(self,data: dict,metricsmembers) -> dict:
        pass