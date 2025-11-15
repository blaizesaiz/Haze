import { useQuery } from '@tanstack/react-query';
import { bettingService } from '@/services/betting.service';
import { format } from 'date-fns';
import { Trophy, TrendingUp, TrendingDown } from 'lucide-react';

export default function MyBets() {
  const { data: betsData } = useQuery({
    queryKey: ['bets'],
    queryFn: () => bettingService.getMyBets(),
  });

  const { data: stats } = useQuery({
    queryKey: ['bet-stats'],
    queryFn: () => bettingService.getBetStats(),
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'won':
        return 'text-green-400';
      case 'lost':
        return 'text-red-400';
      case 'pending':
        return 'text-yellow-400';
      default:
        return 'text-slate-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'won':
        return 'bg-green-500/10 border-green-500';
      case 'lost':
        return 'bg-red-500/10 border-red-500';
      case 'pending':
        return 'bg-yellow-500/10 border-yellow-500';
      default:
        return 'bg-slate-500/10 border-slate-500';
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">My Bets</h1>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Total Bets</p>
                <p className="text-2xl font-bold">{stats.total_bets}</p>
              </div>
              <Trophy className="w-8 h-8 text-primary-500" />
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Win Rate</p>
                <p className="text-2xl font-bold">{stats.win_rate.toFixed(1)}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Total Staked</p>
                <p className="text-2xl font-bold">${stats.total_staked.toFixed(2)}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Total Profit</p>
                <p className={`text-2xl font-bold ${stats.total_profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  ${stats.total_profit.toFixed(2)}
                </p>
              </div>
              {stats.total_profit >= 0 ? (
                <TrendingUp className="w-8 h-8 text-green-500" />
              ) : (
                <TrendingDown className="w-8 h-8 text-red-500" />
              )}
            </div>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {betsData?.bets.map((bet) => (
          <div key={bet.id} className={`card border ${getStatusBg(bet.status)}`}>
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${getStatusColor(bet.status)}`}>
                    {bet.status}
                  </span>
                  <span className="text-slate-400 text-sm">
                    {format(new Date(bet.created_at), 'PPp')}
                  </span>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-3">
                  <div>
                    <p className="text-slate-400 text-xs">Stake</p>
                    <p className="font-bold">${bet.stake.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-xs">Odds</p>
                    <p className="font-bold">{bet.odds_value.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-xs">Potential Payout</p>
                    <p className="font-bold text-green-400">${bet.potential_payout.toFixed(2)}</p>
                  </div>
                  {bet.settled_at && (
                    <div>
                      <p className="text-slate-400 text-xs">Settled</p>
                      <p className="text-sm">{format(new Date(bet.settled_at), 'PP')}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {betsData?.bets.length === 0 && (
        <div className="card text-center py-12">
          <Trophy className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No Bets Yet</h3>
          <p className="text-slate-400">Start betting to see your bet history here</p>
        </div>
      )}
    </div>
  );
}
