const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// 게임 API
export const gameApi = {
  newGame: (gameId = 'default', difficulty = 'beginner') =>
    fetchApi<any>('/api/game/new', {
      method: 'POST',
      body: JSON.stringify({ game_id: gameId, difficulty }),
    }),

  getState: (gameId = 'default') =>
    fetchApi<any>(`/api/game/state?game_id=${gameId}`),

  getLegalMoves: (gameId = 'default', square?: string) =>
    fetchApi<any>(
      `/api/game/legal-moves?game_id=${gameId}${square ? `&square=${square}` : ''}`
    ),

  makeMove: (uciMove: string, gameId = 'default') =>
    fetchApi<any>('/api/game/move', {
      method: 'POST',
      body: JSON.stringify({ game_id: gameId, uci_move: uciMove }),
    }),

  getSuggestions: (gameId = 'default', square?: string) =>
    fetchApi<any>(
      `/api/game/suggestions?game_id=${gameId}${square ? `&square=${square}` : ''}`
    ),
};