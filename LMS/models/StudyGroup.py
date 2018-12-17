import datetime
from . import db
from marshmallow import fields, Schema
from .UserModel import UserSchema
from .x import course_x_group
from .StudyCourse import StudyCourseShema



class StudyGroup(db.Model):
    __tablename__ = 'study_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    department_title = db.Column(db.String(128), nullable=False)
    course_number = db.Column(db.Integer, nullable=False)
    users = db.relationship('UserModel', backref='study_groups', lazy=True)
    study_course = db.relationship('StudyCourse', secondary=course_x_group, backref='study_group',lazy=True)

    def __init__(self, data):
        self.name = data.get('name')
        self.department_title = data.get('department_title')
        self.course_number = data.get('course_number')

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

  
    @staticmethod
    def get_one_group(id):
        return StudyGroup.query.get(id)
    
    @staticmethod
    def get_all_students(id):
        return StudyGroup.query.get(id).users
    
    @staticmethod
    def get_all_courses(id):
        return StudyGroup.query.get(id).study_course

    def __repr__(self):
        return '<id {}>'.format(self.id)
    

class StudyGroupShema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    department_title = fields.Str(required=True)
    course_number = fields.Int(required=True)
    users = fields.Nested(UserSchema, many=True)
    study_courses = fields.Nested(StudyCourseShema, many=True)
    
#     class Meta:
#         fields = ('id', 'name', 'department_title', 'course_number')
    
