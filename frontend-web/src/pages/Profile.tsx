import { useAuthStore } from '@/store/authStore';
import { User, Mail, Calendar, Shield } from 'lucide-react';
import { format } from 'date-fns';

export default function Profile() {
  const { user } = useAuthStore();

  if (!user) return null;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Profile</h1>

      <div className="card">
        <div className="flex items-center space-x-6 mb-6">
          <div className="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center">
            <User className="w-10 h-10 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold">{user.username}</h2>
            {user.full_name && <p className="text-slate-400">{user.full_name}</p>}
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center space-x-3 p-3 bg-slate-700 rounded-lg">
            <Mail className="w-5 h-5 text-slate-400" />
            <div>
              <p className="text-slate-400 text-sm">Email</p>
              <p className="font-medium">{user.email}</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-slate-700 rounded-lg">
            <Shield className="w-5 h-5 text-slate-400" />
            <div>
              <p className="text-slate-400 text-sm">Role</p>
              <p className="font-medium capitalize">{user.role}</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-slate-700 rounded-lg">
            <Calendar className="w-5 h-5 text-slate-400" />
            <div>
              <p className="text-slate-400 text-sm">Member Since</p>
              <p className="font-medium">{format(new Date(user.created_at), 'PPP')}</p>
            </div>
          </div>

          {user.last_login && (
            <div className="flex items-center space-x-3 p-3 bg-slate-700 rounded-lg">
              <Calendar className="w-5 h-5 text-slate-400" />
              <div>
                <p className="text-slate-400 text-sm">Last Login</p>
                <p className="font-medium">{format(new Date(user.last_login), 'PPp')}</p>
              </div>
            </div>
          )}

          <div className="flex items-center space-x-3 p-3 bg-slate-700 rounded-lg">
            <div className="flex items-center space-x-2">
              <span
                className={`w-3 h-3 rounded-full ${user.is_active ? 'bg-green-500' : 'bg-red-500'}`}
              ></span>
              <p className="text-slate-400 text-sm">Status</p>
            </div>
            <p className="font-medium">{user.is_active ? 'Active' : 'Inactive'}</p>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-slate-700 rounded-lg">
            <div className="flex items-center space-x-2">
              <span
                className={`w-3 h-3 rounded-full ${user.is_verified ? 'bg-green-500' : 'bg-yellow-500'}`}
              ></span>
              <p className="text-slate-400 text-sm">Verification</p>
            </div>
            <p className="font-medium">{user.is_verified ? 'Verified' : 'Not Verified'}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
