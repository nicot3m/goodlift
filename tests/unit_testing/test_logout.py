from ... import server


class TestLogout:
    """ Test logout """

    def test_happy_logout(self):
        """ Test logout """
        response = server.app.test_client().get('/logout')
        assert response.status_code == 302
