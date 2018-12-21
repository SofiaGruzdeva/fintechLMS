from . import db

course_x_group = db.Table(
    'course_x_group',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('study_courses._id')),
    db.Column('group_id', db.Integer, db.ForeignKey('study_groups._id')))


teacher_x_course = db.Table(
    'teacher_x_course',
    db.Column('teacher_id',
              db.Integer,
              db.ForeignKey('users._id'),
              primary_key=True),
    db.Column('course_id', db.Integer,
              db.ForeignKey('study_courses._id'),
              primary_key=True))
