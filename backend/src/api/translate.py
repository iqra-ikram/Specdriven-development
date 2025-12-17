"""
Translation API Router
Provides endpoints for translating text to different languages
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from ..services.translate_service import (
    translate_text,
    translate_batch,
    get_supported_languages
)

router = APIRouter()

# Request/Response Models
class TranslateRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    target_language: str = Field(default="ur", description="Target language code (e.g., 'ur' for Urdu)")
    source_language: str = Field(default="en", description="Source language code (default: 'en')")

class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    detected_source: Optional[str] = None
    error: Optional[str] = None

class BatchTranslateRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to translate")
    target_language: str = Field(default="ur", description="Target language code")
    source_language: str = Field(default="en", description="Source language code")

class BatchTranslation(BaseModel):
    original: str
    translated: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    error: Optional[str] = None

class BatchTranslateResponse(BaseModel):
    translations: List[BatchTranslation]

class LanguagesResponse(BaseModel):
    languages: dict

# Endpoints
@router.post("/translate", response_model=TranslateResponse, tags=["translation"])
async def translate(request: TranslateRequest):
    """
    Translate text to target language
    
    Example request:
    ```json
    {
        "text": "What is Physical AI?",
        "target_language": "ur",
        "source_language": "en"
    }
    ```
    """
    try:
        result = translate_text(
            text=request.text,
            target_lang=request.target_language,
            source_lang=request.source_language
        )
        return TranslateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.post("/translate/batch", response_model=BatchTranslateResponse, tags=["translation"])
async def translate_multiple(request: BatchTranslateRequest):
    """
    Translate multiple texts to target language
    
    Example request:
    ```json
    {
        "texts": ["Hello", "Welcome", "Thank you"],
        "target_language": "ur",
        "source_language": "en"
    }
    ```
    """
    try:
        if not request.texts:
            raise HTTPException(status_code=400, detail="No texts provided")
        
        if len(request.texts) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 texts per request")
        
        results = translate_batch(
            texts=request.texts,
            target_lang=request.target_language,
            source_lang=request.source_language
        )
        
        return BatchTranslateResponse(translations=results)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")

@router.get("/translate/languages", response_model=LanguagesResponse, tags=["translation"])
async def get_languages():
    """
    Get list of supported languages
    
    Returns dictionary of language codes and names
    """
    languages = get_supported_languages()
    return LanguagesResponse(languages=languages)
