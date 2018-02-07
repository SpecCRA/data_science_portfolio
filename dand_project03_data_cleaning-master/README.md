# Cleaning OpenStreetMaps' San Francisco Data

## Description
For a project on data cleaning, I chose to use OpenStreetMaps data on San Francisco, my home city. In the project, I audit the data file to find potential problems such as standardization and typos, correct them, and output a file for analysis. 

Some of the files used in this project were too large, so I have provided links hosted in my Google cloud drive.

## Usage
* [Link to downloaded San Francisco osm file](https://drive.google.com/open?id=0B2BGHnr9cnONSEJYd3FTSEQ2TU0)
* `audit_files.py` outputs potential problem areas.
* `clean_and_prep_files.py` outputs csv files containing cleaned map data.
* [`maps_data.db`](https://drive.google.com/open?id=0B2BGHnr9cnONUmd1Z0xDTWJ6bHc) is used for querying.
* `dand_project03.pdf` is a presentation of my findings. 

## Notes
* Two csv files were too large to host on GitHub. They are [`way_nodes.csv`](https://drive.google.com/open?id=0B2BGHnr9cnONQU1IVEZkQ0RUS0k) and [`nodes.csv`](https://drive.google.com/open?id=0B2BGHnr9cnONVXQtOUN4QmtlYTg)

## Credits
* Udacity's Intro to Data Wrangling course provided `data_wrangling_schema.sql`, `csv_to_db.py`, and much of the code in `clean_and_prep_files.py` to output the csv files.

## Tech
* **Python 2**
* **SQL**
