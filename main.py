import os
import json
from getpass import getpass
from client.moonboard_client import MoonboardClient
from utils.auth import get_auth_credentials
from utils.moonboard_setup import MOONBOARD_SETUPS
from utils.logger_config import setup_logger
from visualisations.hold_heatmap import collect_hold_data


logger = setup_logger(__name__)

# Create base directory for storing logbooks
if not os.path.exists("logbooks"):
    os.makedirs("logbooks")

def save_logbook(logbook_data, setup_name):
    # Creates directories and saves main logbook JSON containing all sessions
    if not os.path.exists(f"logbooks/logbook_{setup_name}"):
        os.makedirs(f"logbooks/logbook_{setup_name}")
        os.makedirs(f"logbooks/logbook_{setup_name}/sessions_{setup_name}")
    filename = f"logbooks/logbook_{setup_name}/logbook_{setup_name}.json"
    with open(filename, 'w') as f:
        json.dump(logbook_data, f, indent=2)
    logger.info(f"Saved logbook data for {setup_name} to {filename}")

def save_session_entries(entries_data, session_id, setup_name):
    # Saves individual session data
    filename = f"logbooks/logbook_{setup_name}/sessions_{setup_name}/session_{session_id}.json"
    with open(filename, 'w') as f:
        json.dump(entries_data, f, indent=2)
    logger.info(f"Saved session entries for {setup_name} to {filename}")

def load_existing_logbook(setup_name):
    # Loads previously saved logbook file or returns None if not found
    filename = f"logbooks/logbook_{setup_name}/logbook_{setup_name}.json"
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_existing_session_ids(existing_logbook):
    # Get list of existing session IDs from the logbook data
    if not existing_logbook or "Data" not in existing_logbook:
        return set()
    return {session.get("Id") for session in existing_logbook["Data"] if session.get("Id")}

def process_logbook(client, setup_id, configuration, setup_name):
    # Downloads and saves logbook data, only saving new sessions
    try:
        new_logbook = client.get_logbook(setup_id, configuration)
        
        # Check if user has any sessions
        if new_logbook.get("Total", 0) > 0:
            # Compare with existing data to check for updates
            existing_logbook = load_existing_logbook(setup_name)
            existing_total = existing_logbook.get("Total", 0) if existing_logbook else 0
            
            if new_logbook["Total"] > existing_total:
                save_logbook(new_logbook, setup_name)
                # Get existing session IDs from the logbook
                existing_sessions = get_existing_session_ids(existing_logbook)
                
                # Download only new sessions
                new_sessions = 0
                for session in new_logbook.get("Data", []):
                    session_id = session.get("Id")
                    if session_id and session_id not in existing_sessions:
                        entries = client.get_entries(session_id, setup_id, configuration)
                        save_session_entries(entries, session_id, setup_name)
                        new_sessions += 1
                
                logger.info(f"Downloaded {new_sessions} new sessions for {setup_name}")
            else:
                logger.info(f"No new sessions found for {setup_name}")
        else:
            logger.warning(f"No logbook sessions for {setup_name}.")
        
        return new_logbook
    except Exception as e:
        logger.error(f"Error processing logbook for {setup_name}: {str(e)}")
        return None

def main():
    # Get username and password safely. Note password will not appear in terminal
    username = input("Enter your Moonboard username: ")
    password = getpass("Enter your Moonboard password: ")
    
    try:
        # Get authentication credentials
        auth_creds = get_auth_credentials(username, password)
        client = MoonboardClient(username, auth_creds['cookie'], auth_creds['token'])
        
        # Process logbook for each Moonboard setup
        for setup in MOONBOARD_SETUPS:
            logger.info(f"Processing {setup.setup_name}")
            process_logbook(client, setup.setup_id, setup.configuration, setup.setup_name)
        # Process hold data and generate heatmaps
        collect_hold_data()
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

# Script entry point
if __name__ == "__main__":
    main()
