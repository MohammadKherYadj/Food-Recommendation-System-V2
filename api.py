from fastapi import FastAPI
from setup import Recommand_Food,return_by_rating

app = FastAPI()

@app.get("/")
def get_ready():
    return {"Message ":" OK"}


@app.get("/recommand-food/{food_name}")
def get_Recommand_Food(food_name:str):
    return {"Recommand Food":Recommand_Food(food_name)}

@app.get("/return-by-rating/{rating}")
def get_by_rating(rating:int):
    return return_by_rating(rating)
