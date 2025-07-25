# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_log_path():
    logs_dir = os.path.join(get_project_root(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, 'erp_app.log')

def get_static_path(filename):
    static_dir = os.path.join(get_project_root(), 'static')
    os.makedirs(static_dir, exist_ok=True)
    return os.path.join(static_dir, filename)

def setup_logging():
    logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')