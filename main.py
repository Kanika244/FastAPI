from fastapi import FastAPI
from routes.routes_CRUD import router
from routes.user_routes import router as user_router


app = FastAPI()



app.include_router(router, prefix="/api")
for route in app.routes:
    print(f"Path:{route.path},Method:{route.methods}")

app.include_router(user_router,prefix="/api")
