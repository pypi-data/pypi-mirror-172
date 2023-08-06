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


class LRS_util():
    def __init__(self):
        #
        # MONGO
        # 
        self.mymongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        self.mydb = self.mymongo[MONGO_DB]
        
        self.col_users = self.mydb[MONGO_USERS_COLLECTION]
        self.col_projects = self.mydb[MONGO_PROJECTS_COLLECTION]
        self.col_simulations = self.mydb[MONGO_SIMULATIONS_COLLECTION]
        # dblist = self.mymongo.list_database_names() 

    def get_user(self, user_id):        
        user = self.col_users.find_one({"_id": ObjectId(user_id)})                
        return user
    
    def get_project(self, user_id, project_id):        
        project = self.col_projects.find_one({ 
            "user_id": ObjectId(user_id), 
            "_id": ObjectId(project_id)
        })        
        return project
    
    def get_simulation(self, simulation_id):        
        simulation = self.col_simulations.find_one({"_id": ObjectId(simulation_id)})                
        return simulation

    def get_launch_file(self, user_id, project_id, launch_id):     
        # print("user_id, project_id, launch_id", user_id, project_id, launch_id);        
        project = self.get_project( user_id, project_id)
        # print(project)
                        
        for l in project["launches"]:
            if l["_id"] == launch_id:
                # print("found in launches")
                return None, l                  
                
        for p in project["packages"]:
            for l in p["launches"]:
                if l["_id"] == launch_id:
                    # print("found in packages launches")
                    return p, l   
                
        return None, None        
        
   
   