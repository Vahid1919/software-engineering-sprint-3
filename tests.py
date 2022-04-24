import unittest
from app import app



class CoronaTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # tests to check all unprotected routes are working

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_visitorRegistration_page(self):
        response = self.app.get('/visitor-registration', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_placeRegistration_page(self):
        response = self.app.get('/place-registration', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_agentLogin_page(self):
        response = self.app.get('/agent-login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_hospitalLogin_page(self):
        response = self.app.get('/hospital-login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)





    # test to check that all protected routes fail without registered/loggedin client
    def test_placeHome_page(self):
        response = self.app.get('/place-home', follow_redirects=True)
        self.assertIn(
            b'form class="registration" action="/place-registration" method="post"', response.data)

    def test_visitorHome_page(self):
        response = self.app.get('/visitor-home', follow_redirects=True)
        self.assertIn(
            b'<form class="login" action="/visitor-registration" method="post">', response.data)

    def test_agentHome_page(self):
        response = self.app.get('/agent-home', follow_redirects=True)
        self.assertIn(
            b'<form class="registration" action="agent-login" method="post">', response.data)


    def test_visitorRegistration_fail(self):
        response = self.app.post(
            '/visitor-registration', data=dict(name="test", city="test", address="test", email="sdfsd@sdf.com"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test visitor registration with full data
    def test_visitorRegistration_work(self):
        response = self.app.post(
            '/visitor-registration', data=dict(name="test", city="test", address="test", email="sdfsd@sdf.com", phone="234324424"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test place registration with missing data - leaving out email and phone
    def test_placeRegistration_fail(self):
        response = self.app.post(
            '/place-registration', data=dict(pname="test", address="test", phone="23432"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        
    def test_placeRegistration_fail2(self):
        response = self.app.post(
            '/place-registration', data=dict(pname="test", address="test", email="test@sd.com"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test place registration with full data
    def test_placeRegistration_work(self):
        response = self.app.post(
            '/place-registration', data=dict(pname="test", address="test", email="test@sd.com", phone="2442423432"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test agent login with wrong data

    def test_agentLogin_fail(self):
        response = self.app.post(
            '/agent-login', data=dict(agent_id="10", username="test", password="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        
    def test_agentLogin_invalid(self):
        response = self.app.post(
            '/agent-login', data=dict(agent_id="hello", username="test", password="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 500)

    # test admin login with correct data

    def test_adminLogin_work(self):
        response = self.app.post(
            '/agent-login', data=dict(agent_id=1, username="testname", password="testpassword"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test hospital login with wrong data

    def test_hospitalLogin_fail(self):
        response = self.app.post(
            '/hospital-login', data=dict(hospital_id="10", username="test", password="test"), follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    # test hospital login with correct data

    def test_hospitalLogin_work(self):
        response = self.app.post(
            '/hospital-login', data=dict(hospital_id="1", username="testname", password="testpassword"), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    # test for agent DB search - commented out because this part is not implemented
    # def test_agentDBsearch(self):
    #     response = self.app.post(
    #         '/agent-place-search', data=dict(id="1"), follow_redirects=True)
        
    #     self.assertEqual(response.status_code, 200)

    # test for hospital visitor DB search
    def test_hospitalDBsearch(self):
        
        #setting session that would be available in normal login
        with self.app as tester:
            with tester.session_transaction() as session:
                session["Hospital_name"] = 'testname'
            
        
            response = self.app.post(
                '/hospital-DB-search', data=dict(name="test"), follow_redirects=True)
        
            self.assertEqual(response.status_code, 200)

    # test for hospital visitor status change, to mark as infected
    def test_hospitalDBstatuschange(self):
        response = self.app.post(
            '/hospital-DB-status-change', data=dict(name="test", status=1), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        
    # test for hospital registration, when an agent registers a hospital
    def test_hospitalRegistrationWork(self):
        response = self.app.post(
            '/agent-add-hospital', data=dict(username="testhospital", password="testpassword"), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    # missing password
    def test_hospitalLoginFail(self):
        response = self.app.post(
            '/agent-add-hospital', data=dict(username="testhospital", password=""), follow_redirects=True)
        
        self.assertEqual(response.status_code, 400)
        
    # missing username
    def test_hospitalRegistrationUsernameFail(self):
        response = self.app.post(
            '/agent-add-hospital', data=dict(username="", password="45678ihgc"), follow_redirects=True)
        
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
