import unittest
import dbConnect
import dbUser

class TestAuthenticate(unittest.TestCase):
    def setUp(self):
        self.db = dbConnect.getDatabase()
    
    def test_fake_user(self):
        self.assertFalse(dbUser.has_user(self.db, 'fakeuser'))

    def test_insert_delete_user(self):
        username, password = 'fakeuser', 'fakepassword'
        # Make new salt and key credentials to save
        khash = dbUser.get_new_credentials(username, password)
        # Insert user into database
        dbUser.insert_user(self.db, username, khash)
        # Check user inserted as expected
        self.assertTrue(dbUser.authenticate(self.db, username, password))
        # Delete user
        dbUser.delete_user(self.db, username)
        # Check user is properly removed from database
        self.assertFalse(dbUser.has_user(self.db, username))

    def tearDown(self):
        self.db.close()

if __name__ == '__main__':
    unittest.main()