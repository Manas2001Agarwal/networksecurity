from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI()

# @app.get("/")
# async def home_page(str1:str=" "):
#     return f"This is a home page /n {str1}"

# @app.get("/employee/{name}")
# async def employee(name:str,salary:int):
#     return {"employee_name":name,
#             "salary":salary}

# @app.get("/employee")
# async def employee_page():
#     return f"this is employee page"

items = []

class Item(BaseModel):
    name: str
    price: int
    is_offer: bool = None  # Optional field with a default value

class ItemResponse(BaseModel):
    name:str
    price:int
    
class ItemsResponse(BaseModel):
    items: ItemResponse

@app.post("/items/")
async def create_item(item: Item):
    items.append(item)
    return({"item": item})

@app.get("/items")
async def get_item():
    return {"items":items}
