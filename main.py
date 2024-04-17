import uuid
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError


app = FastAPI()


class Task(BaseModel):
    duration: int


# Список для хранения сообщений
tasks = {}


async def task_worker(id, duration):
    await asyncio.sleep(duration)
    tasks[id] = 'done'
    return 'done'


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    return JSONResponse(content={'status': tasks[task_id]})


@app.get("/tasks/")
async def get_task_status():
    return tasks


@app.post("/task", response_model=dict)
async def create_task(task: Task):
    try:
        task_id = str(uuid.uuid4())
        print(f'New task: {task_id}')
        tasks[task_id] = "running"
        await asyncio.create_task(task_worker(task_id, task.duration))
        print(tasks[task_id])
        return JSONResponse(content={'task_id': task_id})
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=f"Ошибка! Ожидается число")

