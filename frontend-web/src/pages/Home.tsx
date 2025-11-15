import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { sportsService } from '@/services/sports.service';
import { Trophy, RefreshCw } from 'lucide-react';

export default function Home() {
  const { data: sports, isLoading, refetch } = useQuery({
    queryKey: ['sports'],
    queryFn: () => sportsService.getSports(),
  });

  const handleSyncSports = async () => {
    await sportsService.syncSports();
    refetch();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-slate-400">Loading sports...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Welcome to Haze</h1>
          <p className="text-slate-400 mt-2">Choose a sport to start betting</p>
        </div>
        <button onClick={handleSyncSports} className="btn btn-secondary flex items-center space-x-2">
          <RefreshCw className="w-4 h-4" />
          <span>Sync Sports</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sports?.map((sport) => (
          <Link
            key={sport.id}
            to={`/events/${sport.key}`}
            className="card hover:border-primary-500 transition cursor-pointer group"
          >
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-primary-500/10 rounded-full flex items-center justify-center group-hover:bg-primary-500/20 transition">
                <Trophy className="w-6 h-6 text-primary-500" />
              </div>
              <div>
                <h3 className="text-xl font-bold">{sport.name}</h3>
                <p className="text-slate-400 text-sm">View events</p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {sports?.length === 0 && (
        <div className="card text-center py-12">
          <Trophy className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No Sports Available</h3>
          <p className="text-slate-400 mb-4">Click the Sync Sports button to load available sports</p>
        </div>
      )}
    </div>
  );
}
