# Technical Report

## 1. Overview

Intrigued by wondering why a restaurant I liked in Arlington Heights was closed, this project is dedicated to build a model to predict whether a restaurant will be closed in the near future. The model is built on data of permanently closed restaurants and open restaurants obtained from Yelp.com.

## 2. Data Collection
To build a classification model for predicting closed restaurants and open restaurants, data of both sides should be obtained. While webpages of closed restaurants are not explicitly returned via the search under Yelp, they do exist on Yelp.com still. With the name of a closed restaurant given, its Yelp webpage can be accessed through an url in the form of https://www.yelp.com/biz/restaurant_name-chicago. Therefore, names of closed restaurants reported from the following three sources were used to create Yelp urls from which data were collected via the Request library in Python.
1. http://www.gayot.com/closed-restaurants/chicago-area.html
2. http://www.chicagotribune.com/redeye/redeye-closed-bars-and-restaurants-2016-20161228-story.html
3. http://www.chicagotribune.com/redeye/redeye-chicago-closed-bars-and-restaurants-2015-20160104-photogallery.html

### 2.1 Assumptions
#### 2.1.1 Time-wise
The same time window was intended for the inclusion of open and permanently closed restaurants in the data set. Since the date when a restaurant is opened or permanently closed for business is not recorded on Yelp webpages, the dates of the first review and last review were used to approximate those, respectively. A time window of 2012 to 2017 was set for the inclusion of the permanently closed restaurants. That is, for the closed restaurants reported from the three sources above, only those closed between 2012 and 2017 were considered. For fair comparison, only restaurants opened since 2010/01/01 till today are eligible as open restaurants in the data set to contrast with permanently closed restaurants that exist between 2010 till 2012, if any. Therefore, restaurants open today that have their first reviews later than 2010/01/01 were excluded as open restaurants in the data set. Only restaurants that have been reviewed were considered, otherwise the date when a restaurant is opened or permanently closed for business could not be approximated.

#### 2.1.2 Location-wise
The same neighborhoods were intended for the inclusion of open and permanently closed restaurants in the data set. Once the permanently closed restaurants were collected, the distribution of their neighborhoods were recorded. Open restaurants were then sampled from the distribution, in addition to the constraint on their first review dates mentioned above.

### 2.2 Predictors
For each restaurant, the following features were considered as binomial categorical predictors: whether it is claimed by the owner, whether it has a website, accepts credit cards, good for groups, good for kids, takes reservations, outdoor seating, take-out,  delivery, and whether it has TV. The following features were considered as polynomial categorical predictors: category, neighborhood, price range, attire (dressy, formal, casual), parking (garage, street, valet, validated, private lot), alcohol (no, full bar, beer & wine only), noise level (loud, very loud, quiet, average), and Wi-Fi (no, paid, free).

For a given restaurant, the date, star, and text of each review was included in the data set. For the model to be predictive, three time periods (13, 26, and 52 weeks) were set as "block weeks". The block weeks were used to exclude reviews within the last 13, 26, and 52 weeks for a given restaurant for the models to predict whether restaurant will survive in the next 13, 26, and 52 weeks, respectively. The remaining reviews were used to calculate the average number of reviews per year, average rating, and ratings for 5-, 4-, 3-, 2-, 1- star, as numerical predictors.

In addition, Vader sentiment analysis was performed on the text of each remaining review, and the compound and subjectivity scores were calculated. The average compound score, and subjectivity score were also calculated as numerical predictors for each restaurant. To investigate the predicting power of the reviews within a time period before the "block weeks", three time periods (26, 52, and 78 weeks) before the "block weeks" were set as "open weeks". During the "open weeks", linear regressions were performed for ratings, compound scores, and subjectivity scores, respectively, for the reviews in that period. The intercepts and coefficients of rating, compound score, and subjectivity score were also included as numerical predictors. In total, nine data sets were created for different combinations of block weeks and open weeks.

## 3. Model

The voting classifier was employed as the model that contains logistic regression, random forest, and gradient boosted trees. GridSearchCV was also employed to explore the parameter space with cross validation. Accuracy scores and best parameters were recorded. The accuracy scores were used to measure the success of a model.

## 4. Results
While the base line in test set is 0.729, the mean accuracy for 13, 26, and 52 "block weeks" models are 0.863, 0.863, and 0.860, respectively. For models that have the same "block weeks", the span of the accuracy is less than 0.03 for models with different "open weeks". This indicates that the reviews within the "open weeks" do not reinforce the predicting power of the model. Moreover, the predicting power of models to predict whether a restaurant will survive in the next 26, 52, and 78 weeks do not differ with each other significantly.

## 4. Future Work
The neural network modeling technique will be used to increase the accuracy score. In the current model, only neighborhoods are included to study the effect of the location on the failure of a restaurant. If the information of how many restaurants have existed in the past ten years for a specific restaurant location, then a model can be constructed to predict the restaurant failure for a specific location. 
