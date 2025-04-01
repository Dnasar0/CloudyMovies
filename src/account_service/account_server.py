import grpc
from concurrent import futures
import account_pb2
import account_pb2_grpc
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://mongodb:27017/")
db = client["cloudy_movies"]
accounts_collection = db["accounts"]

class AccountServiceServicer(account_pb2_grpc.AccountServiceServicer):
    def CreateAccount(self, request, context):
        try:
            account_data ={
                "username": request.username,
                "password": request.password,
                "highScore": 0,
                "account_type": request.account_type
            }
            result = accounts_collection.insert_one(account_data)
            if result.inserted_id:
                    print(f"Created account with ID: {result.inserted_id}")
                    return account_pb2.Empty()
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error creating account: {str(e)}")
            return account_pb2.Empty()            

    def GetAccount(self, request, context):
        try:
            account_name = request.username
            account = accounts_collection.find_one({"username": account_name})
            if account:
                return account_pb2.Account(
                    id=str(account["_id"]),
                    username=account["username"],
                    password=account["password"],
                    highScore=account["highScore"],
                    account_type=account["account_type"]
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error retrieving account: {str(e)}")
            return None 

    def UpdateAccount(self, request, context):
        try:
            account_id = ObjectId(request.id)
            account = accounts_collection.find_one_and_update(
                {"_id": account_id},
                {"$set": {
                    "username": request.username,
                    "password": request.password,
                    "highScore": request.highScore,
                    "account_type": request.account_type
                }}
            )
            if account:
                print(f"Updated Account with ID: {request.id}")
                return account_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return account_pb2.Empty()
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error updating Account: {str(e)}")
            return account_pb2.Empty()    

    def DeleteAccount(self, request, context):
        try:
            account_id = ObjectId(request.id)
            result = accounts_collection.delete_one({"_id": account_id})
            if result.deleted_count == 0:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return account_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error deleting account: {str(e)}")
            return account_pb2.Empty()    
        # Handle account deletion logic

    def UpdateHighScore(self, request, context):
        try:
            account = accounts_collection.find_one({"username": request.username})
            if not account:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return account_pb2.Empty()

            # Only update if the new score is higher
            if request.highScore > account.get("highScore", 0):
                accounts_collection.update_one(
                    {"username": request.username},
                    {"$set": {"highScore": request.highScore}}
                )
                print(f"High score updated for {request.username} to {request.highScore}")
            else:
                print(f"High score NOT updated for {request.username}, lower score provided.")

            return account_pb2.Empty()
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error updating high score: {str(e)}")
            return account_pb2.Empty()

    def UpdateAccountType(self, request, context):
        try:
            account_id = ObjectId(request.id)
            account = accounts_collection.find_one_and_update(
                {"_id": account_id},
                {"$set": {
                    "account_type": request.account_type
                }}
            )
            if account:
                print(f"Updated Account with ID: {request.id}")
                return account_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return account_pb2.Empty()
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error updating Account: {str(e)}")
            return account_pb2.Empty()       

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
