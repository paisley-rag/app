import os
import boto3

from celery import Celery
from dotenv import load_dotenv
# import app_logger as log
import db.evals.evals as evals

load_dotenv(override=True)

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
print('ENVIRONMENT', ENVIRONMENT)
# log.info('ENVIRONMENT', ENVIRONMENT)

if ENVIRONMENT == 'production':
    session = boto3.Session()
    credentials = session.get_credentials()
    aws_access_key = credentials.access_key
    aws_secret_key = credentials.secret_key
    region = session.region_name or os.getenv('AWS_REGION', 'us-east-1')
    sqs_url = os.getenv('SQS_URL', '')
    app = Celery(
        'tasks',
        broker=f'sqs://{aws_access_key}:{aws_secret_key}@',
        broker_transport_options={
            "region": region,
            "predefined_queues": {
                f"SQSQueue-{os.getenv('INSTANCE_NUM')}.fifo": {  # sqs queue name
                    "url": sqs_url,
                    "access_key_id": aws_access_key,
                    "secret_access_key": aws_secret_key,
                }
            },
        },
        task_create_missing_queues=False,
    )
    print('celery.py:  using AWS SQS as message broker')
    print('REGION IS:', region)
else:
    app = Celery('tasks', broker='redis://localhost')
    print('celery.py:  using local redis as message broker')


@app.task
def run_evals_background(chatbot_id, query, context, output):
    print('celery.py run_evals_background: info received', chatbot_id, query, context, output)
    evals.evaluate_and_store_running_entry(
        chatbot_id,
        query,
        context,
        output
    )
    print('celery.py run_evals_background:  task complete?')
    return f'run_evals_background: chatbot_id: {chatbot_id}, query: {query}'

    # if __name__ == '__main__':
    #     app.start()
