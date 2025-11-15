import api from './api';

export interface Sport {
  id: number;
  key: string;
  name: string;
  is_active: boolean;
  created_at: string;
}

export interface Odds {
  id: number;
  market_id: number;
  bookmaker: string;
  outcome: string;
  price: number;
  point?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Market {
  id: number;
  event_id: number;
  key: string;
  name: string;
  odds: Odds[];
  created_at: string;
}

export interface Event {
  id: number;
  sport_id: number;
  external_id: string;
  home_team: string;
  away_team: string;
  commence_time: string;
  is_live: boolean;
  is_completed: boolean;
  home_score?: number;
  away_score?: number;
  markets: Market[];
  created_at: string;
}

export const sportsService = {
  async getSports(): Promise<Sport[]> {
    const response = await api.get<Sport[]>('/sports');
    return response.data;
  },

  async syncSports(): Promise<void> {
    await api.post('/sports/sync');
  },

  async getEvents(sportKey: string, skip = 0, limit = 100): Promise<{ events: Event[]; total: number }> {
    const response = await api.get(`/sports/${sportKey}/events`, {
      params: { skip, limit },
    });
    return response.data;
  },

  async syncOdds(sportKey: string): Promise<void> {
    await api.post(`/sports/${sportKey}/sync-odds`);
  },

  async getEvent(eventId: number): Promise<Event> {
    const response = await api.get<Event>(`/sports/events/${eventId}`);
    return response.data;
  },
};
