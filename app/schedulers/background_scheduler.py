from apscheduler.schedulers.background import BackgroundScheduler
from app.schedulers.complete_mentorship_cron_job import \
    complete_overdue_mentorship_relations_job


def init_scheduler():
    scheduler = BackgroundScheduler()

    # This cron job runs every day at 23:59h
    # Purpose: complete overdue accepted mentorship relations
    scheduler.add_job(id='complete_mentorship_relations_cron',
                      func=complete_overdue_mentorship_relations_job,
                      trigger='cron', hour=23, minute=59, second=0, day='*',
                      timezone='Etc/UTC',
                      replace_existing=True)

    # for tests purposes
    # scheduler.add_job(id='complete_mentorship_relations_cron',
    #                   func=complete_overdue_mentorship_relations_job,
    #                   trigger='interval', seconds=4,
    #                   replace_existing=True)

    scheduler.start()
