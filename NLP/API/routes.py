from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from fastapi.middleware.cors import CORSMiddleware
from API.config import fsi,fs
import subprocess
import io

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=2) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    file_id = fs.put(file.file, filename=file.filename)
    background_tasks.add_task(run_translation, file.filename)
    return {"message": "File berhasil diupload & sedang diproses", "filename": file.filename, "file_id": str(file_id)}
def run_translation(filename: str):
    subprocess.run(["python", "API/main.py", filename], check=False)  

# simpan ke mongodb


@app.get("/translated/{filenames}")
async def get_translated_file(filenames: str):

    file_data = fsi.find_one({"filenames": filenames})

    if not file_data:
        raise HTTPException(status_code=404, detail="File hasil terjemahan tidak ditemukan")

    return StreamingResponse(io.BytesIO(file_data.read()), media_type="application/pdf",
                             headers={"Content-Disposition": f"attachment; filename={filenames}"})

