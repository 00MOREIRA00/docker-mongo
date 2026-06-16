from fastapi import APIRouter

router = APIRouter(
    prefix="/funcionarios",
    tags=["funcionarios"],
)


@router.get("/")
def health_check():
    return {"mensage": "Is up"}