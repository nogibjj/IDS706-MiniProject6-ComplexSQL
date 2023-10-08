import unittest
import mysql.connector
import main  # Assuming the above code is saved as main.py
from decouple import config


class TestMainMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This method will run once before any tests
        cls.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=config('DB_PASSWORD'),
            auth_plugin='mysql_native_password'
        )
        cls.test_db_name = 'test_sales_database'
        main.create_database(cls.conn, cls.test_db_name)
        cls.conn.database = cls.test_db_name

    @classmethod
    def tearDownClass(cls):
        # This method will run once after all tests are completed
        cursor = cls.conn.cursor()
        cursor.execute(f"DROP DATABASE {cls.test_db_name}")
        cls.conn.close()

    def test_database_population(self):
        # Test whether data is loaded into MySQL from CSVs correctly
        main.populate_database_from_csv(db_name=self.test_db_name)

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]
        self.assertTrue(count > 0)  # Assumes you have data in customers.csv

    def test_query_execution(self):
        # Test whether the SQL query runs without errors
        results = main.execute_query(self.conn)
        self.assertIsInstance(results, list)
        if results:
            self.assertIsInstance(results[0], tuple)


if __name__ == "__main__":
    unittest.main()
