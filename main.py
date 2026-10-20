from fastapi import FastAPI

from controllers import categories_controller

app = FastAPI()

app.include_router(categories_controller.router)