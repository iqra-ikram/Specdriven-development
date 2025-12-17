https://iqra7-physical-ai-backend.hf.space/ 

To add secrets to your backend, you should use the Hugging Face Space settings:

1.  **Navigate to your Space settings:** Go to `https://huggingface.co/spaces/Iqra7/physical-ai-backend`.
2.  **Access "Settings":** Click on the "Settings" tab for your Space.
3.  **Add/Manage "Repository secrets" or "Space secrets":** Find the section for "Repository secrets," "Space secrets," or "Environment Variables." Here, you can add key-value pairs (e.g., `OPENAI_API_KEY`, `DATABASE_URL`, `FRONTEND_URL`) that will be securely injected as environment variables into your Space's runtime.

Avoid committing `.env` files with production secrets to your repository.