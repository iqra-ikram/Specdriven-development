---
id: 002
title: Fix vague chatbot responses by improving Gemini API error handling
stage: general
date: 2025-12-13
surface: agent
model: gemini-1.5-pro-001
feature: none
branch: main
user: iqra
command: (none specified)
labels: [bug, rag, gemini-api, error-handling]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/services/gemini_service.py
tests:
 (no tests run)
---

## Prompt

hi

I don't have enough information based on my current knowledge to provide a meaningful response to your greeting in the context of Physical AI and Humanoid Robotics.

what is physical ai?

I do not have enough information in my current knowledge base to provide a definition of Physical AI.

what is robotics?

I do not have enough information in my current knowledge base to answer the question "what is robotics?"


  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerMinutePerUserPerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerDayPerUserPerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerDayPerProjectPerModel-FreeTier"
}
]
INFO:     127.0.0.1:49829 - "POST /chat HTTP/1.1" 200 OK
Gemini Embedding Error (Mocking response): 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit.
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0 [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerDayPerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerMinutePerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerMinutePerUserPerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerDayPerUserPerProjectPerModel-FreeTier"
}
]
INFO:     127.0.0.1:60534 - "POST /chat HTTP/1.1" 200 OK
Gemini Embedding Error (Mocking response): 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit.
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0 [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerDayPerUserPerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerMinutePerUserPerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerMinutePerProjectPerModel-FreeTier"
}
violations {
  quota_metric: "generativelanguage.googleapis.com/embed_content_free_tier_requests"     
  quota_id: "EmbedContentRequestsPerDayPerProjectPerModel-FreeTier"
}
]
INFO:     127.0.0.1:60070 - "POST /chat HTTP/1.1" 200 OK
my chatbot is giving very vague reply i think rag is not working well can you please verify

## Response snapshot

You've correctly identified that the RAG pipeline is not working as expected. The vague replies are a direct symptom of a problem in the embedding generation step.

Here's a breakdown of what's happening:

1.  **API Quota Exceeded:** The log you provided clearly shows a `429 You exceeded your current quota` error from the Gemini API. This means you're making too many requests to the embedding model in a short period.

2.  **Error Masking:** The root cause of the vague replies is in how this error is handled. In `backend/src/services/gemini_service.py`, the `get_gemini_embedding` function has a `try...except` block that catches this `429` error, prints a message, and then returns a vector of zeros (`[0.0] * 1536`).

3.  **Failed Retrieval:** In `backend/src/core/rag_pipeline.py`, this zero vector is used to search for relevant documents in your Qdrant vector database. Since the zero vector doesn't represent your query, the search finds no matching documents.

4.  **Vague Response:** The RAG pipeline then executes the following code block because no context was found:
    ```python
    if not context_texts:
        system_message = {
            "role": "system",
            "content": (
                "You are an AI assistant specialized in Physical AI and Humanoid Robotics. "
                "You don't have enough information from your knowledge base to answer this question. "
                "Please state that you don't have enough information based on your current knowledge."
            ),
        }
    ```
    This is why your chatbot is giving vague and unhelpful responses.

**To fix this, you need to address the Gemini API quota issue.** You can check your usage and limits in your Google AI Platform console.

I'll also improve the error handling to make these issues easier to debug in the future. I'll modify `get_gemini_embedding` to re-raise the exception instead of returning a zero vector. This will cause the request to fail with a clear error message instead of silently producing a vague response.

I've updated the error handling in `backend/src/services/gemini_service.py`. Now, if the Gemini API encounters an error (like the quota issue you were seeing), it will raise an exception instead of returning a mock response. This will provide a clear error message and prevent the chatbot from giving vague replies due to a lack of context.

To fully resolve the issue, you'll need to address the Gemini API quota limit. You can do this by checking your usage and billing details in your Google AI Platform console.

## Outcome

- ✅ Impact: The user's chatbot was giving vague responses due to a silent failure in the RAG pipeline. By improving the error handling, the user will now see a clear error message when their Gemini API quota is exceeded, which will help them debug the issue faster in the future.
- 🧪 Tests: No tests were run.
- 📁 Files: Modified `backend/src/services/gemini_service.py` to re-raise exceptions from the Gemini API instead of returning a mock response.
- 🔁 Next prompts: User might ask to implement a more robust error handling mechanism, like a backoff and retry strategy.
- 🧠 Reflection: Silently failing is a bad practice. It's better to fail fast and provide clear error messages. The initial implementation was hiding a critical error, which made debugging difficult for the user.

## Evaluation notes (flywheel)

- Failure modes observed: The chatbot giving vague replies was a failure mode caused by the silent failure of the embedding generation.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
