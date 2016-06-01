## OpenStreetMap History Processor
Python port of [processing-osm-history](https://github.com/Rub21/processing-osm-history/) to download the historical edits of a list of OpenStreetMap users.


### Installation

```
git clone https://github.com/planemad/osm-history-processor.git
cd osm-history-processor
pip install -r requirements.txt
```

### Usage
`python get_edits.py date days`, for example - to find changes starting August 4, 2015 and 5 days back in time run `python get_edits.py 2015-8-4 5`
