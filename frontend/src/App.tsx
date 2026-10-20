import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { SlothHeader } from './components/SlothHeader';
import { SlothContract } from './components/SlothContract';
import { PresetDisasters } from './components/PresetDisasters';
import { PantrySelector } from './components/PantrySelector';
import { SlothMetricsMeter } from './components/SlothMetricsMeter';
import { RecipeCard } from './components/RecipeCard';
import { TabPFNExplainerModal } from './components/TabPFNExplainerModal';
import { PresetDisaster, SlothRecipe, SlothContractState } from './types';
import { AlertCircle, Sparkles, ChefHat, Utensils, Clock, Flame } from 'lucide-react';

const LOADING_MESSAGES = [
  "Minimizing unnecessary effort...",
  "Negotiating with your leftovers...",
  "Prior Labs TabPFN calculating flavor harmony...",
  "Consulting Gemma 2 for radical shortcuts...",
  "Enforcing strict 1-pan dish constraints..."
];

export const App: React.FC = () => {
  const [catalog, setCatalog] = useState<string[]>([]);
  const [presets, setPresets] = useState<PresetDisaster[]>([]);
  const [selectedPresetId, setSelectedPresetId] = useState<string | null>(null);
  const [selectedIngredients, setSelectedIngredients] = useState<string[]>([
    "Ramen noodles", "Peanut butter", "Sriracha", "Soy sauce"
  ]);
  const [vesselPreference, setVesselPreference] = useState<string>("One Skillet");
  const [contract, setContract] = useState<SlothContractState>({
    maxActiveMinutes: 5,
    maxCookwareCount: 1,
    maxUtensilCount: 1,
    microwaveOnly: false,
    minimalChopping: true
  });
  
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingMessageIdx, setLoadingMessageIdx] = useState<number>(0);
  const [recipe, setRecipe] = useState<SlothRecipe | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isExplainerOpen, setIsExplainerOpen] = useState<boolean>(false);
  const [inferenceMode, setInferenceMode] = useState<'local' | 'cloud' | 'demo'>('demo');

  // Cycle loading messages when generating
  useEffect(() => {
    let interval: any = null;
    if (isLoading) {
      interval = setInterval(() => {
        setLoadingMessageIdx((prev) => (prev + 1) % LOADING_MESSAGES.length);
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  // Fetch presets, catalog, and health check on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [presetsRes, catalogRes, healthRes] = await Promise.all([
          fetch('/api/pantry/presets'),
          fetch('/api/pantry/catalog'),
          fetch('/api/health')
        ]);
        
        if (presetsRes.ok) {
          const p = await presetsRes.json();
          setPresets(p);
          if (p.length > 0) {
            setSelectedPresetId(p[0].id);
            setSelectedIngredients(p[0].ingredients);
            const initVessel = p[0].vessel_preference || "One Skillet";
            setVesselPreference(initVessel);

            // Auto-generate initial recipe so the application never loads empty
            try {
              setIsLoading(true);
              const genRes = await fetch('/api/recipe/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  ingredients: p[0].ingredients,
                  vessel_preference: initVessel,
                  sloth_intensity: "Maximum",
                  max_active_minutes: 5,
                  max_cookware_count: 1,
                  max_utensil_count: 1,
                  microwave_only: false,
                  minimal_chopping: true
                })
              });
              if (genRes.ok) {
                const recipeData = await genRes.json();
                setRecipe(recipeData);
              }
            } catch (e) {
              console.error("Initial recipe generation error:", e);
            } finally {
              setIsLoading(false);
            }
          }
        }
        
        if (catalogRes.ok) {
          const c = await catalogRes.json();
          setCatalog(c);
        }

        if (healthRes.ok) {
          const h = await healthRes.json();
          // Detect whether Ollama local inference is running or cloud fallback
          if (h.status === 'healthy') {
            setInferenceMode('cloud');
          }
        }
      } catch (err) {
        console.error("Initial data fetch error:", err);
      }
    };
    fetchData();
  }, []);

  const triggerConfetti = () => {
    confetti({
      particleCount: 50,
      spread: 60,
      origin: { y: 0.8 },
      colors: ['#F4D779', '#10b981', '#ffffff']
    });
  };

  const handleGenerate = async (ingredientsOverride?: string[], vesselOverride?: string) => {
    const ings = ingredientsOverride || selectedIngredients;
    const vessel = vesselOverride || (contract.microwaveOnly ? "Microwave Safe Bowl" : vesselPreference);

    if (ings.length === 0) {
      setError("Please add at least one ingredient to your pan.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/recipe/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredients: ings,
          vessel_preference: vessel,
          sloth_intensity: "Maximum",
          max_active_minutes: contract.maxActiveMinutes,
          max_cookware_count: contract.maxCookwareCount,
          max_utensil_count: contract.maxUtensilCount,
          microwave_only: contract.microwaveOnly,
          minimal_chopping: contract.minimalChopping
        })
      });

      if (!res.ok) {
        throw new Error(`Failed to generate recipe (${res.status})`);
      }

      const data: SlothRecipe = await res.json();
      setRecipe(data);
      if (data.harmony_score >= 85) {
        triggerConfetti();
      }
    } catch (err: any) {
      setError(err.message || "Failed to contact SlothChef AI server. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectPreset = (preset: PresetDisaster) => {
    setSelectedPresetId(preset.id);
    setSelectedIngredients(preset.ingredients);
    const vessel = preset.vessel_preference || "One Skillet";
    setVesselPreference(vessel);
    handleGenerate(preset.ingredients, vessel);
  };

  const handleAddIngredient = (item: string) => {
    if (!selectedIngredients.some((i) => i.toLowerCase() === item.toLowerCase())) {
      setSelectedIngredients([...selectedIngredients, item]);
      setSelectedPresetId(null);
    }
  };

  const handleRemoveIngredient = (item: string) => {
    setSelectedIngredients(selectedIngredients.filter((i) => i.toLowerCase() !== item.toLowerCase()));
    setSelectedPresetId(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#242424] text-[#F5F2EB] selection:bg-[#F4D779] selection:text-[#181818]">
      {/* Editorial Navigation Header */}
      <SlothHeader
        onOpenExplainer={() => setIsExplainerOpen(true)}
        inferenceMode={inferenceMode}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8">
        {/* Editorial Hero Intro - Compact Banner */}
        <div className="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/[0.06] pb-5">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-[#181818] border border-white/[0.08] text-[11px] text-[#F4D779] font-medium mb-2">
              <span>🦥 SlothChef Studio</span>
              <span className="w-1 h-1 rounded-full bg-[#F4D779]" />
              <span className="text-[#A5A39D]">DEV Hacktoberfest 2026</span>
            </div>
            <h1 className="font-display font-bold text-2xl sm:text-3xl lg:text-4xl text-[#F5F2EB] tracking-tight leading-snug">
              Cooking should take less effort than deciding what to eat.
            </h1>
            <p className="text-xs sm:text-sm text-[#A5A39D] mt-1">
              Your kitchen. Your ingredients. Absolutely minimal effort. Powered by <span className="text-[#F5F2EB] font-medium">Prior Labs TabPFN-3.5</span> & <span className="text-[#F5F2EB] font-medium">Google Gemma 2</span>.
            </p>
          </div>
          <div className="hidden md:flex items-center gap-2 shrink-0 text-xs text-[#A5A39D] bg-[#181818] px-3.5 py-2 rounded-2xl border border-white/[0.06]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="font-medium text-[#F5F2EB]">Zero-Effort Mode</span>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-medium mb-6 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => handleGenerate()}
              className="px-3 py-1 rounded-xl bg-red-500/20 hover:bg-red-500/30 text-red-200 text-[11px] font-semibold transition-colors cursor-pointer"
            >
              Retry
            </button>
          </div>
        )}

        {/* Fridge Disasters 3-Card Showcase */}
        <PresetDisasters
          presets={presets}
          selectedId={selectedPresetId}
          onSelect={handleSelectPreset}
          isLoading={isLoading}
        />

        {/* Spacious 2-Column Responsive Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Constraints & Ingredient Scavenger (5 cols) */}
          <div className="lg:col-span-5 space-y-6">
            {/* The Sloth Contract Constraints */}
            <SlothContract
              contract={contract}
              onChange={setContract}
              vesselPreference={vesselPreference}
              onVesselChange={setVesselPreference}
            />

            {/* Ingredient Selector */}
            <PantrySelector
              catalog={catalog}
              selectedIngredients={selectedIngredients}
              onAddIngredient={handleAddIngredient}
              onRemoveIngredient={handleRemoveIngredient}
              onGenerate={() => handleGenerate()}
              isLoading={isLoading}
            />
          </div>

          {/* Right Column: Recipe Result & TabPFN Telemetry (7 cols) */}
          <div className="lg:col-span-7">
            {isLoading ? (
              <div className="bg-[#181818] rounded-3xl p-12 border border-white/[0.08] shadow-2xl flex flex-col items-center justify-center text-center min-h-[460px] animate-pulse">
                <div className="w-16 h-16 rounded-3xl bg-[#202020] border border-[#F4D779]/30 flex items-center justify-center text-3xl mb-5 shadow-lg">
                  🦥
                </div>
                <h3 className="font-display font-bold text-lg text-[#F5F2EB] mb-2">
                  {LOADING_MESSAGES[loadingMessageIdx]}
                </h3>
                <p className="text-xs text-[#A5A39D] max-w-sm leading-relaxed">
                  TabPFN evaluates your chemical pairing vectors while Gemma 2 crafts radical low-effort shortcuts.
                </p>
                <div className="w-48 bg-[#292929] rounded-full h-1.5 mt-6 overflow-hidden">
                  <div className="bg-[#F4D779] h-1.5 rounded-full w-2/3 animate-[pulse_1s_ease-in-out_infinite]" />
                </div>
              </div>
            ) : recipe ? (
              <div className="animate-in fade-in duration-300">
                <SlothMetricsMeter
                  prediction={recipe.tabpfn_evidence}
                  slothScore={recipe.sloth_score || 96}
                />
                <RecipeCard
                  recipe={recipe}
                  onRegenerate={() => handleGenerate()}
                  isLoading={isLoading}
                />
              </div>
            ) : (
              /* Editorial Empty State */
              <div className="bg-[#181818] rounded-3xl p-10 border border-white/[0.07] text-center min-h-[400px] flex flex-col items-center justify-center">
                <div className="w-14 h-14 rounded-2xl bg-[#202020] border border-white/[0.08] flex items-center justify-center text-2xl mb-4">
                  🍳
                </div>
                <h3 className="font-display font-bold text-lg text-[#F5F2EB] mb-1">
                  Ready to Cook with Minimal Exertion
                </h3>
                <p className="text-xs text-[#A5A39D] max-w-md leading-relaxed mb-6">
                  Pick a disaster preset above or enter whatever 3 sad ingredients you have in your fridge. 
                  TabPFN and Gemma 2 will handle the culinary chemistry.
                </p>
                <button
                  onClick={() => handleGenerate()}
                  className="px-6 py-2.5 rounded-xl bg-[#F4D779] hover:bg-[#E8CA6B] text-[#181818] text-xs font-bold transition-all cursor-pointer shadow-md"
                >
                  Generate Initial Recipe
                </button>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Editorial Footer */}
      <footer className="border-t border-white/[0.06] bg-[#181818] py-6 text-xs text-[#A5A39D]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-display font-bold text-[#F5F2EB]">SlothChef</span>
            <span>• Built for DEV Hacktoberfest 2026: Week 3 (Slow and Steady)</span>
          </div>
          <div className="flex items-center gap-4 text-[#A5A39D]">
            <span>Prior Labs TabPFN-3.5</span>
            <span>Google Gemma 2</span>
            <span>Render Cloud</span>
          </div>
        </div>
      </footer>

      {/* TabPFN Math Explainer Modal */}
      <TabPFNExplainerModal
        isOpen={isExplainerOpen}
        onClose={() => setIsExplainerOpen(false)}
      />
    </div>
  );
};
