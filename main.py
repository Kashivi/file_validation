from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 79 * 1024
VALID_EXTENSIONS = [".csv", ".json", ".txt"]
REQUIRED_TOKEN = "lh9qejkamtficrrn"


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_1092: str = Header(None)
):

    # 1️⃣ Check token
    if x_upload_token_1092 != REQUIRED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2️⃣ Validate extension
    if not any(file.filename.endswith(ext) for ext in VALID_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    # 3️⃣ Validate size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 4️⃣ Process CSV
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        return {
            "email": "23f3004276@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "totalValue": float(df["value"].sum()),
            "categoryCounts": df["category"].value_counts().to_dict()
        }

    return {"message": "File validated"}