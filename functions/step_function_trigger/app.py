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
import os

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print(event)
    if event['detail']['TrainingJobStatus'] == 'Completed':
    
        executionInput = {
            'trainingJobName': event['detail']['TrainingJobName'],
            'trainingJobTags': event['detail']['Tags'],
            'waitTime': 60
        }

        print('Training Job Completed - Triggering ModelDB Synchronization Workflow for: {}'.format(executionInput))

        stateMachineArn = os.environ['STATE_MACHINE_ARN']
       
        try:
            print('Attempting to Execute State Machine: {}'.format(stateMachineArn))
            response = client.start_execution(
                stateMachineArn=stateMachineArn,
                input=json.dumps(executionInput)
                )
            print('Execution Response: {}'.format(response))
        except Exception as e:
            message = 'Error executing State Machine: {}'.format(e)
            raise Exception(message)