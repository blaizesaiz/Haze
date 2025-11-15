import { create } from 'zustand';
import { Odds, Event } from '@/services/sports.service';

export interface BetSlipItem {
  event: Event;
  odds: Odds;
  stake: number;
}

interface BetSlipState {
  items: BetSlipItem[];
  addToBetSlip: (event: Event, odds: Odds) => void;
  removeFromBetSlip: (oddsId: number) => void;
  updateStake: (oddsId: number, stake: number) => void;
  clearBetSlip: () => void;
  getTotalStake: () => number;
  getTotalPotentialPayout: () => number;
}

export const useBetSlipStore = create<BetSlipState>((set, get) => ({
  items: [],

  addToBetSlip: (event, odds) => {
    set((state) => {
      // Check if already in bet slip
      const exists = state.items.find((item) => item.odds.id === odds.id);
      if (exists) return state;

      return {
        items: [...state.items, { event, odds, stake: 10 }],
      };
    });
  },

  removeFromBetSlip: (oddsId) => {
    set((state) => ({
      items: state.items.filter((item) => item.odds.id !== oddsId),
    }));
  },

  updateStake: (oddsId, stake) => {
    set((state) => ({
      items: state.items.map((item) =>
        item.odds.id === oddsId ? { ...item, stake } : item
      ),
    }));
  },

  clearBetSlip: () => {
    set({ items: [] });
  },

  getTotalStake: () => {
    return get().items.reduce((total, item) => total + item.stake, 0);
  },

  getTotalPotentialPayout: () => {
    return get().items.reduce((total, item) => total + item.stake * item.odds.price, 0);
  },
}));
