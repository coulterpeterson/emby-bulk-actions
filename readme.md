# Emby Bulk Edits

## Installation (Windows)
* `choco install python`
* `python -m pip install -U pip`
* `pip install requests`
* `pip install -U python-dotenv`
* Clone repo
* Copy `.env_example` to `.env` and update values

## Running Disable Unmapped Channels
* `python disable_unmapped_channels.py`
* CTRL+C to cancel at any time
* Note: This script runs at about 10 seconds per channel