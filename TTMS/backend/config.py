import os

# MySQL Database Configuration
# Update these with your actual credentials
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "nazila"),  # Set DB_PASSWORD env var or update here
    "database": os.getenv("DB_NAME", "timetable_db")
}

SECRET_KEY = "college_ai_timetable"

# For development, you can uncomment and set credentials directly:
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "your_password_here",
#     "database": "timetable_db"
# }