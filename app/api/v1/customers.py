from fastapi import APIRouter


router = APIRouter(tags=["customers"])


@router.post("/")
def create_customer():
    return {
        "message": "welcome to the customers API"}

@router.get("/")
def get_customers():
    return {
        "message": "welcome to the customers API"}

@router.get("/{customer_id}")
def get_customer(customer_id: str):
    return {
        "message": f"welcome to the customers API {customer_id}"}

@router.patch("/{customer_id}")
def update_customer_status(customer_id: str):
    return {
        "message": f"welcome to the customers API {customer_id}"}

@router.put("/{customer_id}")
def update_customer(customer_id: str):
    return {
        "message": f"welcome to the customers API {customer_id}"}

@router.delete("/{customer_id}")
def delete_customer(customer_id: str):
    return {
        "message": f"welcome to the customers API {customer_id}"}