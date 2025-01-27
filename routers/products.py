from fastapi import APIRouter

router_product = APIRouter()

@router_product.get("/products")
async def products():
    return ["Product 1", "Product 2", 
            "Product 3", "Product 4", 
            "Product 5"]