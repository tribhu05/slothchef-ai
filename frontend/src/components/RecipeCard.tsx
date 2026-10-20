import React, { useState, useEffect } from 'react';
import { SlothRecipe } from '../types';
import { Clock, Utensils, CheckCircle, Copy, Timer, Shield, Sparkles, RefreshCw, ChefHat, Award } from 'lucide-react';

interface RecipeCardProps {
  recipe: SlothRecipe;
  onRegenerate: () => void;
  isLoading: boolean;
}

export const RecipeCard: React.FC<RecipeCardProps> = ({ recipe, onRegenerate, isLoading }) => {
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
      `Active Time: ${recipe.active_standing_minutes}m | Total Time: ${recipe.total_minutes}m\n\n` +
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

  const heroImage = recipe.image_url || "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80";

  return (
    <div className="bg-[#181818] rounded-3xl overflow-hidden border border-white/[0.08] shadow-2xl mb-8">
      {/* Cinematic Hero Food Photography Header */}
      <div className="relative h-64 sm:h-80 w-full overflow-hidden bg-[#202020]">
        <img
          src={heroImage}
          alt={recipe.title}
          className="w-full h-full object-cover filter brightness-[0.88]"
          onError={(e) => {
            e.currentTarget.src = "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80";
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#181818] via-[#181818]/60 to-transparent" />

        {/* Floating Badges */}
        <div className="absolute top-4 left-4 right-4 flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-[#181818]/85 backdrop-blur-md border border-[#F4D779]/40 text-[#F4D779] shadow-sm">
              {recipe.sloth_score ? `Sloth Score: ${recipe.sloth_score}/100` : recipe.sloth_efficiency}
            </span>
            <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-[#181818]/85 backdrop-blur-md border border-white/[0.1] text-[#F5F2EB]">
              {recipe.vessel_type}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#181818]/85 backdrop-blur-md hover:bg-[#202020] text-[#F5F2EB] border border-white/[0.1] text-xs font-medium transition-all cursor-pointer shadow-xs"
              title="Copy recipe text"
            >
              {copied ? (
                <>
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-[#F4D779]" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Title over Hero Gradient */}
        <div className="absolute bottom-4 left-6 right-6">
          <h2 className="font-display font-extrabold text-2xl sm:text-4xl text-[#F5F2EB] tracking-tight mb-1">
            {recipe.title}
          </h2>
          <p className="text-xs sm:text-sm font-medium text-[#F4D779]">
            {recipe.subtitle}
          </p>
        </div>
      </div>

      {/* Main Content Body */}
      <div className="p-6 sm:p-8">
        {/* Witty Quote Tagline */}
        <div className="p-4 bg-[#202020] rounded-2xl border border-white/[0.06] text-xs text-[#A5A39D] mb-6 flex items-start gap-3">
          <span className="text-xl">🦥</span>
          <p className="leading-relaxed italic text-[#F5F2EB]/90">
            "{recipe.tagline}"
          </p>
        </div>

        {/* Quick Stats Bar & Timer */}
        <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-2xl bg-[#202020] border border-white/[0.06] mb-6 text-xs text-[#A5A39D]">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-[#F4D779]" />
              <strong className="text-[#F5F2EB]">{recipe.active_standing_minutes}m</strong> standing
            </span>
            <span className="flex items-center gap-1.5">
              <Utensils className="w-3.5 h-3.5 text-emerald-400" />
              <strong className="text-[#F5F2EB]">1</strong> utensil ({recipe.utensil})
            </span>
          </div>

          {/* Interactive Cooking Timer */}
          <div className="flex items-center gap-2 bg-[#292929] px-3 py-1.5 rounded-xl border border-white/[0.07]">
            <Timer className="w-3.5 h-3.5 text-[#F4D779]" />
            <span className="font-mono font-bold text-[#F5F2EB]">{formatTimer(timerSeconds)}</span>
            <button
              onClick={() => setTimerActive(!timerActive)}
              className="text-[#F4D779] hover:text-[#E8CA6B] font-semibold text-[11px] underline cursor-pointer ml-1"
            >
              {timerActive ? 'Pause' : timerSeconds === 0 ? 'Reset' : 'Start Timer'}
            </button>
          </div>
        </div>

        {/* Sloth Shortcuts Section */}
        <div className="mb-6">
          <h3 className="font-display font-semibold text-xs uppercase tracking-wider text-[#A5A39D] mb-3 flex items-center gap-2">
            <Award className="w-4 h-4 text-[#F4D779]" />
            <span>Radical Sloth Shortcuts</span>
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {recipe.sloth_shortcuts.map((sc, i) => (
              <div
                key={i}
                className="p-3.5 rounded-2xl bg-[#202020] border border-white/[0.06] text-xs text-[#F5F2EB] flex items-start gap-3"
              >
                <span className="w-5 h-5 rounded-full bg-[#F4D779]/15 text-[#F4D779] border border-[#F4D779]/30 font-bold flex items-center justify-center shrink-0 text-[10px]">
                  {i + 1}
                </span>
                <span className="leading-relaxed">{sc}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Sequential Steps Timeline */}
        <div className="mb-6">
          <h3 className="font-display font-semibold text-xs uppercase tracking-wider text-[#A5A39D] mb-3 flex items-center gap-2">
            <Utensils className="w-4 h-4 text-[#F4D779]" />
            <span>Step-by-Step Execution</span>
          </h3>
          <ol className="space-y-3">
            {recipe.steps.map((step, idx) => (
              <li
                key={idx}
                className="p-4 rounded-2xl bg-[#202020] border border-white/[0.06] text-xs text-[#F5F2EB] flex items-start gap-3.5 hover:border-white/[0.1] transition-colors"
              >
                <span className="w-6 h-6 rounded-xl bg-[#292929] border border-white/[0.08] text-[#F4D779] font-bold flex items-center justify-center shrink-0 text-xs font-mono">
                  {idx + 1}
                </span>
                <span className="leading-relaxed pt-0.5">{step}</span>
              </li>
            ))}
          </ol>
        </div>

        {/* Cleanup Audit */}
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 mb-6 flex items-start gap-3 text-xs">
          <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold uppercase tracking-wider text-emerald-300 block mb-0.5">
              Cleanup Audit:
            </span>
            <p className="leading-relaxed text-emerald-200/90">
              {recipe.cleanup_audit}
            </p>
          </div>
        </div>

        {/* Footer Actions & Open-Source Defense */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-white/[0.07]">
          <div className="flex items-center gap-2 text-[11px] text-[#A5A39D]">
            <Shield className="w-3.5 h-3.5 text-[#F4D779]" />
            <span>On-device processing protects your private pantry habits</span>
          </div>

          <button
            onClick={onRegenerate}
            disabled={isLoading}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#202020] hover:bg-[#292929] text-[#F5F2EB] border border-white/[0.08] text-xs font-semibold transition-all cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-[#F4D779] ${isLoading ? 'animate-spin' : ''}`} />
            <span>Regenerate Recipe</span>
          </button>
        </div>
      </div>
    </div>
  );
};
