<main className="min-h-screen bg-[#131629] text-gray-100 p-6 space-y-6 relative overflow-hidden bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(0,255,136,0.08),rgba(255,255,255,0))]">
  {/* Cartão Estilo Glassmorphism */}
  <div className="bg-[#1c203b]/60 border border-[#2b3054]/80 rounded-2xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.37)] backdrop-blur-xl transition-all duration-300 hover:border-[#00ff88]/30">
    <h2 className="text-gray-400 font-medium text-xs uppercase tracking-wider mb-3">Visão Geral de Liquidez</h2>
    
    {/* Valor em Destaque Verde Néon */}
    <div className="text-3xl font-extrabold text-[#00ff88] drop-shadow-[0_0_15px_rgba(0,255,136,0.35)] flex items-baseline gap-3">
      $ 3,200 <span className="text-xs text-emerald-400 font-medium bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full inline-flex items-center gap-1 shadow-[0_0_10px_rgba(16,185,129,0.15)]">+2.37% ▲</span>
    </div>
  </div>
</main>

/* Estilo escuro com destaques em Verde Neon (Emerald/Green Tailwind) */
<main className="min-h-screen bg-slate-950 text-emerald-400 p-6 max-w-6xl mx-auto space-y-6">
  {/* Cabeçalho */}
  <header className="border-b border-emerald-900/40 pb-4 relative after:absolute after:bottom-[-1px] after:left-0 after:w-24 after:h-[1px] after:bg-emerald-400/80">
    <h1 className="text-2xl font-black text-emerald-400 tracking-wider drop-shadow-[0_0_12px_rgba(52,211,153,0.3)]">
      SMC TRADING ANALYZER
    </h1>
    <p className="text-xs text-emerald-500/80 font-medium tracking-wide mt-1">
      M1/M5 Chart Analysis &amp; Order Flow Engine
    </p>
  </header>

  {/* Botão de Ação Verde Neon */}
  <button className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-3.5 rounded-xl transition-all duration-300 shadow-[0_0_20px_rgba(16,185,129,0.25)] hover:shadow-[0_0_30px_rgba(16,185,129,0.45)] active:scale-[0.99] cursor-pointer">
    🚀 Executar Análise Completa
  </button>
</main>
