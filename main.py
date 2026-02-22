from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 79 * 1024
VALID_EXTENSIONS = [".csv", ".json", ".txt"]
REQUIRED_TOKEN = "lh9qejkamtficrrn"


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):

    # 🔥 Read header manually (robust method)
    token = request.headers.get("x-upload-token-1092")

    if token != REQUIRED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not any(file.filename.endswith(ext) for ext in VALID_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    return {
        "email": "23f3004276@ds.study.iitm.ac.in",
        "filename": file.filename,
        "rows": len(df),
        "columns": df.columns.tolist(),
        "totalValue": round(float(df["value"].sum()), 2),
        "categoryCounts": df["category"].value_counts().to_dict()
    }

    return {"message": "File validated"}


