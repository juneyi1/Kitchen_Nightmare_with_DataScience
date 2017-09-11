# Data Collection


### Gayot

Contains closed restaurants collected from http://www.gayot.com/closed-restaurants/chicago-area.html
- done with GetGayotRestaurants.ipynb
- each restaurant info is saved as a .csv file, and its reviews are saved in the corresponding _review.csv file

### Tribune

Contains closed restaurants collected from http://www.chicagotribune.com/redeye/redeye-closed-bars-and-restaurants-2016-20161228-story.html

http://www.chicagotribune.com/redeye/redeye-chicago-closed-bars-and-restaurants-2015-20160104-photogallery.html

- done with GetTribuneRestaurants.ipynb
- each restaurant info is saved as a .csv file, and its reviews are saved in the corresponding _review.csv file

### OpenRestaurants

Contains open restaurants collected from yelp API

- done with GetOpenRestaurantsYelpApi.ipynb
- each restaurant info is saved as a .csv file, and its reviews are saved in the corresponding _review.csv file

  **note**: some restaurant csv files were deleted to be uploaded to GitHib. 
---

### CombineFiles.ipynb

This file was used to combined closed restaurants from Gayot and Tribune to collect the neighborhoods where closed restaurants located. The list of the neighborhoods was used to pick open restaurants in OpenRestaurants.

### PreliminaryEDA.ipynb

This file was basically used to see the baseline of the whole data frame.

### GetReviewNLP.ipynb

This file was used to add compound, negative, positive, neutral, subjectivity scores with vader sentiment analysis to all _review.csv in Gayot, Tribune, and OpenRestaurants directories.

### GettingCanonicalDataframe.ipynb

This file was used to combine information for each restaurant with their reviews into one big file, where each row corresponds one review. Restaurant info was replicated for rows(reviews) that belong to the same restaurant. The dataframe is saved as CanonicalRestaurants.csv.gz.

### GetTrainTestSplit.ipynb

This file was used to collapse the CanonicalRestaurants dataframe to create a new dataframe where each row corresponds to one restaurant. The new dataframe was then used to do train/test set split.
