from ... import server


class TestIndex:
    """ Test index """

    def test_happy_index(self):
        """ Test index blanck path"""
        response = server.app.test_client().get('/')
        assert response.status_code == 200

    def test_sad_index(self):
        """ Test index wrong path"""
        response = server.app.test_client().get('/wrong_path')
        assert response.status_code == 404
