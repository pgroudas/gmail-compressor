import boto
from boto.s3.key import Key
from boto.s3.bucket import Bucket

class S3:

    def __init__(self, bucket, access_key, secret_key):
        self.s3 = boto.connect_s3(access_key, secret_key)
        self.bucket = Bucket(self.s3, bucket)

    def upload(self, file_name, key_name):
        key = Key(self.bucket)
        key.key = key_name
        key.set_contents_from_filename(file_name)
