from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gas_meter import get_gas_levels
from humidity_meter import get_humidity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/{name}")
async def get_meter(name: str):
    if name == "gas":
        result = get_gas_levels()
    elif name == "humidity":
        result = get_humidity()
    else:
        result = "Unknown meter"
    return {
        "message": result
    }