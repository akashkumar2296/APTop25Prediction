# Kevin Cass, Akash Kumar, Kee Mok, Daniel Lauer, and Carol Sikes
# CSE 6242 Semester Project - Larger Final Machine Learning Model
# 20 November 2018

###############################################################################
###############################################################################

# SECTION I - DATA LOADING AND EXPLORATION:

# Import the python software libraries that will be used in this script:

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as Scatter_plot
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_validate, GridSearchCV

# -----------------------------------------------------------------------------

# Read in/upload the dataset, which has been collected by team members and will 
# be used in building the relevant machine learning model. Make sure to
# navigate to the directory on computer where this dataset file is found:
   
Football_dataset = pd.read_csv("Larger Data Set.csv")
Football_dataset = Football_dataset.loc[:, "Year":"Rank"]

# View the first few rows of "Football_dataset" to explore its features:
    
Football_dataset.head()

# Obtain an overview of the features in "Football_dataset":
    
Football_dataset.describe(include = "all")

# -----------------------------------------------------------------------------

# Determine if the dataset has any missing values (missing values can affect 
# model outcomes):

Football_dataset.isnull().values.sum() # The dataset has 1,670 missing values, 
                                       # which will be handled below.

# Show rows with missing values:

Missing_val_rows = Football_dataset[Football_dataset.isnull().any(axis = 1)]

###############################################################################
###############################################################################

# SECTION II - DATA CLEANING AND PREPARATION:

# Subset the dataset to only include rows with a "Rank" feature value of less
# than 40. The reason for this is that most "Rank" values are at 50, or near
# 50. Because of how prominent those high rank values are, they bias eventual
# rank predictions towards much higher values. Removing them leads to much
# better model performance:

Football_dataset = Football_dataset[Football_dataset["Rank"] < 40]

# -----------------------------------------------------------------------------

# Modify all rows from the dataset with a "GameStatus" feature value of "DNP" 
# ("Did not play"). First, set the "OppTeam" feature for such rows to "BYE":

Football_dataset["OppTeam"][Football_dataset.GameStatus == "DNP"] = "BYE"

# Second, set the "Opp Conf" feature for such rows to the value found in that
# row's "Conference" feature:

Football_dataset["Opp Conf"][Football_dataset.GameStatus == "DNP"] = \
Football_dataset.Conference

# Third, set the "TODiff", "YPPDiff", "PenYdDiff", and "TOPDiff" features to be 
# equal to their respective values found immediately in the row above. This 
# takes care of filling in values for rows with a "GameStatus" feature value of
# "DNP", as well as for other rows with missing values:

Football_dataset = Football_dataset.replace("na", np.nan)
Football_dataset = Football_dataset.replace("#DIV/0!", np.nan)
   
Football_dataset.fillna(method = "ffill", inplace = True)
    
# -----------------------------------------------------------------------------

# Determine the data types of the dataset's features:

Football_dataset.dtypes

# Make a series of data type conversions for various dataset columns, in order
# to make dataset values more compatible for machine learning modeling. For 
# instance, certain string, or "object" variables should be converted to 
# categoricals, as categoricals are easier for a model to interpret:

Cat_feat = ["Year", "Team", "Week", "Conference", "H/A/N", "Fav/Und",\
            "OppTeam", "Opp Conf", "WinLose", "OT?", "GameStatus"]

Num_feat = ["PrevRank", "RankDiff", "ScoreDiff", "TODiff", "YPPDiff", \
            "PenYdDiff", "TOPDiff", "WinPer", "TimeRem"] # Used later on.

Int_feat = ["TODiff", "PenYdDiff", "TOPDiff", "TimeRem"]
Float_feat = ["YPPDiff", "WinPer"]

Football_dataset[Cat_feat] = Football_dataset[Cat_feat].astype("category") 
Football_dataset[Int_feat] = Football_dataset[Int_feat].astype("int") 
Football_dataset[Float_feat] = Football_dataset[Float_feat].astype("float")

# -----------------------------------------------------------------------------

# Scale all numeric features in the dataset according to the unit scale (where
# each feature's values have a mean of 0 and variance of 1), as scaling like 
# this is an important step in model optimization. Note that the one exception 
# to this is our target feature, "Rank", which does not have to be scaled:

Football_dataset[Num_feat] = StandardScaler().\
                             fit_transform(Football_dataset[Num_feat])

###############################################################################
###############################################################################

