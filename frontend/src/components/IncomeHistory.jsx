import { useState, useEffect, useCallback } from 'react';
import { DollarSign, ArrowUpRight, ArrowDownRight, Calendar, Download } from 'lucide-react';
import { hostService } from '../services/hostService';

const IncomeHistory = () => {
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({ total: 0, pending: 0, thisMonth: 0 });
  const [loading, setLoading] = useState(true);

  const fetchIncome = useCallback(async () => {
    setLoading(true);
    const data = await hostService.getIncomeHistory();
    setHistory(data.transactions);
    setStats(data.stats);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchIncome();
  }, [fetchIncome]);

  if (loading) {
    return <div className="animate-pulse space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[1, 2, 3].map(i => <div key={i} className="h-32 bg-gray-100 rounded-xl" />)}
      </div>
      <div className="h-64 bg-gray-100 rounded-xl" />
    </div>;
  }

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div className="bg-green-100 p-2 rounded-lg">
              <DollarSign className="text-green-600" size={24} />
            </div>
            <span className="flex items-center text-green-600 text-sm font-bold bg-green-50 px-2 py-0.5 rounded-full">
              <ArrowUpRight size={14} /> +12%
            </span>
          </div>
          <h3 className="text-gray-500 text-sm font-medium">Revenus Totaux</h3>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stats.total.toLocaleString()} FCFA</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Calendar className="text-blue-600" size={24} />
            </div>
          </div>
          <h3 className="text-gray-500 text-sm font-medium">Ce Mois</h3>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stats.thisMonth.toLocaleString()} FCFA</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div className="bg-orange-100 p-2 rounded-lg">
              <ArrowDownRight className="text-orange-600" size={24} />
            </div>
          </div>
          <h3 className="text-gray-500 text-sm font-medium">En attente</h3>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stats.pending.toLocaleString()} FCFA</p>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 className="font-bold text-gray-900">Dernières Transactions</h3>
          <button className="flex items-center gap-2 text-sm text-blue-600 font-medium hover:bg-blue-50 px-3 py-1.5 rounded-lg transition-colors">
            <Download size={16} /> Exporter
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider font-bold">
                <th className="px-6 py-4">Propriété</th>
                <th className="px-6 py-4">Date</th>
                <th className="px-6 py-4">Type</th>
                <th className="px-6 py-4 text-right">Montant</th>
                <th className="px-6 py-4">Statut</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {history.map((tx) => (
                <tr key={tx.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    <span className="font-medium text-gray-900">{tx.property_title}</span>
                  </td>
                  <td className="px-6 py-4 text-gray-500 text-sm">{tx.date}</td>
                  <td className="px-6 py-4">
                    <span className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-600 font-medium">
                      {tx.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right font-bold text-gray-900">
                    {tx.amount.toLocaleString()} FCFA
                  </td>
                  <td className="px-6 py-4">
                    <span className={`text-xs px-2 py-1 rounded-full font-bold ${
                      tx.status === 'COMPLETED' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
                    }`}>
                      {tx.status === 'COMPLETED' ? 'Payé' : 'En attente'}
                    </span>
                  </td>
                </tr>
              ))}
              {history.length === 0 && (
                <tr>
                  <td colSpan="5" className="px-6 py-12 text-center text-gray-500">
                    Aucune transaction trouvée.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default IncomeHistory;
