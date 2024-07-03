import pandas as pd


def oe_to_data():
    team_file_path = 'Data/team_stats.csv'
    team_df = pd.read_csv(team_file_path)

    player_file_path = 'Data/player_stats.csv'
    player_df = pd.read_csv(player_file_path)

    # Convert 'date' column to date type
    team_df['date'] = pd.to_datetime(team_df['date']).dt.date
    player_df['date'] = pd.to_datetime(player_df['date']).dt.date

    # Sort DataFrame by 'teamname' and 'date'
    team_df = team_df.sort_values(by=['teamname', 'date'])
    player_df = player_df.sort_values(by=['playername', 'date'])

    # List of columns to exclude from average calculations
    exclude_columns = ['playoffs', 'game', 'patch', 'participantid', 'result']

    # Function to calculate average values up to a given day and sum the 'result' column
    def calculate_rolling_stats(dataframe, exclude_cols, group_by):
        numeric_columns = dataframe.select_dtypes(include=['float64', 'int64']).columns
        mean_columns = numeric_columns.difference(exclude_cols)

        # Calculate average values for selected columns from the last 5 rows
        dataframe[mean_columns] = dataframe.groupby(group_by)[mean_columns].transform(
            lambda x: x.rolling(window=8, min_periods=1).mean())

        # Sum the 'result' column
        dataframe['result_cumsum'] = dataframe.groupby(group_by)['result'].cumsum()

        return dataframe

    # Function to recognize game type: BO1, BO3, BO5
    def determine_game_format(group):
        game_count = len(group)
        win_count = group['result'].sum()

        if game_count == 1:
            return 1
        elif game_count == 2:
            return 3
        elif game_count == 3 and (win_count == 1 or win_count == 2):
            return 3
        elif game_count == 3 and (win_count == 0 or win_count == 3):
            return 5
        elif game_count >= 4:
            return 5
        return 0

    # Apply the function to calculate averages and sum
    team_df = calculate_rolling_stats(team_df, exclude_columns, 'teamname')
    player_df = calculate_rolling_stats(player_df, exclude_columns, 'playername')

    # Initialize the new column with default values
    team_df['game_format'] = 0

    # Apply the function to each group and broadcast the result to all rows in the group
    for (date, teamname), group in team_df.groupby(['date', 'teamname']):
        game_format = determine_game_format(group)
        team_df.loc[group.index, 'game_format'] = game_format

    team_df = team_df.drop(columns=['result'])
    player_df = player_df.drop(columns=['result', 'result_cumsum'])

    team_df.to_csv('Data/mean_team_stats.csv', index=False)
    player_df.to_csv('Data/mean_player_stats.csv', index=False)

    print("oe_to_data.py COMPLETED - Data/mean_team_stats.csv, Data/mean_player_stats.csv")
