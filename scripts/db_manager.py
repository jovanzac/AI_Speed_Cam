import os
import pyrebase
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from scripts.helpers import decode_psswd


class DbManager :
    CONFIG = {
        "apiKey": os.environ.get("apiKey"),
        "authDomain": os.environ.get("authDomain"),
        "projectId": os.environ.get("projectId"),
        "storageBucket": os.environ.get("storageBucket"),
        "messagingSenderId": os.environ.get("messageSenderId"),
        "appId": os.environ.get("appId"),
        "measurementId": os.environ.get("measurementId"),
        "serviceAccount": os.environ.get("serviceAccount"),
        "databaseURL": os.environ.get("databaseURL")
    }
    
    def __init__(self) :
        self.firebase = pyrebase.initialize_app(self.CONFIG)
        self.storage = self.firebase.storage()
        
         # Initialize mongodb
        self.uri = os.environ.get("MONGO_DB_URI")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.speed_db = self.client["SpeedAI"]
        print("Connection established with mongodb")
    
    
    def plates_to_storage(self, file_loc) :
        """Add any new plates in the plates directory to firebase storage.

        Args:
            filename (str): name of the file
        """
        print("Here in plate to storage.")
        print(f"Putting plate : {file_loc} in storage")
        if os.path.exists(file_loc) :
            file_name = file_loc[len("./plates/"):]
            self.storage.child(f"Speed_detection_AI/plates/{file_name}").put(file_loc)
            print(f"Put {file_loc} in storage")
            
        
    def authenticate_user(self, username, psswd) :
        user_psswd = decode_psswd(psswd)
        user = self.speed_db["Users"].find_one({"username": username, "password": user_psswd})
        if user:
            # Document with the same username and password exists
            return True
        else:
            # Document does not exist
            return False
        
        
db_manager = DbManager()