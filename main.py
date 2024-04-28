import uvicorn
from fastapi import BackgroundTasks, FastAPI, Depends, Request
import datetime
from typing import Annotated
import logging
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Базовая настройка логирования
logging.basicConfig(filename="log.txt", level=logging.INFO)

# Добавим middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts = ["127.0.0.1"]
)

# Логирование запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# Вывод текущего времени в консоль
def write_time(current_time: str):
    content = f"Текущее время: {current_time}"
    print(content)

# Проверка query-параметра
def QueryChecker(name: str=""):
    if name:
        return name
    return "Параметр отсутствует"

@app.get("/get_time")
async def get_time(background_tasks: BackgroundTasks):
    current_time = datetime.datetime.now().time().strftime("%H:%M:%S")
    background_tasks.add_task(write_time, current_time)
    return {"message": current_time}

@app.get("/check")
async def ckeck(check_content: Annotated[str, Depends(QueryChecker)]):
    return {"check_content_in_query": check_content}

@app.get('/', response_class = HTMLResponse)
def index():
    return "<b> Привет, пользователь! </b>" 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")