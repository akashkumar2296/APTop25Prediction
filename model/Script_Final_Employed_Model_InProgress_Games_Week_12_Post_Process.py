# Kevin Cass, Akash Kumar, Kee Mok, Daniel Lauer, and Carol Sikes
# CSE 6242 Semester Project - Final Employed Model on In-Progress Games Week 12
# 20 November - 3 December 2018

###############################################################################
###############################################################################

# SECTION I - MACHINE LEARNING MODEL (EMPLOYMENT):

# Import the python software libraries that will be used in this script:

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as Scatter_plot
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

# Load up the trained model (trained and stored in the "Script_Final_Trained_
# Model.py" script), so that it can be employed on new data from in-
# progress football games:

Model_reloaded = pickle.load(open("Model_trained.sav", "rb"))

# Read in the in-progress football game dataset, on which the trained machine
# learning model will be employed:

In_prog_dataset = pd.read_csv("Dataset_Final_InProgress_Game_Data_Week_12.csv")

# -----------------------------------------------------------------------------

# Eyeballing the data reveals that it has no missing values or "na"s (except
# for the "Rank" column, which is OK). Thus, skip to checking the data types of 
# the dataset's features:

In_prog_dataset.dtypes                                 

# Make the same data type conversions on this data set as with the "Football_
# dataset" variable in the "Script_Final_Trained_Model.py" script:

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
                                (3600 - In_prog_dataset.TimeRem))).round()

# Scale all numeric features in the dataset exactly as with the "Football_
# dataset" variable in the "Script_Final_Trained_Model.py" script:

In_prog_dataset[Num_feat] = StandardScaler().\
                            fit_transform(In_prog_dataset[Num_feat])

# Perform one-hot encoding on the dataset, exactly as with the "Football_
# dataset" variable in the "Script_Final_Trained_Model.py" script:
                             
In_prog_dataset2 = pd.get_dummies(In_prog_dataset, columns = Cat_feat,\
                                 prefix = Cat_feat)

# Remove the "Rank" target column from the dataset:

In_prog_dataset2 = In_prog_dataset2.loc[:, In_prog_dataset2.columns != "Rank"]

# -----------------------------------------------------------------------------

# Use the reloaded model above to employ the trained model on this dataset,
# now that it has been properly processed:

Model_result = Model_reloaded.predict(In_prog_dataset2)

# -----------------------------------------------------------------------------

# Perform post-processing steps on the predictions in "Model_result":

# Put the raw predicted rankings from "Model_result" into a dataframe, and 
# append the team names and previous ranks associated with the rankings to the
# dataframe:

mod_result = pd.DataFrame(Model_result, columns=['ranks'])
mod_result['Team'] = In_prog_dataset['Team']
mod_result['PrevRank'] = In_prog_dataset['PrevRank']

# Remove results from teams not previously ranked above 50 using the scaled 
# value of PrevRank:

mod_result.drop(mod_result.loc[mod_result['PrevRank'] >= 1].index,\
                inplace=True)

# Sort the resulting rankings in order by the predicted ranks and previous
# rank, then adjust the index of the dataframe so that it is in order:

mod_result = mod_result.sort_values(by=['ranks', 'PrevRank'])
mod_result = mod_result.reset_index(drop=True)

# Create a set to hold rankings that have been assigned so that duplicates can
# be avoided:

rank_set = set()

# Loop through the list of predicted rankings and assign an unique integer
# rank based on team position in the sorted listed as well as deviation 
# between the predicted rank and the location in the list (because this set
# of rankings is based on just a few games that don't represent all the teams
# that would be in the top 25, the rank_diff accounts for the fact that there
# will be gaps in the list of predicted rankings):

for i in range(len(mod_result)):
    pot_rank = i + 1
    rank_diff = mod_result.iloc[i]['ranks'] - pot_rank
    pot_rank2 = mod_result.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set:
        pot_rank += 1
    if pot_rank2 in rank_set:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 2) and (mod_result.iloc[i]['ranks'] < 10):
        mod_result.at[i, 'ranks'] = pot_rank
        rank_set.add(pot_rank)
    else:
        mod_result.at[i, 'ranks'] = pot_rank2
        rank_set.add(pot_rank2)

###############################################################################
###############################################################################

# SECTION II - MACHINE LEARNING MODEL (EMPLOYMENT EVALUATION):

# Output the actual and predicted (from the "mod_result" variable above) AP 
# rankings for all teams previously ranked in the top 25 in the "In_prog_
# dataset" dataset (refer to "PrevRank" feature). Note that all teams ranked
# with a ranking higher than 25 are left out here, as they are not the focus of
# our project, and therefore the trained model was not built to focus on those 
# teams. Also note that integer rankings are listed in the order that top-25 
# teams appear in the dataset. That order is as follows: Alabama, Ohio State,
# Florida, Utah, Notre Dame, Syracuse, Georgia, Michigan, Clemson, Oklahoma,
# LSU, Texas, Iowa State, UCF, and Cincinnati.

