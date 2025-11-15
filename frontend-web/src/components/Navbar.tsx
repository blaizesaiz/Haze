import { Link } from 'react-router-dom';
import { Home, Trophy, Wallet, User, LogOut, TrendingUp } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore();

  return (
    <nav className="bg-slate-800 border-b border-slate-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Trophy className="w-8 h-8 text-primary-500" />
            <span className="text-xl font-bold">Haze</span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link to="/" className="flex items-center space-x-2 hover:text-primary-400 transition">
              <Home className="w-5 h-5" />
              <span>Home</span>
            </Link>

            <Link to="/leaderboard" className="flex items-center space-x-2 hover:text-primary-400 transition">
              <TrendingUp className="w-5 h-5" />
              <span>Leaderboard</span>
            </Link>

            {isAuthenticated ? (
              <>
                <Link to="/my-bets" className="flex items-center space-x-2 hover:text-primary-400 transition">
                  <Trophy className="w-5 h-5" />
                  <span>My Bets</span>
                </Link>

                <Link to="/wallet" className="flex items-center space-x-2 hover:text-primary-400 transition">
                  <Wallet className="w-5 h-5" />
                  <span>Wallet</span>
                </Link>

                <div className="relative group">
                  <button className="flex items-center space-x-2 hover:text-primary-400 transition">
                    <User className="w-5 h-5" />
                    <span>{user?.username}</span>
                  </button>

                  <div className="absolute right-0 mt-2 w-48 bg-slate-800 rounded-lg shadow-lg border border-slate-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 hover:bg-slate-700 rounded-t-lg"
                    >
                      Profile
                    </Link>
                    {user?.role === 'admin' && (
                      <Link
                        to="/admin"
                        className="block px-4 py-2 hover:bg-slate-700"
                      >
                        Admin Panel
                      </Link>
                    )}
                    <button
                      onClick={logout}
                      className="w-full text-left px-4 py-2 hover:bg-slate-700 rounded-b-lg flex items-center space-x-2"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn-secondary">
                  Login
                </Link>
                <Link to="/register" className="btn btn-primary">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
