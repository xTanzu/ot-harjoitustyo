import unittest
from dbaos.user_dbao import UserDbao
from dbaos.clique_dbao import CliqueDbao

class TestCliqueDbao(unittest.TestCase):

    def setUp(self):
        self.test_clique_dbao = CliqueDbao("sqlite3_in_memory")
        self.test_user_dbao = UserDbao("sqlite3_in_memory")

    def tearDown(self):
        self.test_clique_dbao.disconnect()
        self.test_user_dbao.disconnect()

    def test_get_db_type_succesful(self):
        self.assertEqual(self.test_clique_dbao.db_type, "sqlite3_in_memory")

    def test_get_db_path_succesful(self):
        self.assertEqual(self.test_clique_dbao.db_path, "data/data.db")

    def test_wrong_db_type_raises_connection_error(self):
        self.assertRaises(ConnectionError, lambda: CliqueDbao("wrong type"))

    def test_wrong_db_path_raises_connection_error(self):
        self.assertRaises(ConnectionError, lambda: CliqueDbao("sqlite3_file", "folderthatdoesnotexist/data.db"))

    def test_new_user_has_no_cliques(self):
        user1_info = ("testUsername", "testPassword", "testFirstName", "testLastName")
        succesful1 = self.test_user_dbao.insert_new_user(*user1_info)
        self.assertTrue(succesful1)
        result1:list = self.test_clique_dbao.find_cliques_by_head_id(1)
        self.assertEqual(len(result1), 0)
        result2:tuple = self.test_clique_dbao.find_latest_clique_by_head_id(1)
        self.assertIsNone(result2)

    def test_clique_with_existing_head_can_be_inserted_and_found(self):
        user1_info = ("testUsername", "testPassword", "testFirstName", "testLastName")
        succesful1 = self.test_user_dbao.insert_new_user(*user1_info)
        self.assertTrue(succesful1)
        clique1_info = ("testCliqueName", "test clique description", 1)
        succesful2 = self.test_clique_dbao.insert_new_clique(*clique1_info)
        self.assertTrue(succesful2)
        result1:list = self.test_clique_dbao.find_cliques_by_head_id(1)
        self.assertEqual(result1, [(1,) + clique1_info] )
        clique2_info = ("testClique2Name", "test clique2 description", 1)
        succesful3 = self.test_clique_dbao.insert_new_clique(*clique2_info)
        self.assertTrue(succesful3)
        result2:tuple = self.test_clique_dbao.find_latest_clique_by_head_id(1)
        self.assertEqual(result2, (2,) + clique2_info)
        result3:list = self.test_clique_dbao.find_cliques_by_head_id(1)
        self.assertEqual(result3, [(1,) + clique1_info, (2,) + clique2_info] )
        user2_info = ("testUsername2", "testPassword2", "testFirstName2", "testLastName2")
        succesful4 = self.test_user_dbao.insert_new_user(*user2_info)
        self.assertTrue(succesful4)
        clique3_info = ("testClique3Name", "test clique3 description", 2)
        succesful5 = self.test_clique_dbao.insert_new_clique(*clique3_info)
        self.assertTrue(succesful5)
        result4:list = self.test_clique_dbao.find_cliques_by_head_id(2)
        self.assertEqual(result4, [(3,) + clique3_info] )
        result5:tuple = self.test_clique_dbao.find_latest_clique_by_head_id(2)
        self.assertEqual(result5, (3,) + clique3_info)

    def test_clique_with_non_existing_head_cannot_be_inserted(self):
        clique_info = ("testCliqueName", "test clique description", 1)
        succesful = self.test_clique_dbao.insert_new_clique(*clique_info)
        self.assertFalse(succesful)