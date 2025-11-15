import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { Users, Trophy, DollarSign } from 'lucide-react';
import { format } from 'date-fns';

export default function AdminDashboard() {
  const { data: users } = useQuery({
    queryKey: ['admin-users'],
    queryFn: async () => {
      const response = await api.get('/admin/users');
      return response.data;
    },
  });

  const { data: bets } = useQuery({
    queryKey: ['admin-bets'],
    queryFn: async () => {
      const response = await api.get('/admin/bets');
      return response.data;
    },
  });

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Total Users</p>
              <p className="text-3xl font-bold">{users?.length || 0}</p>
            </div>
            <Users className="w-12 h-12 text-primary-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Total Bets</p>
              <p className="text-3xl font-bold">{bets?.length || 0}</p>
            </div>
            <Trophy className="w-12 h-12 text-green-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Total Volume</p>
              <p className="text-3xl font-bold">
                ${bets?.reduce((sum: number, bet: any) => sum + bet.stake, 0).toFixed(2) || '0.00'}
              </p>
            </div>
            <DollarSign className="w-12 h-12 text-yellow-500" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Recent Users</h2>
          <div className="space-y-2">
            {users?.slice(0, 10).map((user: any) => (
              <div
                key={user.id}
                className="flex items-center justify-between p-3 bg-slate-700 rounded-lg"
              >
                <div>
                  <p className="font-medium">{user.username}</p>
                  <p className="text-slate-400 text-sm">{user.email}</p>
                </div>
                <div className="text-right">
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      user.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                    }`}
                  >
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                  <p className="text-slate-400 text-xs mt-1">
                    {format(new Date(user.created_at), 'PP')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">Recent Bets</h2>
          <div className="space-y-2">
            {bets?.slice(0, 10).map((bet: any) => (
              <div
                key={bet.id}
                className="flex items-center justify-between p-3 bg-slate-700 rounded-lg"
              >
                <div>
                  <p className="font-medium">Bet #{bet.id}</p>
                  <p className="text-slate-400 text-sm">User ID: {bet.user_id}</p>
                </div>
                <div className="text-right">
                  <p className="font-bold">${bet.stake.toFixed(2)}</p>
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      bet.status === 'won'
                        ? 'bg-green-500/20 text-green-400'
                        : bet.status === 'lost'
                        ? 'bg-red-500/20 text-red-400'
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}
                  >
                    {bet.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
