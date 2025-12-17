import React from 'react';
import Layout from '@theme-original/Layout';
import type { Props } from '@theme/Layout';
import { ChatbotProvider } from '../ChatbotContext'; // Adjust path as necessary
import ChatbotWidget from '../../components/ChatbotWidget'; // Adjust path as necessary

export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <ChatbotProvider>
      <Layout {...props}>
        {props.children}
        <ChatbotWidget />
      </Layout>
    </ChatbotProvider>
  );
}
