# pyYouTubeAnalysis
Interaction with the YouTube API to pull data and run analysis using statistics and Natural Language Processing (NLP). Contains NLP implementations of text cleaning specific to social media data noise, key-phrase extraction using NLTK and Named-entity Recognition (NER) on a list of strings. 

# Setup
Clone the project and get it setup

```
git clone git@github.com:jsingh811/pyYouTubeAnalysis.git
cd pyYouTubeAnalysis
pip install -e .
python -m spacy download en_core_web_sm
```

# Demos

To see YouTube data extraction examples, see the section [YouTube Data Fetching](https://github.com/jsingh811/pyYouTubeAnalysis#youtube-data-fetching).

To see NER extraction examples, see the section [Extracting Locations](https://github.com/jsingh811/pyYouTubeAnalysis#extracting-locations).

To see Key-phrase extraction examples, see the section [Extracting Keyphrases from Text](https://github.com/jsingh811/pyYouTubeAnalysis#extracting-keyphrases-from-text).

To see data cleaning examples for removing emojis and URLs from text, see the section [Removing Emojis and URLs from Text](https://github.com/jsingh811/pyYouTubeAnalysis#removing-emojis-and-urls-from-text).


# YouTube Data Fetching

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
## Sample output  

The data inside `...video_details.json` file that generates is a list of dictionaries, of the following format as shown in [this file](https://github.com/jsingh811/pyYouTubeAnalysis/blob/master/samples/travel%20vlog_2020-01-01T000000Z_2020-01-02T000000Z_video_details.json).  

The data inside `...comment_details.json` file that generates is a list of dictionaries, of the following format as shown in [this file](https://github.com/jsingh811/pyYouTubeAnalysis/blob/master/samples/travel%20vlog_2020-01-01T000000Z_2020-01-02T000000Z_comment_details.json).

# Extracting Locations

The following contains examples for extracting location from comments file generated above.

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

## Sample output  

The data inside `locations_....json` file that generates using the [command line usage](https://github.com/jsingh811/pyYouTubeAnalysis#command-line-usage-1) example, or the variable `locations` in the [import and use](https://github.com/jsingh811/pyYouTubeAnalysis#import-and-use-1) example is a dictionary of location names as keys and their occurrence counts as values of the format as shown in [this file](https://github.com/jsingh811/pyYouTubeAnalysis/blob/master/samples/locations_travel%20vlog_2020-01-01T000000Z_2020-01-02T000000Z_comment_details.json).


# Extracting Keyphrases from Text

## Import and Use

```
from pyYouTubeAnalysis.phrases import KeyPhraseGenerator

documents = [
            """Did you know about this conference in Miami? It is about Natural
            Language Processing techniques as applied to messy data.""",
            "I really enjoyed the chocolate cheesecake yesterday!"
]

kp = KeyPhraseGenerator()

phrases =  kp.extract_keyphrases(documents)

```

# Removing Emojis and URLs from Text

## Import and Use

```
from pyYouTubeAnalysis import cleaner

document = " emoji was here -> 😃 , and url was here -> https://github.com"

# remove emoji
emoji_removed = cleaner.remove_emojis(document)

# removing url 
url_removed = cleaner.remove_urls(document)

```

# Citation 

Please cite this software as below

## APA

```
Singh, J. (2021). jsingh811/pyYouTubeAnalysis: pyYouTubeAnalysis: YouTube data requests and NER on text (v1.0) [Computer software]. Zenodo. https://doi.org/10.5281/ZENODO.4915746
```

## BibTex 

```
@misc{https://doi.org/10.5281/zenodo.4915746,
  doi = {10.5281/ZENODO.4915746},
  url = {https://zenodo.org/record/4915746},
  author = {Singh,  Jyotika},
  keywords = {YouTube,  NER,  NLP},
  title = {jsingh811/pyYouTubeAnalysis: pyYouTubeAnalysis: YouTube data requests and NER on text},
  publisher = {Zenodo},
  year = {2021},
  copyright = {Open Access}
}
```
