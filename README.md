# Amazon SageMaker ModelDB Sync

![Alt text](docs/diagram.png?raw=true "Diagram")

## Overview

This sample deploys a simple event-based architecture to synchronize SageMaker model metadata to ModelDB with the ModelDB Light API. The synchronization will be triggered when SageMaker Training Jobs complete. A Step Function will be executed to validate certain tags that are applied to training jobs, gather details about the trained model, and synchronize those details to a ModelDB instance using the ModelDB Light API. This solution can be extended to synchronize any data that's supported by the Light API, or used as a pattern for synchronizing to other model metadata management systems.

### Limitations

* Expects a publically accessible ModelDB instance. This is acceptable for some testing but you may want to consider deploying your ModelDB instance within a VPC and updating the template.yaml file to configure the SyncModelWithModelDBFunction Lambda Function to use this VPC. You could also further configure the Lambda Function code to utilize any authentication mechanisms you've implemented as part of your ModelDB deployment.
* Currently supports ModelDB V1. The ModelDB project has announced that ModelDB V2 is comming soon, and once released this project may need to be updated to support V2 depending on any changes made to the Light API.
* Only some details from the SageMaker DescribeTrainingJob API call are synchronized to ModelDB. You can extend this solution to include additional data as required, using this solution as a starting point for your synchronization workflow.

### What's Synchronized to ModelDB

* Project Name
* Project User
* Project Description
* Model Name
* Model Type
* SageMaker Training Job InputDataConfig Channels
* SageMaker Training Job Hyperparameters
* SageMaker Training Job Metrics (train/test)
* SageMaker Training Job Output Model Location

### Step Function

The following diagram shows the Step Function that is executed to synchronize model metadata with Model DB. This step function is triggered by a Amazon SageMaker CloudWatch Event Rule w/ a Lambda target that triggers the Step Function.

![Alt text](docs/stepfunction.png?raw=true "Diagram")

### Getting Sarted
* Deploy this solution into the AWS Account where you are conducting SageMaker Training. When you deploy the solution you will need to provide the following parameters.
    * ModelDB Instance and Port to synchronize with (varies based on how you deploy ModelDB).

### Tag Detail

As you create SageMaker Training Jobs, include the folllowing tags, as they will be used for synchronizing the trained model to ModelDB.

![Alt text](docs/tags.png?raw=true "Tags")

#### Tags

All of the following tags must exist in your Training Job in order for the sync to be successful. If you don't want a training job to be syncronized you can ommit the MODEL_DB_SYNC key while continuing to tag training jobs with other metadata. This is useful if you are reusing existing tag keys and want to indendently control flagging some training jobs to sync, and others to not sync.

    * Key: MODEL_DB_SYNC Value: [Any Value Accepted]
    * Key: MODEL_DB_PROJECT_NAME Value: [Project Name]
    * Key: MODEL_DB_PROJECT_USER Value: [Project User Name]
    * Key: MODEL_DB_PROJECT_DESC Value: [Project Description]
    * Key: MODEL_DB_MODEL_NAME Value: [Model Name]
    * Key: MODEL_DB_MODEL_TYPE Value: [Model Type]

#### Customizing

Tag keys are configurable by overriding the CloudFormation parameter corresponding to the tag you'd like to customize when deploying the solution. This can be useful if you'd like to use tags that already exist on your training jobs. 

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

### Build and Package

Repalce the placeholder values in [] with your values and then run this command with a properly configured SAM environment.

```bash
sam build --use-container

sam package \
    --output-template-file packaged.yaml \
    --s3-bucket S3_BUCKET_TO_STAGE_CODE
```

### Deploy the Stack

#### Console

1. Logon to the AWS Console
2. Open the CloudFormation service.
3. Click "Create Stack"
4. Navigate to the packaged.yaml file stored locally (this package is created with the sam package command and references code artifacts in S3)
5. Enter the required parameters and launch the stack (you will need to confirm a few more screens, and generate a change-set.).

#### CLI

Repalce the placeholder values in [] with your values and then run this command with a properly configured SAM environment.

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