# SECTION III - DATA VISUALIZATION:

# Produce box plots to explore the relationship between categorical features
# and team "Rank" in the dataset (plots are not designed to be aesthetically
# pleasing, but to get a sense of the dataset's categorical features, and
# to determine if any of them could be eliminated from the model - if there is
# no variability between each feature category and "Rank", then the feature
# may be a candidate for removal):

for Categorical_feature in Cat_feat:
    Football_dataset.boxplot("Rank", Categorical_feature) 
    
    # At least some variability is present between each categorical feature and
    # team rank ("Rank"), except for between "Year", "OT?", and "GameStatus" 
    # and rank - these features may be candidates for removal.

# -----------------------------------------------------------------------------

# Produce scatter plots to explore the relationship between numerical features
# and team "Rank" in the dataset (for similar reasons as the boxplots above,
# and not meant to be aesthetically pleasing - if there is no pattern between
# feature values and "Rank", then the feature may be a candidate for removal):

for Numeric_feature in Num_feat:
    Scatter_plot.figure()
    Scatter_plot.plot(Football_dataset[Numeric_feature],\
                      Football_dataset.Rank, 'o') 
    
    # The only numeric feature with a strong relationship with "Rank" is 
    # "PrevRank". "RankDiff" has a somewhat strong relationship, but all other
    # features may be candidates for removal.
                                                                            
###############################################################################
###############################################################################

# SECTION IV - FEATURE SELECTION:
                                                                            
# Python Scikit-Learn treats every feature as numeric. Thus, the categorical
# (previously string) features of our dataset need to be treated as numeric.
# One way of doing this is through one-hot encoding, where each category in
# each feature is given a column of its own, in which the column has values of
# "0" for every row in which that category is not present, and a "1" where it
# is present("1"/"0" interpreted as TRUE/FALSE). The advantage of this is 
# ensuring that all categories are given equal weight by the model.                                                                                     
# This does, of course, have the disadvantage of producing many new features
# and potentially leading to the "curse of dimensionality". Nonetheless, this 
# disadvantage will be avoided through feature selection via a procedure called 
# "SelectKBest", which should reduce the number of features we have down to 
# only the essential ones:

# Execute one-hot encoding on all categorical columns of the dataset:
                                                                            
Football_dataset = pd.get_dummies(Football_dataset, columns = Cat_feat,\
                                  prefix = Cat_feat)

# -----------------------------------------------------------------------------

# Perform "SelectKBest" on the dataset - this reduces the size of the dataset
# to only include the features with the highest "K" score, which in this case
# is determined based off of linear regression analysis performed on each
# feature as it relates to the "Rank" feature (the target feature of interest).
# "k" was chosen to be 90, in order to align with the number of eventual
# features present in the dataset of in-progress games used for employing
# our model (see Section VII below):

Football_dataset_feat = Football_dataset.drop("Rank", 1)

Football_dataset_selected = SelectKBest(score_func = f_regression, k = 90)
Football_dataset_selected_fit = Football_dataset_selected.fit\
                                (Football_dataset_feat, Football_dataset.Rank)

# Now, "Football_dataset_features_fit" has the final features, but doesn't have
# their feature labels. Retrieve the labels and update the "Football_dataset"
# dataframe with them, as well as with their associated features (such that 
# "Football_dataset" will have the most essential features and their labels):

Football_dataset_feat2 = Football_dataset.loc[:,\
                            Football_dataset_selected.get_support()]

Football_dataset = pd.concat([Football_dataset_feat2, Football_dataset.Rank],
                             axis = 1)

###############################################################################
###############################################################################

# SECTION V - MACHINE LEARNING MODEL (TRAINING AND TESTING):

# Indicate that the "Rank" feature is the target feature, and the rest of the
# features are predictors of that target:

Target_feature = Football_dataset.loc[:, "Rank"]
Predict_features = Football_dataset.loc[:, Football_dataset.columns != "Rank"]

# Split the dataset ("Football_dataset") into sections - 70% of the data will
# be used to train the machine learning model, and the other 30% to test it:

Predictor_train, Predictor_test, Target_train, Target_test =\
train_test_split(Predict_features, Target_feature, test_size = 0.3,\
                 random_state = 100)

# -----------------------------------------------------------------------------

# Tune model hyperparameters to determine what the best "max_depth" of the
# decision tree machine learning model should be:

