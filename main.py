import numpy as np
import app.prepare_data  # output: DataSources/lol_lec.csv, Data/teams.csv
import app.oe_matches  # output: Data/matches.csv
import app.oe_to_data_transformed  # output: player_stats.csv i team_stats.csv
import app.add_teamid_to_matches  # output: Data/merged_matches_with_team_ids.csv
import app.oe_to_data  # otuput: Data/mean_team_stats.csv Data/mean_player_stats.csv
import app.compile_data_to_training  # output: Data/training_data.csv
import app.prepare_data_to_forecast  # output: Predictions/ready.csv
import refactored_build_model

# Variable defining whether only matches from the LEC league should be used for training
lec_only = True

# Date up to which historical matches should be considered (used for post ante verification)
date_to = '2024-06-29'

# Path to the file with matches for prediction (note: team names must match the names from the source file (based on Oracle Elixir)
predictions_path = 'Predictions/predict_2024-06-29.csv'

# Used to compare prediction results with actual results (where 1 means team_1 won)
real_data = np.array([1, 1, 1, 1, 0, 1, 0, 1, 0, 0])

# Path to the saved prediction results
prediction_results_path = 'Predictions/prediction_results_2024-06-29.csv'

app.prepare_data.prepare_data(date_to, lec_only)
app.oe_matches.oe_matches()
app.oe_to_data_transformed.oe_to_data_transformed()
app.add_teamid_to_matches.add_teamid_to_matches()
app.oe_to_data.oe_to_data()
app.compile_data_to_training.compile_data_to_training()
app.prepare_data_to_forecast.prepare_data_to_forecast(predictions_path)
refactored_build_model.build_model(real_data, prediction_results_path)
