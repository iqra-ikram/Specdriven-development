import React, { useState, useEffect, useCallback } from 'react';
import styles from './styles.module.css';
import { useChatbot } from '../../theme/ChatbotContext';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

interface Position {
    top: number;
    left: number;
}

const TextSelectionPopup: React.FC = () => {
    const [selectedText, setSelectedText] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [position, setPosition] = useState<Position>({ top: 0, left: 0 });
    const { sendMessage, openChatbot } = useChatbot();
    const { i18n } = useDocusaurusContext();

    const handleTextSelection = useCallback(() => {
        const selection = window.getSelection();
        const text = selection?.toString().trim();

        if (text && text.length > 0) {
            setSelectedText(text);

            // Get the position of the selection
            const range = selection?.getRangeAt(0);
            const rect = range?.getBoundingClientRect();

            if (rect) {
                // Position the popup above the selection, centered
                setPosition({
                    top: rect.top + window.scrollY - 50, // 50px above the selection
                    left: rect.left + window.scrollX + (rect.width / 2) - 25, // Center the icon (50px wide / 2)
                });
                setShowPopup(true);
            }
        } else {
            setShowPopup(false);
            setSelectedText('');
        }
    }, []);

    const handleAskAI = useCallback(() => {
        if (selectedText) {
            // Open the chatbot
            openChatbot();

            // Send the message with the selected text as context
            // Small delay to ensure chatbot is open
            setTimeout(() => {
                const prompt = i18n.currentLocale === 'ur'
                    ? `Explain this in Urdu: "${selectedText}"`
                    : `Explain this: "${selectedText}"`;
                sendMessage(prompt, selectedText);
            }, 100);

            // Hide the popup and clear selection
            setShowPopup(false);
            setSelectedText('');
            window.getSelection()?.removeAllRanges();
        }
    }, [selectedText, sendMessage, openChatbot, i18n.currentLocale]);

    useEffect(() => {
        // Listen for mouseup events to detect text selection
        document.addEventListener('mouseup', handleTextSelection);

        // Also listen for selection change events
        document.addEventListener('selectionchange', handleTextSelection);

        // Hide popup when clicking elsewhere
        const handleClickOutside = (e: MouseEvent) => {
            const target = e.target as HTMLElement;
            if (!target.closest(`.${styles.popup}`)) {
                setShowPopup(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mouseup', handleTextSelection);
            document.removeEventListener('selectionchange', handleTextSelection);
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [handleTextSelection]);

    if (!showPopup) return null;

    return (
        <div
            className={styles.popup}
            style={{
                top: `${position.top}px`,
                left: `${position.left}px`,
            }}
        >
            <button
                className={styles.aiButton}
                onClick={handleAskAI}
                title="Ask AI about this text"
                aria-label="Ask AI about selected text"
            >
                <svg
                    className={styles.aiIcon}
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    {/* AI Sparkle Icon */}
                    <path
                        d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"
                        fill="currentColor"
                    />
                    <path
                        d="M19 4L19.5 5.5L21 6L19.5 6.5L19 8L18.5 6.5L17 6L18.5 5.5L19 4Z"
                        fill="currentColor"
                    />
                    <path
                        d="M19 16L19.5 17.5L21 18L19.5 18.5L19 20L18.5 18.5L17 18L18.5 17.5L19 16Z"
                        fill="currentColor"
                    />
                </svg>
            </button>
        </div>
    );
};

export default TextSelectionPopup;
