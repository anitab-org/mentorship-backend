from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState


class MentorshipRelationModel(db.Model):
    """ Create a Mentorship Relational Model """

    # Specifying database table used for MentorshipRelationModel
    __tablename__ = 'mentorship_relations'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # personal data
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action_user_id = db.Column(db.Integer, nullable=False)
    mentor = db.relationship(UserModel,
                             backref='mentor_relations',
                             primaryjoin="MentorshipRelationModel.mentor_id == UserModel.id")
    mentee = db.relationship(UserModel,
                             backref='mentee_relations',
                             primaryjoin="MentorshipRelationModel.mentee_id == UserModel.id")

    creation_date = db.Column(db.Float, nullable=False)
    accept_date = db.Column(db.Float)
    start_date = db.Column(db.Float)
    end_date = db.Column(db.Float)

    state = db.Column(db.Enum(MentorshipRelationState), nullable=False)
    notes = db.Column(db.String(400))

    tasks_list_id = db.Column(db.Integer, db.ForeignKey('tasks_list.id'))
    tasks_list = db.relationship(TasksListModel, uselist=False, backref="mentorship_relation")

    def __init__(self, action_user_id, mentor_user, mentee_user, creation_date, end_date, state, notes, tasks_list):

        self.action_user_id = action_user_id
        self.mentor = mentor_user
        self.mentee = mentee_user  # same as mentee_user.mentee_relations.append(self)
        self.creation_date = creation_date
        self.end_date = end_date
        self.state = state
        self.notes = notes
        self.tasks_list = tasks_list

    def json(self):
        """ 
            Get information of mentorship as a json file
            Args:
            
            Returns:
            The information of mentorship as a json file.
        """
        return {
            'id': self.id,
            'action_user_id': self.action_user_id,
            'mentor_id': self.mentor_id,
            'mentee_id': self.mentee_id,
            'creation_date': self.creation_date,
            'accept_date': self.accept_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'state': self.state,
            'notes': self.notes
        }

    # def __repr__(self):
    #     return "Mentorship Relation with id = %s, Mentor has id = %s and Mentee has id = %d" \
    #            % (self.id, self.mentor_id, self.mentee_id)

    @classmethod
    def find_by_id(cls, _id):
        """ 
            Find name of person with given id.
            Args:
            _id: The id of a person.
            Returns:
            the name of the person with the given id.
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_empty(cls):
        """ 
            Find if the database if empty or not.
            Args:
            
            Returns:
            True if the database if empty and false if it is not.
        """
        return cls.query.first() is None

    def save_to_db(self):
        """ 
            .
            Args:
            
            Returns:
            
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ 
            Delete a person from the database.
            Args:
            
            Returns:
            
        """
        self.tasks_list.delete_from_db()
        db.session.delete(self)
        db.session.commit()
