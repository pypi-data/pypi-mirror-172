import argparse

from pkg_resources import Distribution
from LRS_com import LRS_com
from bson.objectid import ObjectId
import pymongo
import redis
import yaml
import json
from pathlib import Path

#
# MONGO
# 
# MONGO_CONNECTION_STRING = "mongodb://192.168.50.170:27017/"
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB = 'LRS'
MONGO_USERS_COLLECTION = 'users'
MONGO_PROJECTS_COLLECTION = 'projects'
MONGO_SIMULATIONS_COLLECTION = 'simulations'
#
# REDIS
#
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 5


class LRS_agent():
    def __init__(self, user_id, project_id, simulation_id, simulation_instance_id):   
        self._send_log("+++++++++++++++++++++++++++++++++++++++++")                  
        self.com = LRS_com(user_id, project_id, simulation_id, simulation_instance_id)
        
        self.user_id = user_id                
        self.project_id = project_id                
        self.simulation_id = simulation_id                
        self.simulation_instance_id = simulation_instance_id        
                        
        #
        # MONGO
        # 
        self.mymongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        self.mydb = self.mymongo[MONGO_DB]
        
        self.col_users = self.mydb[MONGO_USERS_COLLECTION]
        self.col_projects = self.mydb[MONGO_PROJECTS_COLLECTION]
        self.col_simulations = self.mydb[MONGO_SIMULATIONS_COLLECTION]
        # dblist = self.mymongo.list_database_names() 
        
        #
        # REDIS
        #         
        self.red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        
        # get data
        self.user = self._get_user()
        self.project = self._get_project()
        self.simulation = self._get_simulation()
        self.simulation_instance = self._get_simulation_instance()
        self._send_log("------------------------------------------")
        
    def __del__(self):
        self._send_event("LRS_agent Terminating: [{self.user_id}],[{self.project_id}],[{self.simulation_id}],[{self.simulation_instance_id}].")
        self._update_simulation_instance_status("done")
        # TODO: send event to DB 
        # TODO: update state of instance        
        pass
    
    def _get_user(self):
        self._send_event(f" + LRS_agent getting user [{self.user_id}]...")        
        user = self.col_users.find_one({"_id": ObjectId(self.user_id)})
        # self._send_log("user", user)
        self._send_event(f" - LRS_agent getting user [{user['username']}] Done.")     
        return user
    
    def _get_project(self):
        self._send_event(f" + LRS_agent getting project [{self.project_id}]...")
        project = self.col_projects.find_one({ 
            "user_id": ObjectId(self.user_id), 
            "_id": ObjectId(self.project_id)
        })
        # self._send_log("project", project)
        self._send_event(f" - LRS_agent getting project [{project['name']}] Done.")
        return project
    
    def _get_simulation(self):
        self._send_event(f" + LRS_agent getting simulation [{self.simulation_id}]...")
        simulation = self.col_simulations.find_one({"_id": ObjectId(self.simulation_id)})
        self._send_event(f" - LRS_agent getting simulation [{simulation['name']}] Done.")
        # self._send_log("simulation", simulation)
        return simulation
    
    def _get_simulation_instance(self):
        self._send_event(f" + LRS_agent getting instance [{self.simulation_instance_id}]...")                
        inst = [inst for inst in self.simulation["instances"] if inst["_id"] == ObjectId(self.simulation_instance_id) ][0]
        # self._send_log(inst)
        self._send_event(f" - LRS_agent getting instance triggered by [{inst['trigger']}] Done.")
        return inst
    
    def _send_event(self, event):
        # self.com.send_event(event)  
        # for arg in args:
        # TODO: implement
        self._send_log("[EVENT]" +  event)        
          
    def _send_log(self, *args):
        # TODO: implement
        # self.com.send_log(log)        
        for arg in args:   
            if type(arg) is str:
                print("[LOG]:", arg)                     
            else:
                print("[LOG]:", json.dumps(arg, indent=2, default=str))        
        
    def _update_simulation_instance_status(self, status):  
        self._send_log("[IMPLEMENT] implement _update_simulation_instance_status:")              
        # TODO
        # self._send_log(f"Updating {status} for simulation instance")
        
    def _add_simulation_instance_message(self):
        self._send_log("[IMPLEMENT] implement _add_simulation_instance_message:")
        # TODO
        # raise "not implemented"        
    
    def _eval_distribution(self, dist: Distribution):
        # TODO
        self._send_log("--- implement: _eval_distribution")  
        
        # TODO: remove Temp - no eval 
        value = dist["params"][0]["value"]
        self._send_log("_eval_distribution: ", value)
        return value
        
    def init_params(self):
        self._send_log("+++++++++++++++++++++++++++++++++++++++++")
        self._send_event(" + LRS_agent init_params")
        self._update_simulation_instance_status("initializing")
        
        config = {}
        self._send_log("------------")
        initFile = [ini for ini in self.project["projectInitFiles"] if ini["_id"] == self.simulation["init_file_id"]][0]                
        paramSettings = {} 
        for ps in initFile["parameterSettings"]:            
            ps["value"] = self._eval_distribution(ps["distribution"])            
            paramSettings[str(ps["param_id"])] = ps                   
        self._send_log("paramSettings", paramSettings)    
        self._send_log("------------")
        self._send_log("parameters: ")
        
        for package in self.project["packages"]:            
            config[package["name"]] = {}
            for node in package["nodes"]:                
                config[package["name"]][node["name"]] = {
                    "ros__parameters": {}
                }
                for parameter in node["parameters"]:                    
                    value = parameter['value']
                    paramSetting = paramSettings.get(str(parameter["_id"]))
                    if paramSetting:
                        value = paramSetting["value"]
                    config[package["name"]][node["name"]]["ros__parameters"][parameter['name']] = value                    
        self._send_log("------------")
        self._send_log("config:", config)
                
        for package_name, val  in config.items():
            # params.yaml
            # Path("vova").mkdir(parents=True, exist_ok=True)
            path = f"install/{package_name}/share/{package_name}/config/"
            Path(path).mkdir(parents=True, exist_ok=True)
            path = path + "params.yaml"
            
            with open(path, 'w') as file:                                     
                yaml.dump(val, file)     
        self._send_log("done writing config files")        
                                   
        # self._send_event("config", config) # TODO: check if ok 
                
        self._send_event(" - LRS_agent init_params done.")
        self._send_log("------------------------------------------")
        pass
    
    def run_simulation(self):
        self._send_log("+++++++++++++++++++++++++++++++++++++++++")
        self._send_event(" + LRS_agent run init_params")
        self._update_simulation_instance_status("running")
        # TODO: run command ros2 run path to launch 
        # TODO: send event to DB 
        # TODO: update state of instance
        self._send_event(" - LRS_agent done running init_params")
        self._send_log("------------------------------------------")
        pass
    
    def upload_bag(self):
        self._send_log("+++++++++++++++++++++++++++++++++++++++++")
        self._send_event(" + LRS_agent uploading bag")
        self._update_simulation_instance_status("uploading")
        # TODO: update bag to DB
        # TODO: send event to DB 
        # TODO: update state of instance
        self._send_event(" - LRS_agent done uploading bag")
        self._send_log("------------------------------------------")
        pass
    
    def run(self):
        self.init_params()
        self.run_simulation()
        self.upload_bag()


