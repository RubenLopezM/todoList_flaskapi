from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__:'user'
    id = db.Column(db.Integer, primary_key=True)
    children = relationship("Task", backref="parent")
    name = db.Column(db.String(120), unique=False, nullable=False)
    is_active= db.Column(db.Boolean(),unique=False, nullable=False)
    

    def __repr__(self):
        return f'User is {self.name}, id:{self.id}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    

    @classmethod
    def get_byid(cls,id_user):
        user= cls.query.filter_by(id=id_user).one_or_none()
        return user
    

    @classmethod
    def get_all(cls):
        users= cls.query.all()
        return users


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


    def delete(self):
        self.is_active=False
        db.session.commit()
        return self

    
        
class Task(db.Model):
    __tablename__:'task'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), unique=False, nullable=False)
    done = db.Column(db.Boolean(),unique=False, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    

    def __repr__(self):
        return f'The task is {self.text}, id:{self.id}'

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "done":self.done
            # do not serialize the password, its a security breach
        }
    
    @classmethod
    def get_byuser(cls,user_id):
        tasks= cls.query.filter_by(user_id=user_id)
        return tasks
    

    @classmethod
    def gettask_id(cls,task_id):
        task=cls.query.get(task_id)
        return task

    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    
    def delete(self):
        self.done=True
        db.session.commit()
        return self
    

    