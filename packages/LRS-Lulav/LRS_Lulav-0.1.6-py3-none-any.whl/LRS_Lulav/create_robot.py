import pymongo
from bson import ObjectId

class LRS_robot_maker():    
    def __init__(self, project_id, launch_name, init_file_name, ):
        
        self.project_id = project_id        
        self.launch_name = launch_name
        
        
        self.init_file_name = init_file_name
        
        # MONGODB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["LRS"]        
        self.col_projects = self.db["projects"]
        self.col_users = self.db["users"]      
        
        self.project = self.col_projects.find_one({
            "_id": ObjectId(self.project_id)
        })
    
    def create_docker(self):
        print(f"Creating Docker")
        
        # return path to docker 
        pass
    
    def build_docker_image(self, docker_path):
        print(f"Building Docker [{docker_path}]")
        
        # return built docker path
        pass
    
    def push_container(self, container_path):
        print(f"Uploading container [{container_path}]")
        # upload docker to dockerhub 
        
        # return the url of the container 
        pass 
    
    def run(self):
        docker_path = self.create_docker()
        container_path = self.build_docker_image(docker_path)
        return self.push_container(container_path)
        
       
    
    
    

def main():
    print(" + LRS_robot_maker.")
    rm = LRS_robot_maker(
        '633fbf8ba57f591861918a9f',
        'demo.launch',
        'first',
        'util/lulav/dockers/ros2docker'
    )
    rm.run()
    print(" - LRS_robot_maker.")
    
if __name__ == "__main__":
    main()

# TODO: check this out. 
# https://github.com/athackst/dockerfiles