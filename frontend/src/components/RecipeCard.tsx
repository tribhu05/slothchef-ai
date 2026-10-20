import React, { useState, useEffect } from 'react';
import { SlothRecipe, TabPFNPrediction } from '../types';
import { 
  Clock, 
  Utensils, 
  CheckCircle, 
  Copy, 
  Timer, 
  Shield, 
  Sparkles, 
  RefreshCw, 
  Award, 
  ChevronDown, 
  ChevronUp, 
  Zap, 
  ChefHat, 
  ArrowRight, 
  ArrowLeft,
  CheckCircle2,
  Check,
  BellRing,
  Printer,
  Volume2,
  VolumeX,
  AlertTriangle,
  Info,
  Plus
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { playTimerDoneChime, playStepCheckSound, speakStep, stopSpeaking } from '../utils/audio';

interface RecipeCardProps {
  recipe: SlothRecipe;
  onRegenerate: () => void;
  isLoading: boolean;
  onOpenExplainer?: () => void;
  onAddMissingAndCook?: (ingredientName: string) => void;
}

export const RecipeCard: React.FC<RecipeCardProps> = ({ 
  recipe, 
  onRegenerate, 
  isLoading,
  onOpenExplainer,
  onAddMissingAndCook
}) => {
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<'overview' | 'cook_along'>('overview');
  
  // Interactive Step Checklist
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [currentCookStep, setCurrentCookStep] = useState(0);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Interactive Timer
  const [timerSeconds, setTimerSeconds] = useState(recipe.active_standing_minutes * 60 || 180);
  const [timerActive, setTimerActive] = useState(false);
  const [timerFinished, setTimerFinished] = useState(false);

  // Collapsible TabPFN Telemetry Drawer
  const [isTelemetryExpanded, setIsTelemetryExpanded] = useState(false);

  // Reset states on new recipe
  useEffect(() => {
    setCompletedSteps([]);
    setCurrentCookStep(0);
    setTimerSeconds(recipe.active_standing_minutes * 60 || 180);
    setTimerActive(false);
    setTimerFinished(false);
  }, [recipe.id]);

  // Timer countdown with Web Audio Chime on 0:00
  useEffect(() => {
    let interval: any = null;
    if (timerActive && timerSeconds > 0) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => {
          if (prev <= 1) {
            setTimerActive(false);
            setTimerFinished(true);
            playTimerDoneChime();
            confetti({
              particleCount: 75,
              spread: 60,
              origin: { y: 0.6 },
              colors: ['#F4D779', '#10b981', '#ffffff']
            });
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [timerActive, timerSeconds]);

  const toggleStep = (index: number) => {
    playStepCheckSound();
    if (completedSteps.includes(index)) {
      setCompletedSteps(completedSteps.filter((i) => i !== index));
    } else {
      const nextCompleted = [...completedSteps, index];
      setCompletedSteps(nextCompleted);
      
      // If all steps completed, celebrate!
      if (nextCompleted.length === recipe.steps.length) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.7 },
          colors: ['#F4D779', '#10b981', '#ffffff']
        });
      }
    }
  };

  const handleCopy = () => {
    const text = `🍳 ${recipe.title} (${recipe.sloth_efficiency})\n\n` +
      `Vessel: ${recipe.vessel_type} | Utensil: ${recipe.utensil}\n` +
      `Active Standing Time: ${recipe.active_standing_minutes}m | Total Time: ${recipe.total_minutes}m\n\n` +
      `RADICAL SLOTH SHORTCUTS:\n${recipe.sloth_shortcuts.map(s => `- ${s}`).join('\n')}\n\n` +
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

  const heroImage = recipe.image_url || "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80";
  const progressPercent = Math.round((completedSteps.length / recipe.steps.length) * 100);
  const tabpfn = recipe.tabpfn_evidence;

  return (
    <div className="bg-[#181818] rounded-3xl overflow-hidden border border-white/[0.08] shadow-2xl mb-8 flex flex-col">
      {/* Top Interactive Mode Navigation & Action Bar */}
      <div className="p-3 sm:p-4 bg-[#202020] border-b border-white/[0.06] flex flex-wrap items-center justify-between gap-3">
        {/* View Switcher: Overview vs Cook-Along Mode */}
        <div className="flex items-center gap-1.5 p-1 bg-[#181818] rounded-2xl border border-white/[0.08]">
          <button
            type="button"
            onClick={() => setViewMode('overview')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer ${
              viewMode === 'overview'
                ? 'bg-[#F4D779] text-[#181818] shadow-sm font-bold'
                : 'text-[#A5A39D] hover:text-[#F5F2EB]'
            }`}
          >
            <span>📖 Recipe Overview</span>
          </button>
          <button
            type="button"
            onClick={() => setViewMode('cook_along')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer ${
              viewMode === 'cook_along'
                ? 'bg-[#F4D779] text-[#181818] shadow-sm font-bold'
                : 'text-[#A5A39D] hover:text-[#F5F2EB]'
            }`}
          >
            <ChefHat className="w-3.5 h-3.5" />
            <span>👨‍🍳 Cook-Along Mode</span>
          </button>
        </div>

        {/* Quick Actions (Timer with Presets & Copy) */}
        <div className="flex items-center gap-2">
          {/* Active Timer Pill with 1m, 3m, 5m presets */}
          <div className="flex items-center gap-1.5 bg-[#181818] p-1.5 rounded-xl border border-white/[0.08] text-xs">
            <Timer className="w-3.5 h-3.5 text-[#F4D779] ml-1" />
            <span className="font-mono font-bold text-[#F5F2EB] mr-1">
              {formatTimer(timerSeconds)}
            </span>
            <div className="hidden sm:flex items-center gap-1 border-l border-white/[0.08] pl-1.5">
              {[1, 3, 5].map((m) => (
                <button
                  key={m}
                  onClick={() => {
                    setTimerSeconds(m * 60);
                    setTimerActive(false);
                    setTimerFinished(false);
                  }}
                  className="px-1.5 py-0.5 rounded text-[10px] bg-[#242424] hover:bg-[#292929] text-[#A5A39D] hover:text-[#F4D779] font-mono cursor-pointer"
                  title={`Set timer to ${m} min`}
                >
                  {m}m
                </button>
              ))}
            </div>
            <button
              onClick={() => {
                if (timerSeconds === 0) {
                  setTimerSeconds(recipe.active_standing_minutes * 60 || 180);
                  setTimerFinished(false);
                } else {
                  setTimerActive(!timerActive);
                }
              }}
              className="text-[#F4D779] hover:text-[#E8CA6B] font-semibold text-[11px] underline cursor-pointer ml-1 pr-1"
            >
              {timerActive ? 'Pause' : timerSeconds === 0 ? 'Reset' : 'Start'}
            </button>
          </div>

          {/* Copy Button */}
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#181818] hover:bg-[#292929] text-[#F5F2EB] border border-white/[0.08] text-xs font-medium transition-all cursor-pointer"
            title="Copy Recipe"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-[#F4D779]" />
                <span>Copy</span>
              </>
            )}
          </button>

          {/* Print Recipe Button */}
          <button
            onClick={() => window.print()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#181818] hover:bg-[#292929] text-[#F5F2EB] border border-white/[0.08] text-xs font-medium transition-all cursor-pointer no-print"
            title="Print or Save as PDF"
          >
            <Printer className="w-3.5 h-3.5 text-[#F4D779]" />
            <span className="hidden sm:inline">Print</span>
          </button>
        </div>
      </div>

      {/* Timer Finished Alert Banner with Web Audio Ding */}
      {timerFinished && (
        <div className="bg-[#F4D779] text-[#181818] px-4 py-2.5 flex items-center justify-between text-xs font-bold animate-in slide-in-from-top duration-300">
          <div className="flex items-center gap-2">
            <BellRing className="w-4 h-4 animate-bounce" />
            <span>⏰ Ding! 1-Pan Survival Meal Ready! No pans were harmed in this cook.</span>
          </div>
          <button
            onClick={() => {
              setTimerFinished(false);
              setTimerSeconds(recipe.active_standing_minutes * 60 || 180);
            }}
            className="px-2.5 py-1 rounded-lg bg-[#181818] text-[#F4D779] text-[11px] font-extrabold hover:bg-black transition-colors cursor-pointer"
          >
            Reset Timer
          </button>
        </div>
      )}

      {/* VIEW 1: RECIPE OVERVIEW */}
      {viewMode === 'overview' && (
        <div>
          {/* Cinematic Hero Food Photography */}
          <div className="relative h-64 sm:h-72 w-full overflow-hidden bg-[#202020]">
            <img
              src={heroImage}
              alt={recipe.title}
              className="w-full h-full object-cover filter brightness-[0.88]"
              onError={(e) => {
                e.currentTarget.src = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80";
              }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#181818] via-[#181818]/60 to-transparent" />

            {/* Floating Top Badges */}
            <div className="absolute top-4 left-4 right-4 flex items-center justify-between gap-2 flex-wrap">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold px-3 py-1 rounded-full bg-[#181818]/90 backdrop-blur-md border border-[#F4D779]/40 text-[#F4D779] shadow-md">
                  Sloth Score: {recipe.sloth_score || 96}/100
                </span>
                <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-[#181818]/90 backdrop-blur-md border border-white/[0.1] text-[#F5F2EB]">
                  {recipe.vessel_type}
                </span>
              </div>

              <div className="flex items-center gap-2">
                {recipe.image_caption && (
                  <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-medium px-2.5 py-1 rounded-full bg-[#181818]/90 backdrop-blur-md border border-white/[0.1] text-[#F5F2EB]/90">
                    <span>📷</span>
                    <span>{recipe.image_caption}</span>
                  </span>
                )}
                <span className="text-xs font-mono font-medium px-2.5 py-1 rounded-full bg-emerald-500/20 backdrop-blur-md border border-emerald-500/30 text-emerald-300">
                  🍳 1 Pan • 🍴 1 Utensil • 🔪 0 Knives
                </span>
              </div>
            </div>

            {/* Title & Tagline overlay */}
            <div className="absolute bottom-4 left-6 right-6">
              <h1 className="font-display font-extrabold text-2xl sm:text-4xl text-[#F5F2EB] tracking-tight mb-1">
                {recipe.title}
              </h1>
              <p className="text-xs sm:text-sm font-medium text-[#F4D779]">
                {recipe.subtitle}
              </p>
            </div>
          </div>

          <div className="p-6 sm:p-8 space-y-6">
            {/* Witty Quote Tagline */}
            <div className="p-4 bg-[#202020] rounded-2xl border border-white/[0.06] text-xs text-[#A5A39D] flex items-start gap-3">
              <span className="text-2xl">🦥</span>
              <p className="leading-relaxed italic text-[#F5F2EB]/95 pt-0.5">
                "{recipe.tagline}"
              </p>
            </div>

            {/* Food Safety & Cooking Feasibility Notice */}
            {recipe.safety_warnings && recipe.safety_warnings.length > 0 && (
              <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/25 text-amber-300 text-xs flex items-start gap-3 animate-in fade-in">
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <span className="font-bold uppercase tracking-wider text-amber-300 block mb-0.5">
                    Cooking Feasibility & Food Safety Advisory:
                  </span>
                  {recipe.safety_warnings.map((warn, wIdx) => (
                    <p key={wIdx} className="leading-relaxed text-amber-200/90">{warn}</p>
                  ))}
                </div>
              </div>
            )}

            {/* State: NEEDS_INGREDIENTS Spotlight Card */}
            {recipe.status === "NEEDS_INGREDIENTS" && recipe.missing_suggestions && recipe.missing_suggestions.length > 0 && (
              <div className="p-5 sm:p-6 rounded-3xl bg-[#202020] border-2 border-[#F4D779]/40 shadow-xl space-y-4 animate-in fade-in slide-in-from-top-2 duration-300">
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#F4D779] uppercase tracking-wider">
                    <Sparkles className="w-4 h-4 text-[#F4D779]" />
                    <span>You're {recipe.missing_suggestions.length} ingredient away from a proper meal!</span>
                  </div>
                  <span className="text-[11px] font-mono text-[#A5A39D] bg-[#181818] px-2.5 py-1 rounded-full border border-white/[0.06]">
                    Target: {recipe.title}
                  </span>
                </div>

                <p className="text-xs text-[#F5F2EB] leading-relaxed">
                  {recipe.decision_message || "Your pantry has the foundation, but adding one key item unlocks a cohesive, takeout-grade dish."}
                </p>

                <div className="space-y-3 pt-1">
                  {recipe.missing_suggestions.map((sug, sIdx) => (
                    <div key={sIdx} className="p-4 rounded-2xl bg-[#181818] border border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="space-y-1 max-w-lg">
                        <div className="flex items-center gap-2">
                          <span className="font-display font-bold text-sm text-[#F4D779]">
                            + {sug.ingredient_name}
                          </span>
                          <span className="text-[10px] uppercase font-semibold text-[#A5A39D] bg-[#242424] px-2 py-0.5 rounded-full">
                            Missing Anchor
                          </span>
                        </div>
                        <p className="text-xs text-[#A5A39D] leading-relaxed">
                          {sug.reason}
                        </p>
                        {sug.substitutes && sug.substitutes.length > 0 && (
                          <p className="text-[11px] text-[#A5A39D]/80">
                            <span className="text-[#F5F2EB]/80 font-medium">Substitutes: </span>
                            {sug.substitutes.join(", ")}
                          </p>
                        )}
                      </div>

                      <button
                        onClick={() => onAddMissingAndCook?.(sug.ingredient_name)}
                        className="px-4 py-2.5 rounded-xl bg-[#F4D779] hover:bg-[#E8CA6B] text-[#181818] font-bold text-xs flex items-center justify-center gap-2 shadow-md cursor-pointer transition-all shrink-0 hover:scale-[1.02] active:scale-[0.98]"
                      >
                        <Plus className="w-3.5 h-3.5 stroke-[3]" />
                        <span>Add to Pan & Cook</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* State: NO_GOOD_MATCH Card */}
            {recipe.status === "NO_GOOD_MATCH" && (
              <div className="p-5 sm:p-6 rounded-3xl bg-[#202020] border-2 border-amber-500/30 shadow-xl space-y-4">
                <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
                  <Info className="w-4 h-4 text-amber-400" />
                  <span>Culinary Reality Check</span>
                </div>
                <h3 className="font-display font-bold text-sm sm:text-base text-[#F5F2EB]">
                  {recipe.decision_message}
                </h3>
                {recipe.fit_explanation && (
                  <p className="text-xs text-[#A5A39D] leading-relaxed">
                    {recipe.fit_explanation}
                  </p>
                )}

                {recipe.missing_suggestions && recipe.missing_suggestions.length > 0 && (
                  <div className="pt-2">
                    <span className="text-xs font-semibold text-[#F4D779] block mb-2">
                      Suggested pantry staples to anchor this meal:
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                      {recipe.missing_suggestions.map((sug, idx) => (
                        <div key={idx} className="p-3 rounded-2xl bg-[#181818] border border-white/[0.06] flex items-center justify-between gap-2">
                          <div>
                            <span className="font-bold text-xs text-[#F5F2EB] block">
                              {sug.ingredient_name}
                            </span>
                            <span className="text-[10px] text-[#A5A39D]">
                              Unlocks: {sug.unlocks_recipe_title}
                            </span>
                          </div>
                          <button
                            onClick={() => onAddMissingAndCook?.(sug.ingredient_name)}
                            className="px-3 py-1.5 rounded-lg bg-[#F4D779] hover:bg-[#E8CA6B] text-[#181818] font-bold text-[11px] flex items-center gap-1 cursor-pointer transition-all"
                          >
                            <Plus className="w-3 h-3" />
                            <span>Add & Cook</span>
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Culinary Synergy Note (for READY dishes) */}
            {recipe.status === "READY" && recipe.fit_explanation && (
              <div className="p-4 bg-[#202020] rounded-2xl border border-white/[0.06] text-xs text-[#A5A39D] flex items-start gap-3">
                <ChefHat className="w-4 h-4 text-[#F4D779] shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-[#F4D779] block mb-0.5">
                    Culinary Pairing Physics:
                  </span>
                  <p className="leading-relaxed text-[#F5F2EB]/90">
                    {recipe.fit_explanation}
                  </p>
                </div>
              </div>
            )}

            {/* Integrated Collapsible TabPFN Telemetry Bar */}
            <div className="bg-[#202020] rounded-2xl border border-white/[0.07] overflow-hidden">
              <div 
                onClick={() => setIsTelemetryExpanded(!isTelemetryExpanded)}
                className="p-4 flex items-center justify-between cursor-pointer hover:bg-white/[0.02] transition-colors select-none"
              >
                <div className="flex items-center gap-2.5">
                  <Zap className="w-4 h-4 text-[#F4D779]" />
                  <span className="font-display font-bold text-xs uppercase tracking-wider text-[#F5F2EB]">
                    TabPFN-3.5 Flavor Harmony & Prior Fitting
                  </span>
                  <span className="text-[11px] font-mono font-bold text-[#F4D779] bg-[#F4D779]/10 px-2 py-0.5 rounded-full border border-[#F4D779]/20">
                    {tabpfn.harmony_score}% Match
                  </span>
                </div>

                <div className="flex items-center gap-2 text-xs text-[#A5A39D]">
                  <span className="hidden sm:inline">
                    {isTelemetryExpanded ? 'Collapse Chemistry' : 'Expand Flavor Radar'}
                  </span>
                  {isTelemetryExpanded ? (
                    <ChevronUp className="w-4 h-4 text-[#F4D779]" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-[#F4D779]" />
                  )}
                </div>
              </div>

              {/* Collapsed Metric Pills */}
              <div className="px-4 pb-3 grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 border-t border-white/[0.04]">
                <div className="text-center p-2 rounded-xl bg-[#292929]">
                  <span className="text-[10px] text-[#A5A39D] block">Sloth Score</span>
                  <span className="font-display font-extrabold text-sm text-[#F4D779]">
                    {recipe.sloth_score || 96}/100
                  </span>
                </div>
                <div className="text-center p-2 rounded-xl bg-[#292929]">
                  <span className="text-[10px] text-[#A5A39D] block">Active Standing</span>
                  <span className="font-display font-extrabold text-sm text-[#F5F2EB]">
                    {recipe.active_standing_minutes} mins
                  </span>
                </div>
                <div className="text-center p-2 rounded-xl bg-[#292929]">
                  <span className="text-[10px] text-[#A5A39D] block">Dish Wash Cap</span>
                  <span className="font-display font-extrabold text-sm text-emerald-400">
                    1 Pan Only
                  </span>
                </div>
                <div className="text-center p-2 rounded-xl bg-[#292929]">
                  <span className="text-[10px] text-[#A5A39D] block">Prior Alignment</span>
                  <span className="font-display font-extrabold text-sm text-[#F5F2EB]">
                    {Math.round(tabpfn.confidence * 100)}%
                  </span>
                </div>
              </div>

              {/* Expanded Flavor Radar Details */}
              {isTelemetryExpanded && (
                <div className="p-4 border-t border-white/[0.06] bg-[#1a1a1a] space-y-4 animate-in fade-in duration-200">
                  <div>
                    <span className="text-[11px] font-semibold text-[#A5A39D] uppercase tracking-wider block mb-2">
                      Chemical Flavor Synergy Radar
                    </span>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                      {Object.entries(tabpfn.flavor_balance).map(([key, val]) => (
                        <div key={key} className="bg-[#242424] p-2.5 rounded-xl border border-white/[0.05]">
                          <div className="flex justify-between text-xs mb-1">
                            <span className="capitalize text-[#A5A39D]">{key}</span>
                            <span className="font-mono text-[#F4D779] font-bold">{val}%</span>
                          </div>
                          <div className="w-full bg-[#181818] rounded-full h-1">
                            <div
                              className="bg-[#F4D779] h-1 rounded-full"
                              style={{ width: `${val}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {tabpfn.pairing_synergies && tabpfn.pairing_synergies.length > 0 && (
                    <div>
                      <span className="text-[11px] font-semibold text-[#A5A39D] uppercase tracking-wider block mb-1.5">
                        In-Context TabPFN Flavor Interactions
                      </span>
                      <div className="space-y-1">
                        {tabpfn.pairing_synergies.map((syn, idx) => (
                          <div key={idx} className="text-xs text-[#F5F2EB] flex items-center gap-2">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                            <span>{syn}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Radical Sloth Shortcuts & Steps (Only when a valid dish is ready or in progress) */}
            {recipe.status !== "NO_GOOD_MATCH" && (
              <>
                {/* Ingredients in this Pan Breakdown */}
                {recipe.ingredients_used && recipe.ingredients_used.length > 0 && (
                  <div className="p-4 sm:p-5 rounded-2xl bg-[#202020] border border-white/[0.07] space-y-3">
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <h3 className="font-display font-semibold text-xs uppercase tracking-wider text-[#A5A39D] flex items-center gap-2">
                        <Utensils className="w-4 h-4 text-[#F4D779]" />
                        <span>Ingredients in this Pan ({recipe.ingredients_used.length} Items)</span>
                      </h3>
                      <div className="flex items-center gap-2 text-[11px] font-mono">
                        <span className="text-[#A5A39D] bg-[#181818] px-2.5 py-0.5 rounded-full border border-white/[0.06]">
                          Vessel: <strong className="text-[#F5F2EB]">{recipe.vessel_type}</strong>
                        </span>
                        <span className="text-[#A5A39D] bg-[#181818] px-2.5 py-0.5 rounded-full border border-white/[0.06]">
                          Tool: <strong className="text-[#F5F2EB]">{recipe.utensil}</strong>
                        </span>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {recipe.ingredients_used.map((ing, i) => {
                        const isOptional = ing.toLowerCase().includes('optional');
                        return (
                          <span
                            key={i}
                            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition-colors ${
                              isOptional
                                ? 'bg-[#181818] border-dashed border-white/20 text-[#A5A39D]'
                                : 'bg-[#181818] border-white/10 text-[#F5F2EB]'
                            }`}
                          >
                            <span className="text-[10px]">{isOptional ? '⚪' : '🟢'}</span>
                            <span className="capitalize">{ing.replace(/\s*\(optional\)/i, '')}</span>
                            {isOptional && (
                              <span className="text-[9px] text-[#A5A39D] uppercase tracking-wider bg-[#242424] px-1.5 py-0.5 rounded font-mono">
                                optional
                              </span>
                            )}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Radical Sloth Shortcuts */}
                <div>
                  <h3 className="font-display font-semibold text-xs uppercase tracking-wider text-[#A5A39D] mb-3 flex items-center gap-2">
                    <Award className="w-4 h-4 text-[#F4D779]" />
                    <span>Radical Sloth Shortcuts (No Prep Allowed)</span>
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

            {/* Interactive Step-by-Step Checklist */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-display font-semibold text-xs uppercase tracking-wider text-[#A5A39D] flex items-center gap-2">
                  <Utensils className="w-4 h-4 text-[#F4D779]" />
                  <span>Interactive Cooking Checklist (Tap Steps as You Cook)</span>
                </h3>
                <span className="text-[11px] font-mono font-medium text-[#F4D779]">
                  {completedSteps.length} of {recipe.steps.length} done ({progressPercent}%)
                </span>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-[#202020] rounded-full h-1.5 mb-3.5 overflow-hidden">
                <div
                  className="bg-[#F4D779] h-1.5 rounded-full transition-all duration-300"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>

              {/* Interactive Step List */}
              <div className="space-y-2.5">
                {recipe.steps.map((step, idx) => {
                  const isDone = completedSteps.includes(idx);
                  return (
                    <div
                      key={idx}
                      onClick={() => toggleStep(idx)}
                      className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-start gap-3.5 select-none ${
                        isDone
                          ? 'bg-[#181818] border-emerald-500/30 text-[#A5A39D]'
                          : 'bg-[#202020] border-white/[0.06] hover:border-white/[0.12] text-[#F5F2EB]'
                      }`}
                    >
                      {/* Checkbox button */}
                      <button
                        type="button"
                        className={`w-6 h-6 rounded-xl flex items-center justify-center shrink-0 transition-colors border ${
                          isDone
                            ? 'bg-emerald-500 text-[#181818] border-emerald-500'
                            : 'bg-[#292929] border-white/[0.1] text-[#A5A39D]'
                        }`}
                      >
                        {isDone ? (
                          <Check className="w-3.5 h-3.5 stroke-[3]" />
                        ) : (
                          <span className="text-xs font-mono font-bold">{idx + 1}</span>
                        )}
                      </button>

                      <span className={`text-xs leading-relaxed pt-0.5 ${isDone ? 'line-through text-[#A5A39D]/70' : ''}`}>
                        {step}
                      </span>
                    </div>
                  );
                })}
              </div>

              {completedSteps.length === recipe.steps.length && (
                <div className="mt-4 p-4 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center justify-between gap-3 animate-in fade-in zoom-in duration-200">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🎉</span>
                    <span>Meal complete! You successfully survived cooking with only 1 pan.</span>
                  </div>
                  <button
                    onClick={() => setCompletedSteps([])}
                    className="text-[11px] underline text-emerald-200 hover:text-white cursor-pointer"
                  >
                    Reset checklist
                  </button>
                </div>
              )}
            </div>

                {/* Cleanup Audit Alert */}
                <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-start gap-3 text-xs">
                  <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold uppercase tracking-wider text-emerald-300 block mb-0.5">
                      1-Pan Dish & Cleanup Audit:
                    </span>
                    <p className="leading-relaxed text-emerald-200/90">
                      {recipe.cleanup_audit}
                    </p>
                  </div>
                </div>
              </>
            )}

            {/* Footer Regenerate Action */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-white/[0.07]">
              <div className="flex items-center gap-2 text-[11px] text-[#A5A39D]">
                <Shield className="w-3.5 h-3.5 text-[#F4D779]" />
                <span>
                  Engine: <strong className="text-[#F5F2EB]">{recipe.ai_engine_used || "SlothChef Decision Engine"}</strong> • Prior Labs TabPFN-3.5
                </span>
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
      )}

      {/* VIEW 2: DISTRACTION-FREE COOK-ALONG MODE */}
      {viewMode === 'cook_along' && (
        <div className="p-8 sm:p-12 min-h-[500px] flex flex-col justify-between animate-in fade-in duration-200">
          <div>
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/[0.06]">
              <div className="flex items-center gap-2">
                <ChefHat className="w-5 h-5 text-[#F4D779]" />
                <span className="font-display font-bold text-sm text-[#F5F2EB]">
                  Cook-Along Focus Mode
                </span>
              </div>
              
              <div className="flex items-center gap-2">
                {/* Voice Read Aloud Button */}
                <button
                  type="button"
                  onClick={() => {
                    if (isSpeaking) {
                      stopSpeaking();
                      setIsSpeaking(false);
                    } else {
                      setIsSpeaking(true);
                      speakStep(recipe.steps[currentCookStep], () => setIsSpeaking(false));
                    }
                  }}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border transition-all cursor-pointer ${
                    isSpeaking
                      ? 'bg-[#F4D779] text-[#181818] border-[#F4D779] font-bold shadow-sm'
                      : 'bg-[#202020] hover:bg-[#292929] text-[#F4D779] border-white/[0.08]'
                  }`}
                  title="Hands-free cooking: listen to instruction"
                >
                  {isSpeaking ? (
                    <>
                      <VolumeX className="w-3.5 h-3.5 animate-pulse" />
                      <span>Stop Voice</span>
                    </>
                  ) : (
                    <>
                      <Volume2 className="w-3.5 h-3.5" />
                      <span>Read Aloud 🔊</span>
                    </>
                  )}
                </button>

                <span className="font-mono text-xs text-[#F4D779] bg-[#F4D779]/10 px-3 py-1 rounded-full border border-[#F4D779]/20">
                  Step {currentCookStep + 1} of {recipe.steps.length}
                </span>
              </div>
            </div>

            {/* Big readable step card */}
            <div className="bg-[#202020] rounded-3xl p-8 border border-white/[0.08] shadow-lg mb-8">
              <span className="text-xs uppercase tracking-widest text-[#F4D779] font-bold block mb-3">
                Instruction {currentCookStep + 1}
              </span>
              <p className="font-display font-bold text-xl sm:text-2xl text-[#F5F2EB] leading-relaxed">
                {recipe.steps[currentCookStep]}
              </p>
            </div>

            {/* Quick Cooking Tip for this step */}
            <div className="p-4 rounded-2xl bg-[#242424] border border-white/[0.06] text-xs text-[#A5A39D] flex items-center gap-2.5 mb-6">
              <span className="text-lg">💡</span>
              <span>
                Sloth Principle: Never use extra bowls. If an ingredient needs mixing, do it right in the pan.
              </span>
            </div>
          </div>

          {/* Navigation Controls */}
          <div className="flex items-center justify-between gap-4 pt-6 border-t border-white/[0.06]">
            <button
              onClick={() => {
                stopSpeaking();
                setIsSpeaking(false);
                setCurrentCookStep((prev) => Math.max(0, prev - 1));
              }}
              disabled={currentCookStep === 0}
              className={`flex items-center gap-2 px-5 py-3 rounded-2xl text-xs font-bold transition-all cursor-pointer ${
                currentCookStep === 0
                  ? 'opacity-40 cursor-not-allowed bg-[#202020] text-[#A5A39D]'
                  : 'bg-[#202020] hover:bg-[#292929] text-[#F5F2EB]'
              }`}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous Step</span>
            </button>

            {currentCookStep < recipe.steps.length - 1 ? (
              <button
                onClick={() => {
                  stopSpeaking();
                  setIsSpeaking(false);
                  toggleStep(currentCookStep);
                  setCurrentCookStep((prev) => prev + 1);
                }}
                className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-[#F4D779] hover:bg-[#E8CA6B] text-[#181818] font-bold text-xs transition-all shadow-lg cursor-pointer"
              >
                <span>Step Done & Next</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={() => {
                  stopSpeaking();
                  setIsSpeaking(false);
                  toggleStep(currentCookStep);
                  setViewMode('overview');
                  confetti({
                    particleCount: 100,
                    spread: 80,
                    origin: { y: 0.6 }
                  });
                }}
                className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-emerald-400 hover:bg-emerald-300 text-[#181818] font-bold text-xs transition-all shadow-lg cursor-pointer"
              >
                <span>Complete Recipe & Feast 🦥</span>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
