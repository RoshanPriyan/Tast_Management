from fastapi import APIRouter
from .views.create_book_api import create_book_api
from .views.all_book_api import get_all_book_api
from .views.get_book_api import get_book_api
from .views.update_book_api import update_book_api
from .views.delete_book_api import delete_book_api

router = APIRouter(prefix="/api/book", tags=["BOOK"])

router.add_api_route("/create-book", create_book_api, methods=["POST"])
router.add_api_route("/books", get_all_book_api, methods=["GET"])
router.add_api_route("/book", get_book_api, methods=["GET"])
router.add_api_route("/update-book", update_book_api, methods=["PUT"])
router.add_api_route("/delete-book", delete_book_api, methods=["DELETE"])
