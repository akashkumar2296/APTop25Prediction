# Kevin Cass, Akash Kumar, Kee Mok, Daniel Lauer, and Carol Sikes
# CSE 6242 Semester Project - Final Employed Model on Completed Games Wk 9 - 11
# 20 November - 3 December 2018

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
# feature) of greater than 30, as the focus of our project is on top-25 teams
# (nonetheless, "30" here was chosen because it led to better model results for
# top-25 teams):

Completed_game_dataset = Completed_game_dataset.dropna()
Completed_game_dataset = Completed_game_dataset[Completed_game_dataset["Rank"]\
                                                <= 30]

# Reset index after dropping low-ranked teams:

Completed_game_dataset = Completed_game_dataset.reset_index(drop=True)

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
                             
Completed_game_dataset2 = pd.get_dummies(Completed_game_dataset, columns =\
                                        Cat_feat, prefix = Cat_feat)

# Perform "SelectKBest" on the dataset to get it down to 90 features (89 + 
# "Rank"), such that it is compatible with the trained model, and done exactly 
# as with the "Football_dataset" variable in the "Script_Final_Trained_
# Model.py" script. 90 features were originally chosen to align with the size 
# of one of the one-hot encoded datasets of in-progress games (see "Script_
# Final_Employed_Model_InProgress_Games_Week_12_Post_Process"):

Completed_game_dataset_feat = Completed_game_dataset2.drop("Rank", 1)

Completed_game_dataset_selected = SelectKBest(score_func = f_regression,\
                                              k = 89)

Completed_game_dataset_selected_fit = Completed_game_dataset_selected.fit\
                                (Completed_game_dataset_feat,\
                                 Completed_game_dataset2.Rank)

Completed_game_dataset_feat2 = Completed_game_dataset2.loc[:,\
                               Completed_game_dataset_selected.get_support()]

Completed_game_dataset2 = pd.concat([Completed_game_dataset_feat2,\
                                    Completed_game_dataset2.Rank], axis = 1)

# -----------------------------------------------------------------------------

# Use the reloaded model above to employ the trained model on this dataset,
# now that it has been properly processed:

Model_result = Model_reloaded.predict(Completed_game_dataset2)

# -----------------------------------------------------------------------------

# Perform post-processing steps on the predictions in "Model_result":

# Put the raw predicted rankings from "Model_result" into a dataframe, and 
# append the team names and previous ranks associated with the rankings to the
# dataframe:

mod_result = pd.DataFrame(Model_result, columns=['ranks'])
mod_result['Team'] = Completed_game_dataset['Team']
mod_result['PrevRank'] = Completed_game_dataset['PrevRank']
mod_result['Week'] = Completed_game_dataset['Week']

# Remove results from teams not previously ranked above 50 using the scaled 
# value of PrevRank, and split up results by week:

result_wk9 = mod_result[(mod_result['Week'] == 9)]
result_wk10 = mod_result[(mod_result['Week'] == 10)]
result_wk11 = mod_result[(mod_result['Week'] == 11)]

# Sort the resulting rankings in order by the predicted ranks and previous
# rank, then adjust the index of the dataframe so that it is in order:

result_wk9 = result_wk9.sort_values(by=['ranks', 'PrevRank'])
result_wk10 = result_wk10.sort_values(by=['ranks', 'PrevRank'])
result_wk11 = result_wk11.sort_values(by=['ranks', 'PrevRank'])
result_wk9 = result_wk9.reset_index(drop=True)
result_wk10 = result_wk10.reset_index(drop=True)
result_wk11 = result_wk11.reset_index(drop=True)

# Create a set to hold rankings that have been assigned so that duplicates can
# be avoided:

rank_set_wk9 = set()
rank_set_wk10 = set()
rank_set_wk11 = set()

# Loop through the list of predicted rankings and assign an unique integer
# rank based on team position in the sorted listed as well as deviation 
# between the predicted rank and the location in the list (because this set
# of rankings is based on most games but don't represent all the teams due to
# bye weeks that would be in the top 25, the rank_diff accounts for the fact 
# that there will be gaps in the list of predicted rankings):

for i in range(len(result_wk9)):
    pot_rank = i + 1
    rank_diff = result_wk9.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_wk9.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_wk9:
        pot_rank += 1
    if pot_rank2 in rank_set_wk9:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 4) and (result_wk9.iloc[i]['ranks'] < 25):
        result_wk9.at[i, 'ranks'] = pot_rank
        rank_set_wk9.add(pot_rank)
    else:
        result_wk9.at[i, 'ranks'] = pot_rank2
        rank_set_wk9.add(pot_rank2)

