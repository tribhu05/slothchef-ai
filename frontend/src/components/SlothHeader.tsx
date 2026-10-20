import React from 'react';
import { Brain, Cpu, Sparkles } from 'lucide-react';

interface SlothHeaderProps {
  onOpenExplainer: () => void;
  inferenceMode: 'local' | 'cloud' | 'demo';
}

export const SlothHeader: React.FC<SlothHeaderProps> = ({ onOpenExplainer, inferenceMode }) => {
  const getBadgeConfig = () => {
    switch (inferenceMode) {
      case 'local':
        return {
          label: 'Local AI (Gemma 2)',
          dotColor: 'bg-emerald-400',
          textColor: 'text-emerald-400',
          bgColor: 'bg-emerald-500/10',
          borderColor: 'border-emerald-500/20'
        };
      case 'cloud':
        return {
          label: 'Cloud AI (TabPFN + Gemma)',
          dotColor: 'bg-amber-300',
          textColor: 'text-[#F4D779]',
          bgColor: 'bg-[#F4D779]/10',
          borderColor: 'border-[#F4D779]/20'
        };
      case 'demo':
      default:
        return {
          label: 'Fast Engine (TabPFN-3.5)',
          dotColor: 'bg-[#F4D779]',
          textColor: 'text-[#F4D779]',
          bgColor: 'bg-[#F4D779]/10',
          borderColor: 'border-[#F4D779]/20'
        };
    }
  };

  const badge = getBadgeConfig();

  return (
    <header className="border-b border-white/[0.07] bg-[#181818]/90 backdrop-blur-xl sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between gap-4">
        {/* Logo and Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-[#202020] border border-white/[0.08] flex items-center justify-center text-xl shadow-inner">
            🦥
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <span className="font-display font-bold text-lg tracking-tight text-[#F5F2EB]">
                SlothChef
              </span>
              <span className="text-[10px] font-semibold tracking-wide px-2 py-0.5 rounded-full bg-white/[0.05] text-[#A5A39D] border border-white/[0.08] uppercase">
                DEV W3
              </span>
            </div>
            <p className="text-[11px] text-[#A5A39D] font-normal hidden sm:block">
              Your kitchen. Your ingredients. Absolutely minimal effort.
            </p>
          </div>
        </div>

        {/* Status Indicators & Actions */}
        <div className="flex items-center gap-2.5 text-xs">
          {/* Real Inference Mode Badge */}
          <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full ${badge.bgColor} ${badge.borderColor} border font-medium ${badge.textColor}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${badge.dotColor} animate-pulse`} />
            <span className="text-[11px] font-mono tracking-tight">{badge.label}</span>
          </div>

          {/* TabPFN Telemetry Button */}
          <button
            onClick={onOpenExplainer}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#202020] hover:bg-[#292929] text-[#A5A39D] hover:text-[#F5F2EB] border border-white/[0.08] transition-all cursor-pointer font-medium"
            title="Inspect Prior Labs TabPFN Bayesian In-Context Model"
          >
            <Brain className="w-3.5 h-3.5 text-[#F4D779]" />
            <span className="hidden sm:inline text-xs">TabPFN Math</span>
          </button>
        </div>
      </div>
    </header>
  );
};
