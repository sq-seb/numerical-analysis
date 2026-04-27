from abc import ABC, abstractmethod

class IterativeMethod(ABC):
    """Base class for iterative numerical methods"""
    
    @abstractmethod
    def solve(self, **kwargs) -> dict:
        """Solve the equation using iterative method"""
        pass
    
    @abstractmethod
    def validate_input(self, **kwargs) -> bool | str:
        """Validate input parameters"""
        pass
