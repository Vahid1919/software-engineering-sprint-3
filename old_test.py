import unittest
from app import app
from flask import json


class CoronaTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # tests to check all unprotected routes are working

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_visitorRegistration_page(self):
        response = self.app.get('/register_visitor', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_placeRegistration_page(self):
        response = self.app.get('/register_place', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_agentLogin_page(self):
        response = self.app.get('/login_agent', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_hospitalLogin_page(self):
        response = self.app.get('/login_hospital', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        
        
        
        

    # tests to check that all protected routes fail without registered/loggedin client

    def test_placeHome_page(self):
        response = self.app.get('/register_place', follow_redirects=True)
        self.assertIn(
            b'<form class="login" action="/register_place" method="POST">', response.data)

    def test_visitorHome_page(self):
        response = self.app.get('/QR_code_scan', follow_redirects=True)
        self.assertIn(
            b'<form class="login" action="/register_visitor" method="POST">', response.data)

    def test_agentHome_page(self):
        response = self.app.get('/agent_page', follow_redirects=True)
        self.assertIn(
            b'<form class="login" action="/login_agent" method="POST">', response.data)

    def test_hospitalHome_page(self):
        response = self.app.get('/hospital_dashboard', follow_redirects=True)
        self.assertIn(
            b'<form class="login" action="/login_hospital" method="POST">', response.data)

    # test visitor registration with missing data - leaving out phone
    def test_visitorRegistration_fail(self):
        response = self.app.post(
            '/register_visitor', data=dict(fname="test", lname="test", city="test", address="test", email="sdfsd@sdf"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test visitor registration with full data
    def test_visitorRegistration_work(self):
        response = self.app.post(
            '/register_visitor', data=dict(fullname="test name", address="test", email="sdfsd@sdf.com", phone="+491522203945"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # test place registration with missing data - leaving out email
    def test_placeRegistration_fail(self):
        response = self.app.post(
            '/register_place', data=dict(placename="", address="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test place registration with full data
    def test_placeRegistration_work(self):
        response = self.app.post(
            '/register_place', data=dict(placename="test", address="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test agent login with wrong data (non existent account)
    def test_agentLogin_fail(self):
        response = self.app.post(
            '/login_agent', data=dict(username="test", password="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test admin login with correct data (account exists)
    def test_adminLogin_work(self):
        response = self.app.post(
            '/login_agent', data=dict(username="agent1", password="password"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test hospital login with wrong data (non existent account)
    def test_hospitalLogin_fail(self):
        response = self.app.post(
            '/login_hospital', data=dict(username="test", password="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test hospital login with correct data
    def test_hospitalLogin_work(self):
        response = self.app.post(
            '/login_hospital', data=dict(username="BremenNord", password="Bremen123"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test logout functionality of routes

    # test login and logout of visitor
    def test_visitorLogout_working(self):
        login_response = self.app.post(
            '/register_visitor', data=dict(fullname="test name", address="test", email="sdfsd@sdf.com", phone="+491522203945"), follow_redirects=True)

        logout_response = self.app.get('/logout_visitor')

        return self.assertEqual(login_response.status_code, 200) and self.assertIn(
            b'<form class="user-type" action="./" method="POST">', response.data)

    # test login and logout of place
    def test_placeLogout_working(self):
        login_response = self.app.post(
            '/register_place', data=dict(placename="test name", address="test"), follow_redirects=True)

        logout_response = self.app.get('/logout_place')

        return self.assertEqual(login_response.status_code, 200) and self.assertIn(
            b'<form class="user-type" action="./" method="POST">', response.data)

    # test login and logout of agent
    def test_agentLogout_working(self):
        login_response = self.app.post(
            '/login_agent', data=dict(username="agent1", password="password"), follow_redirects=True)

        logout_response = self.app.get('/logout_agent')

        return self.assertEqual(login_response.status_code, 200) and self.assertIn(
            b'<form class="user-type" action="./" method="POST">', response.data)

    # test login and logout of hospital
    def test_hospitalLogout_working(self):
        login_response = self.app.post(
            '/login_hospital', data=dict(username="BremenNord", password="Bremen123"), follow_redirects=True)

        logout_response = self.app.get('/logout_hospital')

        return self.assertEqual(login_response.status_code, 200) and self.assertIn(
            b'<form class="user-type" action="./" method="POST">', response.data)

    # test if hospital registration worked
    def test_hospitalRegistration_working(self):
        self.app.post(
            '/login_agent', data=dict(username="agent1", password="password"), follow_redirects=True)

        response = self.app.post('/register_hospital',
                                 data=dict(username="testhospital"))

        self.assertIn(
            b'Registered Username', response.data)

    # test if visitor sign in to page worked
    def test_visitorSignin(self):
        self.app.post(
            '/register_visitor', data=dict(fname="test", lname="test", city="test", address="test", email="sdfsd@sdf"), follow_redirects=True)

        # existing test place from database
        response = self.app.get(
            '/place/89ad85ab-1c32-4386-b61a-54e5c6f3010a', follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test if visitor sign out of page worked
    def test_visitorSignOut(self):
        self.app.post(
            '/register_visitor', data=dict(fname="test", lname="test", city="test", address="test", email="sdfsd@sdf"), follow_redirects=True)

        self.app.get(
            '/place/89ad85ab-1c32-4386-b61a-54e5c6f3010a', follow_redirects=True)

        response = self.app.post('/signout',
                                 data=dict(qrcode="89ad85ab-1c32-4386-b61a-54e5c6f3010a"),  follow_redirects=True)

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
