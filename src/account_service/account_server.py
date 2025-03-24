import grpc
from concurrent import futures
import account_pb2
import account_pb2_grpc
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["account_service"]
accounts_collection = db["accounts"]

class AccountServiceServicer(account_pb2_grpc.AccountServiceServicer):
    def CreateAccount(self, request, context):
        # Handle account creation logic
        print(f"Creating account: {request.username}")
        return account_pb2.Empty()  # Return an empty response on success

    def GetAccountById(self, request, context):
        # Simulate getting account from a database
        print(f"Fetching account with ID: {request.id}")
        return account_pb2.Account(
            username="example_user",
            password="password123",
            highScore=100,
            account_type="basic"
        )

    def UpdateAccount(self, request, context):
        # Handle account update logic
        print(f"Updating account: {request.username}")
        return account_pb2.Empty()  # Return an empty response on success

    def DeleteAccount(self, request, context):
        # Handle account deletion logic
        print(f"Deleting account with ID: {request.id}")
        return account_pb2.Empty()  # Return an empty response on success

def serve():
    # Connect to MongoDB (replace with your MongoDB URI if needed)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_AccountServiceServicer_to_server(AccountServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Account server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
