# skpodcasty.sk podcast downloader

Slovenský návod tu: [README-SK.md](README-SK.md)

A simple tool for downloading podcasts from skpodcasty.sk. The program creates a folder with the podcast name and downloads, sorts and rename all available episodes.

## Features

- Automatic detection of page count and episodes
- Batch downloading for lower memory usage
- Graphical interface for easy use
- Maintains episode order by publication date
- Respects rate limiting server using time delays between downloads
- Continues downloading with the next episode in case of an error
- Supports only podcasts from skpodcasty.sk

## Requirements

- Python 3.12/3.13
- requests
- beautifulsoup4

## Installation

1. Install [Python](https://www.python.org/) 3.12/3.13 

2. Install the required packages:
```bash
pip install requests
pip install beautifulsoup4
```

## Usage

1. Run the script by double-clicking or in the console:

```bash
python skpodcasty.py
```

2. Enter the podcast URL from skpodcasty.sk in the window
   - Example: `https://skpodcasty.sk/podcasts/nazov-podcastu`

3. Click the "Stiahnuť" (Download) button

4. The program will create a folder with the podcast name and download all available episodes to this folder

## Output

- Downloaded files are named in the format: `{podcast_name}_{episode_number}_{episode_id}.mp3`

- Example: `nazov-podcastu_001_id-epizody.mp3`

## License

Free

