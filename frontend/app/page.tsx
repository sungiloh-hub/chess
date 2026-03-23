"use client";

import { useEffect, useState, useCallback } from "react";
import { gameApi } from "@/lib/api";
import styles from "./page.module.css";

const FILES = ["a", "b", "c", "d", "e", "f", "g", "h"];
const RANKS = ["8", "7", "6", "5", "4", "3", "2", "1"];

// 흰색 말과 검은색 말 유니코드를 명확히 구분
const PIECE_DISPLAY: Record<string, Record<string, string>> = {
  white: { k: "♔", q: "♕", r: "♖", b: "♗", n: "♘", p: "♙" },
  black: { k: "♚", q: "♛", r: "♜", b: "♝", n: "♞", p: "♟" },
};

interface Suggestion {
  from: string;
  to: string;
  uci: string;
  san: string;
  score: number;
  reasons: string[];
}

const DIFFICULTIES = [
  { key: "beginner", label: "입문", icon: "🌱", desc: "랜덤에 가까운 수" },
  { key: "easy", label: "초급", icon: "🎯", desc: "잡을 수 있으면 잡음" },
  { key: "intermediate", label: "중급", icon: "⚔️", desc: "전략적 사고" },
  { key: "advanced", label: "고급", icon: "🧠", desc: "정밀한 평가" },
  { key: "expert", label: "전문가", icon: "👑", desc: "2수 앞을 예측" },
];

