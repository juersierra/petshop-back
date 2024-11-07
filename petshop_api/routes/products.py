from fastapi import APIRouter, HTTPException
from petshop_api.database.connection import get_database
from petshop_api.models.products import Product
from bson import ObjectId

db = get_database()
router = APIRouter()

# ----- PRODUCT'S ENDPOINTS -----

# Creates a new product in the DB

@router.post("/products", tags=["Products"])
async def create_product(product: Product):
    new_product = product.model_dump()
    result = db["products"].insert_one(new_product)
    new_product["_id"] = str(result.inserted_id)
    return new_product

# Retrieves all products stored in the DB

@router.get("/products", tags=["Products"])
async def get_all_products():
    products_cursor = db["products"].find()
    products = [product for product in products_cursor]
    for product in products:
        product["_id"] = str(product["_id"]) #This lines converts the ObjectId into a JSON string
    return products

# Retrieves a single product using its ID

@router.get("/products/{product_id}", tags=["Products"])
async def get_product(product_id: str):
    product = db["products"].find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"]) #Converst ObjectId to JSON string
    return product

# Updates a specific product (using its ID)

@router.put("/products/{product_id}", tags=["Products"])
async def update_product(product_id: str, updated_product: Product):
    result = db["products"].update_one({"_id": ObjectId(product_id)}, {"$set": updated_product.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return{"message": "Product updated successfully"}

# Deletes a single product using its ID

@router.delete("/products/{product_id}", tags=["Products"])
async def delete_product(product_id: str):
    result = db["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
