'use client';

import React, { useState } from 'react';
import UploadImagem from '../components/UploadImagem';
import FormParametros from '../components/FormParametros';
import FormTradeJournal from '../components/FormTradeJournal';
import PainelResultados from '../components/PainelResultados';
import { ParametrosGrafico, RespostaAnalise } from '../types';
import { analisarSetup } from '../services/api';

export default function Home() {
  const [imagem, setImagem] = useState<File | null>(null);
  const [params, setParams] = useState<ParametrosGrafico>({
    pdh: 0, pdl: 0, pdc: 0, pdo: 0,
    max_h4: 0, min_h4: 0,
    max_atual: 0, min_atual: 0
  });
  const [resultado, setResultado] = useState<RespostaAnalise | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setParams({ ...params, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleAnalisar = async () => {
    if (!imagem) {
      setErro('Por favor, faça o upload da imagem do gráfico antes de analisar.');
      return;
    }
    setErro('');
    setCarregando(true);
    try {
      const res = await analisarSetup(imagem, params);
      setResultado(res);
    } catch (err: any) {
      setErro(err.message || 'Erro ao conectar com o backend.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0d111d] text-gray-100 p-4 md:p-8 max-w-7xl mx-auto space-y-6 relative overflow-hidden bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(0,255,136,0.06),rgba(255,255,255,0))]">
      
      {/* Dynamic Glow background effects */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#00ff88]/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 left-10 w-96 h-96 bg-blue-600/5 rounded-full blur-3xl pointer-events-none" />

      {/* Header Profissional */}
      <header className="border-b border-[#232943] pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4 relative">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#00ff88] to-emerald-400 tracking-tight drop-shadow-[0_0_12px_rgba(0,255,136,0.2)]">
              SMC TRADING ANALYZER
            </h1>
            <span className="hidden sm:inline-flex items-center gap-1.5 bg-[#00ff88]/10 border border-[#00ff88]/30 px-2.5 py-0.5 rounded-full text-[10px] font-semibold text-[#00ff88] tracking-wider uppercase">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00ff88] animate-pulse" /> Live Engine
            </span>
          </div>
          <p className="text-xs text-gray-400 font-medium tracking-wide mt-1">
            Análise visual avançada com IA + Mapeamento de Níveis SMC (Smart Money Concepts)
          </p>
        </div>
      </header>

      {/* Alerta de Erro Customizado */}
      {erro && (
        <div className="bg-red-500/10 border border-red-500/30 backdrop-blur-md p-4 rounded-xl text-sm text-red-300 flex items-center gap-3 shadow-lg animate-in fade-in duration-200">
          <span className="text-base">⚠️</span>
          <span className="font-medium">{erro}</span>
        </div>
      )}

      {/* Grid Principal estilo Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 relative z-10">
        
        {/* Painel Esquerdo: Input de Dados */}
        <div className="space-y-6">
          <div className="bg-[#151a2e]/70 border border-[#262c4a] rounded-2xl p-5 shadow-2xl backdrop-blur-xl transition-all duration-300 hover:border-[#00ff88]/30 space-y-6">
            <UploadImagem onImageSelect={setImagem} />
            <FormParametros params={params} onChange={handleInputChange} />
            
            <button
              onClick={handleAnalisar}
              disabled={carregando}
              className="w-full bg-[#00ff88] hover:bg-[#00e67a] active:scale-[0.99] text-[#0b0e17] font-extrabold py-3.5 px-6 rounded-xl transition-all duration-300 shadow-[0_0_20px_rgba(0,255,136,0.25)] hover:shadow-[0_0_30px_rgba(0,255,136,0.45)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm tracking-wide uppercase cursor-pointer"
            >
              {carregando ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-[#0b0e17]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span>A Processar Análise...</span>
                </>
              ) : (
                <>
                  <span>🚀 Executar Análise Completa</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Painel Direito: Resultados & Journal */}
        <div className="space-y-6">
          <div className="bg-[#151a2e]/70 border border-[#262c4a] rounded-2xl p-5 shadow-2xl backdrop-blur-xl transition-all duration-300 hover:border-blue-500/30 space-y-6">
            <PainelResultados resultado={resultado} />
            <FormTradeJournal />
          </div>
        </div>

      </div>
    </main>
  );
}
