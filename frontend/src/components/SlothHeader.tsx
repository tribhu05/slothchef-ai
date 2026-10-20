import React from 'react';
import { Sparkles, Utensils, Brain, ShieldCheck } from 'lucide-react';

interface SlothHeaderProps {
  onOpenExplainer: () => void;
}

export const SlothHeader: React.FC<SlothHeaderProps> = ({ onOpenExplainer }) => {
  return (
    <header className="border-b border-amber-200/60 bg-amber-100/40 backdrop-blur-md sticky top-0 z-30">
      <div className="max-w-6xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-amber-600 to-amber-400 flex items-center justify-center text-2xl shadow-md shadow-amber-900/10 transform -rotate-3">
            🦥
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display font-bold text-xl tracking-tight text-amber-950">
                SlothChef
              </span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                DEV Hacktoberfest W3
              </span>
            </div>
            <p className="text-xs text-amber-800/80 font-medium hidden sm:block">
              The Extreme Low-Effort, One-Pan Survival Engine
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={onOpenExplainer}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/80 hover:bg-white text-stone-700 hover:text-stone-900 border border-amber-200 transition-all shadow-xs cursor-pointer font-medium"
          >
            <Brain className="w-3.5 h-3.5 text-purple-600" />
            <span>TabPFN-3.5 Math</span>
          </button>

          <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-200/50 text-amber-900 border border-amber-300/60 font-medium">
            <Utensils className="w-3.5 h-3.5 text-amber-700" />
            <span>Rule: Strict 1-Pan Cap</span>
          </div>

          <div className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-emerald-500/10 text-emerald-800 border border-emerald-500/20 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Gemma 2 + TabPFN</span>
          </div>
        </div>
      </div>
    </header>
  );
};
