import api from './api';

export interface Bet {
  id: number;
  user_id: number;
  event_id: number;
  odds_id: number;
  stake: number;
  odds_value: number;
  potential_payout: number;
  status: 'pending' | 'won' | 'lost' | 'void' | 'cashed_out';
  outcome?: string;
  settled_at?: string;
  created_at: string;
}

export interface PlaceBetData {
  event_id: number;
  odds_id: number;
  stake: number;
}

export interface BetStats {
  total_bets: number;
  won_bets: number;
  lost_bets: number;
  pending_bets: number;
  total_staked: number;
  total_profit: number;
  win_rate: number;
}

export const bettingService = {
  async placeBet(data: PlaceBetData): Promise<Bet> {
    const response = await api.post<Bet>('/bets', data);
    return response.data;
  },

  async getMyBets(skip = 0, limit = 100): Promise<{ bets: Bet[]; total: number }> {
    const response = await api.get('/bets', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getBetStats(): Promise<BetStats> {
    const response = await api.get<BetStats>('/bets/stats');
    return response.data;
  },

  async getBet(betId: number): Promise<Bet> {
    const response = await api.get<Bet>(`/bets/${betId}`);
    return response.data;
  },
};
