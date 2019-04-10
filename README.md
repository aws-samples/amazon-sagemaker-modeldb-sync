# Amazon SageMaker ModelDB Sync

![Alt text](docs/diagram.png?raw=true "Diagram")

## Overview

This sample deploys a simple event-based architecture to synchronize SageMaker Training Jobs to ModelDB with the ModelDB Light API. To synchronize your training jobs to ModelDB, you simply need to perform the following.

### Limitations

* Expects a publically accessible ModelDB instance. This is acceptable for some testing but you may want to consider deploying your ModelDB instance within a VPC, and updating the template.yaml file to configure the SyncModelWithModelDBFunction Lambda Function to use this VPC. You could also further configure the Lambda Function code to utilize any authentication mechanisms you've implemented as part of your ModelDB deployment.
* Currently supports ModelDB V1. The ModelDB project has announced that ModelDB V2 is comming soon, and once released this project may need to be updated to support V2 depending on any changes made to the Light API.

### Getting Sarted
* Deploy this solution into the AWS Account where you are conducting SageMaker Training. When you deploy the solution you will need to provide the following parameters.
    * ModelDB Instance and Port to synchronize with.

### Tag Detail

As you create SageMaker Training Jobs, include the folllowing tags, as they will be used for synchronizing the trained model to ModelDB.

![Alt text](docs/tags.png?raw=true "Tags")

    * Key: MODEL_DB_SYNC Value: [Key Must Exist to Sync, Any Value Accepted]
    * Key: MODEL_DB_PROJECT_NAME Value: [Project Name]
    * Key: MODEL_DB_PROJECT_USER Value: [Project User Name]
    * Key: MODEL_DB_PROJECT_DESC Value: [Project Description]
    * Key: MODEL_DB_MODEL_NAME Value: [Model Name]
    * Key: MODEL_DB_MODEL_TYPE Value: [Model Type]

NOTE: Tag keys are configurable by overriding the parameter corresponding to the tag you'd like to customize. This can be useful if you'd like to use tags that already exist on your training jobs. 

* TagModelDBSync = MODEL_DB_SYNC
* TagModelDBProjectName = MODEL_DB_PROJECT_NAME
* TagModelDBProjectUser = MODEL_DB_PROJECT_USER
* TagModelDBProjectDesc = MODEL_DB_PROJECT_DESC
* TagModelDBModelName = MODEL_DB_MODEL_NAME
* TagModelDBModelType = MODEL_DB_MODEL_TYPE

## Deployment

### Prerequisites

1. Install the AWS Serverless Application Model CLI - https://aws.amazon.com/serverless/sam/
2. Configure your local AWS Credentials (aws configure).
3. Create an S3 bucket to store the packaged code and replace S3_BUCKET_TO_STAGE_CODE with the name of your bucket in the comamands below. 
4. This solution assumes that you have source data located in S3 and partitioned by data type (ie: item, user, user-item interactions). You can see some example source data below in JSON format, however this solution should work for any source data type that can be classified with AWS Glue.

### Building and Packaging

AWS CLI commands to package, deploy and describe outputs defined within the cloudformation stack:

## Pre Launch Steps

```bash
sam build --use-container

sam package \
    --output-template-file packaged.yaml \
    --s3-bucket S3_BUCKET_TO_STAGE_CODE
```

## Launching the Stack

### Console

1. Logon to the AWS Console
2. Open the CloudFormation service.
3. Click "Create Stack"
4. Navigate to the packaged.yaml file stored locally (this package is created with the sam package command and references code artifacts in S3)
5. Enter the required parameters and launch the stack (you will need to confirm a few more screens, and generate a change-set.).

### CLI

Repalce the placeholder values in [] with your values and then run this command with a properly configured SAM environment. You can also customize the source and destination columns as needed.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name aws-sagemaker-modeldb-connector \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    ModelDBInstanceUrl=[MODEL_DB_INSTANCE_URL] \
    ModelDBInstancePort=[MODEL_DB_INSTANCE_PORT]

aws cloudformation describe-stacks \
    --stack-name amazon-personalize-data-conversion-pipeline --query 'Stacks[].Outputs'
```