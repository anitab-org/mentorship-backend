import base64
import boto3


def upload_to_aws(encoded_input, bucket_name, file_name):
    s3_resource = boto3.resource('s3')
    first_object = s3_resource.Object(
        bucket_name=bucket_name, key=file_name)
    first_object.put(Body=base64.b64decode(encoded_input))
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)
    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location['LocationConstraint'], bucket_name, file_name)
    return object_url
