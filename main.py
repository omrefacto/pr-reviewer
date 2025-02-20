from dotenv import load_dotenv
from fastapi import FastAPI
import listener

app = FastAPI()

# Include listener router
app.include_router(listener.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
