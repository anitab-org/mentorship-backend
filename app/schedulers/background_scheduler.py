from apscheduler.schedulers.background import BackgroundScheduler
from app.schedulers.complete_mentorship_cron_job import complete_overdue_mentorship_relations_job
from app.schedulers.remove_unverified_user_cron_job import remove_unverified_user_job


def init_scheduler():
    scheduler = BackgroundScheduler()

    # This cron job runs every day at 23:59h
    # Purpose: complete overdue accepted mentorship relations
    scheduler.add_job(id='complete_mentorship_relations_cron', func=complete_overdue_mentorship_relations_job,
                      trigger='cron', hour=23, minute=59, second=0, day='*', timezone='Etc/UTC',
                      replace_existing=True)

    # for tests purposes
    # scheduler.add_job(id='complete_mentorship_relations_cron', func=complete_overdue_mentorship_relations_job,
    #                   trigger='interval', seconds=4,
    #                   replace_existing=True)

    # This cron job runs runs every day at 23:59:59h
    # Purpose : Remove unverified users after their verification token expiry.
    scheduler.add_job(id='remove_unverified_user_cron', func=remove_unverified_user_job, trigger='cron',
                        hour=23, minute=59, second=59, day='*', timezone='Etc/UTC', replace_existing=True)

    scheduler.start()
