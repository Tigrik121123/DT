# worker.py для Cloudflare Workers (Python via Pyodide)

from js import Response, Request
import asyncio

async def on_fetch(request):
    # Получаем метод и URL
    method = request.method
    url = str(request.url)
    
    # Для GET-запроса показываем инструкцию
    if method == "GET":
        return Response.new(
            "Отправьте POST-запрос с JSON: {'text': 'ваш текст'}\n" +
            "Или добавьте ?text=ваштекст к URL",
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
    
    # Обработка POST-запроса
    if method == "POST":
        try:
            # Пробуем получить JSON
            data = await request.json()
            text = data.get("text", "")
        except:
            # Если не JSON, пробуем получить как текст
            text = await request.text()
        
        if not text:
            # Пробуем получить из параметров URL
            url_obj = URL.new(url)
            text = url_obj.searchParams.get("text", "")
        
        return Response.new(
            f"Вы отправили: {text}",
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
    
    # Для других методов
    return Response.new(
        f"Метод {method} не поддерживается",
        status=405
    )

def fetch(request, env):
    # Обертка для асинхронной функции
    return asyncio.ensure_future(on_fetch(request))
