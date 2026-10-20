import React from 'react';
import { X, Brain, Zap, Layers, CheckCircle2 } from 'lucide-react';

interface TabPFNExplainerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TabPFNExplainerModal: React.FC<TabPFNExplainerModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white rounded-3xl max-w-2xl w-full p-6 md:p-8 border border-amber-200 shadow-2xl relative max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full hover:bg-stone-100 text-stone-500 hover:text-stone-800 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-3">
          <div className="w-9 h-9 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-display font-bold text-lg text-stone-900">
              Why TabPFN-3.5 Powers SlothChef
            </h3>
            <span className="text-xs text-purple-700 font-semibold">
              Prior Labs Tabular Foundation Model Integration
            </span>
          </div>
        </div>

        <p className="text-xs text-stone-600 leading-relaxed mb-4">
          Most AI apps attempt to use LLMs for everything, including tabular prediction and numerical regression. 
          LLMs hallucinate culinary ratios, misjudge moisture/lipid physics, and are notoriously slow.
        </p>

        <div className="space-y-3 mb-6 text-xs">
          <div className="p-3.5 rounded-2xl bg-purple-50/70 border border-purple-200 text-stone-800">
            <div className="flex items-center gap-2 font-bold text-purple-900 mb-1">
              <Zap className="w-4 h-4 text-purple-700" />
              <span>1. In-Context Tabular Prediction Without Training</span>
            </div>
            <p className="leading-relaxed text-stone-600">
              TabPFN approximates Bayesian inference over synthetic prior data in a single forward pass. 
              SlothChef transforms raw ingredients into chemical vectors (umami, acidity, moisture, lipid richness, and saltiness) 
              and queries TabPFN to predict flavor harmony and effort indices in sub-50 milliseconds.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-amber-50/70 border border-amber-200 text-stone-800">
            <div className="flex items-center gap-2 font-bold text-amber-900 mb-1">
              <Layers className="w-4 h-4 text-amber-700" />
              <span>2. Multi-Objective Sloth Constraints</span>
            </div>
            <p className="leading-relaxed text-stone-600">
              Beyond taste harmony, TabPFN predicts **Physical Human Effort**: active standing minutes, cooking vessel bounds, 
              and cleanup overhead. If a combination requires more than 1 pan or 5 minutes of standing, it triggers penalties.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-emerald-50/70 border border-emerald-200 text-stone-800">
            <div className="flex items-center gap-2 font-bold text-emerald-900 mb-1">
              <CheckCircle2 className="w-4 h-4 text-emerald-700" />
              <span>3. The Dual-Engine Pipeline (TabPFN + Gemma 2)</span>
            </div>
            <p className="leading-relaxed text-stone-600">
              TabPFN acts as the analytical brain (chemical affinity, numeric scoring, effort bounds), 
              while Google's Gemma 2 acts as the culinary diplomat (turning numbers into an unapologetically lazy, witty recipe).
            </p>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-stone-900 text-white font-bold text-xs hover:bg-stone-800 transition-colors cursor-pointer"
          >
            Got it, let's cook lazy
          </button>
        </div>
      </div>
    </div>
  );
};
