'''
helper utility to upload files to aws s3
'''
import os
import boto3

import db.app_logger as log

class UseS3Error(Exception):
    pass

def get_buckets():
    s3 = boto3.resource('s3')
    print('S3 IS:', s3)
    for bucket in s3.buckets.all():
        print(bucket.name)


def ul_file(file, tag='kb_files'):
    s3_bucket_name = os.getenv('S3_BUCKET_NAME', '')
    if s3_bucket_name == '':
        raise UseS3Error('No s3 bucket name defined in .env')

    s3 = boto3.client('s3')

    # Make sure directory exists
    if not os.path.exists(f"./tmpfiles/{file.filename}"):
        raise UseS3Error(f'./tmpfiles/{file.filename} not found for upload to s3')

    log.info('use_s3.py: ', 'filename', file.filename, 'tag', tag)

    # note: tmpfiles is currently hardcoded in kb_config.py / def _save_file_locally
    with open(f"./tmpfiles/{file.filename}", "rb") as f:
        s3.upload_fileobj(f, s3_bucket_name, f"{tag}/{file.filename}")


# if __name__ == "__main__":
#     get_buckets()
