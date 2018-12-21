from marshmallow import fields, Schema
from . import db
from .x import teacher_x_course
from .db_class_base import db_class_base


class user_model(db.Model, db_class_base):

    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    study_group_id = db.Column(db.Integer,
                               db.ForeignKey('study_groups._id'),
                               nullable=True)
    degree = db.Column(db.String(128), nullable=True)
    form_of_study = db.Column(db.String(128), nullable=True)
    learning_base = db.Column(db.String(128), nullable=True)
    type_of_user = db.Column(db.String(128), nullable=False)
    study_course_id = db.relationship('study_course',
                                      secondary=teacher_x_course,
                                      backref='users', lazy=True)

    def __init__(self, data, login):
        self.name = data.get('name')
        self.login = login
        self.password = data.get('password')
        self.study_group_id = data.get('study_group_id')
        self.degree = data.get('degree')
        self.form_of_study = data.get('form_of_study')
        self.learning_base = data.get('learning_base')
        self.type_of_user = data.get('type_of_user')

    @staticmethod
    def get_all_users():
        return user_model.query.all()

    @staticmethod
    def get_one_user(_id):
        return user_model.query.get(_id)

    def __repr(self):
        return '<_id {}>'.format(self._id)

    @staticmethod
    def get_user_by_login(f_log):
        return user_model.query.filter(user_model.login == f_log).first()


class UserSchema(Schema):
    _id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True)
    study_group_id = fields.Int(required=False)
    degree = fields.Str(required=False)
    form_of_study = fields.Str(required=False)
    learning_base = fields.Str(required=False)
    type_of_user = fields.Str(required=True)
