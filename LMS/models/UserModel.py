from marshmallow import fields, Schema
import datetime
from . import db
# from .StudyGroup import StudyGroupShema
from .x import teacher_x_course

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    study_group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=True)
    degree = db.Column(db.String(128), nullable=True)
    form_of_study = db.Column(db.String(128), nullable=True)
    learning_base = db.Column(db.String(128), nullable=True)
    type_of_user = db.Column(db.String(128), nullable=False)
    study_course_id = db.relationship('StudyCourse', secondary=teacher_x_course, backref='users', lazy=True)


    def __init__(self, data, login):
        self.name = data.get('name')
        self.login = login
        self.password = data.get('password')
        self.study_group_id = data.get('study_group_id')
        self.degree = data.get('degree')
        self.form_of_study = data.get('form_of_study')
        self.learning_base = data.get('learning_base')
        self.type_of_user = data.get('type_of_user')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    
#     def get_role(self, id):
#         user = UserModel.query.get(id)
#         return user.

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

  
    def __repr(self):
        return '<id {}>'.format(self.id)

    def get_user_by_login(v):
        return UserModel.query.filter(UserModel.login == v).first()
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True)
    study_group_id = fields.Int(required=False)
    degree = fields.Str(required=False)
    form_of_study = fields.Str(required=False)
    learning_base = fields.Str(required=False)
    type_of_user = fields.Str(required=True)
    