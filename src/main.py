import io
import json
import logging
from typing import List

import uvicorn
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles

from config import ServiceConfig
from connector import PostGresConnector

from src.service.QAService import QAService

app = FastAPI(title='VisualQARest',
              description='<img width="30%" height="30%" src="static/Title.png" alt="bear">\n\n '
                          'This app contains a Visual Answering Model and uses it per rest api',
              version="0.1")
app.mount("/static", StaticFiles(directory="static/"), name="static")

service_config = ServiceConfig()


def init_database(config: ServiceConfig):
    database_opts = dict(
        server=config.database.host,
        database=config.database.database,
        user=config.database.user,
        pw=config.database.password,
        port=config.database.port
    )

    if config.database.driver == "postgres":
        return PostGresConnector(driver="", **database_opts)

    raise Exception(f"Unknown database driver: {config.database.driver}")


database_connector = init_database(service_config)
#database_connector = None
#geo_service = NERService(config=service_config, connector=database_connector)
vqa_service = QAService(config=service_config, connector=database_connector)


class MyText(BaseModel):
    content: str = "What can you see in the picture? "


@app.post("/vaq", description="Returns an answer based on  an image.", tags=["Visual Questioning"])
async def vaq(message: str, file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)

        print("image consumed")
        result = vqa_service.ask_question(message, image)
        return json.loads(json.dumps(result))

    except Exception as e:
        result = {"error_message": str(e)}
        result = eval(json.dumps(result))
        return JSONResponse(content=result)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
