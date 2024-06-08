from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, Path, HTTPException, Body
from starlette.responses import RedirectResponse
from model.elastic import Elastic
from tools import Scrapper, Extractor, Analyzer
from utils import get_vt_config
import model
from constants import ANALYZER_EXAMPLE, SCRAPPER_EXAMPLE, EXTRACTOR_EXAMPLE
from utils.configuration import get_elastic_config

app = FastAPI(openapi_prefix="/api/v1")
analyzer = Analyzer(get_vt_config())
elastic_config: dict[str, Any] = get_elastic_config()
elastic: None | Elastic = None
if elastic_config.get("enabled") == "True":
    elastic: Elastic = Elastic(elastic_config.get("api_host"))


@app.get("/", include_in_schema=False)
async def go_to_docs() -> RedirectResponse:
    """
    Redirects to Swagger
    """
    return RedirectResponse(url="/docs", status_code=303)


@app.get("/ips")
async def search_ip(index: str = "ips") -> object:
    """
    Search for all ip address
    :param index: Index where all the IP are stored in elasticsearch
    :return: Results from elasticsearch
    """
    try:
        if results := await elastic.search(index=index):
            return results["hits"]
        else:
            raise HTTPException(status_code=404, detail="Index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/emails")
async def search_emails(index: str = "emails") -> object:
    """
    Search for all email addresses
    :param index: Index where all the email are stored in elasticsearch
    :return: Results from elasticsearch
    """
    try:
        if results := await elastic.search(index=index):
            if elastic:
                await elastic.index_document(index="files", document=results)
            return results["hits"], 200
        else:
            raise HTTPException(status_code=404, detail="Index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files")
async def search_files(index: str = "files") -> object:
    """
    Search for all files
    :param index: Index where all the files are stored in elasticsearch
    :return: Results from elasticsearch
    """
    try:
        if results := await elastic.search(index=index):
            if elastic is not None:
                await elastic.index_document(index="files", document=results)
            return results["hits"]
        else:
            raise HTTPException(status_code=404, detail="Index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/metadata")
async def extract_metadata(url: model.Url = Body(example={"url": EXTRACTOR_EXAMPLE})) -> object:
    """
    Extracts metadata from a pdf file and stores it in elasticsearch
    :param url: File's url
    :return: Metadata extracted from pdf file
    """
    try:
        if results := await Extractor.extract_metadata_from_online_pdf(url.url):
            if elastic is not None:
                await elastic.index_document(index="files", document=results)
            return results
        else:
            raise HTTPException(status_code=500, detail="Failed to extract metadata")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/ip/{ip_address}")
async def analyze_ip(ip_address: str = Path(description="IP Address", example=ANALYZER_EXAMPLE)) -> object:
    """
    Analyze the IP Address using VT and stores results in elasticsearch
    :param ip_address: IP Address to analyze
    :return: VT results
    """
    try:
        if results := await analyzer.analyze_ip(ip_address):
            if elastic is not None:
                await elastic.index_document(index="ips", document=results)
            return results
        else:
            raise HTTPException(status_code=500, detail="Failed to analyze IP address")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scrap/emails")
async def scrap_emails(url: model.Url = Body(example={"url": SCRAPPER_EXAMPLE})) -> object:
    """
    Scrap emails and stores it in elasticsearch
    :param url: Url that contains the emails to be scrapped
    :return: Found emails
    """
    try:
        if results := await Scrapper.scrape_emails(url.url):
            if elastic is not None:
                await elastic.index_documents(index="emails", documents=results)
            return results
        else:
            raise HTTPException(status_code=500, detail="Failed to scrap emails")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/index/{index}")
async def delete_index(index: str = None) -> object:
    """
    Deletes an index from Elasticsearch
    This endpoint is only used to perform tests
    :param index: Index to be deleted
    :return: Status code of the operation
    """
    try:
        if results := await elastic.delete_index(index):
            return 200
        else:
            raise HTTPException(status_code=404, detail="Index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
