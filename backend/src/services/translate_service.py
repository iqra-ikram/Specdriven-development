"""
Translation Service using Deep Translator
Provides free translation functionality for the backend API
"""
from deep_translator import GoogleTranslator
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def translate_text(text: str, target_lang: str = "ur", source_lang: str = "en") -> Dict[str, str]:
    """
    Translate text to target language
    
    Args:
        text: Text to translate
        target_lang: Target language code (default: 'ur' for Urdu)
        source_language: Source language code (default: 'en' for English)
        
    Returns:
        Dictionary with original text, translated text, and language codes
    """
    try:
        # Deep Translator GoogleTranslator
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        
        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "detected_source": source_lang # approximate
        }
    except Exception as e:
        logger.error(f"Translation error: {e}")
        # Return original text if translation fails
        return {
            "original_text": text,
            "translated_text": text,
            "source_language": source_lang,
            "target_language": target_lang,
            "error": str(e)
        }

def translate_batch(texts: List[str], target_lang: str = "ur", source_lang: str = "en") -> List[Dict[str, str]]:
    """
    Translate multiple texts to target language
    
    Args:
        texts: List of texts to translate
        target_lang: Target language code
        source_lang: Source language code
        
    Returns:
        List of translation results
    """
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        results = translator.translate_batch(texts)
        
        translations = []
        for original, result in zip(texts, results):
            translations.append({
                "original": original,
                "translated": result,
                "source_language": source_lang,
                "target_language": target_lang
            })
        
        return translations
    except Exception as e:
        logger.error(f"Batch translation error: {e}")
        # Return original texts if translation fails
        return [
            {
                "original": text,
                "translated": text,
                "error": str(e)
            }
            for text in texts
        ]

# Supported languages (subset for display, Deep Translator supports many)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "ur": "Urdu",
    "ar": "Arabic",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh-CN": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean"
}

def get_supported_languages() -> Dict[str, str]:
    """Get dictionary of supported language codes and names"""
    return SUPPORTED_LANGUAGES
