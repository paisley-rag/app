import boto3
import os


def get_buckets():
    s3 = boto3.resource('s3')
    print('S3 IS:', s3)
    for bucket in s3.buckets.all():
        print(bucket.name)


def ul_file(file, tag='kb_files'):
    s3_bucket_name = os.getenv('S3_BUCKET_NAME', 'kb_files')
    print('use_s3 ul_file', file)

    s3 = boto3.client('s3')

     # Make sure directory exists
    os.makedirs(f'./{tag}', exist_ok=True)

    with open(f"./{tag}/{file}", "rb") as f:
        s3.upload_fileobj(f, s3_bucket_name, f"{tag}/{file}")


# if __name__ == "__main__":
#     get_buckets()
