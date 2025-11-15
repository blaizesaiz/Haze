import api from './api';

export interface Wallet {
  id: number;
  user_id: number;
  balance: number;
  currency: string;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: number;
  wallet_id: number;
  type: 'deposit' | 'withdrawal' | 'bet_placed' | 'bet_won' | 'bet_refund' | 'bonus' | 'adjustment';
  amount: number;
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
  description?: string;
  reference_id?: string;
  bet_id?: number;
  created_at: string;
}

export interface DepositRequest {
  amount: number;
  payment_method: string;
}

export interface WithdrawalRequest {
  amount: number;
}

export const walletService = {
  async getWallet(): Promise<Wallet> {
    const response = await api.get<Wallet>('/wallet');
    return response.data;
  },

  async deposit(data: DepositRequest): Promise<Transaction> {
    const response = await api.post<Transaction>('/wallet/deposit', data);
    return response.data;
  },

  async withdraw(data: WithdrawalRequest): Promise<Transaction> {
    const response = await api.post<Transaction>('/wallet/withdraw', data);
    return response.data;
  },

  async getTransactions(skip = 0, limit = 100): Promise<Transaction[]> {
    const response = await api.get<Transaction[]>('/wallet/transactions', {
      params: { skip, limit },
    });
    return response.data;
  },
};
