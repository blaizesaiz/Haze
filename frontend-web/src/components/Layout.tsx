import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import BetSlip from './BetSlip';

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <Navbar />
      <div className="container mx-auto px-4 py-8 flex gap-6">
        <main className="flex-1">
          <Outlet />
        </main>
        <aside className="w-80 hidden lg:block">
          <BetSlip />
        </aside>
      </div>
    </div>
  );
}
