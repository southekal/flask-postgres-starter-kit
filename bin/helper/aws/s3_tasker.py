import json
import os
import uuid
from werkzeug.utils import secure_filename

import boto3
from botocore.exceptions import ClientError
import requests

from log_config.custom_logger import logger


def get_presigned_s3_url(filedata, hashid, upload_bucket):
    """
        Ref - https://devcenter.heroku.com/articles/s3-upload-python
        These attributes are also available
        file.filename           
        file.content_type
        file.content_length
        file.mimetype
    """

    file_name = f"{hashid}/{filedata.filename}"
    file_type = filedata.content_type

    s3 = boto3.client('s3')

    presigned_post = s3.generate_presigned_post(
        Bucket = upload_bucket,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    generated_data = {
        'data': presigned_post,
        'url': f'https://{upload_bucket}.s3.amazonaws.com/{file_name}'
    }

    logger.info(f"aws presigned data {generated_data};")
    
    return generated_data



def upload_files_to_s3(form_files, hashid, upload_bucket):

    """
        returns: s3 upload urls
        takes files uploaded and directly pushes them into s3
    """
    
    s3_upload_urls = []
    
    for f in form_files:
        secure_name = secure_filename(f.filename)
        logger.info(f"aws starting file save; {secure_name}")
        
        # aws presigned url
        presigned_data = get_presigned_s3_url(
            filedata=f,  
            hashid=hashid,
            upload_bucket=upload_bucket
        )

        s3_url = presigned_data["url"]

        payload = presigned_data["data"]["fields"]
        payload["file"] = f

        # post information to aws url
        # requests: multi-part payload use "files" instead of "data"
        r = requests.post(
            presigned_data["data"]["url"], 
            files=payload
        ) 
        logger.info(f"aws post information; {r.text}; {r.status_code}")

        s3_upload_urls.append(s3_url)

    logger.info(f"s3 upload urls returned {s3_upload_urls}")
    return s3_upload_urls


def get_s3_file_key(s3_url):
    s3_key_value = s3_url.split("s3.amazonaws.com/")[-1]
    return s3_key_value


def delete_s3_files(s3_filename_list, upload_bucket):
    
    try:
        s3 = boto3.resource('s3')
        for s3_file in s3_filename_list:
            logger.info(f"deleting s3 file - {s3_file}")
            s3_key_value = get_s3_file_key(s3_url=s3_file)
            s3.Object(upload_bucket, s3_key_value).delete()

    except ClientError as e:
        logger.error(f"error deleting s3 {e}")
        return None


