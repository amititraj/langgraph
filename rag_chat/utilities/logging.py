from loguru import logger
import os

# Ensure the log folder exists
os.makedirs("log", exist_ok=True)

logger.add(
    "log/application.log",
    rotation="10 MB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)