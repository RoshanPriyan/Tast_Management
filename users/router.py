from fastapi import APIRouter
from .views.register import user_register_api
from .views.login import user_login_api

router = APIRouter(prefix="/api/user", tags=["User"])

router.add_api_route("/register", user_register_api, methods=["POST"])
router.add_api_route("/login", user_login_api, methods=["POST"])