import os
os.system("pip install js")
from js import Response, Request
import asyncio

async def on_fetch(request):
    method = request.method
    url = str(request.url)
    
    if method == "GET":
        return Response.new(
            "Send POST-quest for JSON: {'text': 'Your text'}\n" +
            "or add ?text=YourText in URL",
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
    
    if method == "POST":
        try:
            data = await request.json()
            text = data.get("text", "")
        except:
            text = await request.text()
        
        if not text:
            url_obj = URL.new(url)
            text = url_obj.searchParams.get("text", "")
        
        return Response.new(
            f"You say: {text}",
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
    
    return Response.new(
        f"Method {method} Not working here!",
        status=405
    )

def fetch(request, env):
    return asyncio.ensure_future(on_fetch(request))