# Loop through the list of predicted rankings and assign an unique integer
# rank based on team position in the sorted listed as well as deviation 
# between the predicted rank and the location in the list (because this set
# of rankings is based on most games but don't represent all the teams due to
# bye weeks that would be in the top 25, the rank_diff accounts for the fact 
# that there will be gaps in the list of predicted rankings):
        
for i in range(len(result_wk10)):
    pot_rank = i + 1
    rank_diff = result_wk10.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_wk10.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_wk10:
        pot_rank += 1
    if pot_rank2 in rank_set_wk10:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 4) and (result_wk10.iloc[i]['ranks'] < 25):
        result_wk10.at[i, 'ranks'] = pot_rank
        rank_set_wk10.add(pot_rank)
    else:
        result_wk10.at[i, 'ranks'] = pot_rank2
        rank_set_wk10.add(pot_rank2)
                    
# Loop through the list of predicted rankings and assign an unique integer
# rank based on team position in the sorted listed as well as deviation 
# between the predicted rank and the location in the list (because this set
# of rankings is based on most games but don't represent all the teams due to
# bye weeks that would be in the top 25, the rank_diff accounts for the fact 
# that there will be gaps in the list of predicted rankings):
        
for i in range(len(result_wk11)):
    pot_rank = i + 1
    rank_diff = result_wk11.iloc[i]['ranks'] - pot_rank
    pot_rank2 = result_wk11.iloc[i]['ranks'].round()
    
# If potential rank values are already in the set of assigned rankings, then
# the potential value is increased by 1:
    
    if pot_rank in rank_set_wk11:
        pot_rank += 1
    if pot_rank2 in rank_set_wk11:
        pot_rank2 += 1
        
# To adjust for gaps that should occur in the rankings when predictions are 
# made for an incomplete list, particularly an issue for higher ranking (top
# ten) teams, "if" statement checks that potential rank is reasonably close to 
# original predicted value and then assigns either the potential rank based
# on the for loop index or the original rounded rank accordingly:
        
    if (rank_diff <= 4) and (result_wk11.iloc[i]['ranks'] < 25):
        result_wk11.at[i, 'ranks'] = pot_rank
        rank_set_wk11.add(pot_rank)
    else:
        result_wk11.at[i, 'ranks'] = pot_rank2
        rank_set_wk11.add(pot_rank2)
    
# Join results from separate weeks back together:

final_result = pd.concat([result_wk9, result_wk10, result_wk11], axis=0)

# Sort both results and original data so that the order is the same
#result_wk9 = result_wk9.sort_values(by=['ranks', 'PrevRank']):

final_result = final_result.sort_values(by=['Week', 'Team'])
final_result = final_result.reset_index(drop=True)
Completed_game_dataset = Completed_game_dataset.sort_values(by=['Week', 'Team'])
Completed_game_dataset = Completed_game_dataset.reset_index(drop=True)


###############################################################################
###############################################################################

# SECTION II - MACHINE LEARNING MODEL (EMPLOYMENT EVALUATION):

# Evaluate the model's accuracy in predicting "Rank" values for completed
# games through metrics:

Emp_model_evaluation_r2 = metrics.r2_score(final_result.ranks,\
                                           Completed_game_dataset.Rank)
Emp_model_evaluation_MAE = metrics.mean_absolute_error\
                                          (final_result.ranks,\
                                           Completed_game_dataset.Rank)
Emp_model_evaluation_MSE = metrics.mean_squared_error\
                                          (final_result.ranks,\
                                           Completed_game_dataset.Rank)

# The R^2 value is not the best metric of model success, but the fact that it 
# is 0.52 is decent. This means that the predicted and actual "Rank" 
# values are somewhat correlated (since 0.52 is decently near 1 on an R^2 scale 
# of 0 to 1).

# -----------------------------------------------------------------------------

# Evaluate the model's performance via a scatter plot (not to be aesthetically
# pleasing, but to show correlation between predicted and true "Rank"):

Scatter_plot.figure()
Scatter_plot.scatter(Completed_game_dataset.Rank, final_result.ranks)
Scatter_plot.xlabel("True Rank")
Scatter_plot.ylabel("Predicted Rank")

# There is evidently a fair amount of positive correlation between predicted 
# "Rank" (by the model) and true "Rank". It is interesting that there are some
# outlier points, which are most likely the reason for why the R^2 value above
# was lower. If these outliers were to be somehow handled or removed, model
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