from app.database.models.user import UserModel
from run import db


class MentorshipRelationModel(db.Model):
    # Specifying database table used for MentorshipRelationModel
    __tablename__ = 'mentorship_relations'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # personal data
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    mentor = db.relationship(UserModel,
                             backref='mentor_relations',
                             primaryjoin="MentorshipRelationModel.mentor_id == UserModel.id")
    mentee = db.relationship(UserModel,
                             backref='mentee_relations',
                             primaryjoin="MentorshipRelationModel.mentee_id == UserModel.id")

    init_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.String(400))

    def __init__(self, sender_id, receiver_id, mentor_user, mentee_user, init_date, end_date, notes):

        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.mentor = mentor_user
        self.mentee = mentee_user  # same as mentee_user.mentee_relations.append(self)
        self.init_date = init_date
        self.end_date = end_date
        self.notes = notes

    def json(self):
        return {
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'mentor_id': self.mentor_id,
            'mentee_id': self.mentee_id,
            'init_date': str(self.init_date),
            'end_date': str(self.end_date),
            'notes': self.notes
        }

    def __repr__(self):
        return "Mentorship Relation with id = %s, Mentor has id = %s and Mentee has id = %d" \
               % (self.id, self.mentor_id, self.mentee_id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_empty(cls):
        return cls.query.first() is None

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
