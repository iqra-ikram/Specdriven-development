import { useState, useCallback } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Cache to store translations and avoid repeated API calls
const translationCache: Record<string, string> = {};

export function useTranslation() {
    const { siteConfig } = useDocusaurusContext();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Get API base URL from site config or default
    const apiBaseUrl = siteConfig.customFields?.fastApiBaseUrl || 'http://localhost:8000';

    const translate = useCallback(async (text: string, targetLang: string = 'ur'): Promise<string> => {
        // If text is empty, return as is
        if (!text || !text.trim()) return text;

        // Check cache first
        const cacheKey = `${targetLang}:${text}`;
        if (translationCache[cacheKey]) {
            return translationCache[cacheKey];
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${apiBaseUrl}/api/translate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text,
                    target_language: targetLang,
                    source_language: 'en', // Assuming source is English
                }),
            });

            if (!response.ok) {
                throw new Error(`Translation failed: ${response.statusText}`);
            }

            const data = await response.json();
            const translatedText = data.translated_text;

            // Cache the result
            translationCache[cacheKey] = translatedText;

            return translatedText;
        } catch (err) {
            console.error('Translation error:', err);
            setError(err instanceof Error ? err.message : 'Unknown error');
            return text; // Fallback to original text
        } finally {
            setLoading(false);
        }
    }, [apiBaseUrl]);

    const translateBatch = useCallback(async (texts: string[], targetLang: string = 'ur'): Promise<string[]> => {
        if (!texts || texts.length === 0) return [];

        // Filter out cached texts
        const validTexts = texts.filter(t => t && t.trim());
        if (validTexts.length === 0) return texts;

        // Identify which texts need translation (not in cache)
        const textsToTranslate = validTexts.filter(t => !translationCache[`${targetLang}:${t}`]);

        if (textsToTranslate.length === 0) {
            // All in cache
            return validTexts.map(t => translationCache[`${targetLang}:${t}`] || t);
        }

        setLoading(true);
        try {
            const response = await fetch(`${apiBaseUrl}/api/translate/batch`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    texts: textsToTranslate,
                    target_language: targetLang,
                    source_language: 'en',
                }),
            });

            if (!response.ok) {
                throw new Error('Batch translation failed');
            }

            const data = await response.json();

            // Update cache
            data.translations.forEach((item: any) => {
                if (item.original && item.translated) {
                    translationCache[`${targetLang}:${item.original}`] = item.translated;
                }
            });

            // Return all translations (from cache)
            return validTexts.map(t => translationCache[`${targetLang}:${t}`] || t);

        } catch (err) {
            console.error('Batch translation error:', err);
            // Fallback
            return texts;
        } finally {
            setLoading(false);
        }
    }, [apiBaseUrl]);

    return { translate, translateBatch, loading, error };
}
