# api_echo.py - Только JSON API
import json
from datetime import datetime

def fetch(request):
    """Чистое JSON API эхо-сервер"""
    
    method = request.method
    url = str(request.url)
    
    async def handle():
        # Собираем информацию о запросе
        request_info = {
            "method": method,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "headers": dict(request.headers)
        }
        
        # Получаем тело запроса
        if method in ["POST", "PUT", "PATCH"]:
            try:
                content_type = request.headers.get("content-type", "")
                if "application/json" in content_type:
                    request_info["body"] = await request.json()
                else:
                    request_info["body"] = await request.text()
            except:
                request_info["body"] = "Could not parse body"
        
        # Добавляем query параметры
        request_info["query"] = dict(request.query)
        
        # Формируем ответ
        response = {
            "api": "Python Echo API",
            "documentation": "Send any HTTP request to this endpoint",
            "your_request": request_info,
            "server": {
                "platform": "Deno Deploy",
                "language": "Python",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        return {
            "status": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "X-Echo-Server": "Python/Deno"
            },
            "body": json.dumps(response, indent=2, ensure_ascii=False)
        }
    
    import asyncio
    return asyncio.run(handle())
