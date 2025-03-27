from fastapi import FastAPI
from task.router import router as task_router
from users.router import router as user_router
from book.router import router as book_router
from middleware import ExceptionHandlerMiddleware

app = FastAPI()

# middleware handled
app.add_middleware(ExceptionHandlerMiddleware)

# Register router
app.include_router(task_router)
app.include_router(user_router)
app.include_router(book_router)


@app.get("/")
def welcome():
    return {"details": "Task Management API"}
