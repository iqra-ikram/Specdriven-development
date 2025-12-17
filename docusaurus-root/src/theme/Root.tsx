import React from 'react';
import { ChatbotProvider } from './ChatbotContext';
import TextSelectionPopup from '../components/TextSelectionPopup';

// Docusaurus Root component - wraps the entire app
export default function Root({ children }: { children: React.ReactNode }) {
    return (
        <ChatbotProvider>
            {children}
            <TextSelectionPopup />
        </ChatbotProvider>
    );
}
