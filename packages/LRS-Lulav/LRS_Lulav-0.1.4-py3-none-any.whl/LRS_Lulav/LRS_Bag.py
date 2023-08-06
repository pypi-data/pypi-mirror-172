from collections.abc import MutableMapping
from rosidl_runtime_py.convert import get_message_slot_types, message_to_yaml, message_to_csv, message_to_ordereddict
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import numpy as np
import pymongo
import sqlite3
import yaml
import json


class LRS_Bag():
    def __init__(self, path_to_bags, mongo_connection_string, db_name, collection_name, instance_id):
        self.instance_id = instance_id
        self.bags = path_to_bags
     
        self.mymongo = pymongo.MongoClient(mongo_connection_string)
        self.mydb = self.mymongo[db_name]
        self.mycol = self.mydb[collection_name]
        # dblist = self.mymongo.list_database_names()                

    def _flatten_dict(self, d: MutableMapping, parent_key: str = '', sep: str ='.') -> MutableMapping:
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def upload_bag_to_server(self):
        # TODO: upload bag to server (bucket)
        # TODO: upload the metadata of the bag
        pass
    
    def fill_mongo(self):
        # TODO: upload the metadata.yaml of the bag to DB
        for bag in self.bags:            
            metadata_path = "/".join(bag.split("/")[:-1]) +"/metadata.yaml"                                   
            with open(metadata_path, 'r') as file:                                     
                metadata_dict = yaml.load(file) 
                self.mycol.insert_one({
                    "instance_id": self.instance_id,
                    "metadata": metadata_dict
                })                                                     
                
            self.conn = sqlite3.connect(bag)
            self.cursor = self.conn.cursor()

            topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
            self.topics = {name_of:{'type':type_of, 'id':id_of, 'message':get_message(type_of) } for id_of,name_of,type_of in topics_data}

            # simulation_name = bag.split("/")[-1].replace(".", "_")

            for topic_name in self.topics.keys():
                rows = self.cursor.execute(f"select id, timestamp, data from messages where topic_id = {self.topics[topic_name]['id']}").fetchall()
                my_list = []
                for id, timestamp, data in rows:

                    d_data = deserialize_message(data, self.topics[topic_name]["message"])
                    msg_dict = message_to_ordereddict(d_data)
                    row = {
                        "instance_id": self.instance_id,
                        "bag": bag,
                        "id": id, # Ros id 
                        "timestamp": timestamp, # ros timestamp
                        "topic_name": topic_name,
                        "data": msg_dict
                    }
                    my_list.append(row)
                    
                if len(my_list) == 0:
                    continue
                # print("[LOG]:", json.dumps(my_list, indent=2, default=str))        
                self.mycol.insert_many(my_list)
                print(f"Done updating {topic_name} topic for {bag}")
                    
                    
# Test
def main():
    path_to_bags = ['tmp/bag/bag_0.db3']
    bagparser = LRS_Bag(path_to_bags, "mongodb://localhost:27017/", "simulations", "simulation_4")
    bagparser.fill_mongo()

    print("Done")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)




