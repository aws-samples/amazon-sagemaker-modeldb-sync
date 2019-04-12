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
 
import os
import json

from modeldb.basic.ModelDbSyncerBase import *

def syncToModelDB(projectName, projectUser, projectDesc, modelName, modelType, trainingJobDetails, host, port):

    print('Attempting to Synchronize Model To: {}:{}'.format(host, port))

    # Create Syncer
    modeldbSyncer = Syncer.create_syncer(projectName, projectUser, projectDesc, host, int(port))

    # Create DataSets
    datasets = {}
    for dataset in trainingJobDetails['InputDataConfig']:
        datasets[dataset['ChannelName']] = Dataset(dataset['DataSource']['S3DataSource']['S3Uri'], {"CompressionType" : dataset['CompressionType'], "RecordWrapperType" : dataset['RecordWrapperType']})

    # Create Model, ModelConfig, and ModelMetrics Instances
    model = Model(modelType, modelName, trainingJobDetails['ModelArtifacts']['S3ModelArtifacts'])
    
    # Create Model Config (Add HyperParameters)
    hyperparameters = {}
    for hyperparameter in trainingJobDetails['HyperParameters']:
        hyperparameters[hyperparameter] = trainingJobDetails['HyperParameters'][hyperparameter]
    
    modelConfig = ModelConfig(modelType, hyperparameters)

    # Add Metrics to ModelMetrics Instance
    metrics = {}
    for metric in trainingJobDetails['FinalMetricDataList']:
        metrics[metric['MetricName']] = metric['Value']

    modelMetrics = ModelMetrics(metrics)

    # Sync DatsSets to ModelDB
    modeldbSyncer.sync_datasets(datasets)

    # Sync Model to ModelDB
    modeldbSyncer.sync_model("train", modelConfig, model)

    # Sync Metrics to ModelDB
    modeldbSyncer.sync_metrics("test", model, modelMetrics)

    # Perform Sync
    try:
        modeldbSyncer.sync()
    except Exception as e:
        message = 'Error Synchronizing Model to Model DB: {}'.format(e)
        raise Exception(message) 

def getTagValue(tagToGet, tagNames, trainingJobTags):
    for tag in tagNames:
        if tag['Name'] == tagToGet:
            if tag['Value']:
                return trainingJobTags[tag['Value']]
            else:
                return 'Default'

def lambda_handler(event, context):
    print(event)

    modeldbInstanceUrl = os.environ['MODEL_DB_INSTANCE_URL']
    modeldbInstancePort = os.environ['MODEL_DB_INSTANCE_PORT']

    tagNames = event['data']['tagNames']
    trainingJobTags = event['data']['trainingJobTags']

    # Load Training Job Tag Values for Import into ModelDB
    projectName = getTagValue('TAG_MODEL_DB_PROJECT_NAME', tagNames, trainingJobTags)
    projectUser = getTagValue('TAG_MODEL_DB_PROJECT_USER', tagNames, trainingJobTags)
    projectDesc = getTagValue('TAG_MODEL_DB_PROJECT_DESC', tagNames, trainingJobTags)
    modelName = getTagValue('TAG_MODEL_DB_MODEL_NAME', tagNames, trainingJobTags)
    modelType = getTagValue('TAG_MODEL_DB_MODEL_TYPE', tagNames, trainingJobTags)
    
    trainingJobDetails = json.loads(event['data']['trainingJobDetails'])
    
    syncToModelDB(projectName, projectUser, projectDesc, modelName, modelType, trainingJobDetails, modeldbInstanceUrl, modeldbInstancePort)