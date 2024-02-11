from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from api.server.routes.chatbot import router as chatbot_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://itwi.me"],  # Adjust this to your Angular application URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include your chatbot router
app.include_router(chatbot_router, tags=["AI"], prefix="/chat")

# Customized function to modify the OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ClimateSwipe API",  # Set the title to your project name
        version="v0.2",  # Set the version to your desired version
        description="API for ClimateSwipe",  # Describe your API here
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the ClimateSwipe API!"}
