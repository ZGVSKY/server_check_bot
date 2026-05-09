from fastapi import FastAPI
from routers.control import router as control_router
import uvicorn

app = FastAPI(title="PC Control API", description="API for remote PC control via Telegram Bot")

app.include_router(control_router)

@app.get("/")
def read_root():
    return {"message": "PC Control API is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
