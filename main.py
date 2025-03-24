import os
from tinydb import TinyDB
from db.db_query import DBQuery
from api.moonboard_api import MoonboardAPI
from config.config import load_config, update_config
from utils.renew_cookie import get_renewed_cookie
from logging_config import setup_logging


logger = setup_logging()

# Load configuration from env.ini (which now uses an [env] section)
config = load_config()
env = config["env"]
USER_ID = env.get("USER_ID", "").strip()
COOKIE = env.get("COOKIE", "").strip()
USERNAME = env.get("USERNAME", "").strip()
PASSWORD = env.get("PASSWORD", "").strip()
DB_PATH = os.path.join("logbook", "db.json")

# Ensure the logbook directory exists.
if not os.path.exists("logbook"):
    os.makedirs("logbook")

# Initialize TinyDB and the database query object.
db = TinyDB(DB_PATH)
db_query = DBQuery(db)

def update_user_id_and_config(new_id, new_cookie):
    global USER_ID, COOKIE
    USER_ID = new_id
    COOKIE = new_cookie
    update_config(USERNAME=USERNAME, PASSWORD=PASSWORD, COOKIE=COOKIE, USER_ID=USER_ID)
    logger.info("Updated USER_ID and COOKIE in config.")

def process_logbook(api):
    """
    Retrieves the latest logbook data from the API and updates the database 
    if new data is found.
    """
    logbook = api.get_logbook()
    current_logbooks = db.table("logbook").all()
    if current_logbooks:
        stored_total = current_logbooks[0].get("Total", 0)
        new_total = logbook.get("Total", 0)
        if new_total <= stored_total:
            logger.info("No new data found in logbook. Skipping update.")
            return None
    db_query.update_logbook(logbook)
    logger.info("Logbook updated in database.")
    return logbook

def process_new_sessions(api, logbook):
    """
    Processes new sessions found in the logbook by fetching their entries
    and updating the sessions table.
    """
    existing_session_ids = db_query.get_existing_session_ids()
    new_sessions = [session for session in logbook.get("Data", []) if session["Id"] not in existing_session_ids]
    if not new_sessions:
        logger.info("No new sessions found. Skipping session updates.")
        return
    for session in new_sessions:
        session_id = session["Id"]
        logger.info("Fetching entries for session %s...", session_id)
        entries = api.get_entries(session_id)
        db_query.upsert_session(session_id, entries)
        logger.info("Session %s stored in database.", session_id)

def main():
    global USER_ID, COOKIE
    if not USER_ID:
        logger.info("USER_ID is missing. Trying to retrieve it with current cookie...")
        try:
            temp_api = MoonboardAPI(USER_ID, COOKIE)
            new_id = temp_api.get_user_id()
        except Exception as e:
            logger.warning("Failed to get USER_ID using existing cookie, renewing cookie...")
            COOKIE = get_renewed_cookie(USERNAME, PASSWORD)
            new_id = MoonboardAPI("", COOKIE).get_user_id()
        update_user_id_and_config(new_id, COOKIE)
    
    api = MoonboardAPI(USER_ID, COOKIE)
    logbook = process_logbook(api)
    if logbook:
        process_new_sessions(api, logbook)

if __name__ == "__main__":
    main()
