import os
import pyrebase
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from scripts.helpers import decode_psswd, encode_psswd


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
        user = self.speed_db["Users"].find_one({"Username": username})

        if user:
            stored_password = user['Password']
            decoded_password = decode_psswd(stored_password)
            if decoded_password == psswd:
                # Passwords match
                return True

        return False
        
    
    def signup_user(self, uid, name, username, psswd, email, phone_no) :
        user_exists = self.speed_db["Users"].find_one({"Username": username})
        if user_exists:
            # Document with the same username exists
            return False
        else:
            # Document does not exist
            # Encrypt the password
            psswd = encode_psswd(psswd)
            # Put the user in the database
            self.speed_db["Users"].insert_one(
                {
                    "UID": uid,
                    "Name": name,
                    "Username": username,
                    "Email": email,
                    "Phone_no": phone_no,
                    "Password": psswd
                }
            )
                
            return True
        
    
    def get_plates_from_mongo(self) :
        all_plates = list(self.speed_db["Traffic_violation"].find({}, {"_id": 0}))
        return all_plates