from interfaces.db import DB
from firebase_admin import firestore, credentials, initialize_app

cred = credentials.Certificate('key.json')

default_app = initialize_app(cred)
db = firestore.client()


class Firestore(DB):
    _instance = None

    def connect(self):

        self.odds_reff = db.collection('odds')
        return self

    def insert(self, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        try:
            odds = {

                "league": league,
                "home_team": home_team,
                "away_team": away_team,
                "home_team_win_odds": home_team_win_odds,
                "away_team_win_odds": away_team_win_odds,
                "draw_odds": draw_odds,
                "game_date": game_date
            }

            odd = self.odds_reff.add(odds)
            odds = self.odds_reff.document(odd[1].id).get().to_dict()
            odds["id"] = odd[1].id
            print("the odds are",odds)
            return True, [odds]
        except Exception as e:
            return False, f"An Error Occured: {e}"

    def update(self, odd_id, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        try:

            doc = self.odds_reff.document(odd_id).set({

                "league": league,
                "home_team": home_team,
                "away_team": away_team,
                "home_team_win_odds": home_team_win_odds,
                "away_team_win_odds": away_team_win_odds,
                "draw_odds": draw_odds,
                "game_date": game_date
            })

            return True, doc
        except Exception as e:
            return False, f"An Error Occured: {e}"

    def read(self, league, date_from, date_to):
        try:
            odds = []
            docs = self.odds_reff.where("game_date", ">=", date_from).where(
                "game_date", "<=", date_to).stream()
            for doc in docs:
                odds.append(doc.to_dict())

            return True, odds
        except Exception as e:
            return False, f"An Error Occured: {e}"

    def delete(self, home_team, away_team, game_date):
        try:
        
            docs = self.odds_reff.where("home_team","==",home_team).where("away_team","==",away_team).where("game_date","==",game_date).get()
            print("the docs are aw",docs)

            if docs:
                print("the docs are",docs)
                for doc in docs:
                  self.odds_reff.document(doc.id).delete()

            

                return True, "odds"
            return False ,"odds not found"
        except Exception as e:
            print(f"An Error Occured: {e}")
            return False, f"An Error Occured: {e}"

    def get(self, odd_id):
        try:
            doc = self.odds_reff.document(odd_id).get().to_dict()
            if doc:
                return True, [doc]
            return False, "Couldn't find doc"
        except Exception as e:
            return False, f"An Error Occured: {e}"

    def find_by_required_field(self, home_team, away_team, game_date):
        print( home_team, away_team, game_date)
        try:
            returned_odds =  self.odds_reff.where("home_team","==",home_team).where("away_team","==",away_team).where("game_date","==",game_date).get()
            if returned_odds:
                print("from find fields",returned_odds[0].id)
                return True, returned_odds
            return False, f"could'nt find the odds"
        except Exception as e:
            print(f"An Error Occured: {e}")
            return False, f"An Error Occured: {e}"

    @staticmethod
    def getInstance(re_init=False):
        """ get instance of the class """
        if Firestore._instance is None or re_init is True:
            return Firestore()

        return Firestore._instance
