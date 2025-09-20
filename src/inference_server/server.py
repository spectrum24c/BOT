from fastapi import FastAPI, Request
import onnxruntime as ort
import numpy as np
import json
import os

app = FastAPI()

MODEL_PATH = os.getenv('ONNX_MODEL_PATH', '../../sample_data/xgb_model.onnx')
session = None
if os.path.exists(MODEL_PATH):
    session = ort.InferenceSession(MODEL_PATH)

@app.post('/infer')
async def infer(request: Request):
    data = await request.json()
    features = np.array(data['features']).astype(np.float32)
    if session:
        input_name = session.get_inputs()[0].name
        output = session.run(None, {input_name: features})
        return {'prediction': float(output[0][0])}
    else:
        return {'error': 'Model not loaded'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
