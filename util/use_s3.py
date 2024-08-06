import boto3


def get_buckets():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)


def ul_file(file, dir='tmpfiles', tag='test'):
    print('use_s3 ul_file', file)

    s3 = boto3.client('s3')

    with open(f"./{dir}/{file}", "rb") as f:
        s3.upload_fileobj(f, 'jctests3', f"{tag}/{file}")

