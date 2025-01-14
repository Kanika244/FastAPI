from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.routes_CRUD import router

app = FastAPI()



app.include_router(router,prefix="/api")

app.include_router(user_router,prefix="/api")
#app.include_router(router_auth,prefix="/api")
