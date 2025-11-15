import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { walletService } from '@/services/wallet.service';
import { format } from 'date-fns';
import { Wallet as WalletIcon, Plus, Minus, ArrowUpRight, ArrowDownRight } from 'lucide-react';

export default function Wallet() {
  const queryClient = useQueryClient();
  const [showDeposit, setShowDeposit] = useState(false);
  const [showWithdraw, setShowWithdraw] = useState(false);
  const [amount, setAmount] = useState('');

  const { data: wallet } = useQuery({
    queryKey: ['wallet'],
    queryFn: () => walletService.getWallet(),
  });

  const { data: transactions } = useQuery({
    queryKey: ['transactions'],
    queryFn: () => walletService.getTransactions(),
  });

  const depositMutation = useMutation({
    mutationFn: (amount: number) => walletService.deposit({ amount, payment_method: 'stripe' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wallet'] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      setShowDeposit(false);
      setAmount('');
    },
  });

  const withdrawMutation = useMutation({
    mutationFn: (amount: number) => walletService.withdraw({ amount }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wallet'] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      setShowWithdraw(false);
      setAmount('');
    },
  });

  const handleDeposit = () => {
    const value = parseFloat(amount);
    if (value > 0) {
      depositMutation.mutate(value);
    }
  };

  const handleWithdraw = () => {
    const value = parseFloat(amount);
    if (value > 0) {
      withdrawMutation.mutate(value);
    }
  };

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'deposit':
      case 'bet_won':
      case 'bonus':
        return <ArrowDownRight className="w-5 h-5 text-green-500" />;
      case 'withdrawal':
      case 'bet_placed':
        return <ArrowUpRight className="w-5 h-5 text-red-500" />;
      default:
        return <WalletIcon className="w-5 h-5 text-slate-500" />;
    }
  };

  const getTransactionColor = (type: string) => {
    switch (type) {
      case 'deposit':
      case 'bet_won':
      case 'bonus':
        return 'text-green-400';
      case 'withdrawal':
      case 'bet_placed':
        return 'text-red-400';
      default:
        return 'text-slate-400';
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Wallet</h1>

      <div className="card mb-8 bg-gradient-to-br from-primary-600 to-primary-800">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-primary-100 text-sm mb-1">Available Balance</p>
            <p className="text-4xl font-bold text-white">
              ${wallet?.balance.toFixed(2) || '0.00'}
            </p>
            <p className="text-primary-100 text-sm mt-2">{wallet?.currency}</p>
          </div>
          <WalletIcon className="w-16 h-16 text-white/20" />
        </div>

        <div className="flex space-x-4 mt-6">
          <button
            onClick={() => setShowDeposit(true)}
            className="btn bg-white text-primary-600 hover:bg-gray-100 flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Deposit</span>
          </button>
          <button
            onClick={() => setShowWithdraw(true)}
            className="btn bg-primary-700 text-white hover:bg-primary-800 flex items-center space-x-2"
          >
            <Minus className="w-4 h-4" />
            <span>Withdraw</span>
          </button>
        </div>
      </div>

      {showDeposit && (
        <div className="card mb-8 border-primary-500">
          <h3 className="text-xl font-bold mb-4">Deposit Funds</h3>
          <div className="space-y-4">
            <div>
              <label className="label">Amount</label>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="input"
                placeholder="Enter amount"
                min="1"
                max="10000"
              />
            </div>
            <div className="flex space-x-4">
              <button
                onClick={handleDeposit}
                disabled={depositMutation.isPending}
                className="btn btn-success"
              >
                {depositMutation.isPending ? 'Processing...' : 'Deposit'}
              </button>
              <button onClick={() => setShowDeposit(false)} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {showWithdraw && (
        <div className="card mb-8 border-yellow-500">
          <h3 className="text-xl font-bold mb-4">Withdraw Funds</h3>
          <div className="space-y-4">
            <div>
              <label className="label">Amount</label>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="input"
                placeholder="Enter amount"
                min="1"
              />
            </div>
            <div className="flex space-x-4">
              <button
                onClick={handleWithdraw}
                disabled={withdrawMutation.isPending}
                className="btn btn-primary"
              >
                {withdrawMutation.isPending ? 'Processing...' : 'Withdraw'}
              </button>
              <button onClick={() => setShowWithdraw(false)} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <h3 className="text-xl font-bold mb-4">Transaction History</h3>
        <div className="space-y-3">
          {transactions?.map((transaction) => (
            <div
              key={transaction.id}
              className="flex items-center justify-between p-3 bg-slate-700 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                {getTransactionIcon(transaction.type)}
                <div>
                  <p className="font-medium">
                    {transaction.type.replace('_', ' ').charAt(0).toUpperCase() +
                      transaction.type.replace('_', ' ').slice(1)}
                  </p>
                  {transaction.description && (
                    <p className="text-slate-400 text-sm">{transaction.description}</p>
                  )}
                  <p className="text-slate-500 text-xs">
                    {format(new Date(transaction.created_at), 'PPp')}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className={`font-bold ${getTransactionColor(transaction.type)}`}>
                  {['deposit', 'bet_won', 'bonus'].includes(transaction.type) ? '+' : '-'}$
                  {transaction.amount.toFixed(2)}
                </p>
                <span
                  className={`text-xs px-2 py-0.5 rounded ${
                    transaction.status === 'completed'
                      ? 'bg-green-500/20 text-green-400'
                      : transaction.status === 'pending'
                      ? 'bg-yellow-500/20 text-yellow-400'
                      : 'bg-red-500/20 text-red-400'
                  }`}
                >
                  {transaction.status}
                </span>
              </div>
            </div>
          ))}
        </div>

        {transactions?.length === 0 && (
          <p className="text-slate-400 text-center py-8">No transactions yet</p>
        )}
      </div>
    </div>
  );
}
