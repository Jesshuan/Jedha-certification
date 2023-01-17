import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConstrainedList, Field
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame
import mlflow
from typing import List, Union

description = """
# Get Around API

* Advise the rental price for our users...
"""

tags_metadata = [
    {
        "name": "Get started",
        "description": "Just to say hello for the app..."
    },

    {
        "name": "Predictions",
        "description": "For predictions... Input the data of the car and other params and receive a rental price prediction at the output"
    }
]

### 
# Here you can define some configurations 
###

app = FastAPI(
    title="Get Around API",
    description=description,
    version="0.1",
    contact={
        "name": "Jesshuan Diné",
        "url get around analysis": "https://get-arround-analysis.herokuapp.com/",
    },
    openapi_tags=tags_metadata
)

### Class and validator definition ###

class Car_rental_proposition(BaseModel):
    model_key : List[str] = "Citroën", "Ford", "Citroën"
    mileage : List[float] = 140144, 125412, 152475
    engine_power : List[float] = 100, 105, 100
    fuel : List[str] = 'diesel', 'petrol', 'petrol'
    paint_color : List[str] = 'black', 'green', 'white'
    car_type : List[str] = 'convertible','estate', 'suv'
    private_parking_available : List[str] = True, False, False
    has_gps : List[str] = True, True, True
    has_air_conditioning : List[str] = True, False, True
    automatic_car : List[str] = False, False, False
    has_getaround_connect :  List[str] = True, False, False
    has_speed_regulator : List[str] = False, False, True
    winter_tires :  List[str] = False, True, True


class List_of_rental_car(BaseModel):
    input : list = [
    ["Citroën", 140411, 100, "diesel", "black", "convertible", True, True, False, False, True, True, True],
    ["Citroën", 183297, 120, "diesel", "white", "convertible", False, False, False, False, True, False, True],
    ["Citroën", 128035, 135, "petrol", "red", "convertible", True, True, False, False, True, True, True]
]

schema_withchecks = pa.DataFrameSchema({
    "model_key": pa.Column(
        str, pa.Check(lambda s: s.isin(['Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford',
       'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors',
       'Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati',
       'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT',
       'Subaru', 'Suzuki', 'Toyota', 'Yamaha']))),

    "mileage": pa.Column(
        int, [
            pa.Check(lambda s: s >= 0)
        ]),

    "engine_power" : pa.Column(
        int, [
            pa.Check(lambda s: s >= 0)
        ]),

    'fuel' : pa.Column(
        str, pa.Check(lambda s: s.isin(['diesel', 'petrol', 'hybrid_petrol', 'electro']))),

    'paint_color' : pa.Column(
        str, pa.Check(lambda s: s.isin(['black', 'grey', 'white', 'red', 'silver', 'blue', 'orange',
       'beige', 'brown', 'green']))),

    'car_type' : pa.Column(
        str, pa.Check(lambda s: s.isin(['convertible', 'coupe', 'estate', 'hatchback', 'sedan',
       'subcompact', 'suv', 'van']))),

    'private_parking_available' : pa.Column(bool),

    'has_gps' : pa.Column(bool),

    'has_air_conditioning' : pa.Column(bool),

    'automatic_car' : pa.Column(bool),

    'has_getaround_connect' : pa.Column(bool),

    'has_speed_regulator' : pa.Column(bool),

    'winter_tires' : pa.Column(bool)

    })


###
# Here you define enpoints 
###

#GET
@app.get("/", tags=["Get started"])
async def index():

    """
    It's just a default endpoint with a welcome message...
    """

    message = "Hello world!!! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"

    return message

@app.get("/hello", tags=["Get started"])
async def hi():

    
    """
    It's just an other default endpoint with a welcome message... try it to connect to the API
    with a request on https://api-get-around.herokuapp.com/hello
    """

    return 'Hello there 🤗'


#POST

# post request with prediction on fastapi, fisrt option :

