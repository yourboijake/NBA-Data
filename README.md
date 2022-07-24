# NBA-Data
Code for scraping data, prepping/cleaning, and machine learning to predict game outcomes

There are three components to this project: data scraping, data preparation/pipeline, and the machine learning

Data Scraping:
The scraping.py file scrapes data from the NBA website, obtaining basic stats for each game. These stats include game status such as number of 3 points attempted, field goal percentage, etc.

Data Pipeline:
In order to transform the raw data into a dataset useful for machine learning, we need to compute rolling statistics for each team for each game. Including the data from a particular game in the features would create data leakage, so the code aggregates the team performance statistics for the 5 games that precede a particular game, generating features for machine learning.

Machine Learning:
Several different models are used to do classification here, and a multi-layer perceptron model is found to be the most accurate at predicting game outcomes. Accuracy is ~64%, which is better than random guessing, but inferior to multiple attempts to predict game outcomes in the literature, including the following papers, which achieve accuracy in the mid-70s:

- Brown, Bryce. "Predictive Analytics for College Basketball: Using Logistic
Regression for Determining the Outcome of a Game", University of New Hampshire, https://scholars.unh.edu/cgi/viewcontent.cgi?article=1471&context=honors
- Zimmerman, Albrecht et al, "Predicting NCAAB match outcomes using ML
techniques – some results and lessons learned", https://arxiv.org/pdf/1310.3607.pdf


# Three Point Shots
In addition to doing game prediction, I used the data to examine the massive transition in the NBA centering around the importance of the three point shot. The usage of the three point shot has dramatically increased over the last decade, and has become the primary tool in the strategic approach of top offenses across the league. In light of this transition, many are asking whether NBA gameplay has worsened, and whether or not the rules of the game should be altered, including changes to the point values of shots or the distance between the hoop and the three point line. In this analysis, I assess this transition using box score data scraped from the NBA website, and conclude that these concerns are not warranted.

As the data show, over the last 15 years, three point (3P) shots have become an increasingly large portion of shots attempted and made.
![image](https://user-images.githubusercontent.com/44953097/180630796-5ee891aa-292e-4e5a-b825-b969bbe4e81d.png)
