import os
import json
import tempfile

import pytest

import app

headers = {'Content-Type': 'application/json', 'api-key': '1254'}
test_data = {
    "league":  "Champions League",
    "home_team": "Barcelona",
    "away_team": "PSG",
    "home_team_win_odds": 2.1,
    "away_team_win_odds": 3.9,
    "draw_odds": 6.1,
    "game_date": "18-05-2021"
}


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    with app.app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


# test odd creation
def test_create_odds_while_not_authenitcated(client):

    resposnse = client.post('/create', json=test_data)
    json_data = resposnse.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert resposnse.status_code == 403


def test_create_odds_while_authenticated(client):
    response = client.post('/create', headers=headers,
                           json=test_data)
    json_data = response.get_json()

    assert response.status_code == 200

# test with wrong data


def test_create_odds_with_wrong_data(client):
    data = {
        "league":  "Champions League",
        "no_team": "Barcelona",
        "away_team": "PSG",
        "home_team_win_odds": 3.0,
        "away_team_win_odds": 4,
        "draw_odds": 2,
        "game_date": "2020-02-18"
    }
    rv = client.post('/create', headers=headers,
                     json=data,)

    assert rv.status_code == 400


# Test update #############################
def test_update_without_key(client):
    data = {
        "league":  "Champions League",
        "home_team": "Barcelona",
        "away_team": "PSG",
        "home_team_win_odds": 3.0,
        "away_team_win_odds": 7,
        "draw_odds": 2,
        "game_date": "2020-02-19"
    }
    rv = client.put('/update/1', json=data)
    json_data = rv.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert rv.status_code == 403

# Updating odds


def test_update_with_auth(client):
    data = {
        "league":  "Champions League",
        "home_team": "Barcelona",
        "away_team": "PSG",
        "home_team_win_odds": 2,
        "away_team_win_odds": 5,
        "draw_odds": 6,
        "game_date": "04-05-2021",
    }
    response1 = client.post('/create', headers=headers,
                            json=test_data)  # Create it
    resData = response1.get_json()
    odds = resData["odds"]
    odds_id = odds[0]["id"]
    print("the id is", odds_id)
    assert response1.status_code == 200
    response2 = client.put(f'/update/{odds_id}', headers=headers,
                           json=data,)
    assert response2.status_code == 200
    response2 = client.put('/update/3', headers=headers,
                           json=data)  # non existing
    assert response2.status_code == 404


def test_update_with_wrong_data(client):
    data = {
        "no league ": "Barcelona",
        "away_team": "PSG",
        "home_team_win_odds": 5,
        "away_team_win_odds": 2,
        "draw_odds": 1.6,
        "game_dat": "01-05-2030"  # error in this parameter
    }

    rv = client.put('/update/1', headers=headers,
                    json=data,)

    assert rv.status_code == 400


# Test   reading odds
def test_read_odds_without_auth(client):
    data = {
        "league":  "Champions League",
        "date_range": "12-09-2018 to 18-09-2024"
    }
    response = client.get('/read', json=data)
    json_data = response.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert response.status_code == 403


def test_read_odds_with_auth(client):
    data = {
        "league": "Champions League",
        "date_range": "12-09-2018 to 18-09-2024"
    }
    response1 =client.post('/create',json=test_data,headers=headers)
    response = client.get('/read', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200


def test_read_odds_with_invalid_filds(client):
    data = {
        "league": "Champions League",
        "invalid": "112-09-2018 to 18-09-2024"  # wrong param
    }
    response = client.get('/read', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400


# Test Delete
def test_delete_odds_with_no_auth(client):
    data = {
        "league":  "Champions League",
        "home_team": "Barcelona",
        "away_team": "PSG",
        "game_date": "15-06-2025"
    }

    response = client.delete('/delete', json=test_data)
    json_data = response.get_json()

    assert json_data['message'] == 'please contanct admin for api key'
    assert response.status_code == 403


def test_delete_with_auth(client):
    data = {
        "league":  "Champions League",
        "home_team": "Barcelona",
        "away_team": "PSG",
        "game_date": "18-05-2021"

    }
    response1 = client.post('/create', headers=headers, json=test_data)  # Create it
    print("response1 ", response1.get_json())
    assert response1.status_code == 200
    response = client.delete('/delete', json=data, headers=headers)  # Delete it
    print("response2 ", response.get_json())


def test_delete_with_invalid_data(client):
    data = {
        "league":  "Champions League",
        "no_team": "Barcelona",
        "away_team": "PSG",
        "game_date": "215-06-2025"  # wrong param
    }
    response = client.delete('/delete', json=data, headers=headers)
    assert response.status_code == 400
