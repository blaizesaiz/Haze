import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { Trophy, Medal, Award } from 'lucide-react';

export default function Leaderboard() {
  const [period, setPeriod] = useState<'daily' | 'weekly' | 'monthly' | 'all_time'>('all_time');

  const { data, isLoading } = useQuery({
    queryKey: ['leaderboard', period],
    queryFn: async () => {
      const response = await api.get(`/social/leaderboard?period=${period}`);
      return response.data;
    },
  });

  const getRankIcon = (rank: number | null) => {
    if (!rank) return null;

    switch (rank) {
      case 1:
        return <Trophy className="w-6 h-6 text-yellow-500" />;
      case 2:
        return <Medal className="w-6 h-6 text-slate-400" />;
      case 3:
        return <Award className="w-6 h-6 text-amber-700" />;
      default:
        return <span className="text-slate-400 font-bold">#{rank}</span>;
    }
  };

  const getRankBg = (rank: number | null) => {
    if (!rank) return '';

    switch (rank) {
      case 1:
        return 'bg-yellow-500/10 border-yellow-500';
      case 2:
        return 'bg-slate-400/10 border-slate-400';
      case 3:
        return 'bg-amber-700/10 border-amber-700';
      default:
        return '';
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Leaderboard</h1>

      <div className="card mb-6">
        <div className="flex space-x-2">
          {(['daily', 'weekly', 'monthly', 'all_time'] as const).map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`btn ${period === p ? 'btn-primary' : 'btn-secondary'}`}
            >
              {p.replace('_', ' ').charAt(0).toUpperCase() + p.replace('_', ' ').slice(1)}
            </button>
          ))}
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center min-h-[400px]">
          <div className="text-slate-400">Loading leaderboard...</div>
        </div>
      ) : (
        <div className="space-y-3">
          {data?.entries.map((entry: any) => (
            <div
              key={entry.id}
              className={`card flex items-center justify-between border ${getRankBg(entry.rank)}`}
            >
              <div className="flex items-center space-x-4">
                <div className="w-12 flex items-center justify-center">
                  {getRankIcon(entry.rank)}
                </div>
                <div>
                  <p className="font-bold text-lg">{entry.user.username}</p>
                  <p className="text-slate-400 text-sm">{entry.user.full_name}</p>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-8 text-center">
                <div>
                  <p className="text-slate-400 text-xs">Bets</p>
                  <p className="font-bold">{entry.total_bets}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs">Won</p>
                  <p className="font-bold text-green-400">{entry.won_bets}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs">Win Rate</p>
                  <p className="font-bold">{entry.win_rate.toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs">Profit</p>
                  <p
                    className={`font-bold ${entry.total_profit >= 0 ? 'text-green-400' : 'text-red-400'}`}
                  >
                    ${entry.total_profit.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {data?.entries.length === 0 && (
        <div className="card text-center py-12">
          <Trophy className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No Entries Yet</h3>
          <p className="text-slate-400">Be the first to place a bet and appear on the leaderboard!</p>
        </div>
      )}
    </div>
  );
}
