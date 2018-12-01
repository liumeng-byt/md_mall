from celery_tasks.main import celery_app


@celery_app.task(name='send_email')
def send_email():
    print('send_email')
