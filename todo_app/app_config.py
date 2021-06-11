import os

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

    """Base configuration variables."""
    LOGIN_DISABLED = os.environ.get("LOGIN_DISABLED")
    if not LOGIN_DISABLED:
        raise ValueError("No LOGIN_DISABLED set for Flask application. Did you follow the setup instructions?")