# -*- coding: utf-8 -*-
"""Smart Predictive Modeling for Rental Property Prices.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hwiASYi67efA9uC8em7esX18FUbd9BrN

# **IMPORTING** **ESSENTIAL** **LIBRARIES**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

"""# **LOADING** **THE DATASET**"""

data=pd.read_excel("/content/House_Rent_Train.xlsx")
data

"""# EXPLORATORY DATA ANALYSIS"""

data.info()

data.describe()

data.head(15)

data.columns

data.corr()

sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.show()

sns.pairplot(data)

data.isnull().sum()

data.duplicated().sum()

data.nunique()

"""# DATA CLEANING AND TRANSFORMATION

**Handling missing values**
"""

data['locality'].fillna(data['locality'].mode()[0], inplace=True)  #Replaced the null values with mode.

data.dropna(inplace=True)  #Dropped the null values as it is less.

data.isnull().sum()

data.drop_duplicates(inplace=True)

data.shape

data.dtypes

"""**Trasnsforming the data types for its original form.**"""

data['activation_date'] = pd.to_datetime(data['activation_date'])

data['balconies'] = data['balconies'].astype('int64')

data['rent'] = data['rent'].astype('int64')

data['total_floor'] = data['total_floor'].astype('int64')

data['bathroom'] = data['bathroom'].astype('int64')

data['cup_board'] = data['cup_board'].astype('int64')

data['floor'] = data['floor'].astype('int64')

data['parking']=data['parking'].str.lower()

data['parking'].value_counts()

data['water_supply']=data['water_supply'].str.lower()

data['water_supply'].value_counts()

data['furnishing']=data['furnishing'].str.lower()

data['furnishing'].value_counts()

data['locality']=data['locality'].str.lower()

data['locality'].value_counts()

data['property_age']=data['property_age'].astype('int64')

data['property_age'].value_counts()

data['building_type']=data['building_type'].str.lower()

data['building_type'].value_counts()

data['total_floor'].unique()

data['floor'].unique()

data['locality'].unique()

data['type']=data['type'].str.lower()

data['type'].value_counts()

data['property_size'].nunique()

data['property_size'].value_counts()

data['facing']=data['facing'].str.lower()

data['facing'].value_counts()

data['facing'].unique()

data['lease_type']=data['lease_type'].str.lower()

data['lease_type'].value_counts()

data['lease_type'].unique()

data['negotiable'].value_counts()

"""**Outlier Detection**"""

