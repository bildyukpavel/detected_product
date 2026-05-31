import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from check import Check_detecter

app = FastAPI()


checker = Check_detecter()

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    
    suffix = os.path.splitext(file.filename)[1]
    if not suffix:
        suffix = ".jpg"

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        items = checker.result_check(tmp_path)
        return {"check": items}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
