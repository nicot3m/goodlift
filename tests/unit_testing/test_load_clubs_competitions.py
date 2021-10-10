import json


def loadClubs():
    with open('tests/unit_testing/test_clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('tests/unit_testing/test_competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


class TestLoadClubsCompetitions:
    """ Test load club and competitions from json files"""

    def test_happy_load_club(self):
        """ Test load club from json files"""
        test_clubs = [{"name": "test_name", "email": "test@email.com", "points": "13"},
                      {"name": "test_name2", "email": "test@email.com", "points": "5"}]
        assert loadClubs() == test_clubs

    def test_happy_load_competition(self):
        """ Test load competition from json files"""
        test_competitions = [{"name": "test_competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
                             {"name": "test_competition_full", "date": "2020-03-27 10:00:00", "numberOfPlaces": "0"},
                             {"name": "test_comp_one_left", "date": "2020-03-27 10:00:00", "numberOfPlaces": "1"}]
        assert loadCompetitions() == test_competitions
