import boto3
from botocore.exceptions import BotoCoreError, ClientError
from django.conf import settings
from uuid import uuid4

def upload_image_to_s3(file_obj, folder='imagenes/'):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    filename = f"{folder}{uuid4().hex}_{file_obj.name}"

    file_obj.seek(0)  # Ensure the file pointer is at the beginning
    s3.upload_fileobj(
        file_obj,
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        ExtraArgs={'ContentType': file_obj.content_type}
    )

    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return url