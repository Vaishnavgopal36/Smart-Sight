# backend/server/app/routes.py
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

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(None), query: str = Form(""), session_id: str = Form("default")
):
    logger.info(f"Received request: file={file.filename if file else 'None'}, query='{query}', session_id='{session_id}'")
    try:
        # Validate input
        if not file and not query:
            logger.warning("No file or query provided")
            raise HTTPException(status_code=400, detail="Either a file or query must be provided.")

        # Process image if provided
        image = None
        if file:
            logger.info(f"Processing file: {file.filename}")
            image_bytes = await file.read()
            if not image_bytes:
                logger.warning("Uploaded file is empty")
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            try:
                image = Image.open(io.BytesIO(image_bytes))
                image.verify()
                image = Image.open(io.BytesIO(image_bytes))
                logger.info("Image verified successfully")
            except UnidentifiedImageError as e:
                logger.error(f"Invalid image: {str(e)}")
                raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")
            except Exception as e:
                logger.error(f"Image processing error: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")


        # Define a global variable to store the last uploaded image
        global img
        if 'img' not in globals():
            img = None

        # Generate query embedding
        logger.info("Generating query embedding")
        query_embedding = None
        try:
            if file and query:
                logger.info("Generating joint image-text embedding with new upload")
                img = image
                query_embedding = get_joint_embedding(img, query)
            elif file:
                logger.info("Generating image-only embedding")
                img = image
                query_embedding = get_image_embedding(img)
            else:
                logger.info("Generating embedding with text and last uploaded image if available")
                if img is not None and query:
                    query_embedding = get_joint_embedding(img, query)
                elif query:
                    query_embedding = get_text_embedding(query)
                else:
                    raise ValueError("No valid input provided for embedding")
        except ValueError as e:
            logger.error(f"ValueError in embedding generation: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid input for embedding: {str(e)}")
        except Exception as e:
            logger.error(f"Embedding generation error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")


        # Search FAISS index
        logger.info("Searching FAISS index")
        try:
            results = search_faiss(query_embedding, top_k=1)
            print(results)
            if not results:
                logger.warning("No similar images found")
                raise HTTPException(status_code=404, detail="No similar images found.")
            logger.info(f"FAISS search results: {results}")
        except Exception as e:
            logger.error(f"FAISS search error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"FAISS search failed: {str(e)}")

        # Copy files and prepare results
        retrieved_images = []
        retrieved_captions = []
        for img_path, caption in results:
            img_filename = os.path.basename(img_path)  # Extract filename only
            static_img_path = os.path.join(STATIC_DIR, img_filename)
            # Convert relative path from .paths to absolute path
            abs_img_path = os.path.normpath(os.path.join(BASE_IMAGE_DIR, img_filename))
            try:
                logger.info(f"Copying {abs_img_path} to {static_img_path}")
                shutil.copy(abs_img_path, static_img_path)
            except FileNotFoundError as e:
                logger.warning(f"Image file {abs_img_path} not found: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"File copy error: {str(e)}", exc_info=True)
                continue

            retrieved_images.append(f"http://localhost:8000/static/{img_filename}")
            retrieved_captions.append(caption)

        logger.info(f"Retrieved Images: {retrieved_images}")
        logger.info(f"Retrieved Captions: {retrieved_captions}")

        # Query Gemini
        logger.info("Querying Gemini")
        try:
            llm_response = query_gemini(query, retrieved_captions, session_id)
            logger.info(f"LLM Response: {llm_response}")
        except Exception as e:
            logger.error(f"Gemini query error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Gemini query failed: {str(e)}")

        # Return full response
        logger.info("Request processed successfully")
        return JSONResponse(content={
            "message": "Request processed successfully!",
            "similar_images": retrieved_images,
            "retrieved_captions": retrieved_captions,
            "llm_response": llm_response,
            "session_id": session_id
        })

    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")