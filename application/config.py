import os
current_dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SQLITE_DB_DIR = os.path.join(current_dir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(SQLITE_DB_DIR,"kanban_database.sqlite3")
    DEBUG = True