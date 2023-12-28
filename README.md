# GUVI--Smart-Predictive
Developed a Smart Predictive Model
Objective: Developed a predictive model for rental property prices. Dataset: Loaded from 'House_Rent_Train.xlsx'.

Exploratory Data Analysis (EDA):

Utilized libraries:

Pandas
Seaborn
Matplotlib
NumPy
Sklearn
Insights:

Dataset overview
info
summary statistics.
descriptive statistics
Initial correlation analysis through heatmap.
Correlation heatmap.
Visualizations:

Pair plots
box plots
geospatial distribution.
Histograms and bar plots.
Data Cleaning and Transformation:

Handled missing values:
'Locality': Filled with mode.
Other columns: Null values dropped.
Data type transformation for consistency.
Outlier detection:
Retained outliers due to unique nature of data.
Univariate Analysis:

Histograms and bar plots for rent prices and categorical variables.
Geospatial distribution using latitude and longitude.
Data Preprocessing:

Text normalization: Lowercasing for uniformity.
Label encoding for categorical variables.
Standard scaling for numerical features.
Model Building and Training (Linear Regression):

Splited dataset into training and testing sets.
Trained a Linear Regression model.
Evaluated model performance using Mean Squared Error (MSE).
Feature importance analysis.
Ensemble Model (VotingRegressor):

Combined Linear Regression, Random Forest, and Gradient Boosting. Trained and evaluated ensemble model performance using MSE.

Testing Data and Predictions:

Loaded and preprocessed 'House_Rent_Test.xlsx'. Used the trained linear regression model to predict rent prices.

Saved predictions to 'predictions.csv'.
