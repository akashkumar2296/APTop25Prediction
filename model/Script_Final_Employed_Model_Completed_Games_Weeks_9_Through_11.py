# Kevin Cass, Akash Kumar, Kee Mok, Daniel Lauer, and Carol Sikes
# CSE 6242 Semester Project - Final Employed Model on Completed Games
# 20 - 23 November 2018

###############################################################################
###############################################################################

# SECTION I - MACHINE LEARNING MODEL (EMPLOYMENT):

# Import the python software libraries that will be used in this script:

import pandas as pd
import pickle
import matplotlib.pyplot as Scatter_plot
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression

# Load up the trained model (trained and stored in the "Script_Final_Trained_
# Model.py" script), so that it can be employed on new data from completed 
# football games:

Model_reloaded = pickle.load(open("Model_trained.sav", "rb"))

# Read in the completed football game dataset, on which the trained machine
# learning model will be employed:

Completed_game_dataset = pd.read_csv\
                ("Dataset_Final_Completed_Game_Data_Weeks_9_Through_11.csv")
Completed_game_dataset = Completed_game_dataset.loc[:, "Year":"Rank"]

# -----------------------------------------------------------------------------

# Eyeballing the data reveals that it has some missing values. Remove all such
# rows with missing values, as well as those with rankings (from the "Rank"
# feature) of greater than 25, as the focus of our project is on top-25 teams:

Completed_game_dataset = Completed_game_dataset.dropna()
Completed_game_dataset = Completed_game_dataset[Completed_game_dataset["Rank"]\
                                                <= 25]

# Determine the data types of the dataset's features:

Completed_game_dataset.dtypes                                 

# Make the same data type conversions on this data set as with the "Football_
# dataset" variable in the "Script_Final_Trained_Model.py" script:

Cat_feat = ["Year", "Team", "Week", "Conference", "H/A/N", "Fav/Und",\
            "OppTeam", "Opp Conf", "WinLose", "OT?", "GameStatus"]

Num_feat = ["PrevRank", "RankDiff", "ScoreDiff", "TODiff", "YPPDiff", \
            "PenYdDiff", "TOPDiff", "WinPer", "TimeRem"] # Used later on.

Int_feat = ["TODiff", "PenYdDiff", "TOPDiff", "TimeRem"]
Float_feat = ["YPPDiff", "WinPer"]

Completed_game_dataset[Cat_feat] = Completed_game_dataset[Cat_feat]\
                                   .astype("category") 
Completed_game_dataset[Int_feat] = Completed_game_dataset[Int_feat]\
                                   .astype("int") 
Completed_game_dataset[Float_feat] = Completed_game_dataset[Float_feat]\
                                     .astype("float")

# Scale all numeric features in the dataset exactly as with the "Football_
# dataset" variable in the "Script_Final_Trained_Model.py" script:

Completed_game_dataset[Num_feat] = StandardScaler().\
                            fit_transform(Completed_game_dataset[Num_feat])

# Perform one-hot encoding on the dataset, exactly as with the "Football_
# dataset" variable in the "Script_Final_Trained_Model.py" script:
                             
Completed_game_dataset = pd.get_dummies(Completed_game_dataset, columns =\
                                        Cat_feat, prefix = Cat_feat)

# Perform "SelectKBest" on the dataset to get it down to 90 features (89 + 
# "Rank"), such that it is compatible with the trained model, and done exactly 
# as with the "Football_dataset" variable in the "Script_Final_Trained_
# Model.py" script. 90 features were originally chosen to align with the size 
# of the one-hot encoded dataset of in-progress games (see "Script_Final_
# Employed_Model_InProgress_Games"):

Completed_game_dataset_feat = Completed_game_dataset.drop("Rank", 1)

Completed_game_dataset_selected = SelectKBest(score_func = f_regression,\
                                              k = 89)
Completed_game_dataset_selected_fit = Completed_game_dataset_selected.fit\
                                (Completed_game_dataset_feat,\
                                 Completed_game_dataset.Rank)

Completed_game_dataset_feat2 = Completed_game_dataset.loc[:,\
                               Completed_game_dataset_selected.get_support()]

