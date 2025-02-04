import os
import uuid
from io import BytesIO
from PIL import Image, ImageOps
import boto3

s3 = boto3.client('s3')
size = int(os.getenv('THUMBNAIL_SIZE'))

def s3_thumbnail_generator(event, context):
    print("Event::", event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    img_size = event['Records'][0]['s3']['object']['size']

    if not key.endswith("_thumbnail.png"):
        image = get_s3_image(bucket, key)
        thumbnail = image_to_thumbnail(image)
        thumbnail_key = new_filename(key)
        url = upload_to_s3(bucket, thumbnail_key, thumbnail, img_size)
        return {
            "statusCode": 200,
            "body": url
        }

def get_s3_image(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()

    file = BytesIO(image_content)
    img = Image.open(file)
    return img

def image_to_thumbnail(image):
    return ImageOps.fit(image, (size, size), Image.LANCZOS)

def new_filename(key):
    key_split = key.rsplit('.', 1)
    return key_split[0] + "_thumbnail.png"

def upload_to_s3(bucket, key, image, img_size):
    # Save the image into a BytesIO object to avoid writing to disk
    out_thumbnail = BytesIO()
    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)

    response = s3.put_object(
        ACL='public-read',
        Body=out_thumbnail,
        Bucket=bucket,
        ContentType='image/png',
        Key=key
    )
    print(response)

    # url = f"{s3.meta.endpoint_url}/{bucket}/{key}"

    # # Save image URL to DynamoDB
    # s3_save_thumbnail_url_to_dynamo(url_path=url, img_size=img_size)

    # return url

def s3_save_thumbnail_url_to_dynamo(url_path, img_size):
    # Implement this function if you need to save the URL to DynamoDB
    pass

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
