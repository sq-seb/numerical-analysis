from abc import ABC, abstractmethod

class IntervalMethod(ABC):
    """Base class for interval-based numerical methods"""
    
    @abstractmethod
    def solve(self, **kwargs) -> dict:
        """Solve the equation using interval method"""
        pass
    
    @abstractmethod
    def validate_input(self, **kwargs) -> bool | str:
        """Validate input parameters"""
        pass
