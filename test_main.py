import unittest
from unittest.mock import patch, Mock
import main  # Assuming the provided code is saved as main.py


class TestMainMethods(unittest.TestCase):

    @patch('main.create_engine')
    @patch('main.pd.read_csv')
    @patch('main.config', return_value='dummy_password')  # Add this patch
    def test_populate_database_from_csv(self, mock_config, mock_read_csv, mock_create_engine):
        # Mocking the behavior of create_engine, read_csv, and config
        mock_create_engine.return_value = Mock()
        mock_read_csv.return_value = Mock(to_sql=Mock())

        # Testing the function
        main.populate_database_from_csv()

        # Assertions to ensure the mocked methods were called
        mock_create_engine.assert_called_once()
        self.assertEqual(mock_read_csv.call_count, 4)

    @patch('main.mysql.connector.connect')
    def test_execute_query(self, mock_connect):
        # Mocking the behavior of mysql.connector.connect
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_connect.return_value = Mock(cursor=Mock(return_value=mock_cursor))

        # Testing the function
        main.execute_query(mock_connect())

        # Assertions to ensure the mocked methods were called
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()


if __name__ == "__main__":
    unittest.main()
