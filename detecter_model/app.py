import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from Detected_model import Model

app = FastAPI()

MODEL_PATH = "/app/best.pt"
model = Model(MODEL_PATH)

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
   
    suffix = os.path.splitext(file.filename)[1]
    if not suffix:
        suffix = ".jpg"
    
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        result = model.file_type(tmp_path)
        return {"products": result}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
