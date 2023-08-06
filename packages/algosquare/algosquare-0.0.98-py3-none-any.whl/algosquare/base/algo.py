"""Algo base class."""
from abc import ABC, abstractmethod

class Algo(ABC):
    """Base class for all algos."""
    @staticmethod
    def is_private():
        """
        A private algo can only be used by its creator.
        
        Returns: 
            Bool.
        """
        return False
