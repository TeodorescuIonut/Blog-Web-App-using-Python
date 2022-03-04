
from services.post_db_repo import PostDbRepo
from services.post_repo import PostRepo
from services.post_repository_interface import IPostRepository

class Container:
    services_memory = {
    IPostRepository: PostRepo(),   
    }
    services_production = {
    IPostRepository: PostDbRepo(),    
    }
