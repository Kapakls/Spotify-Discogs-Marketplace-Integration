## Spotify Album & Discogs Listing Matcher

This Python script automates the process of finding potential matching listings for albums in your Spotify library on Discogs marketplace.

**Features:**

* Retrieves user data and album information from the Spotify API.
* Scrapes listing data from Discogs for each album in the user's library.
* Analyzes listing titles and identifies potential matches based on Jaccard similarity.

**Requirements:**

* Python 3.x
* `requests` library
* `cloudscraper` library
* `beautifulsoup4` library
* `pycountry` library

**Instructions:**

1. Configure the script with your Spotify API credentials (client ID, client secret, redirect URL) and desired file paths.
2. Configure `python getdata.py`, `searchlistings.py` and `filter.py` with the necessary file paths (folder_path, subprocess_path, album data, user_path, listing data).
3. Run `python getdata.py` to retrieve Spotify data, scrape listing data from Discogs and analyze it to identify potential matches.

**Additional Notes:**

* Replace the placeholders (`folder_path`, `subprocess_path`, etc.) with your desired configurations in each script.
* Ensure you have installed the required libraries using `pip install <library_name>`.
* Just a passion project, this script is provided for educational purposes only and might require modifications depending on your specific needs.

**Disclaimer:**

This code utilizes third-party APIs (Spotify), web-scrapping (Discogs) and libraries. Always refer to their respective terms of service and documentation before using them in your projects.
