# NYCTaxiFare

## Running
1. `pip install -r requirements.txt`
2. Create `test.csv and train.csv`
2. `python NYCTaxiFare.py`

## Notes
Data needs to be from 2014 or above, due to the change in format.

  gcloud ml-engine jobs submit training $JOB_NAME \
  --job-dir ./trainer/ \
  --package-path $TRAINER_PACKAGE_PATH \
  --module-name $MAIN_TRAINER_MODULE \
  --region $REGION \
  --runtime-version=$RUNTIME_VERSION \
  --python-version=$PYTHON_VERSION \
  --scale-tier $SCALE_TIER

  PROJECT_ID=cloudcomputing-222017
  BUCKET_ID=cloud-computing-model-code
  JOB_NAME=taxi_training_$(date +"%Y%m%d_%H%M%S")
  JOB_DIR=gs://$BUCKET_ID/Output
  TRAINING_PACKAGE_PATH="./trainer/"
  MAIN_TRAINER_MODULE=trainer.task
  REGION=us-east1
  RUNTIME_VERSION=1.10
  PYTHON_VERSION=2.7
  SCALE_TIER=BASIC

MODEL_NAME="TestModel"
VERSION_NAME="Test"
INPUT_FILE="Predict_Input.json"