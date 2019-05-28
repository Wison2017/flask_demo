import unittest
from app.models import User


class MyTest(unittest.TestCase):
    def setUp(self):
        print('test start!')

    def tearDown(self):
        print('test end!')

    def testReadSql(self):
        user = User.query.filter_by(username='wison').first()
        print(user.check_password_hash('123456'))
        print(user)