export default function Home() {
  const [boardState, setBoardState] = useState<any>(null);
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
  const [legalMoves, setLegalMoves] = useState<any[]>([]);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [thinking, setThinking] = useState(false);
  const [difficulty, setDifficulty] = useState("beginner");

  const loadGame = useCallback(async () => {
    try {
      const state = await gameApi.getState();
      setBoardState(state);
      setLoading(false);
    } catch {
      setMessage("백엔드 서버에 연결할 수 없습니다");
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadGame();
  }, [loadGame]);

  const handleNewGame = async () => {
    const res = await gameApi.newGame("default", difficulty);
    setBoardState(res.board);
    setSelectedSquare(null);
    setLegalMoves([]);
    setSuggestions([]);
    setThinking(false);
    const diff = DIFFICULTIES.find((d) => d.key === difficulty);
    setMessage(`새 게임! AI 난이도: ${diff?.icon} ${diff?.label}`);
  };

  const handleSquareClick = async (square: string) => {
    if (!boardState || boardState.is_game_over || thinking) return;

    // 유저는 백(white)만 둘 수 있음
    if (boardState.turn !== "white") return;

    // 이미 선택된 말이 있고, 합법적인 이동인 경우 → 수 실행
    if (selectedSquare) {
      const move = legalMoves.find((m) => m.to === square);
      if (move) {
        setSelectedSquare(null);
        setLegalMoves([]);
        setSuggestions([]);
        setThinking(true);
        setMessage(`${move.san} 실행... AI가 생각 중...`);

        const result = await gameApi.makeMove(move.uci);
        if (result.success) {
          setBoardState(result.board);

          // 결과 메시지
          if (result.board.is_checkmate) {
            const winner = result.board.turn === "white" ? "흑(AI)" : "백(당신)";
            setMessage(`🏆 체크메이트! ${winner}이 승리했습니다!`);
          } else if (result.board.is_stalemate) {
            setMessage("🤝 무승부 (스테일메이트)");
          } else if (result.ai_move) {
            let msg = `당신: ${result.move} → AI: ${result.ai_move.move}`;
            if (result.board.is_check) {
              msg += " ⚡ 체크!";
            }
            setMessage(msg);
          } else if (result.board.is_check) {
            setMessage(`⚡ 체크! (${result.move})`);
          } else {
            setMessage(`${result.move} 실행`);
          }
        } else {
          setMessage(result.error);
        }
        setThinking(false);
        return;
      }
    }

    // 백색 말을 클릭한 경우 → 선택
    const piece = boardState.squares[square];
    if (piece && piece.color === "white") {
      setSelectedSquare(square);
      const movesRes = await gameApi.getLegalMoves("default", square);
      setLegalMoves(movesRes.moves);

      if (showSuggestions) {
        const sugRes = await gameApi.getSuggestions("default", square);
        setSuggestions(sugRes.suggestions);
      }
    } else {
      setSelectedSquare(null);
      setLegalMoves([]);
      setSuggestions([]);
    }
  };

  const handleToggleSuggestions = async () => {
    setShowSuggestions(!showSuggestions);
    if (!showSuggestions && selectedSquare) {
      const sugRes = await gameApi.getSuggestions("default", selectedSquare);
      setSuggestions(sugRes.suggestions);
    } else {
      setSuggestions([]);
    }
  };

  const handleGetAllSuggestions = async () => {
    const sugRes = await gameApi.getSuggestions();
    setSuggestions(sugRes.suggestions);
    setShowSuggestions(true);
  };

  const isLegalTarget = (sq: string) => legalMoves.some((m) => m.to === sq);

  const getSquareClass = (file: string, rank: string) => {
    const sq = file + rank;
    const fi = FILES.indexOf(file);
    const ri = RANKS.indexOf(rank);
    const isLight = (fi + ri) % 2 === 0;
    let cls = isLight ? styles.lightSquare : styles.darkSquare;
    if (sq === selectedSquare) cls += ` ${styles.selected}`;
    if (isLegalTarget(sq)) cls += ` ${styles.legalTarget}`;
    return cls;
  };

  if (loading) {
    return <div className={styles.loading}>로딩 중...</div>;
  }

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>♟ Chess Tutor</h1>
      <p className={styles.subtitle}>당신(⬜백) vs AI(⬛흑) — 수를 제안받으며 체스를 배워보세요</p>

      <div className={styles.layout}>
        {/* 체스 보드 */}
        <div className={styles.boardWrapper}>
          <div className={styles.board}>
            {RANKS.map((rank) =>
              FILES.map((file) => {
                const sq = file + rank;
                const piece = boardState?.squares[sq];
                return (
                  <div
                    key={sq}
                    className={getSquareClass(file, rank)}
                    onClick={() => handleSquareClick(sq)}
                  >
                    {isLegalTarget(sq) && !piece && (
                      <div className={styles.dot} />
                    )}
                    {piece && (
                      <span
                        className={`${styles.piece} ${
                          piece.color === "white" ? styles.whitePiece : styles.blackPiece
                        }`}
                      >
                        {PIECE_DISPLAY[piece.color][piece.type]}
                      </span>
                    )}
                  </div>
                );
              })
            )}
          </div>
          <div className={styles.fileLabels}>
            {FILES.map((f) => <span key={f}>{f}</span>)}
          </div>
        </div>

        {/* 사이드 패널 */}
        <div className={styles.panel}>
          <div className={styles.info}>
            <div className={styles.turn}>
              {boardState?.is_game_over
                ? "🏁 게임 종료"
                : thinking
                ? "🤔 AI 생각 중..."
                : "당신의 차례 (⬜ 백)"}
            </div>
            {message && <div className={styles.message}>{message}</div>}
          </div>

          {/* 난이도 선택 */}
          <div className={styles.difficultySection}>
            <h3 className={styles.diffTitle}>AI 난이도</h3>
            <div className={styles.diffGrid}>
              {DIFFICULTIES.map((d) => (
                <button
                  key={d.key}
                  className={`${styles.diffBtn} ${difficulty === d.key ? styles.diffActive : ""}`}
                  onClick={() => setDifficulty(d.key)}
                  title={d.desc}
                >
                  <span className={styles.diffIcon}>{d.icon}</span>
                  <span className={styles.diffLabel}>{d.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div className={styles.buttons}>
            <button onClick={handleNewGame} className={styles.btn}>
              🔄 새 게임
            </button>
            <button
              onClick={handleToggleSuggestions}
              className={`${styles.btn} ${showSuggestions ? styles.btnActive : ""}`}
            >
              💡 힌트 {showSuggestions ? "끄기" : "켜기"}
            </button>
            <button onClick={handleGetAllSuggestions} className={styles.btn}>
              🧠 최선의 수 보기
            </button>
          </div>

          {/* 전략 제안 */}
          {suggestions.length > 0 && (
            <div className={styles.suggestions}>
              <h3>💡 수 제안</h3>
              {suggestions.map((s, i) => (
                <div key={i} className={styles.suggestionCard}>
                  <div className={styles.suggestionHeader}>
                    <span className={styles.moveName}>{s.san}</span>
                    <span className={styles.moveDetail}>
                      ({s.from} → {s.to})
                    </span>
                    <span
                      className={styles.score}
                      style={{
                        color: s.score >= 8 ? "#4ade80" : s.score >= 3 ? "#facc15" : "#888",
                      }}
                    >
                      ★ {s.score}
                    </span>
                  </div>
                  <ul className={styles.reasons}>
                    {s.reasons.map((r, j) => (
                      <li key={j}>{r}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {/* 기보 */}
          {boardState?.move_history?.length > 0 && (
            <div className={styles.history}>
              <h3>📜 기보</h3>
              <div className={styles.moves}>
                {boardState.move_history.map((m: any, i: number) => (
                  <span key={i} className={`${styles.moveRecord} ${m.color === "black" ? styles.blackMove : ""}`}>
                    {i % 2 === 0 && (
                      <span className={styles.moveNum}>{Math.floor(i / 2) + 1}.</span>
                    )}
                    {m.move}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
