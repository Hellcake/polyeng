# test_telegram.py
import pytest
from data_adder import insert_data  # Replace with your actual function

@pytest.fixture
def mock_db(mocker):
    # Mock the database connection and cursor
    mock_conn = mocker.Mock()
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('data_adder.conn', new=mock_conn)  # Replace 'data_adder.conn' with your actual database connection object
    return mock_conn, mock_cursor

def test_insert_data(mock_db):
    _, mock_cursor = mock_db
    # Call the function that adds data to the database
    insert_data()  # Replace with your actual function call
    
    # Assert that executemany was called on the cursor
    mock_cursor.executemany.assert_called()