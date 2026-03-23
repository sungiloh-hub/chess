"""
체스 게임 엔진 - python-chess 기반
게임 상태 관리 및 수 제안 로직
"""

import chess
from typing import Optional


class ChessGame:
    """체스 게임 상태를 관리하는 클래스"""

    def __init__(self, difficulty: str = "beginner"):
        self.board = chess.Board()
        self.difficulty = difficulty
        self.move_history: list[dict] = []

    def get_board_state(self) -> dict:
        """현재 보드 상태를 반환"""
        squares = {}
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                squares[chess.square_name(sq)] = {
                    "type": piece.symbol().lower(),
                    "color": "white" if piece.color == chess.WHITE else "black",
                    "symbol": piece.symbol(),
                }
        return {
            "squares": squares,
            "turn": "white" if self.board.turn == chess.WHITE else "black",
            "is_check": self.board.is_check(),
            "is_checkmate": self.board.is_checkmate(),
            "is_stalemate": self.board.is_stalemate(),
            "is_game_over": self.board.is_game_over(),
            "fen": self.board.fen(),
            "move_count": self.board.fullmove_number,
            "move_history": self.move_history,
        }

    def get_legal_moves(self, square: Optional[str] = None) -> list[dict]:
        """합법적인 수 목록을 반환. square가 주어지면 해당 칸의 수만 반환"""
        moves = []
        for move in self.board.legal_moves:
            from_sq = chess.square_name(move.from_square)
            to_sq = chess.square_name(move.to_square)

            if square and from_sq != square:
                continue

            moves.append({
                "from": from_sq,
                "to": to_sq,
                "uci": move.uci(),
                "san": self.board.san(move),
            })
        return moves

    def make_move(self, uci_move: str) -> dict:
        """수를 실행"""
        try:
            move = chess.Move.from_uci(uci_move)
            if move not in self.board.legal_moves:
                return {"success": False, "error": "불법적인 수입니다."}

            san = self.board.san(move)
            self.board.push(move)

            self.move_history.append({
                "move": san,
                "uci": uci_move,
                "color": "black" if self.board.turn == chess.WHITE else "white",
            })

            result = {
                "success": True,
                "move": san,
                "board": self.get_board_state(),
                "ai_move": None,
            }

            # 게임이 끝나지 않았고 흑의 차례면 AI가 자동 응수
            if not self.board.is_game_over() and self.board.turn == chess.BLACK:
                ai_result = self._make_ai_move()
                if ai_result:
                    result["ai_move"] = ai_result
                    result["board"] = self.get_board_state()

            return result
        except ValueError:
            return {"success": False, "error": "잘못된 수 형식입니다."}

    def _make_ai_move(self) -> dict | None:
        """AI(흑)가 난이도에 맞는 수를 선택하여 둠"""
        import random

        if self.board.is_game_over():
            return None

        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        difficulty_fn = {
            "beginner": self._ai_beginner,
            "easy": self._ai_easy,
            "intermediate": self._ai_intermediate,
            "advanced": self._ai_advanced,
            "expert": self._ai_expert,
        }

        pick_fn = difficulty_fn.get(self.difficulty, self._ai_easy)
        best_move = pick_fn(legal_moves)

        if best_move is None:
            best_move = random.choice(legal_moves)

        san = self.board.san(best_move)
        uci = best_move.uci()
        self.board.push(best_move)

        self.move_history.append({
            "move": san,
            "uci": uci,
            "color": "black",
        })

        return {"move": san, "uci": uci}

    # ===== 난이도별 AI =====

    def _ai_beginner(self, legal_moves: list) -> chess.Move:
        """입문: 거의 랜덤, 체크메이트만 잡음"""
        import random
        # 체크메이트가 있으면 무조건 실행
        for move in legal_moves:
            self.board.push(move)
            if self.board.is_checkmate():
                self.board.pop()
                return move
            self.board.pop()
        return random.choice(legal_moves)

    def _ai_easy(self, legal_moves: list) -> chess.Move:
        """초급: 잡을 수 있으면 잡고, 아니면 랜덤"""
        import random
        captures = []
        for move in legal_moves:
            self.board.push(move)
            if self.board.is_checkmate():
                self.board.pop()
                return move
            self.board.pop()
            if self.board.is_capture(move):
                captures.append(move)

        if captures and random.random() > 0.3:
            return random.choice(captures)
        return random.choice(legal_moves)

    def _ai_intermediate(self, legal_moves: list) -> chess.Move:
        """중급: 평가 함수 사용, 적당한 랜덤성"""
        import random
        scored = []
        for move in legal_moves:
            score, _ = self._evaluate_move(move)
            score += random.uniform(0, 3)  # 노이즈 크게
            scored.append((score, move))

        scored.sort(key=lambda x: x[0], reverse=True)
        # 상위 3개 중 랜덤 선택
        top = scored[:3]
        return random.choice(top)[1]

    def _ai_advanced(self, legal_moves: list) -> chess.Move:
        """고급: 정밀한 평가, 적은 랜덤성"""
        import random
        scored = []
        for move in legal_moves:
            score, _ = self._evaluate_move(move)
            score += random.uniform(0, 0.5)  # 노이즈 작게
            scored.append((score, move))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def _ai_expert(self, legal_moves: list) -> chess.Move:
        """전문가: 2수 앞을 내다보는 미니맥스"""
        import random
        best_score = -9999
        best_move = legal_moves[0]

        for move in legal_moves:
            self.board.push(move)

            if self.board.is_checkmate():
                self.board.pop()
                return move

            # 상대(백)의 최선 응수를 고려
            min_score = 9999
            for opp_move in self.board.legal_moves:
                opp_score, _ = self._evaluate_move(opp_move)
                # 상대의 좋은 수 = AI에게 나쁜 수
                if opp_score < min_score:
                    min_score = opp_score

            # 현재 수의 평가
            self.board.pop()
            my_score, _ = self._evaluate_move(move)
            # AI 점수 - 상대 최선 응수 점수
            total = my_score - min_score * 0.5 + random.uniform(0, 0.2)

            if total > best_score:
                best_score = total
                best_move = move

        return best_move

    def get_move_suggestions(self, square: Optional[str] = None) -> list[dict]:
        """수 제안과 전략 설명을 반환"""
        suggestions = []
        legal_moves = list(self.board.legal_moves)

        for move in legal_moves:
            from_sq = chess.square_name(move.from_square)
            if square and from_sq != square:
                continue

            score, reasons = self._evaluate_move(move)
            san = self.board.san(move)

            suggestions.append({
                "from": from_sq,
                "to": chess.square_name(move.to_square),
                "uci": move.uci(),
                "san": san,
                "score": score,
                "reasons": reasons,
            })

        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions[:5]  # 상위 5개만

    def _evaluate_move(self, move: chess.Move) -> tuple[int, list[str]]:
        """수를 평가하고 이유를 반환"""
        score = 0
        reasons = []

        piece = self.board.piece_at(move.from_square)
        captured = self.board.piece_at(move.to_square)

        # === 기초 전략 ===

        # 1. 상대 말 잡기
        if captured:
            piece_values = {
                chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
            }
            cap_val = piece_values.get(captured.piece_type, 0)
            my_val = piece_values.get(piece.piece_type, 0)
            score += cap_val * 10

            piece_names_kr = {
                chess.PAWN: "폰", chess.KNIGHT: "나이트", chess.BISHOP: "비숍",
                chess.ROOK: "룩", chess.QUEEN: "퀸", chess.KING: "킹",
            }
            cap_name = piece_names_kr.get(captured.piece_type, "")
            reasons.append(f"✅ 상대 {cap_name}을(를) 잡을 수 있습니다 (가치: {cap_val}점)")

            if my_val < cap_val:
                score += 5
                reasons.append("💎 낮은 가치의 말로 높은 가치의 말을 잡는 유리한 교환입니다")

        # 2. 중앙 지배
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        ext_center = [chess.C3, chess.D3, chess.E3, chess.F3,
                      chess.C4, chess.F4, chess.C5, chess.F5,
                      chess.C6, chess.D6, chess.E6, chess.F6]
        if move.to_square in center_squares:
            score += 3
            reasons.append("🎯 중앙을 차지합니다. 중앙 지배는 기본적이고 중요한 전략입니다")
        elif move.to_square in ext_center:
            score += 1
            reasons.append("🎯 확장된 중앙으로 이동합니다")

        # 3. 말 전개 (오프닝)
        if self.board.fullmove_number <= 10 and piece:
            if piece.piece_type in (chess.KNIGHT, chess.BISHOP):
                # 시작 위치에서 나오는 것
                home_ranks = [0, 1] if piece.color == chess.WHITE else [6, 7]
                if chess.square_rank(move.from_square) in home_ranks:
                    score += 4
                    reasons.append("📦 말을 전개합니다. 초반에는 나이트와 비숍을 빨리 꺼내는 것이 중요합니다")

        # 4. 캐슬링
        if self.board.is_castling(move):
            score += 8
            reasons.append("🏰 캐슬링! 킹을 안전하게 보호하고 룩을 활성화합니다")

        # === 중급 전략 ===

        # 5. 체크
        self.board.push(move)
        if self.board.is_check():
            score += 5
            reasons.append("⚡ 체크! 상대 킹을 위협합니다")
        if self.board.is_checkmate():
            score += 100
            reasons.append("🏆 체크메이트! 게임에서 이깁니다!")

        # 6. 위협당하는 곳에서 벗어나기
        self.board.pop()
        if self.board.is_attacked_by(not piece.color, move.from_square):
            if not self.board.is_attacked_by(not piece.color, move.to_square):
                score += 4
                reasons.append("🛡️ 공격받는 위치에서 안전한 곳으로 이동합니다")

        # 7. 폰 구조
        if piece and piece.piece_type == chess.PAWN:
            # 프로모션 가까이
            promo_rank = 7 if piece.color == chess.WHITE else 0
            dist = abs(chess.square_rank(move.to_square) - promo_rank)
            if dist <= 2:
                score += 3
                reasons.append("⬆️ 폰이 프로모션(승급)에 가까워집니다")

        if not reasons:
            reasons.append("일반적인 수입니다")

        return score, reasons

    def reset(self):
        """게임 리셋"""
        self.board = chess.Board()
        self.move_history = []


# 게임 세션 관리 (간단한 인메모리 저장)
games: dict[str, ChessGame] = {}


def get_or_create_game(game_id: str, difficulty: str = "beginner") -> ChessGame:
    if game_id not in games:
        games[game_id] = ChessGame(difficulty=difficulty)
    return games[game_id]


def delete_game(game_id: str):
    if game_id in games:
        del games[game_id]
