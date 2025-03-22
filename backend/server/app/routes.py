# backend/server/app/routes.py
from settings import API_BASE_URL  # Import API_BASE_URL
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import io
import shutil
import os
from settings import STATIC_DIR
from PIL import Image, UnidentifiedImageError
from utils import get_image_embedding, get_joint_embedding, get_text_embedding, search_faiss
from memory import query_gemini
import logging

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Configure logging to console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("debug.log")
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()

# Base directory for images, absolute path from backend/server/app/ to backend/database/images/
BASE_IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "images"))

@router.get("/test/")
async def test_endpoint():
    logger.info("Test endpoint called")
    return {"message": "Test successful"}

@router.post("/reset/")
async def reset_backend():
    from memory import reset_memory
    import shutil

    # Reset session memory
    reset_memory()

    # Reset retrieved images and captions
    global retrieved_images, retrieved_captions, img
    retrieved_images = []
    retrieved_captions = []
    img = None

    # Clear static folder
    try:
        for filename in os.listdir(STATIC_DIR):
            file_path = os.path.join(STATIC_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("✅ Static folder cleared successfully.")
    except Exception as e:
        return {"message": f"Error clearing static folder: {str(e)}"}

    print("✅ Retrieved images, captions, and last uploaded image reset successfully.")
    return {"message": "Backend reset successfully!"}


@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(None), query: str = Form(""), session_id: str = Form("default")
):
    logger.info(f"Received request: file={file.filename if file else 'None'}, query='{query}', session_id='{session_id}'")
    try:
        if not file and not query:
            raise HTTPException(status_code=400, detail="Either a file or query must be provided.")

        image = None
        if file:
            image_bytes = await file.read()
            if not image_bytes:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            try:
                image = Image.open(io.BytesIO(image_bytes))
                image.verify()
                image = Image.open(io.BytesIO(image_bytes))
            except UnidentifiedImageError:
                raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        global img
        if 'img' not in globals():
            img = None

        query_embedding = None
        if file and query:
            img = image
            query_embedding = get_joint_embedding(img, query)
        elif file:
            img = image
            query_embedding = get_image_embedding(img)
        elif query:
            query_embedding = get_joint_embedding(img, query) if img else get_text_embedding(query)
        else:
            raise ValueError("No valid input for embedding")

        logger.info("Searching FAISS index")
        try:
            results = search_faiss(query_embedding, top_k=1)  # Increase k if needed
            if not results:
                raise HTTPException(status_code=404, detail="No similar images found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"FAISS search failed: {str(e)}")

        retrieved_images = []
        retrieved_captions = []
        similarity_percentages = []
        is_image_found = False

        for img_path, caption, similarity in results:  # Assuming (image_path, caption, similarity_score)
            similarity_percentage = round(similarity * 100, 2)
            similarity_percentages.append(similarity_percentage)
            logger.info(f"Similarity Score: {similarity_percentage}% for image {img_path} and caption {caption}")  # Logs similarity score
            
            if similarity_percentage > 50:
                is_image_found = True
                img_filename = os.path.basename(img_path)
                static_img_path = os.path.join(STATIC_DIR, img_filename)
                abs_img_path = os.path.normpath(os.path.join(BASE_IMAGE_DIR, img_filename))
                
                try:
                    shutil.copy(abs_img_path, static_img_path)
                except FileNotFoundError:
                    continue
                
                retrieved_images.append(f"{API_BASE_URL}/static/{img_filename}")
                retrieved_captions.append(caption)

        if not is_image_found:
            retrieved_captions = None

        llm_response = query_gemini(query, retrieved_captions, session_id)

        return JSONResponse(content={
            "message": "Request processed successfully!",
            "similar_images": retrieved_images,
            "retrieved_captions": retrieved_captions,
            "similarity_scores": similarity_percentages,
            "is_image_found": is_image_found,
            "llm_response": llm_response,
            "session_id": session_id
        })

    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
