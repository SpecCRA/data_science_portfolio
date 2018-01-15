# Visualizing the Top 50 NBA Scoring Seasons Since 1981

## Description
This project looks at the top 50 NBA scoring seasons by points per game since 1981. I chose 1981 as the starting point because that is the official introduction of the NBA 3-point line. The finished story can be viewed [here.](https://public.tableau.com/profile/ben.xiao#!/vizhome/top_50_nba_scorers_revised/Story1)

## Usage
* Running `bref_player_stats_scraper.ipynb` will output two `.csv` files. 
* One `.csv` file contains all players and seasons starting from the 1981 season and ending in the 2016 season.
* The second `.csv` files contains the top 50 scoring seasons, with player redundancies from 1981 to 2016 again.

## Notes
* data_vis_description.pdf is the summary file with design choices explained.
* The first draft  and revised draft Tableau workborks are labebled as such.
* For anyone curious about the category meanings, [here is a link to a glossary of terms](https://www.basketball-reference.com/about/glossary.html)

## Credits
* All data is scraped from [basketball-reference.com](https://www.basketball-reference.com/)
* Visualization done on [Tableau Desktop](https://www.tableau.com/)

## Technology used
* **Python 3**
* **Beautifulsoup4**
* **Jupyter Notebook**
* **Pandas** 
* **Tableau**
