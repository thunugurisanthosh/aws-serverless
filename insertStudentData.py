import json
import boto3
from botocore.exceptions import ClientError

# Create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# Use the DynamoDB object to select our table
table = dynamodb.Table('studentData')

# Define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    try:
        # Validate required fields
        required_fields = ["studentid", "name", "class", "age"]
        for field in required_fields:
            if field not in event:
                return {
                    'statusCode': 400,
                    'body': json.dumps(f"Missing required field: {field}")
                }

        # Extract values
        student_id = event['studentid']
        name = event['name']
        student_class = event['class']
        age = event['age']

        # Write student data to the DynamoDB table
        response = table.put_item(
            Item={
                'studentid': student_id,
                'name': name,
                'class': student_class,
                'age': age
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Student data saved successfully!')
        }

    except ClientError as e:
        # DynamoDB error
        return {
            'statusCode': 500,
            'body': json.dumps(f"DynamoDB error: {e.response['Error']['Message']}")
        }
    except Exception as e:
        # Any other error
        return {
            'statusCode': 500,
            'body': json.dumps(f"Unexpected error: {str(e)}")
        }