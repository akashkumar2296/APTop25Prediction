# Kevin Cass, Akash Kumar, Kee Mok, Daniel Lauer, and Carol Sikes
# CSE 6242 Semester Project - Final Employed Model on In-Progress Games Week 13
# 26 November - 3 December 2018

###############################################################################
###############################################################################

# SECTION I - MACHINE LEARNING MODEL (EMPLOYMENT):

# Import the python software libraries that will be used in this script:

import numpy as np
import pandas as pd
import pickle
import os
import matplotlib.pyplot as Scatter_plot
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

# Load up the trained model (trained and stored in the "Script_Final_Trained_
# Model.py" script), so that it can be employed on new data from in-
# progress football games:

Model_reloaded = pickle.load(open(os.getcwd() + "/model/Model_trained.sav", "rb"))

# Read in the in-progress football game dataset, on which the trained machine
# learning model will be employed:

In_prog_dataset = pd.read_csv(os.getcwd() + "/model/Dataset_Final_InProgress_Game_Data_Week_13.csv")

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

# Remove the "Rank" target column from the dataset, and add 14 filler columns
# to the dataset to make it compatible with the trained model's K-selection of
# 90 features (a number chosen based off of the number of features, post-one-
# hot-encoding, in the Week 12 in-progress dataset --> more features lead to
# better predictions in this case):

In_prog_dataset2 = In_prog_dataset2.loc[:, In_prog_dataset2.columns != "Rank"]

for Column in range(0, 14):
    
    In_prog_dataset2[Column] = 0

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
mod_result['TimeRem'] = In_prog_dataset['TimeRem']

# Remove results from teams not previously ranked above 50 using the scaled 
# value of PrevRank:

mod_result.drop(mod_result.loc[mod_result['PrevRank'] >= 1].index,\
                inplace=True)

# Create new dataframes for each quarter of results in "mod_result":

result_1st = mod_result[(mod_result['TimeRem'] > 1)]
result_2nd = mod_result[(mod_result['TimeRem'] > 0) &\
                        (mod_result['TimeRem'] < 1)]
result_3rd = mod_result[(mod_result['TimeRem'] > -1) &\
                        (mod_result['TimeRem'] < 0)]
result_4th = mod_result[(mod_result['TimeRem'] < -1)]

# Sort the resulting rankings in order by the predicted ranks and previous
# rank, then adjust the index of the dataframe so that it is in order:

result_1st = result_1st.sort_values(by=['ranks', 'PrevRank'])
result_2nd = result_2nd.sort_values(by=['ranks', 'PrevRank'])
result_3rd = result_3rd.sort_values(by=['ranks', 'PrevRank'])
result_4th = result_4th.sort_values(by=['ranks', 'PrevRank'])

result_1st = result_1st.reset_index(drop=True)
result_2nd = result_2nd.reset_index(drop=True)
result_3rd = result_3rd.reset_index(drop=True)
result_4th = result_4th.reset_index(drop=True)

# Create a set to hold rankings that have been assigned so that duplicates can
# be avoided:

rank_set_1st = set()
rank_set_2nd = set()
rank_set_3rd = set()
rank_set_4th = set()

# Loop through the list of predicted rankings and assign an unique integer
# rank based on team position in the sorted list as well as deviation 
# between the predicted rank and the location in the list (because this set
# of rankings is based on just a few games that don't represent all the teams
# that would be in the top 25, the rank_diff accounts for the fact that there
# will be gaps in the list of predicted rankings):

for i in range(len(result_1st)):
    pot_rank = i + 1
    rank_diff = result_1st.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_1st.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_1st:
        pot_rank += 1
    if pot_rank2 in rank_set_1st:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 2) and (result_1st.iloc[i]['ranks'] < 10):
        result_1st.at[i, 'ranks'] = pot_rank
        rank_set_1st.add(pot_rank)
    else:
        result_1st.at[i, 'ranks'] = pot_rank2
        rank_set_1st.add(pot_rank2)

# Repeat the loop for each of the other 3 quarters:
        
for i in range(len(result_2nd)):
    pot_rank = i + 1
    rank_diff = result_2nd.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_2nd.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_2nd:
        pot_rank += 1
    if pot_rank2 in rank_set_2nd:
        pot_rank2 += 1
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 2) and (result_2nd.iloc[i]['ranks'] < 10):
        result_2nd.at[i, 'ranks'] = pot_rank
        rank_set_2nd.add(pot_rank)
    else:
        result_2nd.at[i, 'ranks'] = pot_rank2
        rank_set_2nd.add(pot_rank2)

