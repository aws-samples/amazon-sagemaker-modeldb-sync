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

import json
import os

def validateTags(tagNames, trainingJobTags):
    print('Validating the Existance of {} in {}'.format(tagNames, trainingJobTags))
    
    passedValidation = []
    failedValidation = []

    for tag in tagNames:
        if tag['Value'] in trainingJobTags:
            print('Tag {} Exists in Training Job Tags'.format(tag['Value']))
            passedValidation.append(tag)
        else:
            print('Tag {} Does Not Exist in Training Job Tags'.format(tag['Value']))
            failedValidation.append(tag)

    if len(failedValidation) > 0:
        print('The Folllowing Tags Failed Validation: {}'.format(failedValidation))
        return 'FAILED'
    else:
        return 'PASSED'

def lambda_handler(event, context):
    print(event)

    trainingJobName = event['trainingJobName']
    trainingJobTags = event['trainingJobTags']

    tagNames = [
        {
            'Name': 'TAG_MODEL_DB_SYNC',
            'Value': os.environ['TAG_MODEL_DB_SYNC'],
        },
        {
            'Name': 'TAG_MODEL_DB_PROJECT_NAME',
            'Value': os.environ['TAG_MODEL_DB_PROJECT_NAME'],
        },
        {
            'Name': 'TAG_MODEL_DB_PROJECT_USER',
            'Value': os.environ['TAG_MODEL_DB_PROJECT_USER'],
        },
        {
            'Name': 'TAG_MODEL_DB_PROJECT_DESC',
            'Value': os.environ['TAG_MODEL_DB_PROJECT_DESC'],
        },
        {
            'Name': 'TAG_MODEL_DB_MODEL_NAME',
            'Value': os.environ['TAG_MODEL_DB_MODEL_NAME'],
        },
        {
            'Name': 'TAG_MODEL_DB_MODEL_TYPE',
            'Value': os.environ['TAG_MODEL_DB_MODEL_TYPE'],
        }
    ]
 
    try:
        validationResult = validateTags(tagNames, trainingJobTags)

        return {
            'trainingJobName': trainingJobName,
            'tagNames': tagNames,
            'trainingJobTags': trainingJobTags,
            'trainingJobTagValidation': validationResult
             }  

    except Exception as e:
        message = 'Error validating Training Job Tags: {}'.format(e)
        raise Exception(message)