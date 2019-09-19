# aws-sqs-daily-drain-s3

Python script in AWS Lambda for recurring push of messages from an AWS SQS queue to AWS S3 bucket. Script runs daily triggered by a cron job from AWS CloudWatch. Ideal for cases where the messages of a SQS queue needs to be safeguarded beyond the maximum timeframe of 14 days as allowed by AWS SQS service. 

AWS Services needed as part of this demonstration:
1. AWS SQS - This is the queue which is reaching its message retention period of 14 days and needs its messages to be copied somewhere else

2. AWS S3 - This is the location where the recovered messages would be forwarded

3. AWS Lambda - Python script which would extract messages from SQS queue and push each message as an object to S3 bucket. After successfull copy, the script would also delete the message from the SQS queue

4. AWS CloudWatch - This would trigger the Lambda function every 24 hours using a 'rate' schedule expression
