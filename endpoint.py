import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_incorrect_date_format(self):
        response = self.app.get('/?datetime=04-12-24 02:22')
        self.assertEqual(response.status_code, 400)

    def test_ridiculous_time(self):
        response = self.app.get('/?datetime=2024-04-14 04:00')
        self.assertEqual(response.data.strip(),
                         b'{"Day of the week":"Sun","Requested hour":"04:00 AM","open_restaurants":[]}')

    def test_ridiculous_date(self):
        response = self.app.get('/?datetime=1897-04-14 09:22')
        self.assertEqual(response.status_code, 400)

    def test_sat_morning(self):
        response = self.app.get('/?datetime=2024-04-20 09:22')
        self.assertEqual(response.data.strip(),
                         b'{"Day of the week":"Sat","Requested hour":"09:22 AM","open_restaurants":['
                         b'"Tupelo Honey","Char Grill"]}')

    def test_sat_afternoon(self):
        response = self.app.get('/?datetime=2024-04-20 14:22')
        self.assertEqual(response.data.strip(),
                         b'{"Day of the week":"Sat","Requested hour":"02:22 PM","open_restaurants":["The Cowfish '
                         b'Sushi Burger Bar","Morgan St Food Hall","Crawford and Son","Bida Manda","Tupelo Honey",'
                         b'"Player\'s Retreat","Glenwood Grill","Neomonde","Page Road Grill","Mez Mexican","Saltbox",'
                         b'"El Rodeo","Provence","Tazza Kitchen","Mandolin","Mami Nora\'s","Gravy","Char Grill",'
                         b'"Whiskey Kitchen","Sitti","Yard House","David\'s Dumpling","Gringo a Gogo","Centro",'
                         b'"Brewery Bhavana","Dashi","Oakleaf"]}')

    def test_sun_afternoon(self):
        response = self.app.get('/?datetime=2024-04-14 14:22')
        self.assertEqual(response.data.strip(),
                         b'{"Day of the week":"Sun","Requested hour":"02:22 PM","open_restaurants":["The Cowfish '
                         b'Sushi Burger Bar","Morgan St Food Hall","Beasley\'s Chicken + Honey","Garland",'
                         b'"Crawford and Son","Bida Manda","The Cheesecake Factory","Tupelo Honey","Player\'s '
                         b'Retreat","Glenwood Grill","Neomonde","Page Road Grill","Mez Mexican","Saltbox","El Rodeo",'
                         b'"Provence","Tazza Kitchen","Mandolin","Mami Nora\'s","Gravy","Taverna Agora","Char Grill",'
                         b'"Whiskey Kitchen","Sitti","Yard House","Gringo a Gogo","Centro","Brewery Bhavana","Dashi",'
                         b'"Oakleaf"]}')

    def test_tue_evening(self):
        response = self.app.get('/?datetime=2024-04-16 14:22')
        self.assertEqual(response.data.strip(),
                         b'{"Day of the week":"Tue","Requested hour":"02:22 PM","open_restaurants":["The Cowfish '
                         b'Sushi Burger Bar","Morgan St Food Hall","Garland","Crawford and Son","Bida Manda",'
                         b'"The Cheesecake Factory","Tupelo Honey","Player\'s Retreat","Glenwood Grill","Neomonde",'
                         b'"Page Road Grill","Mez Mexican","Saltbox","El Rodeo","Provence","Tazza Kitchen",'
                         b'"Mandolin","Mami Nora\'s","Gravy","Taverna Agora","Char Grill","Whiskey Kitchen","Sitti",'
                         b'"Yard House","David\'s Dumpling","Gringo a Gogo","Brewery Bhavana","Dashi","Top of the '
                         b'Hill","Jose and Sons","Oakleaf","Second Empire"]}')


if __name__ == '__main__':
    unittest.main()
