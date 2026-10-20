import React, { useState } from 'react';
import { Plus, X, Search, Sparkles, Wand2, ChefHat, Check } from 'lucide-react';

interface PantrySelectorProps {
  catalog: string[];
  selectedIngredients: string[];
  onAddIngredient: (name: string) => void;
  onRemoveIngredient: (name: string) => void;
  vesselPreference: string;
  onVesselChange: (vessel: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
}

const VESSELS = ["One Skillet", "Single Pot", "Microwave Safe Bowl"];

export const PantrySelector: React.FC<PantrySelectorProps> = ({
  catalog,
  selectedIngredients,
  onAddIngredient,
  onRemoveIngredient,
  vesselPreference,
  onVesselChange,
  onGenerate,
  isLoading
}) => {
  const [customInput, setCustomInput] = useState('');

  const handleAddCustom = (e: React.FormEvent) => {
    e.preventDefault();
    if (customInput.trim()) {
      onAddIngredient(customInput.trim());
      setCustomInput('');
    }
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-3xl p-5 border border-amber-200/90 shadow-sm mb-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
        <div>
          <h2 className="font-display font-bold text-lg text-stone-900 flex items-center gap-2">
            <span>What sad items are in your fridge right now?</span>
          </h2>
          <p className="text-xs text-stone-500">
            Select staples or type whatever random ingredients you have left.
          </p>
        </div>

        {/* Vessel Preference */}
        <div className="flex items-center gap-1.5 p-1 bg-amber-50 rounded-2xl border border-amber-200/70 self-start md:self-auto">
          {VESSELS.map((v) => (
            <button
              key={v}
              type="button"
              onClick={() => onVesselChange(v)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-xl transition-all cursor-pointer ${
                vesselPreference === v
                  ? 'bg-amber-600 text-white shadow-xs'
                  : 'text-stone-600 hover:text-stone-900'
              }`}
            >
              {v}
            </button>
          ))}
        </div>
      </div>

      {/* Selected Ingredients Tag Cloud */}
      <div className="min-h-[50px] p-3 rounded-2xl bg-amber-50/60 border border-amber-200/60 flex flex-wrap items-center gap-2 mb-4">
        {selectedIngredients.length === 0 ? (
          <span className="text-xs text-amber-900/40 italic">
            No ingredients selected. Pick from the staples below or click a preset above...
          </span>
        ) : (
          selectedIngredients.map((ing) => (
            <span
              key={ing}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/15 text-amber-950 border border-amber-400/40 text-xs font-bold animate-in fade-in zoom-in duration-150"
            >
              <span>{ing}</span>
              <button
                type="button"
                onClick={() => onRemoveIngredient(ing)}
                className="hover:bg-amber-400/30 rounded-full p-0.5 transition-colors cursor-pointer"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </span>
          ))
        )}
      </div>

      {/* Custom Input Bar */}
      <form onSubmit={handleAddCustom} className="flex gap-2 mb-4">
        <div className="relative flex-1">
          <input
            type="text"
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            placeholder="Add custom item (e.g. half a zucchini, leftover curry paste, feta)..."
            className="w-full px-4 py-2.5 rounded-2xl border border-amber-200/80 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/50"
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2.5 rounded-2xl bg-stone-800 hover:bg-stone-900 text-white text-xs font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>Add</span>
        </button>
      </form>

      {/* Quick Select Staples */}
      <div className="mb-5">
        <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400 block mb-2">
          Common Scavenged Staples:
        </span>
        <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto pr-1">
          {catalog.map((item) => {
            const isSelected = selectedIngredients.some(
              (i) => i.toLowerCase() === item.toLowerCase()
            );
            return (
              <button
                key={item}
                type="button"
                onClick={() => {
                  if (isSelected) {
                    onRemoveIngredient(item);
                  } else {
                    onAddIngredient(item);
                  }
                }}
                className={`px-2.5 py-1 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-amber-600 text-white border-amber-600 font-semibold'
                    : 'bg-white hover:bg-amber-100/60 text-stone-700 border-stone-200'
                }`}
              >
                {isSelected && <Check className="w-3 h-3 inline mr-1" />}
                {item}
              </button>
            );
          })}
        </div>
      </div>

      {/* Action Button */}
      <div className="flex items-center justify-between pt-3 border-t border-amber-100">
        <div className="text-xs text-stone-500">
          <span className="font-semibold text-stone-700">{selectedIngredients.length}</span> items ready for TabPFN scoring
        </div>

        <button
          type="button"
          onClick={onGenerate}
          disabled={selectedIngredients.length === 0 || isLoading}
          className={`px-6 py-3 rounded-2xl font-display font-bold text-sm flex items-center gap-2 transition-all shadow-md cursor-pointer ${
            selectedIngredients.length === 0 || isLoading
              ? 'bg-stone-300 text-stone-500 cursor-not-allowed shadow-none'
              : 'bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-700 hover:to-amber-600 text-white shadow-amber-600/20 active:scale-98'
          }`}
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>TabPFN Prior Labs + Gemma 2 Thinking...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Synthesize Sloth Recipe</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
