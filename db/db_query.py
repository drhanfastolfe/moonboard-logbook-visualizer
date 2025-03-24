"""
Module for querying and updating the TinyDB database.
"""

from tinydb import Query
import logging

logger = logging.getLogger(__name__)

class DBQuery:
    def __init__(self, db):
        self.logbook_table = db.table("logbook")
        self.sessions_table = db.table("sessions")
    
    def update_logbook(self, logbook):
        """
        Clears the logbook table and inserts new logbook data.
        """
        logger.info("Updating logbook data in the database.")
        self.logbook_table.truncate()
        self.logbook_table.insert(logbook)
    
    def get_existing_session_ids(self):
        """
        Returns a set of session IDs currently stored in the sessions table.
        """
        return {session["Id"] for session in self.sessions_table.all()}
    
    def upsert_session(self, session_id, entries):
        """
        Upserts a session based on the session_id.
        """
        SessionQuery = Query()
        logger.info("Upserting session %s", session_id)
        self.sessions_table.upsert({"Id": session_id, "entries": entries}, SessionQuery.Id == session_id)
