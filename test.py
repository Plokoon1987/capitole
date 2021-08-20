from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json['msg'], "It's working!")

    # Ensure that update_data works correctly
    def test_update_data(self):
        tester = app.test_client(self)
        response = tester.get('/update_data', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json['msg'], "Los datos se han actualizado correctamente")

    # Ensure that get_day works correctly 
    def test_get_day(self):
        tester = app.test_client(self)
        response = tester.get('/data/day/day1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        response = tester.get('/data/day/day8', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json)

    # Ensure that get_hour works correctly 
    def test_get_hour(self):
        tester = app.test_client(self)
        response = tester.get('/data/hour/hour1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        response = tester.get('/data/hour/hour26', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json)

if __name__ == '__main__':
    unittest.main()
