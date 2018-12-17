from flask_sqlalchemy import SQLAlchemy

# initialize our db
db = SQLAlchemy()


from .UserModel import UserModel, UserSchema
from .StudyGroup import StudyGroup, StudyGroupShema
from .StudyCourse import StudyCourse, StudyCourseShema