# pyYouTubeAnalysis
Interaction with the YouTube API to pull data ans run analysis using statistics and NLP.

# Setup
Clone the project and get it setup

```
git clone git@github.com:jsingh811/pyYouTubeAnalysis.git
cd pyYouTubeAnalysis
pip install -e .
pip install -r requirements/requirements.txt
python -m spacy download en_core_web_sm
```

# Usage

## Command Line Usage

```
cd pyYouTubeAnalysis
```

```
python run_crawl.py -t "<YouTube API key (39 chars long)>" -k "travel vlog" -sd "2020-01-01T00:00:00Z" -ed "2020-01-02T00:00:00Z" -climit 5 -path "/Users/abc/Documents"
```

## Input Arguments

path (-path): Path to the directory you want to save the data in  
keyword (-k): Keyword to search videos for  
start-date (-sd): Starting publish date of video to search. Format YYYY-MM-DDThh:mm:ssZ  
end-date (-ed): Ending publish date of video to search. Format YYYY-MM-DDThh:mm:ssZ  
token (-t): YouTube API access token  
comments (-c): Whether you want to fetch comment text for the videos  
comment-limit (-climit): Per video comment limit to fetch  


## Import and Use

```
import json
from pyYouTubeAnalysis import (run_crawl, crawler)

keyword = "travel"
start_date = "2020-01-01T00:00:00Z"
end_date = "2020-01-02T00:00:00Z"
comment_limit = 5
api_token = "<YouTube API key (39 chars long)>"
path = "/Users/abc/Documents"
api = crawler.YouTubeCrawler(key=api_token)

# Fetch data from the api
[videos, comments] = run_crawl.get_videos_and_comments(
     api,
     keyword=keyword,
     start_date=start_date,
     end_date=end_date,
     comment_limit=comment_limit
)

# Save the fetched data on disk
with open("/".join([
    path,
    "_".join([
        keyword,
        start_date.replace(":", ""),
        end_date.replace(":", ""),
        "video_details.json"
    ])
]), "w") as f:
      json.dump(videos, f, indent=2)
with open("/".join([
    path,
    "_".join([
        keyword,
        start_date.replace(":", ""),
        end_date.replace(":", ""),
        "comment_details.json"
    ])
]), "w") as f:
      json.dump(comments, f, indent=2)
```


# Extracting locations from comments file generated above

## Command Line Usage

```
cd pyYouTubeAnalysis
```

```
python extract_locations.py -filepath "/Users/abc/Documents/travel_comment_details.json"
```  

## Import and Use

```
from pyYouTubeAnalysis import extract_locations

filepath = "/Users/abc/Documents/travel_comment_details.json"

comments = extract_locations.read_comment_text(filepath)
locations = extract_locations.extract_locations(comments)
```
