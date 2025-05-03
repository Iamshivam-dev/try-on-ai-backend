# app/api/v1/controllers/file_controller.py

from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import requests
from typing import Optional
import os


router = APIRouter()
REPLICATE_API_TOKEN=os.getenv("REPLICATE_API_TOKEN")
IMGBB_API_TOKEN=os.getenv("IMGBB_API_TOKEN")
@router.get('/test')
async def test():
    return JSONResponse(content={"success": True})

async def upload_to_fileio(file: UploadFile):
    url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_TOKEN}"
    contents = await file.read()
    print("Working till here")
    response = requests.post(url, files={"image": (file.filename, contents)})
    print("Got response")
    print(response.json())
    if response.ok:
        return response.json()["data"]['url']
    raise Exception("File upload failed")

async def run_virtual_tryon(user_image: UploadFile, cloth_image: UploadFile) -> Optional[str]:
    user_image_url = await upload_to_fileio(user_image)
    cloth_image_url = await upload_to_fileio(cloth_image)
    print("--------------------------------")
    print(user_image_url)
    print(cloth_image_url)
    print("--------------------------------")
    replicate_url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "17fcdc4ce5364f40e0b9c12e8c2ea9379e5d6641b1603fbea16eaac57f50141b",
        "input": {
            "human_img": user_image_url,
            "garm_img": cloth_image_url,
            "category": "upper_body",
            "garment_des": "grey casual top"
        }
    }
    response = requests.post(replicate_url, headers=headers, json=data)
    if response.status_code == 201:
        prediction = response.json()
        print(prediction)
        return prediction
    else:
        print("---------------")
        print(response.json())
        print("---------------")
        return None


@router.post("/upload")
async def upload_file(user_image: UploadFile = File(...), cloth_image: UploadFile = File(...)):
    result = None
    try:
        result = await run_virtual_tryon(user_image, cloth_image)
    except Exception as e:
        print(f"Error during file upload: {e}")
    if result:
        return {"status": "success", "result_id": result["id"]}
    else:
        return {"status": "error", "message": "Virtual try-on failed."}
    
    
@router.get("/check_status")
async def check_status(id: str ): 
    url = f"https://api.replicate.com/v1/predictions/{id}"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        prediction = response.json()
        print(prediction)
        return {"status": prediction["status"], "output": prediction["output"]}
    else:
        return {"status": "error", "output": None}

