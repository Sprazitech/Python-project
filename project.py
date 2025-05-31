import boto3
import time
dynamodb_table = 'student'

# CONFIGURATION 

region = 'us-east-1' 
bucket_name = "project-test-bucket101087"
file_name = "pix.jpeg"


#CREATE S3 BUCKET

s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name)
print("S3 bucket '{bucket_name}' created.")

#UPLOAD FILE TO S3

s3.upload_file(file_name, bucket_name, file_name)
print("File '{file_name}' uploaded to S3.")

#GENERATE PRE-SIGNED URL

url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)
print("Pre-signed URL (valid for 1 hour):\n{url}")


# CREATE DYNAMODB TABLE

dynamodb = boto3.resource('dynamodb', region_name=region)

table = dynamodb.create_table(
    TableName=dynamodb_table,
    KeySchema=[
        {'AttributeName': 'StudentID', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'StudentID', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
)

print("Creating DynamoDB table '{dynamodb_table}'...")
table.wait_until_exists()
print("DynamoDB table '{dynamodb_table}' created.")


# INSERT STUDENT RECORD 

table = dynamodb.Table(dynamodb_table)
student_id = str('208edf7')
student_data = {
    'StudentID': student_id,
    'Name': 'Tobi Solarin',
    'Email': 'tobi@example.com'
}

table.put_item(Item=student_data)
print("Student record inserted: {student_data}")


# ====== RETRIEVE STUDENT RECORD ======

response = table.get_item(Key={'StudentID': student_id})
retrieved = response.get('Item')
print("Retrieved student record:\n{retrieved}")