def main(args):    
    lrs = LRS_agent(args.user_id, args.project_id, args.simulation_id, args.simulation_instance_id)
    lrs.run()    

description = '''
    LRS agent to run inside a docker. 
    The LRS agent should manage the lifecycle of the simulator.     
    ----------------------------------------------------------------     
     - Fill configuration/parameters files for the nodes 
     - Launch the correct ROS2 launch file.
     - Upload BAG to DB after simulation ends / RT
     - 
     - Send system monitoring events to DB. (Stage 3)
     - Send simulation events to DB. (Stage 3)
     - Send Logs to DB.(Stage 3)

    Stage 3:
        - Send RT statistics about the system while running the simulation  
        - Send RT events to DB about the ROS2 state
        - Send Logs to DB.
    ----------------------------------------------------------------
    
    Examples
    --------

    python LRS_manager/LRS_agent.py 63502ab7865fb52ab569e90c 6351584232818a188f45fd59 63523680846b4ecaf0404d00 635236a7846b4ecaf0404d01 
'''
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description)
    parser.add_argument('user_id', type=str, help='user id')
    parser.add_argument('project_id', type=str, help='project id')
    parser.add_argument('simulation_id', type=str, help='simulation id')
    parser.add_argument('simulation_instance_id', type=str, help='simulation instance id')
    args = parser.parse_args()

    main(args)
