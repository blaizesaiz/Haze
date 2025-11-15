import { useState } from 'react';
import { X, Trash2 } from 'lucide-react';
import { useBetSlipStore } from '@/store/betSlipStore';
import { useAuthStore } from '@/store/authStore';
import { bettingService } from '@/services/betting.service';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

export default function BetSlip() {
  const { items, removeFromBetSlip, updateStake, clearBetSlip, getTotalStake, getTotalPotentialPayout } = useBetSlipStore();
  const { isAuthenticated } = useAuthStore();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const placeBetsMutation = useMutation({
    mutationFn: async () => {
      const promises = items.map((item) =>
        bettingService.placeBet({
          event_id: item.event.id,
          odds_id: item.odds.id,
          stake: item.stake,
        })
      );
      return Promise.all(promises);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wallet'] });
      queryClient.invalidateQueries({ queryKey: ['bets'] });
      clearBetSlip();
      setError(null);
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to place bets');
    },
  });

  const handlePlaceBets = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (items.length === 0) {
      setError('No bets in slip');
      return;
    }

    placeBetsMutation.mutate();
  };

  if (items.length === 0) {
    return (
      <div className="card sticky top-8">
        <h2 className="text-xl font-bold mb-4">Bet Slip</h2>
        <p className="text-slate-400 text-center py-8">Your bet slip is empty</p>
      </div>
    );
  }

  return (
    <div className="card sticky top-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Bet Slip ({items.length})</h2>
        <button
          onClick={clearBetSlip}
          className="text-slate-400 hover:text-white transition"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>

      <div className="space-y-4 mb-4 max-h-96 overflow-y-auto">
        {items.map((item) => (
          <div key={item.odds.id} className="bg-slate-700 rounded-lg p-3">
            <div className="flex justify-between items-start mb-2">
              <div className="flex-1">
                <p className="font-medium text-sm">
                  {item.event.home_team} vs {item.event.away_team}
                </p>
                <p className="text-slate-400 text-xs">
                  {item.odds.outcome} @ {item.odds.price.toFixed(2)}
                </p>
              </div>
              <button
                onClick={() => removeFromBetSlip(item.odds.id)}
                className="text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div>
              <label className="text-xs text-slate-400">Stake</label>
              <input
                type="number"
                min="1"
                value={item.stake}
                onChange={(e) => updateStake(item.odds.id, Number(e.target.value))}
                className="input text-sm mt-1"
              />
            </div>

            <div className="mt-2 pt-2 border-t border-slate-600">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Potential Payout:</span>
                <span className="font-medium text-green-400">
                  ${(item.stake * item.odds.price).toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500 text-red-500 rounded-lg p-3 mb-4 text-sm">
          {error}
        </div>
      )}

      <div className="border-t border-slate-700 pt-4 space-y-2">
        <div className="flex justify-between">
          <span className="text-slate-400">Total Stake:</span>
          <span className="font-bold">${getTotalStake().toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-400">Potential Payout:</span>
          <span className="font-bold text-green-400">
            ${getTotalPotentialPayout().toFixed(2)}
          </span>
        </div>
      </div>

      <button
        onClick={handlePlaceBets}
        disabled={placeBetsMutation.isPending}
        className="btn btn-success w-full mt-4"
      >
        {placeBetsMutation.isPending ? 'Placing Bets...' : 'Place Bets'}
      </button>
    </div>
  );
}
