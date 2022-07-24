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

**Significance in Gameplay:**
Commentators have worried that this trend is “breaking the game”, so to speak. By turning to 3P shots, NBA teams are engaging in less of the physical, under-the-net point scoring. This has taken away some of the dynamic, exciting plays that would otherwise feature more heavily. However, it’s not clear that this contention holds up. The chart below examines the correlation between all NBA team’s 3P percentage and their field goal (FG) percentage, and their win loss ratio. As the data demonstrates, having a high 3P percentage is hardly a guarantee of a successful season. In fact, Field Goals Made (FGM) over the last several years has had a higher correlation with season win loss ratio than 3P Made (3PM), indicating a relative balance in the importance of these two point-scoring approaches to performing well over the season.
![image](https://user-images.githubusercontent.com/44953097/180630833-e724f88b-8aa9-4789-b99e-8c017743d15d.png)

In this chart, we don’t see a significant correlation between 3P shots made and win loss ratio, indicating that simply being able to make 3P shots is not sufficient for a team to ensure a successful season.

**The Defensive Response:**
Given the prevalence of the 3P shot, one might wonder whether defenses are adjusting to this strategic shift. However, it’s not clear that they are. Looking at the (arguably) top 5 defensive teams in the 2021-2022 season, we don’t see that they are consistently reducing their opponent’s ability to score 3P shots.
The chart below shows the average opponent 3P percentage for these outstanding defensive teams.
![image](https://user-images.githubusercontent.com/44953097/180630845-7ae2a288-feea-4bb2-ab2e-fafd0d93007f.png)

These results indicate that top defenses have kept opponent’s 3P% around 34-36%, with slight fluctuation, and even upward trends in some cases. This suggests that NBA defenses are not effectively stopping the 3P shot, preventing it from being scored by lowering the 3P% over time, as it becomes more prevalent

**Conclusions:**
The data from this analysis provide three clear insights into the nature of NBA play.
1. 3P shots have become much more common
2. Despite the prevalence of 3P shots, they have not broken the game. FG shots remain essential to success in the league, and teams cannot rise to the top if they neglect FG shots.
3. Teams have not generally responded to the increased use of the 3P shot with effective defensive play. The percentage of attempted 3P shots that are successful has not changed significantly, indicating an inability for teams to shut down this shot.
