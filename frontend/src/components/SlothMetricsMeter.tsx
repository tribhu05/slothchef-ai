import React from 'react';
import { TabPFNPrediction } from '../types';
import { Gauge, Sparkles, UtensilsCrossed, ShieldAlert, CheckCircle2, Zap } from 'lucide-react';

interface SlothMetricsMeterProps {
  prediction: TabPFNPrediction;
}

export const SlothMetricsMeter: React.FC<SlothMetricsMeterProps> = ({ prediction }) => {
  const harmony = prediction.harmony_score;
  const isHighHarmony = harmony >= 85;

  return (
    <div className="bg-gradient-to-br from-amber-900 to-stone-900 text-amber-50 rounded-3xl p-5 shadow-lg border border-amber-800/40 mb-6">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-amber-700/40 pb-3 mb-4">
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <h3 className="font-display font-bold text-sm tracking-wide text-amber-200 uppercase">
            Prior Labs TabPFN-3.5 Telemetry
          </h3>
        </div>
        <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/20">
          In-Context Tabular Prior Foundation Model
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
        {/* Harmony Score */}
        <div className="bg-white/5 rounded-2xl p-4 border border-white/5 flex flex-col justify-between">
          <span className="text-xs text-amber-200/70 block mb-1">Flavor Pairing Harmony</span>
          <div className="flex items-baseline gap-2">
            <span className={`text-4xl font-display font-extrabold ${isHighHarmony ? 'text-amber-400' : 'text-stone-300'}`}>
              {harmony}%
            </span>
            <span className="text-xs text-amber-300/70 font-mono">
              (conf: {Math.round(prediction.confidence * 100)}%)
            </span>
          </div>
          <div className="w-full bg-white/10 rounded-full h-2 mt-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-amber-500 to-emerald-400 h-2 rounded-full transition-all duration-700"
              style={{ width: `${Math.min(100, harmony)}%` }}
            />
          </div>
        </div>

        {/* Dishes To Wash */}
        <div className="bg-white/5 rounded-2xl p-4 border border-white/5 flex flex-col justify-between">
          <span className="text-xs text-amber-200/70 block mb-1">Vessel Dish Overhead</span>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-display font-extrabold text-emerald-400">
              1 Pan
            </span>
            <span className="text-xs text-stone-400 line-through">vs 5 typical</span>
          </div>
          <p className="text-[11px] text-emerald-300/80 mt-2 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>Strict zero-prep-bowl constraint enforced</span>
          </p>
        </div>

        {/* Active Standing Time */}
        <div className="bg-white/5 rounded-2xl p-4 border border-white/5 flex flex-col justify-between">
          <span className="text-xs text-amber-200/70 block mb-1">Active Standing Time</span>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-display font-extrabold text-amber-300">
              {prediction.active_standing_minutes}m
            </span>
            <span className="text-xs text-amber-200/60 font-mono">
              (total: {prediction.total_minutes}m)
            </span>
          </div>
          <span className="text-[11px] px-2 py-0.5 rounded-lg bg-amber-400/20 text-amber-200 self-start mt-2 font-medium">
            {prediction.effort_class}
          </span>
        </div>
      </div>

      {/* Flavor Radar Breakdown & Synergies */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-white/10 text-xs">
        <div>
          <span className="text-amber-300 font-semibold block mb-2">Flavor Balance Breakdown:</span>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(prediction.flavor_balance).map(([key, val]) => (
              <div key={key} className="flex items-center justify-between bg-black/20 px-2.5 py-1.5 rounded-xl border border-white/5">
                <span className="text-stone-300">{key}:</span>
                <span className="font-mono font-bold text-amber-400">{val} / 10</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <span className="text-amber-300 font-semibold block mb-2">TabPFN Detected Synergies:</span>
          <div className="space-y-1.5">
            {prediction.pairing_synergies.length > 0 ? (
              prediction.pairing_synergies.map((syn, idx) => (
                <div key={idx} className="flex items-start gap-1.5 text-stone-300 bg-white/5 p-2 rounded-xl border border-white/5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                  <span className="text-[11px] leading-relaxed">{syn}</span>
                </div>
              ))
            ) : (
              <p className="text-stone-400 italic text-[11px]">No severe ingredient clashes detected.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
