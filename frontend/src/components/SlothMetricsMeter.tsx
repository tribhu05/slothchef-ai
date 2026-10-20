import React from 'react';
import { TabPFNPrediction } from '../types';
import { Zap, CheckCircle2, Sparkles, Clock, Utensils, Award } from 'lucide-react';

interface SlothMetricsMeterProps {
  prediction: TabPFNPrediction;
  slothScore?: number;
}

export const SlothMetricsMeter: React.FC<SlothMetricsMeterProps> = ({ prediction, slothScore = 96 }) => {
  const harmony = prediction.harmony_score;

  return (
    <div className="bg-[#181818] text-[#F5F2EB] rounded-3xl p-5 sm:p-6 shadow-xl border border-white/[0.07] mb-7">
      {/* Header telemetry tag */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-white/[0.06] pb-3.5 mb-5">
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-[#F4D779]" />
          <h3 className="font-display font-bold text-xs tracking-wider text-[#A5A39D] uppercase">
            Prior Labs TabPFN-3.5 Telemetry & Sloth Metrics
          </h3>
        </div>
        <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-white/[0.05] text-[#A5A39D] border border-white/[0.08]">
          In-Context Bayesian Inference
        </span>
      </div>

      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5 mb-5">
        {/* Sloth Score */}
        <div className="bg-[#202020] rounded-2xl p-4 border border-white/[0.06] flex flex-col justify-between">
          <span className="text-xs text-[#A5A39D] block mb-1">Sloth Score</span>
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-display font-extrabold text-[#F4D779]">
              {slothScore}
            </span>
            <span className="text-xs text-[#A5A39D] font-mono">/100</span>
          </div>
          <span className="text-[10px] text-[#A5A39D]/80 mt-2 block font-medium">
            Based on active time & dish load
          </span>
        </div>

        {/* Flavor Harmony */}
        <div className="bg-[#202020] rounded-2xl p-4 border border-white/[0.06] flex flex-col justify-between">
          <span className="text-xs text-[#A5A39D] block mb-1">Flavor Harmony</span>
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-display font-extrabold text-[#F5F2EB]">
              {harmony}%
            </span>
            <span className="text-[11px] text-[#A5A39D] font-mono">
              ({Math.round(prediction.confidence * 100)}% conf)
            </span>
          </div>
          <div className="w-full bg-[#292929] rounded-full h-1.5 mt-2.5 overflow-hidden">
            <div
              className="bg-[#F4D779] h-1.5 rounded-full transition-all duration-700"
              style={{ width: `${Math.min(100, harmony)}%` }}
            />
          </div>
        </div>

        {/* Cookware & Utensil */}
        <div className="bg-[#202020] rounded-2xl p-4 border border-white/[0.06] flex flex-col justify-between">
          <span className="text-xs text-[#A5A39D] block mb-1">Cookware Bound</span>
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-display font-extrabold text-emerald-400">
              1 Pan
            </span>
            <span className="text-[11px] text-[#A5A39D] line-through">vs 4 avg</span>
          </div>
          <span className="text-[10px] text-emerald-400/80 mt-2 flex items-center gap-1 font-medium">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>Strict zero-prep bowls</span>
          </span>
        </div>

        {/* Active Standing Time */}
        <div className="bg-[#202020] rounded-2xl p-4 border border-white/[0.06] flex flex-col justify-between">
          <span className="text-xs text-[#A5A39D] block mb-1">Active Standing Time</span>
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-display font-extrabold text-[#F5F2EB]">
              {prediction.active_standing_minutes}m
            </span>
            <span className="text-[11px] text-[#A5A39D] font-mono">
              (total: {prediction.total_minutes}m)
            </span>
          </div>
          <span className="text-[10px] text-[#A5A39D]/80 mt-2 block font-medium">
            {prediction.effort_class}
          </span>
        </div>
      </div>

      {/* Flavor Radar & Synergies */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-white/[0.06] text-xs">
        <div>
          <span className="text-[#A5A39D] font-medium block mb-2">Flavor Chemistry Breakdown:</span>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(prediction.flavor_balance).map(([key, val]) => (
              <div key={key} className="flex items-center justify-between bg-[#202020] px-3 py-2 rounded-xl border border-white/[0.05]">
                <span className="text-[#A5A39D]">{key}</span>
                <span className="font-mono font-bold text-[#F4D779]">{val} / 10</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <span className="text-[#A5A39D] font-medium block mb-2">Prior Labs TabPFN Synergies:</span>
          <div className="space-y-2">
            {prediction.pairing_synergies.length > 0 ? (
              prediction.pairing_synergies.map((syn, idx) => (
                <div key={idx} className="flex items-start gap-2 text-[#A5A39D] bg-[#202020] p-2.5 rounded-xl border border-white/[0.05]">
                  <Sparkles className="w-3.5 h-3.5 text-[#F4D779] shrink-0 mt-0.5" />
                  <span className="text-[11px] leading-relaxed text-[#F5F2EB]/90">{syn}</span>
                </div>
              ))
            ) : (
              <p className="text-[#A5A39D]/60 italic text-[11px]">Optimal biochemical equilibrium reached.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
