import requests
from logging_config import logger

class MoonboardAPI:
    def __init__(self, user_id, cookie):
        self.user_id = user_id
        self.cookie = cookie
        self.base_url = "https://www.moonboard.com"
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'es,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/Account/Profile/{user_id}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cookie': cookie
        }

    def get_logbook(self):
        logger.info("Requesting logbook data...")
        url = f"{self.base_url}/Account/GetLogbook/{self.user_id}"
        payload = "sort=&page=1&pageSize=40&group=&filter=setupId~eq~'17'~and~Configuration~eq~2"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Logbook data retrieved. Status: %s", response.status_code)
        try:
            return response.json()
        except ValueError:
            logger.error("JSON decode error in get_logbook.")
            raise Exception("Expired cookie or invalid JSON response.")

    def get_entries(self, session_id):
        logger.info("Requesting entries for session %s", session_id)
        url = f"{self.base_url}/Account/GetLogbookEntries/{self.user_id}/{session_id}"
        payload = "sort=&page=1&pageSize=30&group=&filter=setupId~eq~'17'~and~Configuration~eq~2"
        response = requests.post(url, headers=self.headers, data=payload)
        logger.info("Entries for session %s retrieved. Status: %s", session_id, response.status_code)
        try:
            return response.json()
        except ValueError:
            logger.error("JSON decode error in get_entries.")
            raise Exception("Expired cookie or invalid JSON response.")

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
        try:
            return response.json()
        except ValueError:
            logger.error("JSON decode error in get_benckmarks.")
            raise Exception("Expired cookie or invalid JSON response.")
