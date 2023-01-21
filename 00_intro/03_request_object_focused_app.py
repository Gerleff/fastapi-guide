from fastapi import FastAPI
import uvicorn

app = FastAPI(docs_url="/")


@app.get("/ping")
async def healthcheck():
    return "pong"


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="localhost", port=8000, reload=True)