for i in range(len(result_3rd)):
    pot_rank = i + 1
    rank_diff = result_3rd.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_3rd.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_3rd:
        pot_rank += 1
    if pot_rank2 in rank_set_3rd:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 2) and (result_3rd.iloc[i]['ranks'] < 10):
        result_3rd.at[i, 'ranks'] = pot_rank
        rank_set_3rd.add(pot_rank)
    else:
        result_3rd.at[i, 'ranks'] = pot_rank2
        rank_set_3rd.add(pot_rank2)

for i in range(len(result_4th)):
    pot_rank = i + 1
    rank_diff = result_4th.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_4th.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_4th:
        pot_rank += 1
    if pot_rank2 in rank_set_4th:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, if statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 2) and (result_4th.iloc[i]['ranks'] < 10):
        result_4th.at[i, 'ranks'] = pot_rank
        rank_set_4th.add(pot_rank)
    else:
        result_4th.at[i, 'ranks'] = pot_rank2
        rank_set_4th.add(pot_rank2)

###############################################################################
###############################################################################

# SECTION II - MACHINE LEARNING MODEL (EMPLOYMENT EVALUATION):

# Output the actual and predicted (from the "result_1st", etc. variables above) 
# AP rankings for all teams previously ranked in the top 25 in the "In_prog_
# dataset" dataset (refer to "PrevRank" feature). Note that all teams ranked
# with a ranking higher than 25 are left out here, as they are not the focus of
# our project, and therefore the trained model was not built to focus on those 
# teams. Also note that integer rankings are listed in the order that top-25 
# teams appear in the dataset. That order is as follows: Alabama, Ohio State,
# Michigan, Penn State, Florida, Syracuse, Georgia, Pittsburgh, Clemson, LSU,
# Kentucky, and Notre Dame. Also note that each actual ranking is repeated for 
# a team four times, to match those rankings up with predicted rankings for 
# each team for each quarter of their live, in-progress game in Week 13:

Actual_AP_rankings_wk_13 = np.array([1, 1, 1, 1, 10, 10, 10, 10, 4, 4, 4, 4,\
                                     15, 15, 15, 15, 13, 13, 13, 13, 19, 19,\
                                     19, 19, 5, 5, 5, 5, 24, 24, 24, 24, 2,\
                                     2, 2, 2, 8, 8, 8, 8, 17, 17, 17, 17, 3,\
                                     3, 3, 3])

Predicted_AP_rankings_wk_14 = np.array([1, 1, 1, 1, 9, 7, 8, 8, 4, 5, 10, 12,\
                                        14, 14, 14, 14, 16, 16, 16, 16, 17,\
                                        15, 15, 16, 3, 3, 3, 4, 18, 28, 28,\
                                        32, 2, 2, 2, 2, 8, 6, 9, 9, 13, 13,\
                                        12, 15, 15, 4, 4, 3])
    
Actual_AP_rankings_wk_14 = np.array([1, 1, 1, 1, 6, 6, 6, 6, 8, 8, 8, 8,\
                                     12, 12, 12, 12, 10, 10, 10, 10, 18, 18,\
                                     18, 18, 4, 4, 4, 4, 26, 26, 26, 26, 2,\
                                     2, 2, 2, 14, 14, 14, 14, 15, 15, 15,\
                                     15, 3, 3, 3, 3])
    
                           # Note that here, Pittsburgh was given a ranking 
                           # of "26", to denote that it is no longer in the
                           # top 25 (exact ranking unknown). 

# Evaluate the model's accuracy in predicting "Rank" values for in-progress
# games through metrics:

Emp_model_evaluation_r2 = metrics.r2_score(Predicted_AP_rankings_wk_14,\
                                           Actual_AP_rankings_wk_14)
Emp_model_evaluation_MAE = metrics.mean_absolute_error\
                                          (Predicted_AP_rankings_wk_14,\
                                           Actual_AP_rankings_wk_14)
Emp_model_evaluation_MSE = metrics.mean_squared_error\
                                          (Predicted_AP_rankings_wk_14,\
                                           Actual_AP_rankings_wk_14)

