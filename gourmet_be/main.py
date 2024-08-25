from fastapi import FastAPI

from .endpoints.recipes import router as recipes_router

app = FastAPI()

app.include_router(recipes_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
