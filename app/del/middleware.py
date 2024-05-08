# from fastapi.security import OAuth2PasswordBearer

# from fastapi import Depends, HTTPException
# from fastapi.responses import JSONResponse
# from starlette.middleware.base import BaseHTTPMiddleware

# Define a custom middleware for token verification

# class CustomMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         try:
#             content_type = request.headers.get('Content-Type')
#             print(content_type)

#             # Call the verify_access_token function to validate the token
#             verify_access_token(request)
#             # If token validation succeeds, continue to the next middleware or route handler
#             response = await call_next(request)
#             return response
#         except HTTPException as exc:
#             # If token validation fails due to HTTPException, return the error response
#             return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
#         except Exception as exc:
#             # If token validation fails due to other exceptions, return a generic error response
#             return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

# # Add the custom middleware to the FastAPI app
# app.add_middleware(CustomMiddleware)