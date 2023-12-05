from fastapi import FastAPI, Body, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
import requests
from functools import cache
from bs4 import BeautifulSoup
import spacy
from pydantic import BaseModel
from transformers import pipeline
import time
import csv
from datetime import datetime
import io

class SentimentAnalysis(BaseModel):
    title: str  
    sentiment: str 
    range: float
    execution_time: float 

class NLPAnalysis(BaseModel):
    pos_tags: list  
    ner_tags: list  
    embedding: list  

nombre= None
info_predict= None
tiempo =None
def articleAnalytics(text, nlp, title, sentiment_pipeline):
    start_time = time.time()  
    doc = nlp(text)
    max_token_length = 512
    text_parts = [text[i:i+max_token_length] for i in range(0, len(text), max_token_length)]
    sentiment_results = [sentiment_pipeline(part) for part in text_parts]
    sentiment_score = int(sentiment_results[-1][0]['label'].split()[0]) if sentiment_results else 0
    if sentiment_score == 1:
        sentiment = 'Muy Negativo'
        rango = -1.0
    elif sentiment_score == 2:
        sentiment = 'Negativo'
        rango = -0.5
    elif sentiment_score == 3:
        sentiment = 'Neutral'
        rango = 0.0
    elif sentiment_score == 4:
        sentiment = 'Positivo'
        rango = 0.5
    elif sentiment_score == 5:
        sentiment = 'Muy Positivo'
        rango = 1
    execution_time = time.time() - start_time  
    sentiment_results = SentimentAnalysis(
        title=title,
        sentiment=sentiment,
        range=rango,
        execution_time=execution_time
    )
    global nombre
    global info_predict
    global tiempo
    nombre = str(title)
    info_predict= sentiment
    tiempo = execution_time
    pos_tags = [token.pos_ for token in doc]
    ner_tags = [(ent.text, ent.label_) for ent in doc.ents]
    embedding = doc.vector.tolist()
    nlp_results = NLPAnalysis(
        pos_tags=pos_tags,
        ner_tags=ner_tags,
        embedding=embedding
    )
    return sentiment_results, nlp_results

app = FastAPI(title="Detector de noticia ELDEBER")

@cache
def get_nlp():
    return spacy.load("es_core_news_md")

@app.get("/status")
def get_status():
    model_info = {
        "model_name": "Deteccion de noticias",
        "tipo": "spacy",
        "status": "en linea",
        "author": "Pablo Badani"
    }

    model_info2 = {
        "model_name": "Deteccion de sentimiento",
        "tipo": "nlp",
        "status": "en linea",
        "author": "Pablo Badani"
    }

    service_info = {
        "service_name": "Detector de noticia ELDEBER",
        "status": "online"
    }

    return {
        "model_info": model_info,
        "model_info2": model_info2,
        "service_info": service_info
    }

@app.post("/sentiment")
def analyze_news(urls: list = Body(...), nlp=Depends(get_nlp)):
    results_list = []
    sentiment_pipeline = pipeline("text-classification", model="karina-aquino/spanish-sentiment-model")

    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Request for {url} failed!")
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        text_elements = soup.find_all("div", class_="text-editor")

        if text_elements:
            texts = [elem.get_text() for elem in text_elements]
            article_title = soup.title.text.strip() if soup.title else "No Title"
            sentiment_results, _ = articleAnalytics(texts[0], nlp, article_title, sentiment_pipeline)
            results_list.append(sentiment_results)
        else:
            results_list.append({"error": f"No text found for {url}"})

    return results_list

@app.post("/analysis")
def perform_analysis(url: str = Body(...), nlp=Depends(get_nlp)):

    sentiment_pipeline = pipeline("text-classification", model="karina-aquino/spanish-sentiment-model")

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Request for {url} failed!")

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    text_elements = soup.find_all("div", class_="text-editor")

    if text_elements:
        texts = [elem.get_text() for elem in text_elements]
        article_title = soup.title.text.strip() if soup.title else "No Title"
        sentiment_results, nlp_results = articleAnalytics(texts[0], nlp, article_title, sentiment_pipeline)
        return {"sentiment_results": sentiment_results, "nlp_results": nlp_results}
    else:
        raise HTTPException(status_code=404, detail=f"No text found for {url}")
    
@app.get("/reports")
def generate_report():
    global nombre
    global info_predict
    global tiempo
    if nombre is None:
        return {"error": "No se ha hecho ninguna prediccion"}
    with open("report.csv", mode="a", newline="") as csvfile:
        fieldnames = [
            "Nombre de la noticia",
            "Prediccion",
            "Fecha",
            "Execution Time",
            "Modelos",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
        {
            "Nombre de la noticia": nombre,
            "Prediccion": info_predict,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Execution Time": tiempo,
            "Modelos": "spacy & nlp",
        }
    )
    with open("report.csv", mode="r", newline="") as csvfile:
        content = csvfile.read()
        return StreamingResponse(io.StringIO(content), media_type="text/csv")
