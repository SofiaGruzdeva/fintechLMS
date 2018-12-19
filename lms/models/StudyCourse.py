from marshmallow import fields, Schema
from . import db
from .x import course_x_group, teacher_x_course


class study_course(db.Model):
    __tablename__ = 'study_courses'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    study_groups = db.relationship(
        'study_group',
        secondary=course_x_group,
        lazy=True)
    teacher = db.relationship(
        'user_model',
        secondary=teacher_x_course,
        backref='study_courses',
        lazy=True)

    def __init__(self, data):
        self.name = data.get('name')
        self.description = data.get('description')

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

    def add_group(self, group):
        self.study_group.append(group)
        db.session.commit()

    def add_teacher(self, teacher):
        self.teacher.append(teacher)
        db.session.commit()

    @staticmethod
    def get_one_course(_id):
        return study_course.query.get(_id)

    def __repr__(self):
        return '<_id {}>'.format(self._id)


class StudyCourseShema(Schema):
    _id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
