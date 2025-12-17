await route.handle(scope, receive, send)
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\starlette\routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\fastapi\routing.py", line 119, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\fastapi\routing.py", line 105, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\fastapi\routing.py", line 385, in app
    raw_response = await run_endpoint_function(app, request)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\fastapi\routing.py", line 284, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\iqra\Desktop\physical-ai\backend\src\api\chat.py", line 62, in chat_endpoint
    answer, references = await generate_rag_response(
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
    )
    ^
  File "C:\Users\iqra\Desktop\physical-ai\backend\src\core\rag_pipeline.py", line 38, in generate_rag_response
    retrieved_chunks_info = search_vectors(query_embedding, limit=5, min_score=0.7)    
  File "C:\Users\iqra\Desktop\physical-ai\backend\src\services\qdrant_client.py", line 95, in search_vectors
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
    ...<2 lines>...
        score_threshold=min_score,
    )
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\qdrant_client\qdrant_client.py", line 429, in query_points
    return self._client.query_points(
           ~~~~~~~~~~~~~~~~~~~~~~~~~
        collection_name=collection_name,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<14 lines>...
        **kwargs,
        ^^^^^^^^^
    )
    ^
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\qdrant_client\qdrant_remote.py", line 544, in query_points
    query_result = self.http.search_api.query_points(
        collection_name=collection_name,
    ...<2 lines>...
        query_request=query_request,
    )
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\qdrant_client\http\api\search_api.py", line 783, in query_points     
    return self._build_for_query_points(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        collection_name=collection_name,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        query_request=query_request,
    )
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\qdrant_client\http\api\search_api.py", line 181, in _build_for_query_points
    return self.api_client.request(
           ~~~~~~~~~~~~~~~~~~~~~~~^
        type_=m.InlineResponse20021,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
        content=body,
        ^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\qdrant_client\http\api_client.py", line 95, in request
    return self.send(request, type_)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\iqra\AppData\Local\pypoetry\Cache\virtualenvs\backend-dZsz35JC-py3.13\Lib\site-packages\qdrant_client\http\api_client.py", line 130, in send
    raise UnexpectedResponse.for_response(response)
qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 400 (Bad Request)
Raw response content:
b'{"status":{"error":"Wrong input: Vector dimension error: expected dim: 1536, got 384"},"time":0.000614892}' my dear gemini cli please make my backend fully working when im chatting with the chatbot and api is giving this error and please solve this error imediately