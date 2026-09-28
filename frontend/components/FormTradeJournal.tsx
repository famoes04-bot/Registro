'use client';

import React, { useState } from 'react';
import { salvarTrade } from '../services/api';

export default function FormTradeJournal() {
  const [trade, setTrade] = useState({
    par_moeda: 'EURUSD',
    tipo_ordem: 'BUY',
    preco_entrada: 0,
    stop_loss: 0,
    take_profit: 0,
    ideia_nota: ''
  });
  const [mensagem, setMensagem] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await salvarTrade(trade as any);
      setMensagem('Trade/Ideia guardado com sucesso!');
      setTimeout(() => setMensagem(''), 3000);
    } catch (err) {
      setMensagem('Erro ao guardar o trade.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-800 p-4 rounded-xl border border-gray-700 text-white space-y-3">
      <h2 className="text-lg font-bold flex items-center gap-2">
        📝 3. Registar Entrada / Ideia de Trade
      </h2>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="text-xs text-gray-400">Par / Ativo</label>
          <input type="text" value={trade.par_moeda} onChange={e => setTrade({...trade, par_moeda: e.target.value})} className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm" required />
        </div>
        <div>
          <label className="text-xs text-gray-400">Direção</label>
          <select value={trade.tipo_ordem} onChange={e => setTrade({...trade, tipo_ordem: e.target.value as 'BUY' | 'SELL'})} className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm">
            <option value="BUY">BUY 🟩</option>
            <option value="SELL">SELL 🟥</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2">
        <div>
          <label className="text-xs text-gray-400">Preço Entrada</label>
          <input type="number" step="any" onChange={e => setTrade({...trade, preco_entrada: parseFloat(e.target.value)})} className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm" required />
        </div>
        <div>
          <label className="text-xs text-gray-400">Stop Loss (SL)</label>
          <input type="number" step="any" onChange={e => setTrade({...trade, stop_loss: parseFloat(e.target.value)})} className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm" required />
        </div>
        <div>
          <label className="text-xs text-gray-400">Take Profit (TP)</label>
          <input type="number" step="any" onChange={e => setTrade({...trade, take_profit: parseFloat(e.target.value)})} className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm" required />
        </div>
      </div>

      <div>
        <label className="text-xs text-gray-400">Anotação / Ideia do Setup</label>
        <textarea rows={2} value={trade.ideia_nota} onChange={e => setTrade({...trade, ideia_nota: e.target.value})} className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm" placeholder="Ex: Tocamos no PDL, sweep de liquidez + MSS em M1 com FVG" />
      </div>

      <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded transition">
        Guardar Ideia / Trade
      </button>

      {mensagem && <p className="text-xs text-center text-yellow-400 mt-2">{mensagem}</p>}
    </form>
  );
}

