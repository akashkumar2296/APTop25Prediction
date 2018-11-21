# Kevin Cass, Akash Kumar, Kee Mok, Daniel Lauer, and Carol Sikes
# CSE 6242 Semester Project - Initial Machine Learning Model
# 31 October 2018

# ------------------------

# DATA LOADING AND EXPLORATION:

# Import the python software libraries that will be used in this script:

import pandas as Pandas
import matplotlib.pyplot as Scatter_plot
from sklearn.preprocessing import StandardScaler as Scaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_validate

# Read in/upload the dataset, which has been collected by team members and will be 
# used in building the relevant machine learning model. Make sure to navigate to
# the directory on computer where this dataset file is found:
   
Football_dataset = Pandas.read_csv("Initial Data Template Modified.csv")

# View the first few rows of "Football_dataset" to explore its features:
    
Football_dataset.head()

# Obtain an overview of the features in "Football_dataset":
    
Football_dataset.describe(include = "all")

# Determine if the dataset has any missing values (missing values can affect model outcomes):

Football_dataset.isnull().values.sum()

# ------------------------

# DATA CLEANING AND PREPARATION:

# Remove all rows from the dataset with a "GameStatus" feature value of "DNP",
# ("Did not play"), as these rows contain too many "na" values to be informative to our model:

Football_dataset = Football_dataset[Football_dataset.GameStatus != "DNP"]

# Determine the columns/features of the data containing a value of "na":

Football_dataset.isin(["na"]).any(0)

# For those features that will eventually be converted to numerical columns below (and that have "na"),
# convert the "na" values to "0" (NOTE: I'M NOT SURE IF THIS CONVERSION IS CORRECT - IF YOU ALL THINK
# THAT THE "NA" VALUES SHOULD BE HANDLED DIFFERENTLY HERE, NO WORRIES), as "na"
# can be confusing to a machine learning model in its predictions:

Na_features = ["RankDiff", "HistTODiff", "GameTODiff"]

for Na_feature in Na_features:
    Football_dataset[Na_feature] = Football_dataset[Na_feature].replace("na", 0)

# Determine the data types of the dataset's features:

Football_dataset.dtypes

# Make a series of data type conversions for various dataset columns, in order
# to make dataset values more compatible for machine learning modeling. For instance,
# certain string, or "object" variables should be converted to categoricals, as
# categoricals are easier for a machine learning model to interpret:

Categorical_features = ["Team", "Week", "Conference", "GameStatus", "OppTeam", "OppConf", "WinLose", "HomeAway"]
Numeric_features = ["PrevRank", "TimeRemaining", "ScoreDiff", "WinPer", "RankDiff", "HistTODiff", "GameTODiff"] # Will be used later.
Integer_features = ["ScoreDiff", "RankDiff", "HistTODiff", "GameTODiff"]

Football_dataset[Categorical_features] = Football_dataset[Categorical_features].astype("category")  
Football_dataset[Integer_features] = Football_dataset[Integer_features].astype("int")

# Scale all numeric features in the dataset according to the unit scale (where
# each feature's values have a mean of 0 and variance of 1), as scaling like this is an
# important step in model optimization. Note that the one exception to this is
# our target feature, "Rank", which does not have to be scaled:

Football_dataset[Numeric_features] = Scaler().fit_transform(Football_dataset[Numeric_features])

# ------------------------

# DATA VISUALIZATION:

# Produce box plots to explore the relationship between categorical features
# and team "Rank" in the dataset (these plots are not designed to be aesthetically
# pleasing, but simply to get a sense of the dataset's categorical features, and
# to determine if any of them could be eliminated from the model - if there is
# no variability between each feature category and "Rank", then the feature
# may be a candidate for removal):

for Categorical_feature in Categorical_features:
    Football_dataset.boxplot("Rank", Categorical_feature) # At least some variability is present between each categorical
                                                          # feature and team rank ("Rank"), except for between "HomeAway"
                                                          # and rank - "HomeAway" is potential candidate for removal.

# Produce scatter plots to explore the relationship between numerical features
# and team "Rank" in the dataset (for similar reasons as the boxplots above, and
# also not meant to be aesthetically pleasing - if there is not a pattern between
# feature values and "Rank", then the feature may be a candidate for removal):

for Numeric_feature in Numeric_features:
    Scatter_plot.figure()
    Scatter_plot.plot(Football_dataset[Numeric_feature], Football_dataset.Rank, 'o') # The only numeric feature with a strong relationship
                                                                                     # with "Rank" is "PrevRank" - other features may be
                                                                                     # candidates for removal.
                                                                            
# ------------------------

# FEATURE SELECTION:
                                                                            
