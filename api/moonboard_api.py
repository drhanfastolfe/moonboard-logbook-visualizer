import requests
from logging_config import logger

class MoonboardAPI:
    def __init__(self, user_id, cookie):
        self.user_id = user_id
        self.cookie = cookie
        self.base_url = "https://www.moonboard.com"
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie
        }

    def _process_response(self, response):
        # Process the response by raising HTTP errors and decoding JSON.
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
            raise
        except ValueError as json_err:
            logger.error("JSON decode error: %s", json_err)
            raise Exception("Expired cookie or invalid JSON response.") from json_err

    def get_logbook(self):
        logger.info("Requesting logbook data...")
        url = f"{self.base_url}/Account/GetLogbook/{self.user_id}"
        payload = "sort=&page=1&pageSize=40&group=&filter=setupId~eq~'17'~and~Configuration~eq~2"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Logbook data retrieved. Status: %s", response.status_code)
        return self._process_response(response)

    def get_entries(self, session_id):
        logger.info("Requesting entries for session %s", session_id)
        url = f"{self.base_url}/Account/GetLogbookEntries/{self.user_id}/{session_id}"
        payload = "sort=&page=1&pageSize=30&group=&filter=setupId~eq~'17'~and~Configuration~eq~2"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Entries for session %s retrieved. Status: %s", session_id, response.status_code)
        return self._process_response(response)

    def get_user_id(self):
        logger.info("Extracting user id from benchmarks...")
        response = self.get_benckmarks()
        data = response.get("Data", [])
        if data and isinstance(data, list) and len(data) > 0:
            user_id = data[0].get("Id")
            if user_id:
                return user_id
        raise Exception("User id not found in benchmarks response.")

    def get_benckmarks(self):
        logger.info("Requesting benchmarks...")
        url = f"{self.base_url}/Dashboard/GetBenchmarks"
        payload = "sort=&page=1&pageSize=40&group=&aggregate=Score-sum~MaxScore-sum&filter="
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Benchmarks retrieved. Status: %s", response.status_code)
        return self._process_response(response)
