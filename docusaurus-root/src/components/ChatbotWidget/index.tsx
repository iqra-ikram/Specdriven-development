
import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';
import { useChatbot } from '../../theme/ChatbotContext'; // Import useChatbot 
import { useTranslation } from '../../hooks/useTranslation'; // Import useTranslation hook 
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

interface Reference {
  url: string;
  title?: string;
}

// Update ChatMessage interface to include references
interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  references?: Reference[]; // Optional array of references
}

const ChatbotWidget: React.FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Use the chatbot context
  const { messages, sendMessage, isLoading, error, isOpen, openChatbot, closeChatbot } = useChatbot();
  const { translate } = useTranslation();
  const { i18n } = useDocusaurusContext();
  const isUrdu = i18n.currentLocale === 'ur';

  // UI Strings state
  const [uiText, setUiText] = useState({
    title: 'AI Assistant',
    placeholder: 'Ask a question...',
    send: 'Send',
    empty: 'Type a question to get started!',
    thinking: 'Thinking...',
    error: 'Failed to connect'
  });

  useEffect(() => {
    if (isUrdu) {
      // Parallel translation for better performance
      Promise.all([
        translate('AI Assistant', 'ur'),
        translate('Ask a question...', 'ur'),
        translate('Send', 'ur'),
        translate('Type a question to get started!', 'ur'),
        translate('Thinking...', 'ur')
      ]).then(([title, placeholder, send, empty, thinking]) => {
        setUiText({ title, placeholder, send, empty, thinking, error: 'رابطہ کرنے میں ناکام' });
      });
    } else {
      // Reset to English
      setUiText({
        title: 'AI Assistant',
        placeholder: 'Ask a question...',
        send: 'Send',
        empty: 'Type a question to get started!',
        thinking: 'Thinking...',
        error: 'Failed to connect'
      });
    }
  }, [isUrdu, translate]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
    if (inputMessage.trim() === '') return;

    // Call sendMessage from context
    await sendMessage(inputMessage);
    setInputMessage('');
  };

  return (
    <div className={styles.chatbotContainer}>
      <button
        className={styles.toggleButton}
        onClick={() => isOpen ? closeChatbot() : openChatbot()}
        title={isOpen ? 'Close Chat' : 'Open Chat'}
        aria-label={isOpen ? 'Close Chat' : 'Open Chat'}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 12H8.01M12 12H12.01M16 12H16.01M21 12C21 16.4183 16.9706 20 12 20C10.4607 20 9.01172 19.6565 7.74467 19.0511L3 20L4.39499 16.28C3.51156 15.0423 3 13.5743 3 12C3 7.58172 7.02944 4 12 4C16.9706 4 21 7.58172 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className={styles.headerIcon}
              >
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#4ade80" />
                    <stop offset="100%" stopColor="#16a34a" />
                  </linearGradient>
                </defs>
                <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="url(#gradient)" />
                <path d="M19 4L19.5 5.5L21 6L19.5 6.5L19 8L18.5 6.5L17 6L18.5 5.5L19 4Z" fill="url(#gradient)" />
                <path d="M19 16L19.5 17.5L21 18L19.5 18.5L19 20L18.5 18.5L17 18L18.5 17.5L19 16Z" fill="url(#gradient)" />
              </svg>
              {uiText.title}
            </h3>
            <button className={styles.closeButton} onClick={closeChatbot}>
              &times;
            </button>
          </div>
          <div className={styles.messageList}>
            {messages.length === 0 ? (
              <div className={styles.emptyChat}>{uiText.empty}</div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`${styles.messageBubble} ${message.sender === 'user' ? styles.userMessage : styles.botMessage
                    }`}
                >
                  <p>{message.text}</p>
                  {message.references && message.references.length > 0 && (
                    <div className={styles.referencesContainer}>
                      <strong>References:</strong>
                      <ul>
                        {message.references.map((ref, index) => (
                          <li key={index}>
                            <a href={ref.url} target="_blank" rel="noopener noreferrer">
                              {ref.title || ref.url}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && <div className={styles.loadingMessage}>{uiText.thinking}</div>}
            {error && <div className={styles.errorMessage}>{error}</div>}
            <div ref={messagesEndRef} />
          </div>
          <div className={styles.chatInputContainer}>
            <input
              type="text"
              className={styles.chatInput}
              placeholder={uiText.placeholder}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              disabled={isLoading}
            />
            <button className={styles.sendButton} onClick={handleSendMessage} disabled={isLoading}>
              {uiText.send}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotWidget;
