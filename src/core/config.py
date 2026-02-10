# 📁 core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_settings():
    """Load application settings from environment variables."""

    return {
        # 🔐 API Keys
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "SERPAPI_API_KEY": os.getenv("SERPAPI_API_KEY"),

        # 🗄️ Database
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "DB_POOL_SIZE": int(os.getenv("DB_POOL_SIZE", 5)),
        "DB_MAX_OVERFLOW": int(os.getenv("DB_MAX_OVERFLOW", 10)),
        "DB_POOL_TIMEOUT": int(os.getenv("DB_POOL_TIMEOUT", 30)),
        "DB_POOL_RECYCLE": int(os.getenv("DB_POOL_RECYCLE", 1800)),

        # 🌐 Server
        "SERVER_HOST": os.getenv("SERVER_HOST", "localhost"),
        "SERVER_PORT": int(os.getenv("SERVER_PORT", 8080)),
        "SERVER_DEBUG": os.getenv("SERVER_DEBUG", "false").lower() == "true",

        # 📦 Application
        "APP_NAME": os.getenv("APP_NAME", "Travel Agent"),
        "APP_VERSION": os.getenv("APP_VERSION", "0.1.0"),
        "APP_DESCRIPTION": os.getenv(
            "APP_DESCRIPTION",
            "AI-powered Travel Agent for flights and hotels",
        ),
    }

# Load settings once
settings = get_settings()
