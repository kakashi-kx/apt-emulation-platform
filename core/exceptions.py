"""
Custom exceptions for the emulation platform
"""

class EmulationError(Exception):
    """Base exception for emulation errors"""
    pass

class TechniqueExecutionError(EmulationError):
    """Raised when a technique fails to execute"""
    pass

class EnvironmentError(EmulationError):
    """Raised when environment setup fails"""
    pass

class DetectionError(EmulationError):
    """Raised when detection calculation fails"""
    pass
