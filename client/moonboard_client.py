import requests
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

class MoonboardClient:
    def __init__(self, username, cookie, token):
        self.cookie = cookie
        self.token = token
        self.base_url = "https://www.moonboard.com"
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie
        }
        self.user_id = self._get_user_id(username)

    def _process_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
            raise
        except ValueError as json_err:
            logger.error("JSON decode error: %s", json_err)
            raise Exception("Expired cookie or invalid JSON response.") from json_err

    def get_logbook(self, setup_id, configuration):
        logger.info("Requesting logbook data...")
        url = f"{self.base_url}/Account/GetLogbook/{self.user_id}"
        payload = f"sort=&page=1&pageSize=8041&group=&filter=setupId~eq~'{setup_id}'~and~Configuration~eq~{configuration}"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Logbook data retrieved. Status: %s", response.status_code)
        return self._process_response(response)

    def get_entries(self, session_id, setup_id, configuration):
        logger.info("Requesting entries for session %s", session_id)
        url = f"{self.base_url}/Account/GetLogbookEntries/{self.user_id}/{session_id}"
        payload = f"sort=&page=1&pageSize=8041&group=&filter=setupId~eq~'{setup_id}'~and~Configuration~eq~{configuration}"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Entries for session %s retrieved. Status: %s", session_id, response.status_code)
        return self._process_response(response)

    def get_user_profiles(self, username):
        logger.info("Requesting user profiles for username: %s", username)
        url = f"{self.base_url}/Account/GetUserProfiles"
        payload = f"sort=&page=1&pageSize=8041&group=&filter=Query~eq~'{username}'&__RequestVerificationToken={self.token}"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("User profiles retrieved. Status: %s", response.status_code)
        return self._process_response(response)
    
    def _get_user_id(self, username):
        logger.info("Getting user ID for username: %s", username)
        response = self.get_user_profiles(username)
        data = response.get("Data", [])
        if data and isinstance(data, list) and len(data) > 0:
            user_id = data[0].get("Id")
            if user_id:
                logger.info("Found user ID: %s", user_id)
                return user_id
        raise Exception(f"User ID not found for username: {username}") 