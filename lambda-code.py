import json
import boto3

def lambda_handler(event, context):

    sqs_client = boto3.client('sqs')
    s3_client = boto3.client('s3')

    queue_url='<url of SQS queue>'
    dst_s3_bucket='<name of S3 bucket>'

    while True:
        messages = []

    # Read 10 message from the SQS queue

        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )

    # Try to read a message
    
        try:
            messages.extend(resp['Messages'])
        except KeyError:
            print('No messages on the queue!')
            break
        
    # Put the object in S3 bucket. You can use encryption per your needs - SSE or KMS or none
    
        for msg2 in resp['Messages']:
            msgid='folder2/%s' %(msg2['MessageId'])
            response = s3_client.put_object(Body=msg2['Body'],Bucket=dst_s3_bucket,Key=msgid,ServerSideEncryption='AES256') 

    # Signal to the queue to delete the messages since we have read those and dont want to extract dupliacte message again
    
        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in resp['Messages']
        ]
        
        resp2 = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )
        
    # Tells us if there was an error while deleting the message from the queue

        if len(resp2['Successful']) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }    
