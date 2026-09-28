'use client';

import React from 'react';
import { RespostaAnalise } from '../types';

interface Props {
  resultado: RespostaAnalise | null;
}

export default function PainelResultados({ resultado }: Props) {
  if (!resultado) return null;

  const { niveis_calculados, detecoes_visuais, vies_sugerido } = resultado;

  return (
    <div className="bg-gray-800 p-4 rounded-xl border border-gray-700 text-white space-y-4">
      <h2 className="text-xl font-bold text-blue-400 flex items-center gap-2">
        🎯 Resultado da Análise SMC
      </h2>

      {/* Viés Sugerido */}
      <div className="bg-gray-900 p-3 rounded-lg border border-blue-500/30">
        <span className="text-xs text-gray-400 block">Viés do Dia Sugerido:</span>
        <span className="text-lg font-bold text-yellow-300">{vies_sugerido}</span>
      </div>

      {/* Equilibriums Calculados */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-gray-900 p-2 rounded">
          <p className="text-xs text-gray-400">EQ Diário</p>
          <p className="font-bold text-blue-400">{niveis_calculados.diario_anterior.eq_diario}</p>
        </div>
        <div className="bg-gray-900 p-2 rounded">
          <p className="text-xs text-gray-400">EQ H4</p>
          <p className="font-bold text-yellow-400">{niveis_calculados.h4_anterior.eq_h4}</p>
        </div>
        <div className="bg-gray-900 p-2 rounded">
          <p className="text-xs text-gray-400">EQ Atual</p>
          <p className="font-bold text-green-400">{niveis_calculados.dia_atual.eq_atual}</p>
        </div>
      </div>

      {/* Padrões Visuais da IA */}
      <div>
        <h3 className="text-sm font-semibold mb-2">Padrões Identificados pela IA (YOLOv8):</h3>
        {detecoes_visuais.length === 0 ? (
          <p className="text-xs text-gray-500 italic">Nenhum padrão visual detetado com confiança suficiente.</p>
        ) : (
          <ul className="space-y-1">
            {detecoes_visuais.map((item, idx) => (
              <li key={idx} className="bg-gray-900 p-2 rounded text-xs flex justify-between">
                <span className="font-bold text-purple-400">{item.padrao}</span>
                <span className="text-gray-400">Confiança: {(item.confianca * 100).toFixed(1)}%</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

