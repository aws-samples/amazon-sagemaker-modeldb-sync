 # Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy of this
 # software and associated documentation files (the "Software"), to deal in the Software
 # without restriction, including without limitation the rights to use, copy, modify,
 # merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 # permit persons to whom the Software is furnished to do so.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 # PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 # OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 # SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 
import boto3
import json
from datetime import date, datetime

client = boto3.client('sagemaker')

# JSON Serializer for Metric TimeStamps
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable." % type(obj))

def lambda_handler(event, context):

    trainingJobName = event['trainingJobName']
    trainingJobTags = event['trainingJobTags']

    try:
        response = client.describe_training_job(
        TrainingJobName=trainingJobName
        )

        return {
            'trainingJobName': trainingJobName,
            'trainingJobTags': trainingJobTags,
            'trainingJobDetails': json.dumps(response, default=json_serial)
        }  

    except Exception as e:
        message = 'Error describing Training Job: {}'.format(e)
        raise Exception(message)  