# The R^2 value is not the best metric of model success, but the fact that it 
# is 0.74 is good. This means that the predicted and actual "Rank" values 
# are somewhat correlated (since 0.74 is somewhat near 1 on an R^2 scale 
# of 0 to 1).

# -----------------------------------------------------------------------------

# Evaluate the model's performance via a scatter plot (not to be aesthetically
# pleasing, but to show correlation between predicted and true "Rank"):

Scatter_plot.figure()
Scatter_plot.scatter(Actual_AP_rankings_wk_14, Predicted_AP_rankings_wk_14)
Scatter_plot.xlabel("True Rank")
Scatter_plot.ylabel("Predicted Rank")

# There is evidently a decent amount of positive correlation between predicted 
# "Rank" (by the model) and true "Rank".

###############################################################################
###############################################################################

# SECTION III - MACHINE LEARNING MODEL (OUTPUTS FOR UI/VISUALIZATION):

# Provide the outputs required by the visualization/UI component of the project
# here below:

# First, output the current week as an integer:

Current_week = 13

print("This is the current week of interest for our model:")
print(Current_week)

# Second, output predicted and actual ranks for top-25 teams present in the
# "In_prog_dataset" dataset for Week 14. Note that the order of teams here is
# as follows: Alabama, Ohio State, Michigan, Penn State, Florida, Syracuse, 
# Georgia, Pittsburgh, Clemson, LSU, Kentucky, and Notre Dame:

print("These are actual rankings from Wk 14 for a sample of top-25 teams:")

print(Actual_AP_rankings_wk_14)

print("These are predicted rankings for Wk 14 for a sample of top-25 teams:")

print(Predicted_AP_rankings_wk_14)
    
# Third, create a dictionary of dictionaries that contains details of games for
# each row in the "In_prog_dataset_2" dataset. Ensure that the team names are
# formatted/spelled correctly, as required by the UI/Visualization component
# of our project:
    
In_prog_dataset_2 = pd.read_csv\
                    (os.getcwd() + "/model/Dataset_Final_InProgress_Game_Data_Week_13.csv")    
In_prog_dataset_2 = In_prog_dataset_2[In_prog_dataset_2["PrevRank"] <= 25]  

Team_names = ["Team", "OppTeam"]

for Names in Team_names:

    In_prog_dataset_2[Names] = In_prog_dataset_2[Names].str.lower()
    In_prog_dataset_2[Names] = In_prog_dataset_2[Names].str.replace(" ", "")
    
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
        
# Fourth, create a function that outputs a predicted ranking for an input top-
# 25-ranked team in the "In_prog_dataset"/"In_prog_dataset_2" dataset:

def Ranking_prediction(Team):
    
    # NOTE: ensure that "result_1st", "result_2nd", "result_3rd", and
    # "result_4th" are present from above, as they are used in this function.
    
    Func_mod_result_1 = result_1st["ranks"][result_1st["Team"] == Team].item()
    Func_mod_result_2 = result_2nd["ranks"][result_2nd["Team"] == Team].item()
    Func_mod_result_3 = result_3rd["ranks"][result_3rd["Team"] == Team].item()
    Func_mod_result_4 = result_4th["ranks"][result_4th["Team"] == Team].item()

    Func_mod_result_1 = int(Func_mod_result_1)
    Func_mod_result_2 = int(Func_mod_result_2)
    Func_mod_result_3 = int(Func_mod_result_3)
    Func_mod_result_4 = int(Func_mod_result_4)
    
    return Func_mod_result_1, Func_mod_result_2, Func_mod_result_3,\
           Func_mod_result_4

Predicted_teams = ["Alabama", "Ohio State", "Michigan", "Penn State",\
                   "Florida", "Syracuse", "Georgia", "Pittsburgh", "Clemson",\
                   "LSU", "Kentucky", "Notre Dame"]

def Ranking_prediction_all(quarter):
    
    #return prediction of all teams
    idx = int(quarter)-1;
    all_predictions = []
    for Team in Predicted_teams:
        all_predictions.append({'team':Team, 'ranking':Ranking_prediction(Team)[idx]})
    
    return all_predictions


print("These are predictions outputted by the Ranking_prediction function.")
print("Each team has four numbers/predictions, one for each game quarter:")

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