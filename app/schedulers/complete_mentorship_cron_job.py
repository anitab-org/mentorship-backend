from datetime import datetime


def complete_overdue_mentorship_relations_job():
    """
    This function iterates of all the mentorship requests and
    checks if the end date of the relation has passed the current date
    and is in the ACCEPTED state
    if True then marks the relation as COMPLETED, if False does nothing
    """
    from run import application
    with application.app_context():
        from app.utils.enum_utils import MentorshipRelationState
        from app.database.models.mentorship_relation import MentorshipRelationModel
        all_relations = MentorshipRelationModel.query.all()

        current_date_timestamp = datetime.now().timestamp()

        for relation in all_relations:

            if relation.state is MentorshipRelationState.ACCEPTED and relation.end_date < current_date_timestamp:
                relation.state = MentorshipRelationState.COMPLETED
                relation.save_to_db()

            # for tests purposes
            # print('{} | hola hola hola hola hola'.format(datetime.now()))
