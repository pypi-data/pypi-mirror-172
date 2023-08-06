# nrkdl

[![Releases](https://img.shields.io/github/v/release/jenslys/nrkdl.svg)](https://github.com/jenslys/nrkdl/releases/)

Download content from nrk.no

**Disclaimer:** This is for educational purposes **ONLY**.

## Table of contents

- [Installation](#installation) 
  - [Updating](#updating)
  - [System requirements](#system-requirements)
- [Usage](#usage)
  - [Example usage](#example-usage)
    - [Download an entire tv-show with subtitles](#download-an-entire-tv-show-with-subtitles)
    - [Download a single tv-show episode](#download-a-single-tv-show-episode)
    - [Download a movie](#download-a-movie)
  - [Supported sites](#supported-sites)


  
## Installation

```bash
pip install nrkdl
```

## Updating

```bash
pip install nrkdl --upgrade
```

### System requirements

- [python3](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)
- [ffmpeg](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

## Usage

```text
usage: nrkdl.py [-h] --url URL [--write-subs] [--keep-subs] [--audio-only] [--write-metadata]

optional arguments:
  -h, --help        Show this help message and exit
  --url URL         URL for the Movie/TV-show (e.g: https://tv.nrk.no/program/KOID75006720)
  --write-subs      Download and embed subtitles to file
  --keep-subs       Prevent the subtitle files from being deleted after being embeded
  --audio-only      Only extract audio files
  --write-metadata  Write metadata to file
```

### Example usage

#### Download an entire tv-show with subtitles

```bash
nrkdl --url https://tv.nrk.no/serie/exit --write-subs
```

#### Download a single tv-show episode

```bash
nrkdl --url https://tv.nrk.no/serie/exit/sesong/2/episode/6/
```

#### Download a movie

```bash
nrkdl --url https://tv.nrk.no/program/MSUI31006017
```

### Supported sites

```text
NRK
NRKPlaylist
NRKRadioPodkast
NRKSkole: NRK Skole
NRKTV: NRK TV and NRK Radio
NRKTVDirekte: NRK TV Direkte and NRK Radio Direkte
NRKTVEpisode
NRKTVEpisodes
NRKTVSeason
NRKTVSeries
```
