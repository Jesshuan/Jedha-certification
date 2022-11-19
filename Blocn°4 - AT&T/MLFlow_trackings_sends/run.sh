docker run -it \
 -v "$(pwd):/home/app" \
 -e MLFLOW_TRACKING_URI=https://mlflow-jess-aix-86.herokuapp.com/ \
 -e PORT=4000 \
 -e AWS_ACCESS_KEY_ID=AKIA3S5CIUB46CVBFI4J \
 -e AWS_SECRET_ACCESS_KEY=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 \
 -e BACKEND_STORE_URI=postgresql://tqrbxyyxgznivt:391f0aab08d6ba79902d6f69b94e1f2373bf1824c494c2bcff8f7bba326f1db0@ec2-54-174-31-7.compute-1.amazonaws.com:5432/de4uog256cs0i6 \
 -e ARTIFACT_ROOT=s3://mlflow-aix-86/mlflow-artifacts/ \
 mlflow_cancel python train.py --n_estimators=100 --min_samples_split=2 