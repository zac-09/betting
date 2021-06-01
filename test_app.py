import os
import json
import tempfile

import pytest

import app

headers = {'Content-Type': 'application/json', 'api-key': '1254'}
test_data = {
    "league":  "FA",
    "home_team": "Arsenal",
    "away_team": "Man City",
    "home_team_win_odds": 3.0,
    "away_team_win_odds": 4,
    "draw_odds": 2,
    "game_date": "18-05-2021"
}


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    # app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.app.config['DATABASE']
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    with app.app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


# test odd creation
def test_create_without_key(client):

    rv = client.post('/create', json=test_data)
    json_data = rv.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert rv.status_code == 403


def test_create_with_key(client):
    rv = client.post('/create', headers=headers,
                     json=test_data)
    json_data = rv.get_json()

    assert rv.status_code == 200


def test_create_with_key_500(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "home_team_win_odds": 3.0,
        "away_team_win_odds": 4,
        "draw_odds": 2,
        "game_dates_wrong": "2020-02-18"  # wrong data
    }
    rv = client.post('/create', headers=headers,
                     json=data,)

    assert rv.status_code == 400


# Test update #############################
def test_update_without_key(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "home_team_win_odds": 3.0,
        "away_team_win_odds": 7,
        "draw_odds": 2,
        "game_date": "2020-02-19"
    }
    rv = client.put('/update/1', json=data)
    json_data = rv.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert rv.status_code == 403


def test_update_with_key(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "home_team_win_odds": 3.0,
        "away_team_win_odds": 4,
        "draw_odds": 2,
        "game_date": "04-05-2021",
    }
    rv1 = client.post('/create', headers=headers, json=test_data)  # Create it
    response1 = rv1.get_json()
    odds = response1["odds"]
    odds_id = odds[0]["id"]
    print("the id is", odds_id)
    assert rv1.status_code == 200
    rv = client.put(f'/update/{odds_id}', headers=headers,
                    json=data,)
    assert rv.status_code == 200
    rv = client.put('/update/3', headers=headers, json=data)  # non existing
    assert rv.status_code == 404


def test_update_with_key_500(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "home_team_win_odds": 3.0,
        "away_team_win_odds": 4,
        "draw_odds": 2,
        "game_dates_wrong": "01-05-2030"  # error in this parameter
    }

    rv = client.put('/update/1', headers=headers,
                    json=data,)

    assert rv.status_code == 400


# Test   #############################
def test_read_without_key(client):
    data = {
        "league":  "FA",
        "date_range": "12-06-2015 to 15-06-2025"
    }
    rv = client.get('/read', json=data)
    json_data = rv.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert rv.status_code == 403


def test_read_with_key(client):
    data = {
        "league": "FA",
        "date_range": "12-06-2015 to 15-06-2025"
    }
    rv = client.get('/read', json=data, headers=headers)
    json_data = rv.get_json()
    assert rv.status_code == 200


def test_read_with_key_500(client):
    data = {
        "league": "FA",
        "date_ranges_WRONG": "12-06-2015 to 15-06-2025"  # wrong param
    }
    rv = client.get('/read', json=data, headers=headers)
    json_data = rv.get_json()
    assert rv.status_code == 400


# Test Delete
def test_delete_without_key(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "game_date": "15-06-2025"
    }

    rv = client.delete('/delete', json=test_data)
    json_data = rv.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert rv.status_code == 403


def test_delete_with_key(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "game_date": "18-05-2021"

    }
    rv1 = client.post('/create', headers=headers, json=test_data)  # Create it
    print("response1 ",rv1.get_json())
    assert rv1.status_code == 200
    rv = client.delete('/delete', json=data, headers=headers)  # Delete it
    print("response2 ",rv.get_json())

  


def test_delete_with_key_500(client):
    data = {
        "league":  "FA",
        "home_team": "Arsenal",
        "away_team": "Man City",
        "game_date_wrong": "215-06-2025"  # wrong param
    }
    rv = client.delete('/delete', json=data, headers=headers)
    assert rv.status_code == 400
