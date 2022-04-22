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
