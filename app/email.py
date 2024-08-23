from botocore.exceptions import ClientError
from app import ses_client

try:
    response = ses_client.send_email(
        Destination={
            'ToAddresses': recipients
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': html_body,
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': text_body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=sender,
    )
except ClientError as e:
    print(e.response['Error']['Message'])
    # send error to discord
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])