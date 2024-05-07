from apscheduler.schedulers.background import BackgroundScheduler


def job_function1():
    print("Executing job 5 sec...")


def job_function2():
    print("Executing job 8 sec...")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_function1, "interval", seconds=5)
    scheduler.add_job(job_function2, "interval", seconds=8)
    scheduler.start()