numerical_columns = ['property_size', 'rent', 'bathroom', 'property_age', 'floor']
plt.figure(figsize=(15, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(x=data[column])
    plt.title(f'Boxplot of {column}')

plt.tight_layout()
plt.show()

from scipy.stats import zscore
numerical_columns = ['property_size', 'rent', 'bathroom', 'property_age', 'floor']
z_scores = data[numerical_columns].apply(zscore)
threshold = 3
df_no_outliers = data[(z_scores.abs() < threshold).all(axis=1)]
print("Shape before removing outliers:", data.shape)
print("Shape after removing outliers:", df_no_outliers.shape)

"""In this data set there are outliers but property like companies are also included in the data.So we cant conclude the variation as outliers."""

data['bathroom'].value_counts()

data['bathroom'].unique()

data['balconies'].unique()

data['balconies'].value_counts()

"""**Univariate Analysis**"""

plt.figure(figsize=(10, 6))
sns.histplot(data['rent'], bins=30, kde=True)
plt.title('Distribution of Rent Prices')
plt.xlabel('Rent Prices')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='lease_type', y='rent', data=data, palette="Set3")
plt.title('Rent Prices by Lease Type')
plt.show()

sns.barplot(x='bathroom',y='rent',data=data)

sns.barplot(x='balconies',y='rent',data=data)

sns.barplot(x='floor',y='rent',data=data)

sns.barplot(x='water_supply',y='rent',data=data)

sns.barplot(x='furnishing',y='rent',data=data)

sns.barplot(x='property_age',y='rent',data=data)

sns.barplot(x='total_floor',y='rent',data=data)

sns.barplot(x='building_type',y='rent',data=data)

sns.barplot(x='type',y='rent',data=data)

sns.barplot(x='facing',y='rent',data=data)

sns.barplot(x='parking',y='rent',data=data)

sns.barplot(x='cup_board',y='rent',data=data)

import geopandas as gpd
from shapely.geometry import Point
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(figsize=(10, 8))
world.plot(ax=ax, color='lightgray')
gdf.plot(ax=ax, color='red', markersize=10, alpha=0.6)
plt.title('Geospatial Distribution of Rental Properties')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

"""**Data Pre Processing**"""

data['amenities']=data['amenities'].str.lower()

data['amenities'].value_counts()

"""# Data Pre Processing"""

le = LabelEncoder()
data['type'] = le.fit_transform(data['type'])
data['locality'] = le.fit_transform(data['locality'])
data['lease_type'] = le.fit_transform(data['lease_type'])
data['furnishing'] = le.fit_transform(data['furnishing'])
data['building_type'] = le.fit_transform(data['building_type'])
data['water_supply'] = le.fit_transform(data['water_supply'])
data['facing'] = le.fit_transform(data['facing'])
data['amenities'] = le.fit_transform(data['amenities'])
data['parking'] = le.fit_transform(data['parking'])

scaler = StandardScaler()
data[['latitude', 'longitude', 'property_size', 'property_age']] = scaler.fit_transform(data[['latitude', 'longitude', 'property_size', 'property_age']])

data

data.dtypes

data.drop('id',axis=1,inplace=True) # It has unique values  so we can drop it.

data.drop('activation_date',axis=1,inplace=True) #We have property_age so we can drop it.

"""# MODEL BUILDING AND TRAINING"""

x = data.drop('rent',axis=1)
y = data['rent']

x

y

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Initializing and training the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Feature Importance
feature_importance = pd.Series(model.coef_, index=X.columns).sort_values(ascending=False)
print('Feature Importance:')
print(feature_importance)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

y_pred

#ENSEMBLE MODEL

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize individual regressors
linear_regressor = LinearRegression()
random_forest_regressor = RandomForestRegressor(random_state=0)
gradient_boosting_regressor = GradientBoostingRegressor(random_state=0)

# Create the ensemble model (VotingRegressor)
ensemble_model = VotingRegressor(
    estimators=[
        ('linear', linear_regressor),
        ('random_forest', random_forest_regressor),
        ('gradient_boosting', gradient_boosting_regressor)
    ]
)

# Train the ensemble model
ensemble_model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_ensemble = ensemble_model.predict(X_test_scaled)

# Evaluate the ensemble model
mse_ensemble = mean_squared_error(y_test, y_pred_ensemble)
print(f'Mean Squared Error (Ensemble): {mse_ensemble}')

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the training set
y_pred_train = model.predict(X_train)

# Make predictions on the testing set
y_pred_test = model.predict(X_test)

# Evaluate the model on training data
mse_train = mean_squared_error(y_train, y_pred_train)
print(f'Mean Squared Error (Training): {mse_train}')

# Evaluate the model on testing data
mse_test = mean_squared_error(y_test, y_pred_test)
print(f'Mean Squared Error (Testing): {mse_test}')

"""# TESTING DATA"""

df=pd.read_excel('/content/House_Rent_Test.xlsx')
df

"""# PREPROCESSING THE TEST DATA

"""

le = LabelEncoder()
df['type'] = le.fit_transform(df['type'])
df['locality'] = le.fit_transform(df['locality'])
df['lease_type'] = le.fit_transform(df['lease_type'])
df['furnishing'] = le.fit_transform(df['furnishing'])
df['building_type'] = le.fit_transform(df['building_type'])
df['water_supply'] = le.fit_transform(df['water_supply'])
df['facing'] = le.fit_transform(df['facing'])
df['amenities'] = le.fit_transform(df['amenities'])
df['parking'] = le.fit_transform(df['parking'])

scaler = StandardScaler()
df[['latitude', 'longitude', 'property_size', 'property_age']] = scaler.fit_transform(df[['latitude', 'longitude', 'property_size', 'property_age']])

df.drop(['id','activation_date'],axis=1,inplace=True)

df

test_data=df

predictions = model.predict(test_data)

predictions_df = pd.DataFrame({'Rent Prediction': predictions})

predictions_df

predictions_data=predictions_df.astype(int)

predictions_data

predictions_data.to_csv('predictions.csv', index=False)

"""**SUMMARY**



**Objective**: Developed a predictive model for rental property prices.
**Dataset:** Loaded from 'House_Rent_Train.xlsx'.

**Exploratory Data Analysis (EDA):**

**Utilized libraries:**

*  Pandas
*  Seaborn
*  Matplotlib
*  NumPy
*  Sklearn

**Insights:**
* Dataset overview
*info
*summary statistics.
*descriptive statistics
*Initial correlation analysis through heatmap.
*Correlation heatmap.

**Visualizations:**
* Pair plots
* box plots  
* geospatial distribution.
* Histograms and bar plots.

**Data Cleaning and Transformation:**

* Handled missing values:
*'Locality': Filled with mode.
*Other columns: Null values dropped.
*Data type transformation for consistency.
*Outlier detection:
*Retained outliers due to unique nature of data.

**Univariate Analysis:**

* Histograms and bar plots for rent prices and categorical variables.
* Geospatial distribution using latitude and longitude.

**Data Preprocessing:**

* Text normalization: Lowercasing for uniformity.
* Label encoding for categorical variables.
* Standard scaling for numerical features.

**Model Building and Training (Linear Regression):**

* Splited dataset into training and testing sets.
* Trained a Linear Regression model.
* Evaluated model performance using Mean Squared Error (MSE).
* Feature importance analysis.

**Ensemble Model (VotingRegressor):**

Combined Linear Regression, Random Forest, and Gradient Boosting.
Trained and evaluated ensemble model performance using MSE.

**Testing Data and Predictions:**

Loaded and preprocessed 'House_Rent_Test.xlsx'.
Used the trained linear regression model to predict rent prices.

**Saved predictions to 'predictions.csv'**.




"""

