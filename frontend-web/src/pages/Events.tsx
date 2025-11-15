import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { sportsService } from '@/services/sports.service';
import { useBetSlipStore } from '@/store/betSlipStore';
import { format } from 'date-fns';
import { RefreshCw, Calendar, Plus } from 'lucide-react';

export default function Events() {
  const { sportKey } = useParams<{ sportKey: string }>();
  const { addToBetSlip, items } = useBetSlipStore();

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['events', sportKey],
    queryFn: () => sportsService.getEvents(sportKey!),
    enabled: !!sportKey,
  });

  const handleSyncOdds = async () => {
    if (sportKey) {
      await sportsService.syncOdds(sportKey);
      refetch();
    }
  };

  const isInBetSlip = (oddsId: number) => {
    return items.some((item) => item.odds.id === oddsId);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-slate-400">Loading events...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold capitalize">{sportKey?.replace('_', ' ')} Events</h1>
          <p className="text-slate-400 mt-2">{data?.total || 0} events available</p>
        </div>
        <button onClick={handleSyncOdds} className="btn btn-secondary flex items-center space-x-2">
          <RefreshCw className="w-4 h-4" />
          <span>Sync Odds</span>
        </button>
      </div>

      <div className="space-y-4">
        {data?.events.map((event) => (
          <div key={event.id} className="card">
            <div className="flex items-center justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-xl font-bold">
                  {event.home_team} vs {event.away_team}
                </h3>
                <div className="flex items-center space-x-2 text-slate-400 text-sm mt-1">
                  <Calendar className="w-4 h-4" />
                  <span>{format(new Date(event.commence_time), 'PPp')}</span>
                  {event.is_live && (
                    <span className="bg-red-500 text-white px-2 py-0.5 rounded text-xs font-bold">
                      LIVE
                    </span>
                  )}
                </div>
              </div>
              {event.is_live && event.home_score !== undefined && (
                <div className="text-right">
                  <div className="text-2xl font-bold">
                    {event.home_score} - {event.away_score}
                  </div>
                </div>
              )}
            </div>

            {event.markets.length > 0 ? (
              <div className="space-y-4">
                {event.markets.map((market) => (
                  <div key={market.id}>
                    <h4 className="text-sm font-medium text-slate-400 mb-2 uppercase">
                      {market.name}
                    </h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {market.odds.slice(0, 6).map((odds) => (
                        <button
                          key={odds.id}
                          onClick={() => addToBetSlip(event, odds)}
                          disabled={isInBetSlip(odds.id)}
                          className={`p-3 rounded-lg border transition ${
                            isInBetSlip(odds.id)
                              ? 'bg-primary-500/20 border-primary-500'
                              : 'bg-slate-700 border-slate-600 hover:border-primary-500'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="text-left">
                              <p className="text-sm font-medium">{odds.outcome}</p>
                              {odds.point && (
                                <p className="text-xs text-slate-400">
                                  {odds.point > 0 ? '+' : ''}
                                  {odds.point}
                                </p>
                              )}
                            </div>
                            <div className="flex items-center space-x-1">
                              <span className="font-bold text-primary-400">
                                {odds.price.toFixed(2)}
                              </span>
                              {!isInBetSlip(odds.id) && (
                                <Plus className="w-4 h-4 text-slate-400" />
                              )}
                            </div>
                          </div>
                          <p className="text-xs text-slate-500 mt-1">{odds.bookmaker}</p>
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-400 text-center py-4">
                No odds available. Try syncing odds for this sport.
              </p>
            )}
          </div>
        ))}
      </div>

      {data?.events.length === 0 && (
        <div className="card text-center py-12">
          <h3 className="text-xl font-bold mb-2">No Events Available</h3>
          <p className="text-slate-400 mb-4">
            Click Sync Odds to load events and odds for this sport
          </p>
        </div>
      )}
    </div>
  );
}
