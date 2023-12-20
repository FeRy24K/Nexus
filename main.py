from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Kelompok Nexus")

fake_items_db = {}
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/items/", response_model=Dict[str, Item], tags=["Read"])
async def read_items():
    return fake_items_db

@app.get("/items/{item_id}", response_model=Item, tags=["Read Items"])
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

@app.post("/items/", response_model=Item, tags=["Create"])
async def create_item(item: Item):
    item_dict = item.dict()
    fake_items_db[item_dict["name"]] = item_dict
    return item_dict

@app.put("/items/{item_id}", response_model=Item, tags=["Update"])
async def update_item(item_id: str, item: Item):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item.dict(exclude_unset=True)
    fake_items_db[item_id].update(update_data)
    return fake_items_db[item_id]

@app.delete("/items/{item_id}", tags=["Delete"])
async def delete_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_items_db[item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    from pyngrok import ngrok

    ngrok.set_auth_token("2ZVvYajAOV6xS4Dkdj7kYmb3W3H_5vqkmchDuG12CvtPg8yGR")
    ngrok_tunnel = ngrok.connect(8000)
    print('Public URL:', ngrok_tunnel.public_url)
    uvicorn.run(app, port=8000)
