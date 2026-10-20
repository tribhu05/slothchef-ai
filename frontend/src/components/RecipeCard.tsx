import React, { useState, useEffect } from 'react';
import { SlothRecipe } from '../types';
import { Clock, Utensils, CheckCircle, Copy, Share2, Timer, AlertCircle, Shield, Award } from 'lucide-react';

interface RecipeCardProps {
  recipe: SlothRecipe;
}

export const RecipeCard: React.FC<RecipeCardProps> = ({ recipe }) => {
  const [copied, setCopied] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(recipe.total_minutes * 60);
  const [timerActive, setTimerActive] = useState(false);

  useEffect(() => {
    setTimerSeconds(recipe.total_minutes * 60);
    setTimerActive(false);
  }, [recipe]);

  useEffect(() => {
    let interval: any = null;
    if (timerActive && timerSeconds > 0) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => prev - 1);
      }, 1000);
    } else if (timerSeconds === 0) {
      setTimerActive(false);
    }
    return () => clearInterval(interval);
  }, [timerActive, timerSeconds]);

  const handleCopy = () => {
    const text = `🍳 ${recipe.title} (${recipe.sloth_efficiency})\n\n` +
      `Vessel: ${recipe.vessel_type} | Utensil: ${recipe.utensil}\n` +
      `Active Time: ${recipe.active_standing_minutes}m | Total: ${recipe.total_minutes}m\n\n` +
      `SLOTH SHORTCUTS:\n${recipe.sloth_shortcuts.map(s => `- ${s}`).join('\n')}\n\n` +
      `STEPS:\n${recipe.steps.map((st, i) => `${i + 1}. ${st}`).join('\n')}\n\n` +
      `CLEANUP AUDIT:\n${recipe.cleanup_audit}`;
    
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatTimer = (sec: number) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="bg-white rounded-3xl p-6 md:p-8 border-2 border-amber-300 shadow-md mb-8">
      {/* Header Badge & Action */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-amber-500 text-white shadow-xs">
            {recipe.sloth_efficiency}
          </span>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
            {recipe.vessel_type}
          </span>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-stone-100 text-stone-700 border border-stone-200">
            {recipe.utensil}
          </span>
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 text-xs font-bold transition-all cursor-pointer"
        >
          {copied ? (
            <>
              <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
              <span>Copied Recipe!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5 text-amber-700" />
              <span>Copy to Clipboard</span>
            </>
          )}
        </button>
      </div>

      {/* Title & Tagline */}
      <h2 className="font-display font-extrabold text-2xl md:text-3xl text-stone-900 mb-1">
        {recipe.title}
      </h2>
      <p className="text-sm font-semibold text-amber-700 mb-3">
        {recipe.subtitle}
      </p>
      <div className="p-3.5 bg-amber-50/80 rounded-2xl border border-amber-200/80 text-xs italic text-stone-700 mb-6 flex items-start gap-2">
        <span className="text-base">🦥</span>
        <span className="leading-relaxed font-medium">"{recipe.tagline}"</span>
      </div>

      {/* Sloth Shortcuts Section */}
      <div className="mb-6">
        <h3 className="font-display font-bold text-sm uppercase tracking-wider text-amber-950 mb-2 flex items-center gap-2">
          <Award className="w-4 h-4 text-amber-600" />
          <span>Radical Sloth Shortcuts (No Pretentious Chef BS):</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          {recipe.sloth_shortcuts.map((sc, i) => (
            <div
              key={i}
              className="p-3 rounded-2xl bg-amber-50/50 border border-amber-200/60 text-xs text-stone-800 flex items-start gap-2"
            >
              <span className="w-5 h-5 rounded-full bg-amber-200 text-amber-900 font-bold flex items-center justify-center shrink-0 text-[10px]">
                {i + 1}
              </span>
              <span className="leading-relaxed font-medium">{sc}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recipe Steps */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-display font-bold text-sm uppercase tracking-wider text-amber-950 flex items-center gap-2">
            <Utensils className="w-4 h-4 text-amber-600" />
            <span>Execution Steps (Strictly Sequential):</span>
          </h3>

          {/* Interactive Cooking Timer */}
          <div className="flex items-center gap-2 bg-stone-100 px-3 py-1 rounded-xl border border-stone-200 text-xs">
            <Timer className="w-3.5 h-3.5 text-stone-600" />
            <span className="font-mono font-bold text-stone-800">{formatTimer(timerSeconds)}</span>
            <button
              onClick={() => setTimerActive(!timerActive)}
              className="font-bold text-[11px] text-amber-700 hover:text-amber-900 cursor-pointer underline"
            >
              {timerActive ? 'Pause' : timerSeconds === 0 ? 'Reset' : 'Start Timer'}
            </button>
          </div>
        </div>

        <ol className="space-y-3">
          {recipe.steps.map((step, idx) => (
            <li
              key={idx}
              className="p-4 rounded-2xl bg-stone-50 border border-stone-200/70 text-sm text-stone-800 flex items-start gap-3"
            >
              <span className="w-6 h-6 rounded-xl bg-amber-600 text-white font-bold flex items-center justify-center shrink-0 text-xs font-display">
                {idx + 1}
              </span>
              <span className="leading-relaxed font-medium pt-0.5">{step}</span>
            </li>
          ))}
        </ol>
      </div>

      {/* Dish Cleanup Audit */}
      <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-950 mb-6 flex items-start gap-3">
        <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-xs uppercase tracking-wide block text-emerald-800">
            Cleanup Audit:
          </span>
          <p className="text-xs font-medium leading-relaxed mt-0.5">
            {recipe.cleanup_audit}
          </p>
        </div>
      </div>

      {/* Why Open Innovation Matters */}
      <div className="p-4 rounded-2xl bg-stone-50 border border-stone-200 text-stone-700">
        <div className="flex items-center gap-2 mb-1.5">
          <Shield className="w-4 h-4 text-purple-600" />
          <h4 className="font-bold text-xs uppercase tracking-wide text-stone-900">
            Why Open-Source AI Matters Here:
          </h4>
        </div>
        <p className="text-xs leading-relaxed text-stone-600">
          {recipe.open_weights_rationale}
        </p>
      </div>
    </div>
  );
};
