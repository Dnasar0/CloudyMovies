import pytest
from unittest.mock import MagicMock
import grpc
from bson import ObjectId

# Adjust the import path based on your exact project structure
# Assuming account_server.py is in the parent directory of 'tests'
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from account_server import AccountServiceServicer, db
import account_pb2

# Mocks for MongoDB operations
# For unit tests, we replace the actual database collection with a mock object
# so we can control what the database "returns" and verify what the code "does" to it.

@pytest.fixture
def mock_accounts_collection(mocker):
    """Fixture to mock the MongoDB accounts_collection."""
    # We mock the 'accounts_collection' attribute directly on the 'db' object
    # that your AccountServiceServicer uses.
    mock_collection = mocker.patch.object(db, 'accounts', spec=True)
    return mock_collection

@pytest.fixture
def account_servicer(mock_accounts_collection):
    """Fixture to provide an instance of AccountServiceServicer with a mocked collection."""
    # Pass the mocked collection into the servicer, or ensure the servicer uses the mocked 'db.accounts'
    # Since 'db.accounts' is patched globally (or within the scope of this test module),
    # the AccountServiceServicer instance will automatically use the mock.
    return AccountServiceServicer()

@pytest.fixture
def mock_context():
    """Fixture for a mock gRPC context."""
    context = MagicMock()
    context.set_code = MagicMock()
    context.set_details = MagicMock()
    return context

# --- Test Cases ---

def test_create_account_success(account_servicer, mock_accounts_collection, mock_context):
    """Tests successful account creation."""
    # Arrange
    # Configure the mock to simulate a successful database insert
    mock_accounts_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId())
    
    request = account_pb2.CreateAccountRequest(
        username="testuser",
        password="testpassword",
        account_type="standard"
    )

    # Act
    response = account_servicer.CreateAccount(request, mock_context)

    # Assert
    # Verify insert_one was called with the correct data
    mock_accounts_collection.insert_one.assert_called_once()
    assert mock_accounts_collection.insert_one.call_args[0][0]["username"] == "testuser"
    assert mock_accounts_collection.insert_one.call_args[0][0]["password"] == "testpassword"
    assert mock_accounts_collection.insert_one.call_args[0][0]["highScore"] == 0
    assert mock_accounts_collection.insert_one.call_args[0][0]["account_type"] == "standard"

    # Verify no gRPC error was set
    mock_context.set_code.assert_not_called()
    mock_context.set_details.assert_not_called()
    assert isinstance(response, account_pb2.Empty) # CreateAccount returns Empty on success


def test_get_account_found(account_servicer, mock_accounts_collection, mock_context):
    """Tests retrieving an existing account."""
    # Arrange
    mock_account_data = {
        "username": "existinguser",
        "password": "hashedpass",
        "highScore": 100,
        "account_type": "premium"
    }
    # Configure the mock to return an account when find_one is called
    mock_accounts_collection.find_one.return_value = mock_account_data

    request = account_pb2.GetAccountRequest(username="existinguser")

    # Act
    response = account_servicer.GetAccount(request, mock_context)

    # Assert
    mock_accounts_collection.find_one.assert_called_once_with({"username": "existinguser"})
    assert response.username == "existinguser"
    assert response.password == "hashedpass"
    assert response.highScore == 100
    assert response.account_type == "premium"
    mock_context.set_code.assert_not_called()

def test_get_account_not_found(account_servicer, mock_accounts_collection, mock_context):
    """Tests retrieving a non-existent account."""
    # Arrange
    mock_accounts_collection.find_one.return_value = None # Simulate account not found
    request = account_pb2.GetAccountRequest(username="nonexistent")

    # Act
    response = account_servicer.GetAccount(request, mock_context)

    # Assert
    mock_accounts_collection.find_one.assert_called_once_with({"username": "nonexistent"})
    mock_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    mock_context.set_details.assert_called_once_with("Account not found")
    assert response is None # GetAccount returns None on error/not found

def test_update_high_score_higher_score(account_servicer, mock_accounts_collection, mock_context):
    """Tests updating high score when new score is higher."""
    # Arrange
    initial_account = {
        "username": "scorer",
        "password": "p",
        "highScore": 50,
        "account_type": "standard"
    }
    mock_accounts_collection.find_one.return_value = initial_account
    mock_accounts_collection.update_one.return_value = MagicMock(matched_count=1)

    request = account_pb2.UpdateHighScoreRequest(username="scorer", highScore=150)

    # Act
    response = account_servicer.UpdateHighScore(request, mock_context)

    # Assert
    mock_accounts_collection.find_one.assert_called_once_with({"username": "scorer"})
    mock_accounts_collection.update_one.assert_called_once_with(
        {"username": "scorer"},
        {"$set": {"highScore": 150}}
    )
    mock_context.set_code.assert_not_called()
    assert isinstance(response, account_pb2.Empty)

def test_update_high_score_lower_score(account_servicer, mock_accounts_collection, mock_context):
    """Tests updating high score when new score is lower (should not update)."""
    # Arrange
    initial_account = {
        "username": "scorer",
        "password": "p",
        "highScore": 50,
        "account_type": "standard"
    }
    mock_accounts_collection.find_one.return_value = initial_account
    # Ensure update_one is NOT called if score is lower
    mock_accounts_collection.update_one.assert_not_called() # Set expectation before Act

    request = account_pb2.UpdateHighScoreRequest(username="scorer", highScore=30)

    # Act
    response = account_servicer.UpdateHighScore(request, mock_context)

    # Assert
    mock_accounts_collection.find_one.assert_called_once_with({"username": "scorer"})
    mock_accounts_collection.update_one.assert_not_called() # Verify it was NOT called
    mock_context.set_code.assert_not_called()
    assert isinstance(response, account_pb2.Empty)

def test_delete_account_success(account_servicer, mock_accounts_collection, mock_context):
    """Tests successful account deletion."""
    # Arrange
    mock_accounts_collection.delete_one.return_value = MagicMock(deleted_count=1)
    
    # We need a valid ObjectId for the request
    test_object_id = str(ObjectId())
    request = account_pb2.DeleteAccountRequest(id=test_object_id)

    # Act
    response = account_servicer.DeleteAccount(request, mock_context)

    # Assert
    mock_accounts_collection.delete_one.assert_called_once_with({"_id": ObjectId(test_object_id)})
    mock_context.set_code.assert_not_called()
    assert isinstance(response, account_pb2.Empty)

def test_delete_account_not_found(account_servicer, mock_accounts_collection, mock_context):
    """Tests deleting a non-existent account."""
    # Arrange
    mock_accounts_collection.delete_one.return_value = MagicMock(deleted_count=0) # Simulate not found

    test_object_id = str(ObjectId())
    request = account_pb2.DeleteAccountRequest(id=test_object_id)

    # Act
    response = account_servicer.DeleteAccount(request, mock_context)

    # Assert
    mock_accounts_collection.delete_one.assert_called_once_with({"_id": ObjectId(test_object_id)})
    mock_context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)
    mock_context.set_details.assert_called_once_with("Account not found")
    assert isinstance(response, account_pb2.Empty)