Completed_game_dataset = pd.concat([Completed_game_dataset_feat2,\
                                    Completed_game_dataset.Rank], axis = 1)

# -----------------------------------------------------------------------------

# Use the reloaded model above to employ the trained model on this dataset,
# now that it has been properly processed:

Model_result = Model_reloaded.predict(Completed_game_dataset).round()

###############################################################################
###############################################################################

# SECTION II - MACHINE LEARNING MODEL (EMPLOYMENT EVALUATION):

# Evaluate the model's accuracy in predicting "Rank" values for completed
# games through metrics:

Emp_model_evaluation_r2 = metrics.r2_score(Model_result,\
                                           Completed_game_dataset.Rank)
Emp_model_evaluation_MAE = metrics.mean_absolute_error\
                                          (Model_result,\
                                           Completed_game_dataset.Rank)
Emp_model_evaluation_MSE = metrics.mean_squared_error\
                                          (Model_result,\
                                           Completed_game_dataset.Rank)

# The R^2 value is not the best metric of model success, but the fact that it 
# is 0.31 is not promising. This means that the predicted and actual "Rank" 
# values are weakly correlated (since 0.31 is not so near 1 on an R^2 scale 
# of -1 to 1).

# -----------------------------------------------------------------------------

# Evaluate the model's performance via a scatter plot (not to be aesthetically
# pleasing, but to show correlation between predicted and true "Rank"):

Scatter_plot.figure()
Scatter_plot.scatter(Completed_game_dataset.Rank, Model_result)
Scatter_plot.xlabel("True Rank")
Scatter_plot.ylabel("Predicted Rank")

# There is evidently a fair amount of positive correlation between predicted 
# "Rank" (by the model) and true "Rank". It is interesting that there are five
# outlier points, which are most likely the reason for why the R^2 value above
# was so high. If these outliers were to be somehow handled or removed, model
# performance would improve drastically for this dataset. Further analysis
# would be necessary to determine the cause of these outliers (perhaps an error
# in data processing), but because our focus is on the predictions of in-
# progress games, this analysis will not be conducted.

###############################################################################
###############################################################################

# SECTION III - REFERENCES (which helped guide us in all modeling scripts):
    
# 1) https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
# 2) https://chrisalbon.com/python/data_wrangling/pandas_dropping_column_and_rows/
# 3) https://www.shanelynn.ie/using-pandas-dataframe-creating-editing-viewing-data-in-python/
# 4) https://stackoverflow.com/questions/25025621/check-for-value-in-list-of-pandas-data-frame-columns
# 5) https://stackoverflow.com/questions/23307301/pandas-replacing-column-values-in-dataframe
# 6) https://www.datacamp.com/community/tutorials/categorical-data
# 7) https://datascience.stackexchange.com/questions/9443/when-to-use-one-hot-encoding-vs-labelencoder-vs-dictvectorizor
# 8) https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
# 9) http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html#sklearn.feature_selection.SelectKBest                                                                          
# 10) http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_regression.html#sklearn.feature_selection.f_regression
# 11) https://stackoverflow.com/questions/39812885/retain-feature-names-after-scikit-feature-selection
# 12) https://acadgild.com/blog/decision-tree-python
# 13) https://stats.stackexchange.com/questions/111467/is-it-necessary-to-scale-the-target-value-in-addition-to-scaling-features-for-re/112152
# 14) https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
# 15) http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html
# 16) https://stackoverflow.com/questions/30447083/python-pandas-return-only-those-rows-which-have-missing-values
# 17) https://stackoverflow.com/questions/19226488/change-one-value-based-on-another-value-in-pandas
# 18) https://stackoverflow.com/questions/22546425/using-pandas-to-select-rows-conditional-on-multiple-equivalencies
# 19) https://stackoverflow.com/questions/27905295/how-to-replace-nans-by-preceding-values-in-pandas-dataframe
# 20) https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
# 21) https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
# 22) http://www.espn.com/college-football/rankings/_/poll/1/week/12/year/2018/seasontype/2
# 23) http://www.espn.com/college-football/rankings/_/poll/1/week/13/year/2018/seasontype/2
# 24) https://erikrood.com/Python_References/iterate_rows_pandas.html