import argparse
from this import d

from pkg_resources import Distribution
from soupsieve import match
from bson.objectid import ObjectId
import pymongo
import redis
import yaml
import json
from pathlib import Path

#
# MONGO
# 
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB = 'LRS'
MONGO_USERS_COLLECTION = 'users'
MONGO_PROJECTS_COLLECTION = 'projects'
MONGO_SIMULATIONS_COLLECTION = 'simulations'


class LRS_params():
    def __init__(self, user_id, project_id, simulation_id, simulation_run_id, simulation_instance_id):
        #
        # MONGO
        # 
        self.mymongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        self.mydb = self.mymongo[MONGO_DB]
        
        self.col_users = self.mydb[MONGO_USERS_COLLECTION]
        self.col_projects = self.mydb[MONGO_PROJECTS_COLLECTION]
        self.col_simulations = self.mydb[MONGO_SIMULATIONS_COLLECTION]
        # dblist = self.mymongo.list_database_names() 
        
        # get data
        self.user_id = user_id
        self.project_id = project_id   
        self.simulation_id = simulation_id    
        self.simulation_run_id = simulation_run_id
        self.simulation_instance_id = simulation_instance_id
        self.user = self._get_user()
        self.project = self._get_project()    
        self.simulation = self._get_simulation()

    def _get_user(self):        
        user = self.col_users.find_one({"_id": ObjectId(self.user_id)})                
        return user
    
    def _get_project(self):        
        project = self.col_projects.find_one({ 
            "user_id": ObjectId(self.user_id), 
            "_id": ObjectId(self.project_id)
        })        
        return project
    
    def _get_simulation(self):        
        simulation = self.col_simulations.find_one({"_id": ObjectId(self.simulation_id)})                
        return simulation
        
    def _eval_distribution(self, dist: Distribution):    
        import numpy as np
        
        if dist["type"] == "normal":                            
            return np.random.normal(dist["params"][0]["value"], dist["params"][1]["value"])
        
        if dist["type"] == "normal":                            
            return np.random.exponential(dist["params"][0]["value"])
        
        if dist["type"] == "laplace":                 
            return np.random.laplace(dist["params"][0]["value"], dist["params"][1]["value"])
        
        if dist["type"] == "poisson":                            
            return np.random.poisson(dist["params"][0]["value"])
        
        if dist["type"] == "power":                            
            return np.random.power(dist["params"][0]["value"])
                
        if dist["type"] == "laplace":                 
            return np.random.uniform(dist["params"][0]["value"], dist["params"][1]["value"])
           
        if dist["type"] == "zipf":                            
            return np.random.zipf(dist["params"][0]["value"])   
        
        if dist["type"] == "vonmises":                 
            return np.random.vonmises(dist["params"][0]["value"], dist["params"][1]["value"])
          
        if dist["type"] == "rayleigh":                            
            return np.random.rayleigh(dist["params"][0]["value"])   
        
        if dist["type"] == "const":                            
            return dist["params"][0]["value"]
        
        if dist["type"] == "string":                            
            return dist["params"][0]["value"]
                                    
        raise f"Error: {dist['type']} is not supported."        
        
    def init_params(self):
        config = {}        
        initFile = [ini for ini in self.project["projectInitFiles"] if ini["_id"] == self.simulation["init_file_id"]][0]                
        paramSettings = {} 
        for ps in initFile["parameterSettings"]:            
            ps["value"] = self._eval_distribution(ps["distribution"])            
            paramSettings[str(ps["param_id"])] = ps                   
        
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
                
        for package_name, val in config.items():
            # params.yaml
            # Path("vova").mkdir(parents=True, exist_ok=True)
            path = f"install/{package_name}/share/{package_name}/config/"
            Path(path).mkdir(parents=True, exist_ok=True)
            path = path + "params.yaml"
            
            with open(path, 'w') as file:                                     
                yaml.dump(val, file)           
        
        print(f" ----- uploading to {self.simulation_id}_{self.simulation_run_id}")
        
        db = self.mymongo["simulations"]
        col = db[f"{self.simulation_id}_{self.simulation_run_id}"]
        
        col.update_one({
                "type": "metadata",
                "simulation_id": self.simulation_id,
                "simulation_run_id": self.simulation_run_id,
                "simulation_instance_id": self.simulation_instance_id,
            },
            { 
                "$set":{
                    "type": "metadata",
                    "simulation_id": self.simulation_id,
                    "simulation_run_id": self.simulation_run_id,
                    "simulation_instance_id": self.simulation_instance_id,                                
                    "paramSettings": paramSettings,
                    "config": config,                    
                }
            },
            upsert=True
        )    
       