Decision_tree_hp = DecisionTreeRegressor()
Decision_tree_max_depth = {'max_depth': [1, 10, 100, 1000]}
Decision_tree_hp_results = GridSearchCV(estimator = Decision_tree_hp,\
                                        param_grid = Decision_tree_max_depth,\
                                        cv = 10).fit(Predictor_train,\
                                        Target_train)

# Print the result of this tuning to output the best "max_depth":

print (Decision_tree_hp_results.best_params_)

# -----------------------------------------------------------------------------

# Train the machine learning model:

Decision_tree = DecisionTreeRegressor(max_depth = 10, random_state = 100)
Machine_learning_model = Decision_tree.fit(Predictor_train, Target_train)

# Test the model on the "test" portion of the dataset:

Model_test = Machine_learning_model.predict(Predictor_test).round()

###############################################################################
###############################################################################

# SECTION VI - MACHINE LEARNING MODEL (EVALUATION):

# Evaluate the model's accuracy in predicting "Rank" values through metrics:

Model_evaluation_r2 = metrics.r2_score(Target_test, Model_test)
Model_evaluation_MAE = metrics.mean_absolute_error(Target_test, Model_test)
Model_evaluation_MSE = metrics.mean_squared_error(Target_test, Model_test)

# The R^2 value is not the best metric of model success, but the fact that it 
# is 0.91 may be promising (assuming the model is not overfit). This means that 
# the predicted and actual "Rank" values are strongly correlated (since 0.95 
# is comparatively near 1 on an R^2 scale of -1 to 1).

# -----------------------------------------------------------------------------

# Evaluate the model's performance via a scatter plot (not to be aesthetically
# pleasing, but to show correlation between predicted and true "Rank"):

Scatter_plot.figure()
Scatter_plot.scatter(Target_test, Model_test)
Scatter_plot.xlabel("True Rank")
Scatter_plot.ylabel("Predicted Rank")

# There is evidently a fair amount of positive correlation between predicted 
# "Rank" (by the model) and true "Rank".

# -----------------------------------------------------------------------------

# Evaluate the model's accuracy through cross-validation:

Cross_validation = cross_validate(Decision_tree, Predict_features,\
                                  Target_feature, cv = 3,\
                                  scoring = ("r2", "neg_mean_absolute_error",\
                                  "neg_mean_squared_error"),\
                                  return_train_score = False)

# Here, the dataset was split into three subsections, and each was trained and
# tested using the machine learning model created above. The evaluation metrics
# of MAE, MSE, and R^2 are in general agreement with those calculated above.
                                  
###############################################################################
###############################################################################

# SECTION VII - MACHINE LEARNING MODEL (STORAGE, EMPLOYMENT, AND OUTPUT):
                                  
# Store the trained machine learning model to a local directory (so that it
# doesn't have to be trained again, but can simply be referenced and easily
# called upon for employment to new data):

Model_saved = "Trained_model.sav"
pickle.dump(Machine_learning_model, open(Model_saved, "wb"))

# -----------------------------------------------------------------------------

# Re-load the trained model, so that it can be employed on new data from in-
# progress football games. Note that all code can be run below without running
# any code above, and predictions can still be made:

import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

Model_reloaded = pickle.load(open("Trained_model.sav", "rb"))

# Read in the in-progress football game dataset, on which the trained machine
# learning model will be employed:

In_prog_dataset = pd.read_csv("In Progress Data.csv")

# Eyeballing the data reveals that it has no missing values or "na"s. Thus,
# skip to checking the data types of the dataset's features:

In_prog_dataset.dtypes                                 

# Make the same data type conversions on this data set as with the "Football_
# dataset" above:

Cat_feat = ["Year", "Team", "Week", "Conference", "H/A/N", "Fav/Und",\
            "OppTeam", "Opp Conf", "WinLose", "OT?", "GameStatus"]

Num_feat = ["PrevRank", "RankDiff", "ScoreDiff", "TODiff", "YPPDiff", \
            "PenYdDiff", "TOPDiff", "WinPer", "TimeRem"] # Used later on.

Int_feat = ["TODiff", "PenYdDiff", "TOPDiff", "TimeRem"]
Float_feat = ["YPPDiff", "WinPer"]

In_prog_dataset[Cat_feat] = In_prog_dataset[Cat_feat].astype("category") 
In_prog_dataset[Int_feat] = In_prog_dataset[Int_feat].astype("int") 
In_prog_dataset[Float_feat] = In_prog_dataset[Float_feat].astype("float")

