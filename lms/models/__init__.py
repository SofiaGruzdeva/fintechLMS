from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .UserModel import user_model, UserSchema
from .StudyGroup import study_group, StudyGroupShema
from .StudyCourse import study_course, StudyCourseShema
