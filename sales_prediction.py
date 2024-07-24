
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

"""Data Collection & Analysis"""

# loading the dataset from csv file to a Pandas DataFrame
big_mart_data = pd.read_csv('train.csv')

# first 5 rows of the dataframe
big_mart_data.head()

big_mart_data.shape

big_mart_data.info()

"""Categorical Features:

* Item Identifier

* Item_Fat_Content

* Item_Type

* Outlet Identifier

* Outlet_Size

* Outlet_Location_Type

* Outlet Type
"""

big_mart_data.isnull().sum()

"""Handling Missing Values :

Mean -> average value

Mode -> Most repeated value
"""

# mean value of "Item_Weight" column
big_mart_data['Item_Weight'].mean()

# filling the missing values in "Item_Weight" column with "Mean" value
big_mart_data['Item_Weight'].fillna(big_mart_data['Item_Weight'].mean(), inplace = True)

big_mart_data.isnull().sum()

"""Replacing the missing values in "Outlet_Size" with mode

"""

big_mart_data["Outlet_Size"] = big_mart_data["Outlet_Size"].fillna(big_mart_data["Outlet_Size"].mode()[0])

# checking for missing values
big_mart_data.isnull().sum()

"""Data Analyis"""

# statistical measures about the data
big_mart_data.describe()

"""Numerical Features"""

sns.set()

# Item Weight distribution
plt.figure(figsize=(6,6))
sns.distplot (big_mart_data['Item_Weight'])
plt.show()

# Item Visibility distribution
plt.figure(figsize=(6,6))
sns.distplot (big_mart_data['Item_Visibility'])
plt.show()

# Item MRP distribution
plt.figure(figsize=(6,6))
sns.distplot (big_mart_data['Item_MRP'])
plt.show()

# Item Outlet Sales distribution
plt.figure(figsize=(6,6))
sns.distplot (big_mart_data['Item_Outlet_Sales'])
plt.show()

# Outlet Establishment Year column
plt.figure(figsize=(6,6))
sns.countplot(x= 'Outlet_Establishment_Year', data=big_mart_data)
plt.show()

"""Categorical Features"""

# Item_Fat_Content column
plt.figure(figsize=(6,6))
sns.countplot(x= 'Item_Fat_Content', data=big_mart_data)
plt.show()

# Item_Type column
plt.figure(figsize=(25,6))
sns.countplot(x= 'Item_Type', data=big_mart_data)
plt.title('Item_Type count')
plt.show()

"""Data Preprocessing"""

big_mart_data.head()

# Drop the Item_Identifier column from dataset
big_mart_data.drop('Item_Identifier', axis=1, inplace=True)

# Drop the Outlet_Identifier column from dataset
big_mart_data.drop('Outlet_Identifier', axis=1, inplace=True)

big_mart_data[ 'Item_Fat_Content' ]. value_counts()

big_mart_data.replace({'Item_Fat_Content': {'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'}}, inplace=True)

big_mart_data['Item_Fat_Content'].value_counts()

"""Label Encoding (to convert categorical values into numerical values)"""

encoder = LabelEncoder()

big_mart_data['Item_Fat_Content'] = encoder.fit_transform(big_mart_data['Item_Fat_Content'])
fat_content_classes = list(encoder.classes_)  # Save the classes for later use

big_mart_data['Outlet_Size'] = encoder.fit_transform(big_mart_data['Outlet_Size'])
outlet_size_classes = list(encoder.classes_)  # Save the classes for later use

big_mart_data['Outlet_Location_Type'] = encoder.fit_transform(big_mart_data['Outlet_Location_Type'])
location_type_classes = list(encoder.classes_)  # Save the classes for later use

big_mart_data['Outlet_Type'] = encoder.fit_transform(big_mart_data['Outlet_Type'])
outlet_type_classes = list(encoder.classes_)  # Save the classes for later use

big_mart_data.head()

"""Splitting features and Target"""

X = big_mart_data.drop(columns='Item_Outlet_Sales', axis=1)
Y = big_mart_data['Item_Outlet_Sales']

print(X)

print(Y)

X = pd.get_dummies(X, columns=['Item_Type'])

"""Splitting the data into Training data & Testing Data"""

X_train, X_test, Y_train, Y_test = train_test_split (X, Y, test_size=0.2, random_state=2)

print(X. shape, X_train. shape, X_test.shape)

"""Machine Learning Model Training

XGBoost Regressor
"""

regressor = XGBRegressor()

regressor.fit(X_train, Y_train)
# regressor.fit(X_test, Y_test)

"""Evaluation"""

# prediction on training data
training_data_prediction = regressor.predict(X_train)
# training_data_prediction = regressor.predict(X_test)

# R squared Value
r2_train = metrics.r2_score (Y_train, training_data_prediction)
# r2_test = metrics.r2_score (Y_test, training_data_prediction)

print('R Squared value = ', r2_train)

big_mart_data.dtypes
big_mart_data["Item_Type"]

# prediction on test data
test_data_prediction = regressor.predict(X_test)

r2_test = metrics.r2_score (Y_test, test_data_prediction)

print('R Squared value = ', r2_test)

def predict_sales(input_data):
    # Creating a DataFrame for the input data
    input_df = pd.DataFrame([input_data])

    # Encoding categorical features using previously saved classes
    def encode_feature(feature, classes):
        encoder = LabelEncoder()
        encoder.classes_ = np.array(classes)
        return encoder.transform(feature)

    input_df['Item_Fat_Content'] = encode_feature(input_df['Item_Fat_Content'], fat_content_classes)
    input_df['Outlet_Size'] = encode_feature(input_df['Outlet_Size'], outlet_size_classes)
    input_df['Outlet_Location_Type'] = encode_feature(input_df['Outlet_Location_Type'], location_type_classes)
    input_df['Outlet_Type'] = encode_feature(input_df['Outlet_Type'], outlet_type_classes)

    # One-hot encoding for 'Item_Type'
    input_df = pd.get_dummies(input_df, columns=['Item_Type'])

    # Ensure the input_df has the same columns as the training set
    for col in X.columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[X.columns]

    # Making the prediction
    prediction = regressor.predict(input_df)
    return prediction[0]

# Example input for prediction
example_input = {
    'Item_Weight': 9.3,
    'Item_Fat_Content': 'Low Fat',
    'Item_Visibility': 0.016047,
    'Item_Type': 'Dairy',
    'Item_MRP': 249.8092,
    'Outlet_Establishment_Year': 1999,
    'Outlet_Size': 'Medium',
    'Outlet_Location_Type': 'Tier 1',
    'Outlet_Type': 'Supermarket Type1'
}

# Predicting sales for the example input
predicted_sales = predict_sales(example_input)
print('Predicted Sales:', predicted_sales)
