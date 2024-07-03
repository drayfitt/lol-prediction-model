# Importing libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Load data from CSV file
data = pd.read_csv('Data/training_data.csv')

data = data.drop(columns=['gameid', 'date', 'team1_teamname', 'team2_teamname'])

# Split into features (X) and labels (y)
X = data.drop('result', axis=1)
X = X.select_dtypes(include=[float, int])  # Assuming that the 'label' column contains labels
y = data['result']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Define models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Support Vector Machine': SVC(),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5)
}

# Create pipelines with imputation
pipelines = {name: Pipeline(steps=[('imputer', SimpleImputer(strategy='mean')), ('model', model)]) for name, model in
             models.items()}


# Function to train and evaluate models
def evaluate_models(pipelines, X_train, y_train, X_test, y_test):
    results = {}
    for model_name, pipeline in pipelines.items():
        # Train model
        pipeline.fit(X_train, y_train)
        # Predict
        y_pred = pipeline.predict(X_test)
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        results[model_name] = {'accuracy': accuracy, 'f1_score': f1}
    return results


# Evaluate models
results = evaluate_models(pipelines, X_train, y_train, X_test, y_test)

# Display results
for model_name, metrics in results.items():
    print(f"Model: {model_name}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")
    print("-" * 30)

# Select the best model
best_model_name = max(results, key=lambda x: results[x]['f1_score'])
print(f"The best model is: {best_model_name} with F1 Score: {results[best_model_name]['f1_score']:.4f}")
