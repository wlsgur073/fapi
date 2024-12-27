from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

from routes import blog
from utils.common import lifespan
from utils import exc_handler, middleware


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

# add_middleware는 stack마냥 후차순으로 실행된다.
app.add_middleware(middleware.DummyMiddleware)
app.add_middleware(middleware.MethodOverrideMiddleware)

app.include_router(blog.router)

# exception handler 등록
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_http_exception_hander)
app.add_exception_handler(RequestValidationError, exc_handler.validation_exception_handler)