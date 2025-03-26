# Moonboard Logbook Visualizer

A tool to download and visualize your Moonboard climbing data to track your progress and analyze your performance.

## Overview

This tool allows you to:
- Download your complete Moonboard climbing history across all Moonboard setups (2016, 2017, 2019, 2020, 2024)
- Store the data locally in JSON format for analysis
- [Coming Soon] Visualize your climbing progress through graphs and statistics

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/moonboard-logbook-visualizer.git
cd moonboard-logbook-visualizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install browser requirements for Playwright:
```bash
playwright install
```

## Usage

1. Run the data collection script:
```bash
python main.py
```

2. Enter your Moonboard username and password when prompted. The script will:
   - Authenticate with the Moonboard website
   - Download your climbing history for all Moonboard setups
   - Store the data in the `logbooks` directory

The data is organized as follows:
```
logbooks/
├── logbook_2016-25/
├── logbook_2016-40/
├── logbook_2017-25/
├── logbook_2017-40/
├── logbook_2019-25/
├── logbook_2019-40/
├── logbook_2020-40/
├── logbook_2024-25/
└── logbook_2024-40/
```

## Data Schema

The downloaded data includes:
- Complete session history
- Detailed problem information
- Grades and attempts
- User ratings and comments
- Hold configurations

For a detailed description of the data schema, see [docs/schema.md](docs/schema.md).

## Coming Soon

Future features planned:
- Grade progression visualization
- Session frequency analysis
- Success rate tracking
- Hold type usage analysis
- Grade pyramid visualization
- Send attempts distribution
- Training load tracking

## Privacy & Security

- Your Moonboard credentials are never stored
- All data is stored locally on your machine
- No data is shared with third parties

## Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Share ideas for visualizations and analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.
