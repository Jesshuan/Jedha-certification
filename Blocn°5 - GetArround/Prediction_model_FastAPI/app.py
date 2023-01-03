import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow


description = """
# Get Around API

* Advise the rental price for our users
"""

tags_metadata = [
    {
        "name": "Get started",
        "description": "Just to say hello for the app..."
    },

    {
        "name": "Predictions",
        "description": "For predictions..."
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

###
# Here you define enpoints 
###

#GET
@app.get("/", tags=["Get started"])
async def index():

    message = "Hello world!!! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"

    return message

@app.get("/hello", tags=["Get started"])
async def hi():
    return 'Hello there 🤗'


#POST

class Features(BaseModel):
    v1 : str
    v2 : str

@app.post("/predict")
async def create_blog_article(simple_predict: Features):
    prediction_dict = {
        'v1' : [simple_predict.v1],
        'v2' : [simple_predict.v2],
    }
    df = pd.DataFrame(prediction_dict)
    logged_model = 'runs:/f1da9e19318f4fe4a99f0ea8e47b7643/AT&T_predictions'
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    prediction = loaded_model.predict(df)

    response = {"prediction": prediction.tolist()}

    return response

    #df.append(simple_predict, ignore_index=True)

    #return loaded_model.predict(pd.DataFrame(df)).to_json()


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)

