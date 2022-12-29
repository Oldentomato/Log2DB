from pymongo import MongoClient
from dataclasses import dataclass


@dataclass
class SetMongoDB:
    db_username : str
    db_password: str
    db_cluster_name : str
    db_document_name : str
    db_collection_name : str
    port : int

    def Connect_DB(self) -> object:
        #self.__변수명 : 비공개 속성
        self.__mongo_url = "mongodb+srv://"+self.db_username+":"+self.db_password+"@"+self.db_cluster_name+".g7o5t.mongodb.net/?retryWrites=true&w=majority"
        try:
            client = MongoClient(host = self.__mongo_url, port = self.port)
        except:
            print("Faild to Connection")
            return None
        else:
            db = client[self.db_document_name]
            collection = db[self.db_collection_name]
            return collection

