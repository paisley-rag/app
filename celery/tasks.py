import os

from celery import Celery
from dotenv import load_dotenv
# import app_logger as log
import db.evals.evals as evals

load_dotenv(override=True)

ENVIRONMENT = os.environ["ENVIRONMENT"]
print('ENVIRONMENT', ENVIRONMENT)
# log.info('ENVIRONMENT', ENVIRONMENT)

if ENVIRONMENT == 'production':
    app = Celery('tasks', broker='sqs://')
    print('celery.py:  using AWS SQS as message broker')
else:
    app = Celery('tasks', broker='redis://localhost')
    print('celery.py:  using local redis as message broker')


@app.task
def run_evals_background(chatbot_id, query, response):
    print('celery.py run_evals_background: info received', chatbot_id, query, response)
    evals.store_running_eval_data(
        chatbot_id,
        query,
        response
    )
    print('celery.py run_evals_background:  task complete?')
    return f'run_evals_background: chatbot_id: {chatbot_id}, query: {query}'

    # if __name__ == '__main__':
    #     app.start()
