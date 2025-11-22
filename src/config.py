"""
Configuration management for MediMind AI
Centralized settings and constants
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Settings
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_MODEL = "models/gemini-flash-latest"
    
    # Agent Settings
    TEMPERATURE = 0.7
    TOP_P = 0.95
    MAX_TOKENS = 2048
    
    # Memory Settings
    MAX_CONVERSATION_HISTORY = 20  # Maximum messages to keep in memory
    MEMORY_BANK_PATH = "data/memory_bank.json"
    
    # Tool Settings
    ENABLE_GOOGLE_SEARCH = False  # Set to True when implementing search
    MAX_SEARCH_RESULTS = 3
    
    # Data Paths
    DATA_DIR = "data"
    SYMPTOMS_DB = os.path.join(DATA_DIR, "symptoms.json")
    MEDICATIONS_DB = os.path.join(DATA_DIR, "medications.json")
    INTERACTIONS_DB = os.path.join(DATA_DIR, "interactions.json")
    
    # Safety Settings
    EMERGENCY_KEYWORDS = [
        "chest pain", "can't breathe", "suicide", "overdose",
        "severe bleeding", "unconscious", "stroke", "heart attack"
    ]
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validate configuration
if not Config.GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")