from fastapi import  APIRouter
from .views.create_task_api import create_task_api
from .views.task_list_api import list_tasks_api
from .views.update_task_api import update_task_api
from .views.delete_task_api import delete_task_api
from .views.task_list import task_list_api

router = APIRouter(prefix="/api/task", tags=["Task"])

router.add_api_route("/add-task", create_task_api, methods=["POST"])
router.add_api_route("/task-list", list_tasks_api, methods=["GET"])
router.add_api_route("/update-task", update_task_api, methods=["PUT"])
router.add_api_route("/delete-task", delete_task_api, methods=["DELETE"])
router.add_api_route("/list", task_list_api, methods=["GET"])
