import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb


def build_model(real_data, prediction_results_path):
    # Function to create and train a pipeline
    def create_and_train_pipeline(imputer_strategy, model, X_train, y_train):
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy=imputer_strategy)),
            ('classifier', model)
        ])
        pipeline.fit(X_train, y_train)
        return pipeline

    # Function to evaluate a model
    def evaluate_model(pipeline, X_test, y_test):
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy

    # Function to compare predictions with real data
    def compare_predictions(predictions, real_data):
        comparison_results = {}
        for model_name, prediction in predictions.items():
            match_percentage = np.mean(prediction == real_data) * 100
            comparison_results[model_name] = match_percentage
        return comparison_results

    # Load and preprocess data
    data = pd.read_csv('Data/training_data.csv')

    data = data.drop(columns=['gameid', 'date', 'team1_teamname', 'team2_teamname', 'team1_id', 'team2_id'])

    # Data
    X = data.drop('result', axis=1).select_dtypes(include=[float, int])
    y = data['result']

    # Correlations
    correlation_matrix = X.corr()

    # Set the correlation threshold
    threshold = 0.85

    # Find pairs of highly correlated features
    highly_correlated_pairs = []

    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > threshold:
                colname_i = correlation_matrix.columns[i]
                colname_j = correlation_matrix.columns[j]
                highly_correlated_pairs.append((colname_i, colname_j))

    features_to_drop = set()

    for pair in highly_correlated_pairs:
        features_to_drop.add(pair[0])  # You can change the logic to decide which feature to drop

    # Drop the features from the Xset
    X = X.drop(columns=features_to_drop)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Create and train pipelines
    pipelines = {
        'Logistic Regression': create_and_train_pipeline('mean', LogisticRegression(max_iter=1000), X_train, y_train),
        'Random Forest': create_and_train_pipeline('mean', RandomForestClassifier(), X_train, y_train),
        'SVC': create_and_train_pipeline('mean', SVC(), X_train, y_train),
        'K-Nearest Neighbors': create_and_train_pipeline('mean', KNeighborsClassifier(), X_train, y_train),
        'DecisionTreeClassifier': create_and_train_pipeline('mean', DecisionTreeClassifier(), X_train, y_train),
        'GradientBoostingClassifier': create_and_train_pipeline('mean', GradientBoostingClassifier(), X_train, y_train),
        'GaussianNB': create_and_train_pipeline('mean', GaussianNB(), X_train, y_train),
        'MLPClassifier': create_and_train_pipeline('mean', MLPClassifier(hidden_layer_sizes=(100,)), X_train, y_train),
        'XGBClassifier': create_and_train_pipeline('mean',
                                                   xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
                                                   X_train, y_train)

    }

    # Evaluate pipelines
    for model_name, pipeline in pipelines.items():
        accuracy = evaluate_model(pipeline, X_test, y_test)
        print(f"Accuracy: {accuracy:.2f} - {model_name} ")

    print("\n")

    # Predict results for new data
    new_data = pd.read_csv('Predictions/ready.csv')
    new_data = new_data.drop(columns=features_to_drop)

    predictions = {model_name: pipeline.predict(new_data) for model_name, pipeline in pipelines.items()}

    # Real data for comparison

    comparison_results = compare_predictions(predictions, real_data)

    prediction_results = []
    # Print predictions
    for model_name, prediction in predictions.items():
        match_percentage = comparison_results[model_name]
        prediction_results.append(
            {'Model': model_name, 'Predictions': prediction.astype('int64'), 'Match Percentage': match_percentage})
        print(f"Predictions: {prediction.astype('int64')} Match Percentage: {match_percentage:.0f}% {model_name}")
    print("Real data:  ", real_data)

    prediction_results.append(
        {'Model': 'Real data', 'Predictions': real_data, 'Match Percentage': ''})

    prediction_df = pd.DataFrame(prediction_results)
    prediction_df.to_csv(prediction_results_path, index=False)
