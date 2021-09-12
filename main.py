from fastapi import FastAPI

# run with
# production mode: uvicorn main:app
# debug mode: uvicorn main:app --reload
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
