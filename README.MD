## Openstreetmap History Processor
Python port of [processing-osm-history](https://github.com/Rub21/processing-osm-history/)

### Installation

### Usage
Find the latest edition number from http://planet.osm.org/replication/day/000/000/ . Eg `936`

Then use this command to donwload the history changesets for the last 7 days and extracts edits per user. The edits for each day of the team will be compressed into a file edition_number.zip

```python process.py <edition_number>```
