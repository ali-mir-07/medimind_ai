"""
Helper functions for MediMind AI
Common utilities used across the application
"""

from typing import List, Dict, Any
import json
import os
from datetime import datetime

def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        path: Directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)

def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load JSON data from file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        filepath: Path to save file
    """
    ensure_directory(os.path.dirname(filepath))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_timestamp() -> str:
    """
    Get current timestamp in ISO format
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()

def detect_emergency(text: str, keywords: List[str]) -> bool:
    """
    Detect if text contains emergency keywords
    
    Args:
        text: Text to check
        keywords: List of emergency keywords
        
    Returns:
        True if emergency detected, False otherwise
    """
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."