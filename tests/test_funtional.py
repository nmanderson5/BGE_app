import pytest
from BGE_app.project import main, db, User, Egg

main.config.update({
    "TESTING": True,
    })

def test_homepage():
    with main.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'Create an account or login!' in response.data


def test_register():
    # Trying to create a new user and checking if it redirects to the user's dashboard
    with main.test_client() as test_client:
        response = test_client.post('/register', data={
            'username': 'testuser',
            'password': 'test1234'
            }, follow_redirects=True)
        assert response.status_code == 200
        assert b"testuser's Egg" in response.data

        # Trying to create the same user again and checking for the error message
        response = test_client.post('/register', data={
            'username': 'testuser',
            'password': 'test1234'
            }, follow_redirects=True)
        assert response.status_code == 200
        assert b'User already exists!' in response.data


def test_login_logout():
    # Trying to log in with the user created in the last test
    with main.test_client() as test_client:
        response = test_client.post('/login', data={
            'username': 'testuser',
            'password': 'test1234'
            }, follow_redirects=True)
        assert response.status_code == 200
        assert b"testuser's Egg" in response.data

        # Now log user out and follow redirect to homepage
        response = test_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Create an account or login!' in response.data
        
        # Delete the created user and their egg from the database
        test_user = User.query.filter_by(username='testuser').first()
        db.session.delete(Egg.query.filter_by(user_id=test_user.id).first())
        db.session.delete(test_user)
        db.session.commit()


def test_browse():
    with main.test_client() as test_client:
        response = test_client.get('/browse')
        assert response.status_code == 200
        assert b'Browse for recipes!' in response.data

        response = test_client.post('/browse', data={
            'term': 'Lamb',
            'entree': 'True',
            'temp': '400',
            'cook_method': 'Both'
        })
        assert response.status_code == 200
        assert b'Results!' in response.data