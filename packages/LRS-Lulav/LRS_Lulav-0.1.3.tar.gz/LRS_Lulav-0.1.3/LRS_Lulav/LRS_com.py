import pymongo
import redis
from multiprocessing import Pool, Process
import json
import time

#
# MONGO
# 
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB = 'vertical_descent'
MONGO_COLLECTION = 'test_collection_v1'
#
# REDIS
#
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 5


class LRS_com():
    def __init__(self, user_id, project_id, simulation_id, instance_id): 
        # print("__init__") 
        self.user_id = user_id
        self.project_id = project_id
        self.simulation_id = simulation_id
        self.instance_id = instance_id
              
        #
        # MONGO
        # 
        self.mymongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        self.mydb = self.mymongo[MONGO_DB]
        self.mycol = self.mydb[MONGO_COLLECTION]
        # dblist = self.mymongo.list_database_names() 
        
        #
        # REDIS
        #         
        self.red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        
        #
        # PROCCESS
        #
        self.p_events = Process(target=self._run_events)
        self.p_logs = Process(target=self._run_logs)
        self.run()
    
    def __del__(self):
        self.p_events.kill()
        self.p_events.join()
        self.p_logs.kill()
        self.p_logs.join()              
    
    def _upload_event(self, event):
        # TODO: update to mongo
        print(event)
        pass
    
    def _upload_log(self, log):
        # TODO: update to mongo
        print(log)
        pass
    
    def run(self):        
        self.p_events.start()        
        self.p_logs.start()                  
    
    def _run_events(self):
        while(True):
            while(self.red.llen(f"event_{self.user_id}") > 0):
                event = self.red.lpop(f"event_{self.user_id}")                               
                self._upload_event(json.loads(event))
            time.sleep(0.1)
                
    def _run_logs(self):
        while(True):
            while(self.red.llen(f"log_{self.user_id}") > 0):
                log = self.red.lpop(f"log_{self.user_id}")                
                self._upload_event(json.loads(log))
            time.sleep(0.1)
                
    def send_event(self, message):    
        data = json.dumps({
            "user_id": self.user_id,
            "project_id": self.project_id,
            "simulation_id": self.simulation_id,
            "instance_id": self.instance_id,
            "message": message           
        })           
        self.red.rpush(f"event_{self.user_id}", data)        
    
    def send_log(self, log):
        data = json.dumps({            
            "user_id": self.user_id,
            "project_id": self.project_id,
            "simulation_id": self.simulation_id,
            "instance_id": self.instance_id,
            "log": log           
        })
        self.red.rpush(f"log_{self.user_id}", data)  
        
    def update_simulation_instance_status(self, status):
        
        pass
    
    def add_message_simulation_instance(self, message):
        
        pass
        
        
# --------------------------------------------------
def main():
    lrs = LRS_com('vova', 'p1', 's1', 'i1')
    
    lrs.send_event("vova event1")
    lrs.send_log("vova event1")

if __name__ == '__main__':
    main()