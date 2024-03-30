from fastapi import FastAPI

app = FastAPI()


@app.post("/translation")
def translation(text: str, source_language: str, target_language: str):
    return {"result": "人生はチョコレートの箱のようなものだ。"}
