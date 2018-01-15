# StarCraft 2 Replay Analysis Data Exploration

## Description
This project explores a set of replay data in the real-time strategy game, StarCraft II. The data is from the first iteration of StarCraft II, Wings of Liberty. I primarily explore what are possible important factors or practices that sepaarte skill levesl, measured by league placement. 

## Usage
* `projecttemplate.html` is an HTML file that outputs my findings as well as explanations of exploratory analysis. 
* `projectemplate.rmd` contains all the code for graphs, created variables, and anything else. 

## Notes
* The link to the data source contains explanations to each variable abbreviation.
* **PAC:** PAC stands for Perception Action Cycle. An APM is a single action by the user. One PAC is defined as a shift of the screen to a new location for some time followed by at least one action then shift to another location. The delay to the first action in a PAC turns out to be one of the best predictors across all leagues, and the best in certain leagues (beating out the venerable APM, which, despite it’s faults, is a good predictor of league).

## Credits
* [Link to data source](https://www.kaggle.com/sfu-summit/starcraft-ii-replay-analysis)

## Technology used
* **R**
* **ggplot2**