Actual_AP_rankings_wk_12 = np.array([1, 9, 15, 21, 3, 12, 5, 4, 2, 6, 10,\
                                     13, 18, 11, 19])

Predicted_AP_rankings_wk_13 = np.array([1, 10, 11, 26, 4, 21, 5, 2, 3, 6, 15,\
                                        12, 25, 8, 30])
    
Actual_AP_rankings_wk_13 = np.array([1, 10, 11, 17, 3, 20, 5, 4, 2, 6, 7,\
                                     14, 25, 9, 26])

# Evaluate the model's accuracy in predicting "Rank" values for in-progress
# games through metrics:

Emp_model_evaluation_r2 = metrics.r2_score(Predicted_AP_rankings_wk_13,\
                                           Actual_AP_rankings_wk_13)
Emp_model_evaluation_MAE = metrics.mean_absolute_error\
                                          (Predicted_AP_rankings_wk_13,\
                                           Actual_AP_rankings_wk_13)
Emp_model_evaluation_MSE = metrics.mean_squared_error\
                                          (Predicted_AP_rankings_wk_13,\
                                           Actual_AP_rankings_wk_13)

# The R^2 value is not the best metric of model success, but the fact that it 
# is 0.86 is promising. This means that the predicted and actual "Rank" values 
# are strongly correlated (since 0.86 is comparatively near 1 on an R^2 scale 
# of 0 to 1).

# -----------------------------------------------------------------------------

# Evaluate the model's performance via a scatter plot (not to be aesthetically
# pleasing, but to show correlation between predicted and true "Rank"):

Scatter_plot.figure()
Scatter_plot.scatter(Actual_AP_rankings_wk_13, Predicted_AP_rankings_wk_13)
Scatter_plot.xlabel("True Rank")
Scatter_plot.ylabel("Predicted Rank")

# There is evidently a fair amount of positive correlation between predicted 
# "Rank" (by the model) and true "Rank".

###############################################################################
###############################################################################

# SECTION III - MACHINE LEARNING MODEL (OUTPUTS FOR UI/VISUALIZATION):

# Provide the outputs required by the visualization/UI component of the project
# here below:

# First, output the current week as an integer:

Current_week = 12

print("This is the current week of interest for our model:")
print(Current_week)

# Second, output predicted and actual ranks for top-25 teams present in the
# "In_prog_dataset" dataset for Week 13. Note that the order of teams here is
# as follows: Alabama, Ohio State, Florida, Utah, Notre Dame, Syracuse,
# Georgia, Michigan, Clemson, Oklahoma, LSU, Texas, Iowa State, UCF, and 
# Cincinnati:

print("These are actual rankings from Wk 13 for a sample of top-25 teams:")

print(Actual_AP_rankings_wk_13)

print("These are predicted rankings for Wk 13 for a sample of top-25 teams:")

print(Predicted_AP_rankings_wk_13)
    
# Third, create a dictionary of dictionaries that contains details of games for
# each row in the "In_prog_dataset_2" dataset. Ensure that the team names are
# formatted/spelled correctly, as required by the UI/Visualization component
# of our project:
    
In_prog_dataset_2 = pd.read_csv\
                    ("Dataset_Final_InProgress_Game_Data_Week_12.csv")    
In_prog_dataset_2 = In_prog_dataset_2[In_prog_dataset_2["PrevRank"] <= 25]  

In_prog_dataset_2["Team"] = In_prog_dataset_2["Team"].str.lower()
In_prog_dataset_2["Team"] = In_prog_dataset_2["Team"].str.replace(" ", "")
    
print("These are the game details for our model:")

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
# 25-ranked team in the "In_prog_dataset"/"In_prog_dataset_2" dataset:

def Ranking_prediction(Team):
    
    # NOTE: ensure that "mod_result" is present from above, as it is used in
    # this function.
    
    Func_model_result = mod_result["ranks"][mod_result["Team"] == Team].item()

    Func_model_result = int(Func_model_result)
    
    return Func_model_result

Predicted_teams = ["Alabama", "Ohio State", "Florida", "Utah", "Notre Dame",\
                   "Syracuse", "Georgia", "Michigan", "Clemson", "Oklahoma",\
                   "LSU", "Texas", "Iowa State", "UCF", "Cincinnati"]

print("These are predictions outputted by the Ranking_prediction function:")

for Team in Predicted_teams:

    print(str(Team) + ":" + " " + str(Ranking_prediction(Team)))

###############################################################################
###############################################################################

# SECTION IV - REFERENCES (which helped guide us in all modeling scripts):
    
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