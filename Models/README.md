## EDA.ipynb

Further EAD was done in this files.

---

## Models.ipynb

Nine models were created. Each corresponds to a different block/open weeks combination. Block weeks could be 13, 26, or 52 weeks, whereas open weeks could be 26, 52, or 78 weeks. Each combination has its own dataframe written as a .csv file. Voting classifier was employed as the model that conatains logistic regression, random forest, and gradient boosted trees. GridSearchCV was also employed to explore parameter space with cross validation. Scores and best parameters of all models were written in results.txt.
