import uvicorn
from fastapi import FastAPI

from routes.v1.funcionarios import router as funcionarios_router


app = FastAPI(
    title="Integração de Funcionários",
    description="API para administração de funcionários",
    version="1.0.0",
)

app.include_router(funcionarios_router)










if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000) 
