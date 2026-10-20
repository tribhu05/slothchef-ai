import React from 'react';
import { X, Brain, Zap, Layers, CheckCircle2 } from 'lucide-react';

interface TabPFNExplainerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TabPFNExplainerModal: React.FC<TabPFNExplainerModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-[#181818] rounded-3xl max-w-2xl w-full p-6 md:p-8 border border-white/[0.1] shadow-2xl relative max-h-[90vh] overflow-y-auto text-[#F5F2EB]">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full hover:bg-white/[0.08] text-[#A5A39D] hover:text-[#F5F2EB] transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Title */}
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-2xl bg-[#202020] border border-[#F4D779]/30 text-[#F4D779] flex items-center justify-center">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-display font-bold text-lg text-[#F5F2EB]">
              Prior Labs TabPFN-3.5 Foundation Model
            </h3>
            <span className="text-xs text-[#F4D779] font-medium font-mono">
              In-Context Bayesian Tabular Inference
            </span>
          </div>
        </div>

        <p className="text-xs text-[#A5A39D] leading-relaxed mb-5">
          Most generative AI cooking apps attempt to use LLMs for both text generation and numerical prediction. 
          LLMs hallucinate culinary chemistry ratios, misjudge moisture/lipid physics, and are notoriously slow.
        </p>

        <div className="space-y-3 mb-6 text-xs">
          <div className="p-4 rounded-2xl bg-[#202020] border border-white/[0.06]">
            <div className="flex items-center gap-2 font-semibold text-[#F5F2EB] mb-1.5">
              <Zap className="w-4 h-4 text-[#F4D779]" />
              <span>1. In-Context Inference Without Training</span>
            </div>
            <p className="leading-relaxed text-[#A5A39D]">
              TabPFN approximates Bayesian inference over synthetic prior distributions in a single forward pass (sub-45 milliseconds). 
              SlothChef transforms raw ingredients into continuous chemical vectors (umami, acidity, moisture, lipid richness, and saltiness) 
              and queries TabPFN to predict flavor harmony and physical prep fatigue without iterative gradient updates.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#202020] border border-white/[0.06]">
            <div className="flex items-center gap-2 font-semibold text-[#F5F2EB] mb-1.5">
              <Layers className="w-4 h-4 text-[#F4D779]" />
              <span>2. Multi-Objective Sloth Constraints</span>
            </div>
            <p className="leading-relaxed text-[#A5A39D]">
              Beyond taste synergy, TabPFN evaluates physical human effort: active standing minutes, vessel load bounds, 
              and cleanup overhead. If a combination exceeds 1 pan or 5 minutes of standing, it applies mathematical effort penalties.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#202020] border border-white/[0.06]">
            <div className="flex items-center gap-2 font-semibold text-[#F5F2EB] mb-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>3. The Decoupled Dual-Engine Architecture</span>
            </div>
            <p className="leading-relaxed text-[#A5A39D]">
              TabPFN serves as the analytical brain (chemical affinity, numeric scoring, physical effort bounds), 
              while Google Gemma 2 acts as the culinary diplomat, translating those numerical constraints into witty, low-effort cooking instructions.
            </p>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2.5 rounded-xl bg-[#F4D779] text-[#181818] font-bold text-xs hover:bg-[#E8CA6B] transition-colors cursor-pointer"
          >
            Close & Cook Lazy
          </button>
        </div>
      </div>
    </div>
  );
};
