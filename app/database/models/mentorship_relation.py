from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from app.utils.enum_utils import MentorshipRelationState


class MentorshipRelationModel(DB.Model):
    # Specifying database table used for MentorshipRelationModel
    # pylint: disable=too-many-arguments,too-many-instance-attributes
    __tablename__ = "mentorship_relations"
    __table_args__ = {"extend_existing": True}

    id = DB.Column(DB.Integer, primary_key=True)

    # personal data
    mentor_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    mentee_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    action_user_id = DB.Column(DB.Integer, nullable=False)
    mentor = DB.relationship(
        UserModel,
        backref="mentor_relations",
        primaryjoin="MentorshipRelationModel.mentor_id == UserModel.id",
    )
    mentee = DB.relationship(
        UserModel,
        backref="mentee_relations",
        primaryjoin="MentorshipRelationModel.mentee_id == UserModel.id",
    )

    creation_date = DB.Column(DB.Float, nullable=False)
    accept_date = DB.Column(DB.Float)
    start_date = DB.Column(DB.Float)
    end_date = DB.Column(DB.Float)

    state = DB.Column(DB.Enum(MentorshipRelationState), nullable=False)
    notes = DB.Column(DB.String(400))

    tasks_list_id = DB.Column(DB.Integer, DB.ForeignKey("tasks_list.id"))
    tasks_list = DB.relationship(
        TasksListModel, uselist=False, backref="mentorship_relation"
    )

    def __init__(
            self,
            action_user_id,
            mentor_user,
            mentee_user,
            creation_date,
            end_date,
            state,
            notes,
            tasks_list,
    ):

        self.action_user_id = action_user_id
        self.mentor = mentor_user
        self.mentee = (
            mentee_user
        )  # same as mentee_user.mentee_relations.append(self)
        self.creation_date = creation_date
        self.end_date = end_date
        self.state = state
        self.notes = notes
        self.tasks_list = tasks_list

    def json(self):
        return {
            "id": self.id,
            "action_user_id": self.action_user_id,
            "mentor_id": self.mentor_id,
            "mentee_id": self.mentee_id,
            "creation_date": self.creation_date,
            "accept_date": self.accept_date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "state": self.state,
            "notes": self.notes,
        }

    # def __repr__(self):
    #     return "Mentorship Relation with id = %s, " \
    #            "Mentor has id = %s and Mentee has id = %d" \
    #            % (self.id, self.mentor_id, self.mentee_id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_empty(cls):
        return cls.query.first() is None

    def save_to_db(self):
        DB.session.add(self)
        DB.session.commit()

    def delete_from_db(self):
        self.tasks_list.delete_from_db()
        DB.session.delete(self)
        DB.session.commit()
