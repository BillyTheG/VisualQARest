import json
import logging
from typing import List

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles

from config import ServiceConfig
from connector import MariaDbConnector, PostGresConnector
from service.NERService import NERService

app = FastAPI(title='GeoReferenceAI-Service IREC',
              description='<img width="30%" height="30%" src="static/Title.png" alt="bear">\n\n '
                          '*GRAI* (<b>G</b>eo <b>R</b>eference <b>A</b>rtifical <b>I</b>ntelligence) ist ein Dienst, der eine automatische Georeferenzierung für beliebige Text bereitstellt. \n\n Durch den Einsatz von SpaCy- und '
                          'Word2Vec/FastText-Modellen\n ist der Service in der Lage, (geographische) Orte bzw. Entitäten aus Textpassagen zu extrahieren. Es wird eine Schnittstelle via REST angeboten. Siehe dazu unten \n\n'
                          'Mithilfe der Endpoints können Sie einzelne Funktionen aufgreifen. Beispielanfragen sind angefügt über das Framework [Swagger](https://swagger.io/). *Hinweis*: Bitte verwenden Sie nur echte Entitäten vom Planeten Erde. \n\n'
                          'Geoinformationen aus anderen Universen werden noch nicht angewendet. Bei Fragen wenden Sie sich bitte an [Hptm Bilal Günaydin](https://wiki.bundeswehr.org/display/~BilalGuenaydin) \n \n'
                          'Link to Repo: [GIT](https://vgit.coi.air/SMArtIP/Svc.GeoReferenceAI)',
              version="0.1")
app.mount("/static", StaticFiles(directory="../static/"), name="static")

service_config = ServiceConfig()


def init_database(config: ServiceConfig):
    database_opts = dict(
        server=config.database.host,
        database=config.database.database,
        user=config.database.user,
        pw=config.database.password,
        port=config.database.port
    )

    if config.database.driver == "mariadb":
        return MariaDbConnector(driver="", **database_opts)
    elif config.database.driver == "postgres":
        return PostGresConnector(driver="", **database_opts)

    raise Exception(f"Unknown database driver: {config.database.driver}")


#database_connector = init_database(service_config)
database_connector = None
geo_service = NERService(config=service_config, connector=database_connector)
# geo_service = None


class MyText(BaseModel):
    content: str = "The political row broke out on Sunday after Israel’s foreign ministry said the two countries’ " \
                   "foreign ministers had met the previous week. The statement said Israel’s Cohen and Mangoush, " \
                   "his Libyan counterpart in the " \
                   "Tripoli-based administration, spoke at a meeting in Rome hosted by Italian foreign minister Antonio Tajani.. "


@app.post("/ner", description="Returns a list of entities found within a text by SpaCy.",
          openapi_extra={
              "requestBody": {
                  "content": {"application/json": {"schema": MyText.model_json_schema()}},
                  "required": True,
              },
          }, tags=["NER"])
async def ner(request: Request):
    try:
        message_string = await request.json()
        message = dict(message_string)
        result = geo_service.returns_all_entities(message['content'])
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