@app.post("/predict", tags=["Predictions"])
async def prediction_list(data: Car_rental_proposition):

    """
    To be used preferably.
    For inputs as a dictionnary.
    Submit your data in the sample format shown below (and also in the "Schema" information panel below).
    constraints :
    - model_key : one of theses : 'Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford',
       'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors',
       'Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati',
       'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT',
       'Subaru', 'Suzuki', 'Toyota', 'Yamaha'
    - mileage : a positive integer
    - engine_power : a positive integer
    - fuel : one of theses : 'diesel', 'petrol', 'hybrid_petrol', 'electro'
    - paint_color : on of theses : 'black', 'grey', 'white', 'red', 'silver', 'blue', 'orange', 'beige', 'brown', 'green'
    - car_type : on of theses : 'convertible', 'coupe', 'estate', 'hatchback', 'sedan', 'subcompact', 'suv', 'van'
    - private_parking_available : a boolean (true or false)
    - has_gps : a boolean (true or false)
    - has_air_conditioning : a boolean (true or false)
    - automatic_car : a boolean (true or false)
    - has_getaround_connect : a boolean (true or false)
    - has_speed_regulator : a boolean (true or false)
    - winter_tires : a boolean (true or false)
    """

    # encoding data as a dataframe (with josonable_encoder for fastapi)
    try:
        df = pd.DataFrame(jsonable_encoder(data))
    except Exception as e :
        return JSONResponse(
        status_code=418,
        content={"message": f"Problem with the data construction... Detail: {e.args}"},
    )

    # data conversion (pydantic format disturbed the dataframe, so we need to find again the good types)

    df['mileage'] = df['mileage'].apply(lambda v : int(v))
    df['engine_power'] = df['engine_power'].apply(lambda v : int(v))
    df['private_parking_available'] = df['private_parking_available'].apply(lambda v : bool(v))
    df['has_gps'] = df['has_gps'].apply(lambda v : bool(v))
    df['has_air_conditioning'] = df['has_air_conditioning'].apply(lambda v : bool(v))
    df['automatic_car'] = df['automatic_car'].apply(lambda v : bool(v))
    df['has_getaround_connect'] = df['has_getaround_connect'].apply(lambda v : bool(v))
    df['has_speed_regulator'] = df['has_speed_regulator'].apply(lambda v : bool(v))
    df['winter_tires'] = df['winter_tires'].apply(lambda v : bool(v))

    # validation of the inputs with the pandera library :

    

    # here, we try to validate the dataframe with the pandera validator
    # Otherwise, we generate an exception and we display what is the problematic input for the user
    
    try:
        df =  schema_withchecks.validate(df)

    except pa.errors.SchemaError as e :
        return JSONResponse(
        status_code=418,
        content={"message": f"Oops! Wrong format... Check your input types and categories... Detail : {e.args}"},
    )

    # Model importation (code from MlFlow)
   
    logged_model = 'runs:/1718f1437779437ca76a68ac2258d5f2/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # Prediction and response
    prediction = loaded_model.predict(df)

    response = {"prediction": prediction.tolist()}

    return response


# post request with prediction on fastapi, second option :

@app.post("/predict_list_of_inputs", tags=["Predictions"])
async def prediction_list_of_inputs(data: List_of_rental_car):

    """
    For inputs as a list of list of inputs.
    Submit your data in the sample format shown below (and also in the "Schema" information panel below).
    Constraints :
    - model_key : one of theses : 'Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford',
       'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors',
       'Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati',
       'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT',
       'Subaru', 'Suzuki', 'Toyota', 'Yamaha'
    - mileage : a positive integer
    - engine_power : a positive integer
    - fuel : one of theses : 'diesel', 'petrol', 'hybrid_petrol', 'electro'
    - paint_color : on of theses : 'black', 'grey', 'white', 'red', 'silver', 'blue', 'orange', 'beige', 'brown', 'green'
    - car_type : on of theses : 'convertible', 'coupe', 'estate', 'hatchback', 'sedan', 'subcompact', 'suv', 'van'
    - private_parking_available : a boolean (true or false)
    - has_gps : a boolean (true or false)
    - has_air_conditioning : a boolean (true or false)
    - automatic_car : a boolean (true or false)
    - has_getaround_connect : a boolean (true or false)
    - has_speed_regulator : a boolean (true or false)
    - winter_tires : a boolean (true or false)
    """

    df = pd.DataFrame(columns=[
    "model_key",
    "mileage",
    "engine_power",
    "fuel",
    "paint_color",
    "car_type",
    "private_parking_available",
    "has_gps",
    "has_air_conditioning",
    "automatic_car",
    "has_getaround_connect",
    "has_speed_regulator",
    "winter_tires"
  ])

    for i, row in enumerate(data.input):
        try:
            df.loc[i] = row
        except Exception as e:
            return JSONResponse(
            status_code=418,
            content={"message": f"Problem with the data construction... Detail: {e.args}"},
            ) 

    try:
        df =  schema_withchecks.validate(df)

    except pa.errors.SchemaError as e :
        return JSONResponse(
        status_code=418,
        content={"message": f"Oops! Wrong format... Check your input types and categories... Detail : {e.args}"},
    )

    logged_model = 'runs:/1718f1437779437ca76a68ac2258d5f2/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # Prediction and response
    prediction = loaded_model.predict(df)

    response = {"prediction": prediction.tolist()}

    return response


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)

