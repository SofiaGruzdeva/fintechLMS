from . import db


class db_class_base():
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self._id

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    