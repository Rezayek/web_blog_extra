import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)


from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from config_env import settings
from debugger_file import set_up_logger
import uvicorn

logger = set_up_logger(file_name= settings.log_microservice)
app = FastAPI(debug=True)

# add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# define the API Gateway route
# define the API Gateway routes
@app.get("/{route:path}")
@app.post("/{route:path}")
@app.put("/{route:path}")
@app.delete("/{route:path}")
async def api_gateway(request: Request, route: str):
    logger.debug(f"route: {route}")
    # define the microservice URLs
    auth_url = settings.auth_service_path
    posts_url = settings.posts_service_path
    comments_url = settings.comments_service_path
    # dispatch the request to the appropriate microservice based on the URL path
    if route.startswith('auth'):
        if request.url.query != "":
            url = auth_url + request.url.path + '?' + request.url.query
        else:
            url = auth_url + request.url.path 
        logger.debug(f"Dispatching request to auth microservice: {request.method} {url}")
        async with AsyncClient() as client:
            response = await client.request(request.method, url, headers=request.headers, data=request.stream())
            
    elif route.startswith('posts'):
        if request.url.query != "":
            url = posts_url + request.url.path + '?' + request.url.query
        else:
            url = posts_url + request.url.path 
        logger.debug(f"Dispatching request to posts microservice: {request.method} {url}")
        async with AsyncClient() as client:
            response = await client.request(request.method, url, headers=request.headers, data=request.stream())
            
    elif route.startswith('comments'):
        if request.url.query != "":
            url = comments_url + request.url.path + '?' + request.url.query
        else:
            url = comments_url + request.url.path 
        logger.debug(f"Dispatching request to comments microservice: {request.method} {url}")
        async with AsyncClient() as client:
            response = await client.request(request.method, url, headers=request.headers, data=request.stream())
        
    
    
    else:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # return the response from the microservice
    return Response(content=response.content, status_code=response.status_code, headers=response.headers)
    



if __name__ == "__main__":
    # run the API Gateway on the main thread
    uvicorn.run("main:app", host=settings.api_gateway_service_host, port=settings.api_gateway_service_port, reload= True)
