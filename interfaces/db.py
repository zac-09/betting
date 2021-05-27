from abc import ABC, abstractclassmethod

class DB(ABC):
    @abstractclassmethod
    def connect():
        raise NotImplementedError

    @abstractclassmethod
    def insert():
        raise NotImplementedError

    @abstractclassmethod
    def update():
        raise NotImplementedError

    @abstractclassmethod
    def get():
        raise NotImplementedError
    @abstractclassmethod
    def delete():
        raise NotImplementedError
 