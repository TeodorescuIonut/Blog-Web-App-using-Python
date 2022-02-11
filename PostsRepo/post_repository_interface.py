import abc
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())



class IPostRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_all') and
                callable(subclass.get_all) and
                hasattr(subclass, 'get_by_id') and
                callable(subclass.get_by_id) and
                hasattr(subclass, 'create') and
                callable(subclass.create) and
                hasattr(subclass, 'update') and
                callable(subclass.update) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete) and
                hasattr(subclass, 'get_previews') and
                callable(subclass.get_previews) and
                hasattr(subclass, 'create_preview') and
                callable(subclass.create_preview))
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, post_id):
        raise NotImplementedError
    @abc.abstractmethod
    def create(self, post):
        raise NotImplementedError

    @abc.abstractmethod    
    def update(self, post):
        raise NotImplementedError

    @abc.abstractmethod 
    def delete(self, post):
        raise NotImplementedError
    def get_previews(self):
        raise NotImplementedError
    def create_preview(self,post):
        raise NotImplementedError
    
    