# Python Scikit-Learn treats every feature as numeric. Therefore, the categorical
# (previously string) features of our dataset need to be treated as numeric. The best
# way to do this (that I know of) is through one-hot encoding, where each category
# in each feature is given a column of its own, in which the column has values of "0"
# for every row in which that category is not present, and a "1" where it is present (interpreted as TRUE/FALSE).
# The advantage of this is ensuring that all categories are given equal weight by the model.                                                                                     
# This does, of course, have the disadvantage of producing many new columns/features
# and potentially leading to the "curse of dimensionality". Nonetheless, this disadvantage
# will be avoided through feature selection via a procedure called "SelectKBest",
# which should reduce the number of features we have down to only the essential ones
# (NOTE: I AM OPEN TO OTHER IDEAS FOR HOW WE CAN PERFORM FEATURE SELECTION, AS
# I AM NOT SURE IF THIS IS THE BEST METHOD).

# Execute one-hot encoding on all categorical columns of the dataset:
                                                                            
Football_dataset = Pandas.get_dummies(Football_dataset, columns = Categorical_features, prefix = Categorical_features)

# Perform "SelectKBest" on the dataset - this reduces the size of the dataset to
# only include the features with the highest "K" score, which in this case is
# determined based off of linear regression analysis performed on each feature
# as it relates to the "Rank" feature (the target feature of interest):

Football_dataset_features = SelectKBest(score_func = f_regression, k = 40)
Football_dataset_features_fit = Football_dataset_features.fit_transform(Football_dataset, Football_dataset.Rank)

# Now, "Football_dataset_features_fit" has the final features, but doesn't have
# their feature labels. Retrieve the labels and update the "Football_dataset"
# dataframe with them, as well as with their associated features (such that 
# "Football_dataset" will have the most essential features and their labels):

Football_dataset = Football_dataset.loc[:, Football_dataset_features.get_support()]

# ------------------------

# MACHINE LEARNING MODEL - TRAINING AND TESTING:

# Indicate that the "Rank" feature is the target feature, and the rest of the
# features are predictors of that target:

Target_feature = Football_dataset.loc[:, "Rank"]
Predictor_features = Football_dataset.loc[:, Football_dataset.columns != "Rank"]

# Split the dataset ("Football_dataset") into sections - 70% of the dataset will
# be used to train the machine learning model, and the other 30% to test it:

Predictor_train, Predictor_test, Target_train, Target_test = train_test_split(Predictor_features, Target_feature, test_size = 0.3, random_state = 100)

# Train the machine learning model:

Decision_tree = DecisionTreeRegressor(max_depth = 10, random_state = 100)
Machine_learning_model = Decision_tree.fit(Predictor_train, Target_train)

# Test the model on the "test" portion of the dataset:

Model_test = Machine_learning_model.predict(Predictor_test)

# ------------------------

# MACHINE LEARNING MODEL - EVALUATION:

# Evaluate the model's accuracy in predicting "Rank" values through metrics:

Model_evaluation_r2 = metrics.r2_score(Target_test, Model_test)
Model_evaluation_MAE = metrics.mean_absolute_error(Target_test, Model_test)
Model_evaluation_MSE = metrics.mean_squared_error(Target_test, Model_test)

# The R^2 value is not the best metric of model success, but the fact that it is 
# 0.76 is pretty promising. This means that the predicted and actual "Rank" values
# are relatively correlated (since 0.76 is comparatively near 1 on an R^2 scale of
# -1 to 1).

# Evaluate the model's accuracy through a scatter plot (not meant to be aesthetically
# pleasing, but to give a sense of correlation between predicted and true "Rank"):

Scatter_plot.figure()
Scatter_plot.scatter(Target_test, Model_test)
Scatter_plot.xlabel("True Rank")
Scatter_plot.ylabel("Predicted Rank")

# There is evidently a fair amount of positive correlation between predicted "Rank"
# (by the model) and true "Rank".

# Evaluate the model's accuracy through cross-validation:

Cross_validation = cross_validate(Decision_tree, Predictor_features, Target_feature, cv = 3, \
                                  scoring = ("r2", "neg_mean_absolute_error", "neg_mean_squared_error"), \
                                  return_train_score = False)

# Here, the dataset was split into three subsections, and each was trained and
# tested using the machine learning model created above. The evaluation metrics
# of MAE, MSE, and R^2 are not quite as indicative of an accurate model here,
# BUT that is to be expected, since the dataset was split into comparatively small pieces.
# With a larger dataset, these evaluation metrics should improve.
 
# With more data and model tweaking, our model should hopefully improve to optimized 
# form, but this is a decent start.

# ------------------------

# REFERENCES (which helped guide us in developing the code in this script):
    
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
