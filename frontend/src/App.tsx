import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { SlothHeader } from './components/SlothHeader';
import { PresetDisasters } from './components/PresetDisasters';
import { PantrySelector } from './components/PantrySelector';
import { SlothMetricsMeter } from './components/SlothMetricsMeter';
import { RecipeCard } from './components/RecipeCard';
import { TabPFNExplainerModal } from './components/TabPFNExplainerModal';
import { PresetDisaster, SlothRecipe, TabPFNPrediction } from './types';
import { AlertCircle, Sparkles, ChefHat, HeartHandshake } from 'lucide-react';

export const App: React.FC = () => {
  const [catalog, setCatalog] = useState<string[]>([]);
  const [presets, setPresets] = useState<PresetDisaster[]>([]);
  const [selectedPresetId, setSelectedPresetId] = useState<string | null>(null);
  const [selectedIngredients, setSelectedIngredients] = useState<string[]>([
    "Ramen noodles", "Peanut butter", "Sriracha", "Soy sauce"
  ]);
  const [vesselPreference, setVesselPreference] = useState<string>("One Skillet");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [recipe, setRecipe] = useState<SlothRecipe | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isExplainerOpen, setIsExplainerOpen] = useState<boolean>(false);

  // Fetch presets and catalog on initial mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [presetsRes, catalogRes] = await Promise.all([
          fetch('/api/pantry/presets'),
          fetch('/api/pantry/catalog')
        ]);
        if (presetsRes.ok) {
          const p = await presetsRes.json();
          setPresets(p);
          if (p.length > 0) {
            setSelectedPresetId(p[0].id);
          }
        }
        if (catalogRes.ok) {
          const c = await catalogRes.json();
          setCatalog(c);
        }
      } catch (err) {
        console.error("Failed to fetch initial pantry data:", err);
      }
    };
    fetchData();
  }, []);

  const triggerConfetti = () => {
    confetti({
      particleCount: 50,
      spread: 60,
      origin: { y: 0.8 },
      colors: ['#f59e0b', '#10b981', '#fbbf24']
    });
  };

  const handleGenerate = async (ingredientsOverride?: string[], vesselOverride?: string) => {
    const ings = ingredientsOverride || selectedIngredients;
    const vessel = vesselOverride || vesselPreference;

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
          sloth_intensity: "Maximum"
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
      setError(err.message || "Failed to contact SlothChef AI server.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectPreset = (preset: PresetDisaster) => {
    setSelectedPresetId(preset.id);
    setSelectedIngredients(preset.ingredients);
    setVesselPreference(preset.vessel_preference || "One Skillet");
    handleGenerate(preset.ingredients, preset.vessel_preference);
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
    <div className="min-h-screen flex flex-col bg-[#FAF7F2] text-stone-900">
      <SlothHeader onOpenExplainer={() => setIsExplainerOpen(true)} />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center max-w-2xl mx-auto mb-8">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 text-amber-900 border border-amber-300 text-xs font-bold mb-3 shadow-2xs">
            <span>🦥 Happy International Sloth Day!</span>
          </div>
          <h1 className="font-display font-extrabold text-3xl sm:text-5xl text-stone-900 tracking-tight mb-3">
            Radically Lazy. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-600 via-amber-700 to-amber-900">
              Shockingly Edible.
            </span>
          </h1>
          <p className="text-sm sm:text-base text-stone-600 leading-relaxed">
            The anti-gourmet survival engine that pairs whatever 3 sad ingredients you have left 
            using <strong>Prior Labs' TabPFN-3.5</strong> and <strong>Google Gemma 2</strong>. 
            Zero dishes to soak. Zero grocery store trips.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-900 text-xs font-medium mb-6 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Preset Disasters for 1-Click Testing */}
        <PresetDisasters
          presets={presets}
          selectedId={selectedPresetId}
          onSelect={handleSelectPreset}
          isLoading={isLoading}
        />

        {/* Interactive Pantry Ingredient Picker */}
        <PantrySelector
          catalog={catalog}
          selectedIngredients={selectedIngredients}
          onAddIngredient={handleAddIngredient}
          onRemoveIngredient={handleRemoveIngredient}
          vesselPreference={vesselPreference}
          onVesselChange={setVesselPreference}
          onGenerate={() => handleGenerate()}
          isLoading={isLoading}
        />

        {/* Recipe & TabPFN Telemetry Display */}
        {recipe && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-300">
            <SlothMetricsMeter prediction={recipe.tabpfn_evidence} />
            <RecipeCard recipe={recipe} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-amber-200/60 bg-amber-100/30 py-6 text-center text-xs text-stone-500">
        <div className="max-w-5xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-1.5">
            <span className="font-display font-bold text-stone-800">SlothChef</span>
            <span>• Open-Source AI for DEV Hacktoberfest 2026 Week 3</span>
          </div>
          <div className="flex items-center gap-4 text-stone-600">
            <span>TabPFN-3.5 (Prior Labs)</span>
            <span>Google Gemma 2</span>
            <span>Hosted on Render</span>
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
