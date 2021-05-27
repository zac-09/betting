# Betting API 
This api implements the CRUD  endpoints to start the api run the following
1. From your root diremctory run `python install -m -r requirements.txt` to install all dependacies
2. To run the api locally on your machine 
on linux and macos run `export FLASK_APP=app.py`
on windows run `set FLASK_APP=app`
on windows powershell run `$env:FLASK_APP="app.py"`

## -/create

Create odds. 
Accepts json with the following fields: 
league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date and saves this into a database
Returns: 
- 200 if it succeeds
- 500 for server error
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request

## -/read

Read game odds. 
Accepts json with the following fields: 
league, date_range
Returns: 
- 200 if it succeeds. For a 200 response, return a json array with odds for that whole league for the specified date range
- 500 for server error.
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request

## -/update 

## Update game odds.
Accepts json with the following fields: 
league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date and saves this into a database
Returns:
- 200 if it succeeds
- 500 for server error
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request

## -/delete

Delete game odds.
Accepts json with the following fields: 
league, home_team, away_team and game_date and deletes this from the database
Returns: 
- 200 if it succeeds
- 500 for server error
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request
