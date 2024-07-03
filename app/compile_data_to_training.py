import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler


def compile_data_to_training():
    mean_team_stats = pd.read_csv('Data/mean_team_stats.csv')
    mean_player_stats = pd.read_csv('Data/mean_player_stats.csv')

    teams_dtype = {
        'team_id': 'int64',
        'teamname': 'object'
    }

    teams = pd.read_csv('Data/teams.csv', dtype=teams_dtype)

    dtype = {
        'team1_id': 'int64',
        'team1_teamname': 'object',
        'team2_id': 'int64',
        'team2_teamname': 'object'
    }

    matches_df = pd.read_csv('Data/merged_matches_with_team_ids.csv', dtype=dtype)
    mean_player_stats = mean_player_stats.drop(columns='date')

    # Pivot player stats to have one row per game and team, with columns prefixed by the position
    player_stats_pivot = mean_player_stats.pivot_table(
        index=['gameid', 'teamname'],
        columns='position',
        values=[col for col in mean_player_stats.columns if col not in ['gameid', 'teamname']],
        aggfunc='first'
    )

    # Flatten the columns and add the prefix
    player_stats_pivot.columns = [f'{pos}_{stat}' for stat, pos in player_stats_pivot.columns]
    player_stats_pivot.reset_index(inplace=True)

    # Merge the pivoted player stats with the team stats
    merged_stats = pd.merge(mean_team_stats, player_stats_pivot, on=['gameid', 'teamname'], how='left')

    # Add team_id from teams.csv
    merged_df = merged_stats.merge(teams, how='left', left_on='teamname', right_on='teamname')

    numeric_df = merged_df.select_dtypes(include=['number']).columns
    numeric_df = numeric_df.difference(['team_id', 'game_format', 'game', 'result_cumsum'])

    negative_value_columns = merged_df[numeric_df].columns[(merged_df[numeric_df] < 0).any()].tolist()
    positive_value_columns = merged_df[numeric_df].columns[(merged_df[numeric_df] >= 0).all()].tolist()

    # Create an instance of MinMaxScaler
    scaler = MinMaxScaler()
    scaler1 = MinMaxScaler(feature_range=(-1, 1))

    # Fit and transform the numerical columns using the MinMaxScaler
    merged_df[positive_value_columns] = scaler.fit_transform(merged_df[positive_value_columns])
    merged_df[negative_value_columns] = scaler1.fit_transform(merged_df[negative_value_columns])

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv('Data/merged_team_player_stats.csv', index=False)

    print("compile_data_to_training.py COMPLETED - Data/merged_team_player_stats.csv")

    # ***********************************************************************************

    # Load the CSV files
    stats_df = merged_df

    stats_df.drop(columns=['patch', 'participantid'], inplace=True)

    # Merge team data into matches data
    stats_df_team1 = stats_df.add_suffix('_team1')
    merged_df = matches_df.merge(stats_df_team1, how='left', left_on=['gameid', 'team1_id'],
                                 right_on=['gameid_team1', 'team_id_team1'])

    stats_df_team2 = stats_df.add_suffix('_team2')
    merged_df = merged_df.merge(stats_df_team2, how='left', left_on=['gameid', 'team2_id'],
                                right_on=['gameid_team2', 'team_id_team2'])

    # Drop redundant team_name columns from the merged dataframe
    merged_df.drop(
        columns=['date_team1', 'date_team2', 'gameid_team1', 'gameid_team2', 'teamname_team1', 'teamname_team2',
                 'team_id_team1', 'team_id_team2'], inplace=True)

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv('Data/training_data.csv', index=False)

    print("prepare_data_training.py COMPLETED - Data/training_data.csv")
