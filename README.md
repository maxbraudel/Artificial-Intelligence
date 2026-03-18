
2026-03-18 15:47:02,171 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/sendMessage "HTTP/1.1 200 OK"
2026-03-18 15:47:02,692 - httpx - INFO - HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 401 Unauthorized"
2026-03-18 15:47:02,696 - telegram.ext.Application - ERROR - No error handlers are registered, logging exception.
Traceback (most recent call last):
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/telegram/ext/_application.py", line 1315, in process_update
    await coroutine
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/telegram/ext/_handlers/conversationhandler.py", line 841, in handle_update
    new_state: object = await handler.handle_update(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/telegram/ext/_handlers/basehandler.py", line 159, in handle_update
    return await self.callback(update, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/handlers/conversation.py", line 91, in handle_cv_document
    return await _process_cv(update, context, raw_text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/handlers/conversation.py", line 98, in _process_cv
    result = await llm.evaluate_cv(raw_text)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/services/llm.py", line 48, in evaluate_cv
    raw = await _chat(messages)
          ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/services/llm.py", line 20, in _chat
    response = await _client.chat.completions.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/openai/resources/chat/completions/completions.py", line 2714, in create
    return await self._post(
           ^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1884, in post
    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1669, in request
    raise self._make_status_error_from_response(err.response) from None
openai.AuthenticationError: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
2026-03-18 15:47:10,979 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
2026-03-18 15:47:21,013 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
2026-03-18 15:47:31,039 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
2026-03-18 15:47:41,065 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
2026-03-18 15:47:51,091 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
^C^C%                                                                                                                        
(.venv) maxbraudel@macbook-pro-de-max Artificial Intelligence % python3 bot.py
2026-03-18 15:54:54,672 - __main__ - INFO - Bot is running…
2026-03-18 15:54:55,037 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getMe "HTTP/1.1 200 OK"
2026-03-18 15:54:55,063 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/deleteWebhook "HTTP/1.1 200 OK"
2026-03-18 15:54:55,064 - telegram.ext.Application - INFO - Application started
2026-03-18 15:55:03,095 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
2026-03-18 15:55:03,466 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/sendMessage "HTTP/1.1 200 OK"
2026-03-18 15:55:06,634 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"
2026-03-18 15:55:06,704 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/sendMessage "HTTP/1.1 200 OK"
2026-03-18 15:55:07,454 - httpx - INFO - HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 401 Unauthorized"
2026-03-18 15:55:07,459 - telegram.ext.Application - ERROR - No error handlers are registered, logging exception.
Traceback (most recent call last):
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/telegram/ext/_application.py", line 1315, in process_update
    await coroutine
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/telegram/ext/_handlers/conversationhandler.py", line 841, in handle_update
    new_state: object = await handler.handle_update(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/telegram/ext/_handlers/basehandler.py", line 159, in handle_update
    return await self.callback(update, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/handlers/conversation.py", line 59, in handle_cv_text
    return await _process_cv(update, context, raw_text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/handlers/conversation.py", line 98, in _process_cv
    result = await llm.evaluate_cv(raw_text)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/services/llm.py", line 48, in evaluate_cv
    raw = await _chat(messages)
          ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/services/llm.py", line 20, in _chat
    response = await _client.chat.completions.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/openai/resources/chat/completions/completions.py", line 2714, in create
    return await self._post(
           ^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1884, in post
    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/maxbraudel/Études/IMAC/Artificial Intelligence/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1669, in request
    raise self._make_status_error_from_response(err.response) from None
openai.AuthenticationError: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
2026-03-18 15:55:16,661 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8745406088:AAHDAEjKBGq3nC0oTyh8qMbuxL1OJfDkgF8/getUpdates "HTTP/1.1 200 OK"


parfait ! maintenant j(ai envie que t'ajoutes un mode. Quand une réponse est envoyée elleest oujours jugée satisfaisante ou insatisfaisante. Mais je veux une 3eme possibilité. Elle peut aussi être jguée offansante. Si elle la réposne est impertinente, ou stupide ou remet en question le rôle du bot... Elle est considérée comme offensante. Si la réposne est ocnsidérée comme offensante. 