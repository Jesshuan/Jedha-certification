import pandas as pd
import numpy as np
import datetime
import os

import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score
from sklearn.pipeline import Pipeline

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re

import mlflow
from mlflow.models.signature import infer_signature

if __name__ == "__main__":
    
    mlflow.tensorflow.autolog()

    nlp = spacy.load('en_core_web_md')

    ### MLFLOW Experiment setup
    experiment_name="AT&T_predictions"

    mlflow.set_experiment(experiment_name)

    experiment = mlflow.get_experiment_by_name(experiment_name)

    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)

    print("training model...")
    

    # Call mlflow autolog
    

    # import data

    data = pd.read_csv('./spam.csv', encoding = 'ISO-8859-1')
    data = data[['v1','v2']]

    nb_val = int(len(data)*0.15)
    data_val = data.sample(nb_val)
    data_train = data.iloc[[i for i in data.index if i not in data_val.index],:]
    print(f'Split of data..... train_data : {len(data_train)} - val_data : {len(data_val)}...')

    # ---PREPROCESSING ---

    # lemmatization
    def lemmatization_process(df):
        df['v2_clean'] = df['v2'].apply(lambda s : re.sub(r'[^\w\s]', '', s).lower())
        df['v2_clean'] = df['v2_clean'].apply(lambda s : re.sub('[0-9]+', '', s))
        df["v2_lemma"] = df["v2_clean"].apply(lambda x: " ".join([token.lemma_ for token in nlp(x) if (token.lemma_ not in STOP_WORDS) and (token.text not in STOP_WORDS)]))
        return df

    data_lemma = lemmatization_process(data_train)

    # tokenization
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=2000, oov_token="out_of_vocab")
    tokenizer.fit_on_texts(data_lemma['v2_lemma'])
    vocab_size = tokenizer.num_words

    def tokeniser_process(df):
        df["v2_tokenized"] = tokenizer.texts_to_sequences(df['v2_lemma'])
        return df

    data_token = tokeniser_process(data_lemma)

    

    # undersampling for fit
    def data_under_sampling(data, nb_reduce):
        data_sample_2 = data.loc[data['v1']=='spam',:]
        len_class_sub = len(data_sample_2)
        data_sample_1 = data.loc[data['v1']=='ham',:].sample(nb_reduce * len_class_sub)
        return pd.concat([data_sample_1,data_sample_2], axis=0).sample(frac=1).reset_index(drop=True)

    data_red = data_under_sampling(data_token, 5)

    # padding_process

    max_len_sentence = max([len(token) for token in data_token['v2_tokenized'].to_list()])

    def padding_process(data):
        global max_len_sentence
        v2_pad_train = tf.keras.preprocessing.sequence.pad_sequences(data_red['v2_tokenized'], padding="post", maxlen=max_len_sentence)
        return v2_pad_train

    v2_pad_train = padding_process(data_red)

    preprocessor = LabelEncoder()
    y = preprocessor.fit_transform(data_red['v1'])

    def preprocessing_y(data):
        y = preprocessor.transform(data['v1'])
        #y_val = preprocessor.transform(data_val['v1'])
        return y

    # preprocessing fonction for inference
    def preprocessing_total(df):
        df = lemmatization_process(df)
        df = tokeniser_process(df)
        df_pad = padding_process(df)
        y = preprocessing_y(data)
        return df_pad, y
    
    x_val, y_val = preprocessing_total(data_val)

    # splitting for fit
    x_train, x_test, y_train, y_test = train_test_split(v2_pad_train, y, test_size=0.2, stratify=y, random_state=2)
    train_batch = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(len(x_train)).batch(64)
    test_batch = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(64)

    AUTOTUNE = tf.data.AUTOTUNE
    train_batch = train_batch.cache().prefetch(buffer_size=AUTOTUNE)
    test_batch = train_batch.cache().prefetch(buffer_size=AUTOTUNE)

    # model architechure
    model_1 = tf.keras.Sequential([        
                  tf.keras.layers.Embedding(vocab_size+1, 128, input_shape=[x_train.shape[1],],name="embedding"),
                  tf.keras.layers.GlobalAveragePooling1D(),
                  tf.keras.layers.Dense(64, activation='relu'),
                  tf.keras.layers.Dropout(0.3),
                  tf.keras.layers.Dense(32, activation='relu'),
                  tf.keras.layers.Dropout(0.1),
                  tf.keras.layers.Dense(8, activation='relu'),
                  tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    optimizer= tf.keras.optimizers.Adam()

    model_1.compile(optimizer="adam",
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics = [tf.keras.metrics.BinaryAccuracy(name='accuracy'),
                         tf.keras.metrics.Precision(name='precision'),
                         tf.keras.metrics.Recall(name='recall')])


    print('start training...')

    # Log experiment to MLFlow

    mlflow.autolog(log_models=False)

    with mlflow.start_run(run_id = run.info.run_id) as run:
        model_1.fit(train_batch, epochs=20, verbose=1, validation_data=test_batch)
        predictions = model_1.predict(x_test)
        predictions_val = model_1.predict(x_val)
    
    print("log on MLFlow...")

    #mlflow.sklearn.log_model(
    #       sk_model=model_1,
    #        artifact_path="AT&T_predictions",
     #       registered_model_name="model_1",
     #       signature=infer_signature(x_test, predictions)
     #   )

    model_complete = Pipeline(steps=[
        ("Preprocessing", preprocessing_total),
        ("Model_complete",model_1)
    ])

    mlflow.sklearn.log_model(
            sk_model=model_complete,
            artifact_path="AT&T_predictions",
            registered_model_name="model_1_complete",
            signature=infer_signature(data_val[['v1','v2']], predictions_val)
        )

    mlflow.evaluate(model_complete,data_val[['v1','v2']], targets=y_val, model_type="classifier")
    

    #mlflow.tensorflow.autolog()

    print("...Done!")
 