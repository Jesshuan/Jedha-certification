import mlflow
import os

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline

from xgboost import XGBRegressor

# Link to mlflow

mlflow.set_tracking_uri(os.environ["APP_URI"])

print(f'Link to mlflow site : {os.environ["APP_URI"]} done...')

if __name__ == "__main__":

    # -- DATA IMPORTATION AND PREPROCESSING -- 

    print('Data importation and preprocessing...')

    data = pd.read_csv('./src/get_around_pricing_project.csv')

    data.drop('Unnamed: 0', axis=1, inplace=True)

    to_keep = (abs(data['engine_power'] - data['engine_power'].mean()) <= 3*data['engine_power'].std()) & (data['engine_power']>50)
    data = data.loc[to_keep,:]

    to_keep = (abs(data['mileage'] - data['mileage'].mean()) <= 3*data['mileage'].std()) & (data['mileage']>=0)
    data = data.loc[to_keep,:]

    data_x = data.drop('rental_price_per_day', axis=1)
    y = data['rental_price_per_day']

    # Splitting :

    x_train, x_test, y_train, y_test = train_test_split(data_x, y, test_size=0.2, random_state=42)

    # -- DEFINE PREPROCESSOR -- 

    numericals = ['mileage','engine_power']
    categoricals = data_x.columns.drop(numericals)

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numericals),
        ('cat', OneHotEncoder(drop='first'), categoricals)
    ])


    # -- TRACKING CONFIG ON MLFLOW -- 

    EXPERIMENT_NAME="get-arround-predictions"

    mlflow.set_experiment(EXPERIMENT_NAME)

    print(f'Experiment created as {EXPERIMENT_NAME} on mlflow... ')

    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    print(f'ID of experiment : {experiment}')


    # -- MODEL DEFINITION & TRAINING -- 

    mlflow.sklearn.autolog(registered_model_name='xgboost_for_testing_and_scoring')

    with mlflow.start_run(experiment_id = experiment.experiment_id):

        model = XGBRegressor(eta=0.1, n_estimators=170, min_child_weight=2, gamma=0.8, colsample_bytree=0.4)

        model_pipeline = Pipeline([
        ('preprocessing', preprocessor),
        ('prediction', model)
        ])

        print('Start training for the test model...')

        model_pipeline.fit(x_train, y_train)

        print('...Done ...')

        y_pred_test = model_pipeline.predict(x_test)
        r2 = r2_score(y_test, y_pred_test)

        print(f'R2 score prediction on test set : {r2}')

        mlflow.log_metric('r2_score_test_set', r2 )


    
    mlflow.sklearn.autolog(log_input_examples=True, registered_model_name='xgboost_for_production')

    with mlflow.start_run(experiment_id = experiment.experiment_id):

        model = XGBRegressor(eta=0.1, n_estimators=170, min_child_weight=2, gamma=0.8, colsample_bytree=0.4)

        model_pipeline = Pipeline([
        ('preprocessing', preprocessor),
        ('prediction', model)
        ])

        print('Start training for the production model...')

        model_pipeline.fit(data_x, y)

        print('...Done ...')

        y_pred_test = model_pipeline.predict(x_test)
        r2 = r2_score(y_test, y_pred_test)

        print(f'R2 score prediction on test set : {r2}')

        mlflow.log_metric('r2_score_test_set', r2 )

        
