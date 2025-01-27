from fastapi import APIRouter

products_list = ["Product 1", "Product 2", 
            "Product 3", "Product 4", 
            "Product 5"]

router_product = APIRouter(prefix="/products",
                            tags=["products"],
                           responses={404: {"description": "Not found"}})

@router_product.get("/")
async def products():
    return products_list

@router_product.get("/{id}")
async def product(id: int):
    return products_list[id]