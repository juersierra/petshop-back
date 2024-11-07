from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from petshop_api.routes.products import router as products_router

app = FastAPI()

# Includes routes
app.include_router(products_router, prefix="/api")

# Exception validation handler. 
# This section is used to personalize error messages from our API, so front end developers
# and 3rd parties consumming our app can better and easily understand the errors they're getting.

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = [
        {
            "field": ".".join(map(str, error['loc'][1:])), # ej. body.price
            "message": error['msg'] # Error message 
        }
        for error in errors
    ]
    return JSONResponse(
        status_code=422, # HTTP Code for 'Unprocessable Entity'
        content={"detail": custom_errors}
    )


@app.get("/", tags=["General"])
def read_root():
    return {"Hello": "World"}

