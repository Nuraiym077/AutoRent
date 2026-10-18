from fastapi import FastAPI
import uvicorn
from mysite.api import user
from mysite.agent import agent

auto_app = FastAPI(title="AutoRent")

auto_app.include_router(user.api_router)
auto_app.include_router(agent.chain_router)

if __name__ == "__main__":
    uvicorn.run(auto_app, host="127.0.0.1", port=8000)