import boto3
from django.conf import settings


def upload_image_to_s3(file_obj, file_name):
    # Funcion para subir imagenes a S3 de AWS
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    file_obj.seek(0)  # Ensure the file pointer is at the beginning
    s3.upload_fileobj(
        file_obj,
        settings.AWS_STORAGE_BUCKET_NAME,
        file_name,
        ExtraArgs={'ContentType': file_obj.content_type}
    )

    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    return url


def generate_url_presigned(file_name):
    expiracion=86400
    s3 = boto3.client('s3', region_name='us-east-1')

    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 
            'Key': file_name
        },
        ExpiresIn=expiracion  # segundos (86400   = 1 dia)
    )
    return url