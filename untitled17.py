# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rbQxGiJMiREJWcORZzm6lflkFzl_kDZv
"""

import pandas as pd

df = pd.read_csv(r'/content/car.csv')

df.info()

df.shape[0] # samples

df.shape[1] #features

df.isnull().sum()

import pandas as pd
import statsmodels.api as sm

df = pd.read_csv(r'/content/car.csv')

# Check for unique values in each column to identify potential mapping issues
for col in df.columns:
    print(f"Unique values in {col}: {df[col].unique()}")

# Improved mapping with error handling to avoid NaN values
mapping_dict = {
    'buying': {'vhigh': 0, 'high': 1, 'med': 2, 'low': 3},
    'doors': {'2': 0, '3': 1, '4': 2, '5more': 3},
    'lug_boot': {'small': 0, 'med': 1, 'big': 2},
    'class': {'unacc': 0, 'acc': 1, 'good': 2, 'vgood': 3}, # corrected 'class' mapping
    'maint': {'vhigh': 0, 'high': 1, 'med': 2, 'low': 3},
    'persons': {'2': 0, '4': 1, 'more': 2},
    'safety': {'low': 0, 'med': 1, 'high': 2}
}


for col, mapping in mapping_dict.items():
    df[col] = df[col].map(mapping).fillna(-1) # Replace NaN with -1 or another placeholder


X = df.drop('class', axis=1)
Y = df['class']
x_const = sm.add_constant(X)

df.head()

df.isnull().sum()

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()

model.fit(x_const,Y)

y_predicted =model.predict(x_const)

y_predicted

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

X_train.value_counts()

# Explanation of the 'class' column values after mapping:

# The 'class' column represents the evaluation of the car.
# The original values were strings: 'unacc', 'acc', 'good', 'vgood'.
# These have been mapped to numerical values for the model:

# 0: 'unacc' (unacceptable)
# 1: 'acc' (acceptable)
# 2: 'good'
# 3: 'vgood' (very good)

# This numerical representation allows the logistic regression model to work with the data.

import matplotlib.pyplot as plt
import seaborn as sns

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Create the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

import matplotlib.pyplot as plt
# Visualize the relationship between each feature and the target variable ('class')
for col in X.columns:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='class', y=col, data=df)
    plt.title(f'Boxplot of {col} vs. Class')
    plt.xlabel('Class')
    plt.ylabel(col)
    plt.show()

# prompt: Model Training:
# ○ Train and evaluate a classification model (Logistic Regression, Random Forest,
# etc.).
# ○ Use train-test split and show accuracy, precision, recall.

from sklearn.metrics import accuracy_score, precision_score, recall_score

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted') # Use weighted average for multi-class
recall = recall_score(y_test, y_pred, average='weighted') # Use weighted average for multi-class

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")

# prompt: 6. Feature Importance (optional):
# ○ Identify and rank the most important features affecting heart disease

import pandas as pd
# Feature Importance using feature_importances_ from DecisionTreeClassifier

# Get the feature importances from the trained model
feature_importances = model.feature_importances_

# Create a DataFrame to store feature names and their corresponding importances
feature_importance = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})

# Sort the DataFrame by the importance values to rank features
feature_importance = feature_importance.sort_values('Importance', ascending=False)


print("\nFeature Importance based on DecisionTreeClassifier:")
feature_importance


#Alternatively, if you were using Logistic Regression you could use coef_
# from sklearn.linear_model import LogisticRegression
# lr_model = LogisticRegression()
# lr_model.fit(X_train, y_train)
# coefficients = lr_model.coef_[0]  # Access the first row (only one set of coefficients)
# feature_importance_lr = pd.DataFrame({'Feature': X.columns, 'Coefficient': coefficients})
# feature_importance_lr = feature_importance_lr.reindex(feature_importance_lr['Coefficient'].abs().sort_values(ascending=False).index)
# print(feature_importance_lr)

# prompt: Model Comparison:
# ○ Compare multiple models: Logistic Regression, KNN, Random Forest, Decision
# Tree

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# Initialize models
knn_model = KNeighborsClassifier()
rf_model = RandomForestClassifier(random_state=42)  # Added random_state for reproducibility
dt_model = DecisionTreeClassifier(random_state=42)  # Added random_state for reproducibility

# Train and evaluate each model
models = {
    "KNN": knn_model,
    "Random Forest": rf_model,
    "Decision Tree": dt_model,
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"--- {name} ---")
    print(classification_report(y_test, y_pred))
    print("---")

# prompt: . Model deployment:
# ● Find best model in terms of F1 score and deploy it to streamlit

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load your data (replace with your actual data loading)
df = pd.read_csv(r'/content/car.csv')

# Mapping (as provided in your code)
mapping_dict = {
    'buying': {'vhigh': 0, 'high': 1, 'med': 2, 'low': 3},
    'doors': {'2': 0, '3': 1, '4': 2, '5more': 3},
    'lug_boot': {'small': 0, 'med': 1, 'big': 2},
    'class': {'unacc': 0, 'acc': 1, 'good': 2, 'vgood': 3},
    'maint': {'vhigh': 0, 'high': 1, 'med': 2, 'low': 3},
    'persons': {'2': 0, '4': 1, 'more': 2},
    'safety': {'low': 0, 'med': 1, 'high': 2}
}

for col, mapping in mapping_dict.items():
    df[col] = df[col].map(mapping).fillna(-1)

X = df.drop('class', axis=1)
y = df['class']  # Use 'y' instead of 'Y' for consistency
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the best model (RandomForestClassifier in this example)
best_model = RandomForestClassifier(random_state=42)
best_model.fit(X_train, y_train)

# Streamlit app
st.title("Car Evaluation Model")

# Input features (replace with actual input fields)
buying = st.selectbox("Buying Price", list(mapping_dict['buying'].keys()))
maint = st.selectbox("Maintenance Price", list(mapping_dict['maint'].keys()))
doors = st.selectbox("Number of Doors", list(mapping_dict['doors'].keys()))
persons = st.selectbox("Number of Persons", list(mapping_dict['persons'].keys()))
lug_boot = st.selectbox("Luggage Boot Size", list(mapping_dict['lug_boot'].keys()))
safety = st.selectbox("Safety", list(mapping_dict['safety'].keys()))


# Create input dataframe
input_data = pd.DataFrame({
    'buying': [mapping_dict['buying'][buying]],
    'maint': [mapping_dict['maint'][maint]],
    'doors': [mapping_dict['doors'][doors]],
    'persons': [mapping_dict['persons'][persons]],
    'lug_boot': [mapping_dict['lug_boot'][lug_boot]],
    'safety': [mapping_dict['safety'][safety]]
})

# Make prediction
if st.button("Predict"):
    prediction = best_model.predict(input_data)[0]
    st.write(f"Predicted Car Class: {list(mapping_dict['class'].keys())[int(prediction)]}")

    # Display classification report (optional)
    y_pred = best_model.predict(X_test)
    st.text(classification_report(y_test, y_pred))
