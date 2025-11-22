"""
Logging configuration for MediMind AI
Provides structured logging with different levels
"""

import logging
import sys
from typing import Optional
from src.config import Config

class Logger:
    """Custom logger for MediMind AI"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get or create a logger with the specified name
        
        Args:
            name: Logger name (usually __name__ of the module)
            
        Returns:
            Configured logger instance
        """
        if name in Logger._loggers:
            return Logger._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Create formatter
        formatter = logging.Formatter(Config.LOG_FORMAT)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        # Cache logger
        Logger._loggers[name] = logger
        
        return logger

# Convenience function
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return Logger.get_logger(name)