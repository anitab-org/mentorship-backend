from apscheduler.schedulers.background import BackgroundScheduler

import config
from app.schedulers.complete_mentorship_cron_job import (
    complete_overdue_mentorship_relations_job,
)
from app.schedulers.delete_unverified_users_cron_job import delete_unverified_users_job

scheduler = BackgroundScheduler()


def init_schedulers():
    """Runs all schedulers"""
    init_complete_relation_scheduler()
    init_delete_unverified_users_scheduler()
    if not scheduler.running:
        scheduler.start()


def init_complete_relation_scheduler():
    # This cron job runs every day at 23:59h
    # Purpose: complete overdue accepted mentorship relations
    scheduler.add_job(
        id="complete_mentorship_relations_cron",
        func=complete_overdue_mentorship_relations_job,
        trigger="cron",
        hour=23,
        minute=59,
        second=0,
        day="*",
        timezone="Etc/UTC",
        replace_existing=True,
    )

    # for tests purposes
    # scheduler.add_job(id='complete_mentorship_relations_cron', func=complete_overdue_mentorship_relations_job,
    #                   trigger='interval', seconds=4,
    #                   replace_existing=True)


def init_delete_unverified_users_scheduler():
    threshold_days = config.BaseConfig.UNVERIFIED_USER_THRESHOLD // 86400

    scheduler.add_job(
        id="delete_unverified_users_cron",
        func=delete_unverified_users_job,
        trigger="cron",
        day=threshold_days,
        replace_existing=True,
    )
