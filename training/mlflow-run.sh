#! /bin/bash

export MLFLOW_TRACKING_URI=https://projet-hackathon-ntts-2025-mlflow.user.lab.sspcloud.fr/
export MLFLOW_S3_ENDPOINT_URL=https://minio.lab.sspcloud.fr
export MLFLOW_EXPERIMENT_NAME=test

export AWS_ACCESS_KEY_ID=hackathon2025
export AWS_SECRET_ACCESS_KEY=8YJkCIle2Gd4Avhg7gxj5g==
export MC_HOST_s3=https://$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY:@minio.lab.sspcloud.fr
ENTRY_POINT=main


SOURCE=SENTINEL2
DATASETS='["BE100_2018"]'
TILES_SIZE=250
TYPE_LABELER=CLCplus-Backbone
USE_S3=0
EPOCHS=10
BATCH_SIZE=1
TEST_BATCH_SIZE=1
LR=0.00005
SCHEDULER_NAME=one_cycle
BUILDING_CLASS_WEIGHT=2
FREEZE_ENCODER=0
LOSS_NAME=cross_entropy_weighted
MODULE_NAME=segformer-b5
LABEL_SMOOTHING=0.0
LOGITS=1
CUDA=1
AUGMENT_SIZE=512
PATIENCE=10
N_BANDS=14

mlflow run ~/work/hackathon-ntts-2025/training/ \
    --env-manager=local \
    --entry-point $ENTRY_POINT \
    -P remote_server_uri=$MLFLOW_TRACKING_URI \
    -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
    -P source=$SOURCE \
    -P datasets="$DATASETS" \
    -P type_labeler=$TYPE_LABELER \
    -P tiles_size=$TILES_SIZE \
    -P epochs=$EPOCHS \
    -P batch_size=$BATCH_SIZE \
    -P test_batch_size=$TEST_BATCH_SIZE \
    -P lr=$LR \
    -P scheduler_name=$SCHEDULER_NAME \
    -P from_s3=$USE_S3 \
    -P loss_name=$LOSS_NAME \
    -P module_name=$MODULE_NAME \
    -P label_smoothing=$LABEL_SMOOTHING \
    -P logits=$LOGITS \
    -P building_class_weight=$BUILDING_CLASS_WEIGHT \
    -P freeze_encoder=$FREEZE_ENCODER \
    -P augment_size=$AUGMENT_SIZE \
    -P patience=$PATIENCE \
    -P n_bands=$N_BANDS \
    -P cuda=$CUDA
