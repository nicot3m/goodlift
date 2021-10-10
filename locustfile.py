from locust import HttpUser, task, between

import server


class LocustServer(HttpUser):
    """ Locust test of Server """

    wait_time = between(1, 2.5)
    club = server.clubs[0]
    competition = server.competitions[0]

    def on_start(self):
        """
        Test Index to show the login form and
        Test ShowSummary to show a summary
        """

        # Index
        self.client.get('/')

        # ShowSummary
        self.client.post("/showSummary", data=dict(email=self.club["email"]))

    @task
    def book(self):
        """ Test book to show the competition informations """
        self.client.get("/book/" + self.competition["name"] + "/" + self.club["name"])

    @task
    def purchasePlaces(self):
        """ Test purchasePlaces to buy places """
        self.client.post("/purchasePlaces", data=dict(club=self.club["name"], competition=self.competition["name"],
                                                      places="2"))

    @task
    def displayPoints(self):
        """ Test club points display no login required """
        self.client.get("/displayPoints")

    def on_stop(self):
        """ Test logout """
        self.client.get("/logout")
