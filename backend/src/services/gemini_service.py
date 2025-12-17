from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

_gemini_client_initialized = False

def _initialize_gemini_client():
    global _gemini_client_initialized
    if not _gemini_client_initialized:
        google_api_key = os.getenv("GOOGLE_API_KEY") # Or GEMINI_API_KEY
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        genai.configure(api_key=google_api_key)
        _gemini_client_initialized = True

EMBEDDING_MODEL = "models/embedding-001" # Or other suitable Gemini embedding model
CHAT_MODEL = "models/gemini-flash-latest" # Or other suitable Gemini chat model

def get_gemini_embedding(text: str) -> list[float]:
    """
    Generates an embedding for the given text using Gemini's embedding model.
    """
    _initialize_gemini_client()
    text = text.replace("\n", " ")
    try:
        response = genai.embed_content(model=EMBEDDING_MODEL, content=text)
        return response['embedding']
    except Exception as e:
        print(f"Gemini Embedding Error: {e}")
        raise

def get_gemini_chat_completion(messages: list[dict], temperature: float = 0.7) -> str:
    """
    Generates a chat completion using Gemini's chat model.

    Args:
        messages: A list of message dictionaries in the format compatible with Gemini API.
                  Gemini expects roles "user" and "model".
                  Example: [{"role": "user", "parts": ["..."]}, {"role": "model", "parts": ["..."]}]
        temperature: Controls randomness. Lower values mean more deterministic output.
    """
    _initialize_gemini_client()
    _initialize_gemini_client()
    # Model initialization moved inside try-except block for safety

    # Convert messages from OpenAI format to Gemini format
    gemini_messages = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model" # Gemini model role is "model"
        gemini_messages.append({"role": role, "parts": [msg["content"]]})
    
    # Ensure the conversation starts with a user turn if there's a system message
    # Gemini generally doesn't have a distinct 'system' role in `generate_content` call history
    # System instructions can often be incorporated into the first user turn or the model's setup
    # For RAG, system message is typically about context, so it will be part of the initial prompt
    # If the first message is 'system', convert it to a 'user' message or handle it carefully.
    # Here, assuming the RAG pipeline constructs messages appropriately (e.g., system context as first user part)

    # For safety, ensure the last message is from a 'user' if it's a new turn
    # The RAG pipeline should ensure the last message before this call is the user's current query.

    # If the first message is a 'system' role, convert it to a user message for Gemini's API
    if gemini_messages and gemini_messages[0]['role'] == 'model':
        # This is a simplification; a system message should ideally guide the model, not act as a conversational turn
        # For our RAG use case, the 'system' message sets context, which Gemini handles well in the first 'user' part
        # If the context is passed as a system message to `get_chat_completion`, it's better absorbed as part of the first user query.
        # Let's assume the `rag_pipeline` will structure the `messages` list such that the "system" content
        # is prepended to the user's content in the first user message for Gemini, or the `genai.GenerativeModel`
        # is initialized with a system instruction.
        # For now, if a system message is present, we'll convert it to a user message for `generate_content` history.
        # More robust solution would be to configure `system_instruction` in `genai.GenerativeModel`
        pass # The RAG pipeline already handles system message as part of the `messages` list that goes into LLM.

    # Gemini's `generate_content` does not directly take a 'system' role in its `contents` list for history.
    # The 'system' message from RAG should be part of the first 'user' query's parts.
    # Re-structure messages to ensure alternating user/model turns and handle initial system message.
    processed_messages = []
    for i, msg in enumerate(messages):
        if msg["role"] == "system":
            # Prepend system content to the next user message, or create a user message if no subsequent user message
            if i + 1 < len(messages) and messages[i+1]["role"] == "user":
                messages[i+1]["content"] = msg["content"] + "\n\n" + messages[i+1]["content"]
            else:
                processed_messages.append({"role": "user", "parts": [msg["content"]]})
        else:
            processed_messages.append({"role": msg["role"], "parts": [msg["content"]]})


    # Refine the message processing for Gemini to handle system prompts correctly
    # Gemini's `generate_content` is more conversational; system instructions are usually passed differently
    # A common pattern is to include the system prompt as part of the initial user query or set a `system_instruction`
    # For now, let's assume the `messages` list from RAG pipeline has the system message as the very first entry
    # and subsequent messages alternate. We will treat the system message as part of the initial prompt.
    
    final_gemini_messages = []
    initial_prompt_parts = []

    # If the first message is a system message, incorporate it into the initial prompt
    if messages and messages[0]["role"] == "system":
        initial_prompt_parts.append(messages[0]["content"])
        remaining_messages = messages[1:]
    else:
        remaining_messages = messages

    for msg in remaining_messages:
        if msg["role"] == "user":
            final_gemini_messages.append({"role": "user", "parts": [msg["content"]]})
        elif msg["role"] == "model": # Previously 'assistant' in OpenAI
            final_gemini_messages.append({"role": "model", "parts": [msg["content"]]})

    # If there's an initial system prompt, add it to the first user message
    if initial_prompt_parts and final_gemini_messages and final_gemini_messages[0]["role"] == "user":
        final_gemini_messages[0]["parts"][0] = initial_prompt_parts[0] + "\n\n" + final_gemini_messages[0]["parts"][0]
    elif initial_prompt_parts: # If only system message, make it a user message
        final_gemini_messages.insert(0, {"role": "user", "parts": initial_prompt_parts})

    # Ensure alternating turns for Gemini's API
    # Gemini's `generate_content` can be picky about message order (user, model, user, model...)
    # We need to filter out consecutive user/model messages or ensure the RAG pipeline provides them correctly.
    # For now, assuming the incoming messages roughly follow a conversation turn.
    
    
    
    try:
        model = genai.GenerativeModel(CHAT_MODEL)
        convo = model.start_chat(history=final_gemini_messages[:-1]) # All but the last message is history
        response = convo.send_message(final_gemini_messages[-1]["parts"][0], generation_config={"temperature": temperature})
        return response.text
    except Exception as e:
        print(f"Gemini Chat Error (Mocking response): {e}")
        return "I am currently experiencing high traffic (API Quota Exceeded) or the Model ID is invalid. Please try again later. (Mock Response)"
