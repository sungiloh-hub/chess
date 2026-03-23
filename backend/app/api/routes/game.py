from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.core.chess_engine import get_or_create_game, delete_game

router = APIRouter(prefix="/game", tags=["game"])


class MoveRequest(BaseModel):
    game_id: str = "default"
    uci_move: str  # e.g. "e2e4"


class NewGameRequest(BaseModel):
    game_id: str = "default"
    difficulty: str = "beginner"


@router.post("/new")
async def new_game(req: NewGameRequest):
    """새 게임 시작"""
    delete_game(req.game_id)
    game = get_or_create_game(req.game_id, req.difficulty)
    return {"success": True, "board": game.get_board_state()}


@router.get("/state")
async def game_state(game_id: str = "default"):
    """현재 게임 상태"""
    game = get_or_create_game(game_id)
    return game.get_board_state()


@router.get("/legal-moves")
async def legal_moves(game_id: str = "default", square: Optional[str] = None):
    """합법적인 수 목록"""
    game = get_or_create_game(game_id)
    return {"moves": game.get_legal_moves(square)}


@router.post("/move")
async def make_move(req: MoveRequest):
    """수 실행"""
    game = get_or_create_game(req.game_id)
    result = game.make_move(req.uci_move)
    return result


@router.get("/suggestions")
async def get_suggestions(game_id: str = "default", square: Optional[str] = None):
    """수 제안 및 전략 설명"""
    game = get_or_create_game(game_id)
    suggestions = game.get_move_suggestions(square)
    return {"suggestions": suggestions}
