from fastapi import FastAPI
from pydantic import BaseModel
from model import recommend, output_recommended_recipes
import pandas as pd
import os

app = FastAPI()

# Load your data
# Ensure the path to dataset.csv is correct. Adjust path as needed.
data_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
dataframe = pd.read_csv(data_path)

class RecommendationRequest(BaseModel):
    _input: list
    ingredients: list = []
    params: dict = {'n_neighbors': 5, 'return_distance': False}

@app.post("/recommend/")
async def get_recommendations(request: RecommendationRequest):
    try:
        # Generate recommendations based on input
        recommendations = recommend(dataframe, request._input, request.ingredients, request.params)
        
        # Format the recommendations for output
        output = output_recommended_recipes(recommendations)
        
        return {"recommendations": output}
    except Exception as e:
        return {"error": str(e)}
