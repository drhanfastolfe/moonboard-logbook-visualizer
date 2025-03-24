# Moonboard Logbook Visualizer

A Python application for tracking and visualizing Moonboard climbing progress. This tool syncs session data with a TinyDB database and will include desktop data visualization in future versions.

## Features
- Fetches logbook data from the Moonboard API
- Tracks climbing sessions and their details
- Automatic cookie renewal using Playwright
- Ensures database consistency with TinyDB
- Provides configurable environment variables
- **Future Feature:** Desktop data visualization with Python

## Project Structure
```
├── api
│   └── moonboard_api.py
├── config
│   └── config.py
├── db
│   └── db_query.py
├── docs
│   └── db_schema.md ([DB Schema](docs/db_schema.md))
├── utils
│   └── renew_cookie.py
├── logging_config.py
├── main.py
├── env.ini
├── db.json
├── .gitignore
└── README.md
```

## Setup Instructions
1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
- Create an `env.ini` file in the root directory following the template:
```
[env]
USERNAME=your_username
PASSWORD=your_password
COOKIE=your_cookie_data
USER_ID=your_user_id
```
(Note: You can get the `COOKIE` and `USER_ID` by logging in to the website and inspecting the network requests. If left empty; the script will automatically fetch them.)

3. **Run the Application:**
```bash
python main.py
```

## Dependencies
- `requests`
- `tinydb`
- `playwright`
- `configparser`

## Future Improvements
- Desktop data visualization for Moonboard climbing insights
- Improved filtering and sorting for your climbing data

## Contributing
Feel free to fork this repository, submit issues, or suggest improvements. PRs are welcome!

## License
This project is licensed under the MIT License.