# Scale the "ScoreDiff", "TODiff", "PenYdDiff", and "TOPDiff" linearly based
# on the time remaining in the game (out of 3,600 seconds total for a game):

Scale_feat = ["ScoreDiff", "TODiff", "PenYdDiff", "TOPDiff"]

for Feature in Scale_feat:
    In_prog_dataset[Feature] = (In_prog_dataset[Feature] * (3600 / \
                                In_prog_dataset.TimeRem)).round()

# Scale all numeric features in the dataset exactly as with the "Football_
# dataset" above:

In_prog_dataset[Num_feat] = StandardScaler().\
                            fit_transform(In_prog_dataset[Num_feat])

# Perform one-hot encoding on the dataset, exactly as with the "Football_
# dataset" above:
                             
In_prog_dataset = pd.get_dummies(In_prog_dataset, columns = Cat_feat,\
                                 prefix = Cat_feat)

# Remove the "Rank" target column from the dataset:

In_prog_dataset = In_prog_dataset.loc[:, In_prog_dataset.columns != "Rank"]

# Use the reloaded model above to employ the trained model on this dataset:

Model_result = Model_reloaded.predict(In_prog_dataset).round()

# -----------------------------------------------------------------------------

# Provide the outputs required by the visualization/UI component of the project
# here below:

# First, output the current week as an integer:

Current_week = 12

# Second, output the actual and predicted AP rankings for all teams previously
# ranked in the top-25 in the "In_prog_dataset" dataset (refer to "PrevRank"
# feature). Note that integer rankings are listed in the order that top-25 
# teams appear in the dataset. For example, in "Actual_AP_rankings", "1" refers
# to Alabama, while "19" refers to Cincinnati:

import numpy as np

Actual_AP_rankings = np.array([1, 9, 15, 21, 3, 12, 5, 4, 2, 6, 10, 13, 18,\
                              11, 19])

Predicted_AP_rankings = np.array([3, 10, 11, 15, 4, 21, 5, 3, 4, 7, 15, 11,\
                                  25, 10, 30])
    
# Third, create a dictionary of dictionaries that contains details of games for
# each row in the "In_prog_dataset" dataset:
    
In_prog_dataset_2 = pd.read_csv("In Progress Data.csv")    
In_prog_dataset_2 = In_prog_dataset_2[In_prog_dataset_2["PrevRank"] < 25]    
    
Game_details = {}

for Index, Row in In_prog_dataset_2.iterrows():
    
    if (Row["H/A/N"] == "H"):
        Game_details["team1"] = {"Id":str(Row["Team"]),\
                                 "score":int(Row["ScoreDiff"])}
        Game_details["team2"] = {"Id":str(Row["OppTeam"]),\
                                 "score":int(Row["ScoreDiff"])}
        Game_details["time"] = str(Row["TimeRem"])
        
        print(Game_details)
    
    elif (Row["H/A/N"] == "A"):
        Game_details["team1"] = {"Id":str(Row["OppTeam"]),\
                                 "score":int(Row["ScoreDiff"])}
        Game_details["team2"] = {"Id":str(Row["Team"]),\
                                 "score":int(Row["ScoreDiff"])}
        Game_details["time"] = str(Row["TimeRem"])
        
        print(Game_details)
    
    elif (Row["H/A/N"] == "N"):
        Game_details["team1"] = {"Id":"Notre Dame", "score":20}
        Game_details["team2"] = {"Id":"Syracuse", "score":20}
        Game_details["time"] = str(1800)
        
        print(Game_details)
        
# Fourth, create a function that outputs a predicted ranking for an input top-
# 25-ranked team in the "In_prog_dataset" dataset:

def Ranking_prediction(Team):
    
    # NOTE: ensure that both "In_prog_dataset" and "Model_reloaded" are both
    # present from above, as they are used in this function.
    
    Team_rank = In_prog_dataset[In_prog_dataset["Team" + "_" + str(Team)] == 1]
    
    Func_model_result = Model_reloaded.predict(Team_rank).round()
    Func_model_result = Func_model_result.astype("int")
    Func_model_result = Func_model_result[0]
    
    return Func_model_result

###############################################################################
###############################################################################

# SECTION VIII - REFERENCES (which helped guide us):
    
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
# 23) https://erikrood.com/Python_References/iterate_rows_pandas.html
 