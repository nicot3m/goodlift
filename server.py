import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    """ load clubs from json file """
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    """ load competitions from json file """
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """ Route to show the login form """
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """ Route to show a summary """
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash("Invalid email")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """ Route to show the competition informations """
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
    except IndexError:
        flash("Invalid club")
        return redirect(url_for('index'))
    try:
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("Invalid competition")
        return redirect(url_for('index'))

    # Book if competition not full
    if foundClub and foundCompetition and int(foundCompetition["numberOfPlaces"]) > 0:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("No more places for sale!")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """ Route to buy places """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
    club['points'] = int(club['points'])

    # Debug hotfix test_sad_purchase purchase more than 12 places
    if placesRequired > 12:
        flash("You cannot buy more than 12 places!")

    # Debug hotfix test_sad_purchase2 not enough points
    elif placesRequired > club['points']:
        flash("You have not enough points!")

    # Debug hotfix test_sad_purchase3 purchase more places than left in competition
    elif placesRequired > competition['numberOfPlaces']:
        flash("Not so many places for sell!")

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

        # Debug hotfix test_happy_purchase
        club['points'] = int(club['points'])-placesRequired

        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/displayPoints')
def displayPoints():
    """ Route to display points """
    return render_template('display_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    """ Route to logout """
    return redirect(url_for('index'))
