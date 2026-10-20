import React, { useState } from 'react';
import { PresetDisaster, SlothContractState } from '../types';
import { 
  Sparkles, 
  Flame, 
  Zap, 
  Clock, 
  Utensils, 
  Scissors, 
  Plus, 
  X, 
  Check, 
  ArrowRight, 
  Search, 
  Filter, 
  Trash2,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';

interface KitchenStudioProps {
  catalog: string[];
  selectedIngredients: string[];
  onAddIngredient: (name: string) => void;
  onRemoveIngredient: (name: string) => void;
  onClearIngredients: () => void;
  presets: PresetDisaster[];
  selectedPresetId: string | null;
  onSelectPreset: (preset: PresetDisaster) => void;
  contract: SlothContractState;
  onContractChange: (contract: SlothContractState) => void;
  vesselPreference: string;
  onVesselChange: (vessel: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
  predictedHarmony?: number;
}

const CATEGORIES = [
  { id: 'all', label: 'All Staples' },
  { id: 'carbs', label: '🍜 Carbs & Bases' },
  { id: 'proteins', label: '🍳 Proteins & Fats' },
  { id: 'sauces', label: '🌶️ Sauces & Umami' },
  { id: 'veggies', label: '🥦 Veggies' }
];

const CATEGORY_MAP: Record<string, string[]> = {
  carbs: ['ramen', 'rice', 'tortilla', 'chips', 'bread', 'noodles', 'pasta'],
  proteins: ['peanut butter', 'eggs', 'egg', 'beans', 'cheese', 'chickpeas', 'tofu', 'tuna'],
  sauces: ['soy sauce', 'sriracha', 'salsa', 'curry powder', 'coconut milk', 'hot sauce', 'mayo', 'olive oil', 'butter'],
  veggies: ['peas', 'garlic', 'onion', 'tomato', 'spinach', 'scallions', 'corn']
};

const VESSEL_OPTIONS = [
  { label: 'Skillet', full: 'One Skillet', icon: '🍳' },
  { label: 'Pot', full: 'Single Pot', icon: '🍲' },
  { label: 'Microwave', full: 'Microwave Bowl', icon: '⚡' },
];

export const KitchenStudio: React.FC<KitchenStudioProps> = ({
  catalog,
  selectedIngredients,
  onAddIngredient,
  onRemoveIngredient,
  onClearIngredients,
  presets,
  selectedPresetId,
  onSelectPreset,
  contract,
  onContractChange,
  vesselPreference,
  onVesselChange,
  onGenerate,
  isLoading,
  predictedHarmony = 94
}) => {
  const [activeTab, setActiveTab] = useState<'presets' | 'scavenger'>('presets');
  const [customInput, setCustomInput] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const handleAddCustom = (e: React.FormEvent) => {
    e.preventDefault();
    if (customInput.trim()) {
      onAddIngredient(customInput.trim());
      setCustomInput('');
    }
  };

  const updateContract = (updates: Partial<SlothContractState>) => {
    onContractChange({ ...contract, ...updates });
  };

  // Filter catalog by category and search
  const filteredCatalog = catalog.filter((item) => {
    const matchesSearch = item.toLowerCase().includes(searchQuery.toLowerCase());
    if (!matchesSearch) return false;
    if (selectedCategory === 'all') return true;

    const keywords = CATEGORY_MAP[selectedCategory] || [];
    return keywords.some((kw) => item.toLowerCase().includes(kw));
  });

  return (
    <div className="bg-[#181818] rounded-3xl border border-white/[0.08] shadow-2xl p-5 sm:p-6 flex flex-col gap-6">
      {/* Studio Header & Segmented Mode Switcher */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="font-display font-bold text-lg text-[#F5F2EB] flex items-center gap-2">
              <span>Kitchen Workbench</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-[#F4D779]/10 text-[#F4D779] border border-[#F4D779]/20 font-sans font-semibold">
                Interactive
              </span>
            </h2>
            <p className="text-xs text-[#A5A39D] mt-0.5">
              Choose a disaster preset or build your meal from random fridge leftovers.
            </p>
          </div>
        </div>

        {/* Mode Switcher Tabs */}
        <div className="grid grid-cols-2 gap-1.5 p-1 bg-[#202020] rounded-2xl border border-white/[0.06]">
          <button
            type="button"
            onClick={() => setActiveTab('presets')}
            className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 cursor-pointer ${
              activeTab === 'presets'
                ? 'bg-[#F4D779] text-[#181818] shadow-md'
                : 'text-[#A5A39D] hover:text-[#F5F2EB] hover:bg-white/[0.04]'
            }`}
          >
            <Zap className="w-3.5 h-3.5" />
            <span>1-Click Disasters ({presets.length})</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('scavenger')}
            className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 cursor-pointer ${
              activeTab === 'scavenger'
                ? 'bg-[#F4D779] text-[#181818] shadow-md'
                : 'text-[#A5A39D] hover:text-[#F5F2EB] hover:bg-white/[0.04]'
            }`}
          >
            <span>🥫 Fridge Scavenger</span>
            {selectedIngredients.length > 0 && (
              <span className="w-5 h-5 rounded-full bg-[#181818] text-[#F4D779] text-[10px] flex items-center justify-center font-bold">
                {selectedIngredients.length}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* TAB 1: 1-Click Disasters List */}
      {activeTab === 'presets' && (
        <div className="space-y-3 animate-in fade-in duration-200">
          <div className="text-[11px] font-semibold text-[#A5A39D] uppercase tracking-wider flex items-center justify-between">
            <span>Curated Low-Effort Scenarios</span>
            <span className="text-[#F4D779]">Tap to load & synthesize</span>
          </div>

          <div className="space-y-2.5">
            {presets.slice(0, 3).map((preset) => {
              const isSelected = selectedPresetId === preset.id;
              return (
                <div
                  key={preset.id}
                  onClick={() => onSelectPreset(preset)}
                  className={`p-3.5 rounded-2xl border transition-all cursor-pointer flex items-center gap-3.5 group select-none ${
                    isSelected
                      ? 'bg-[#202020] border-[#F4D779] shadow-lg shadow-[#F4D779]/5 ring-1 ring-[#F4D779]/40'
                      : 'bg-[#202020]/70 hover:bg-[#202020] border-white/[0.06] hover:border-white/[0.12]'
                  }`}
                >
                  {/* Thumbnail */}
                  <div className="w-16 h-16 rounded-xl overflow-hidden bg-[#242424] shrink-0 relative">
                    <img
                      src={preset.image_url || "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=400&q=80"}
                      alt={preset.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-black/20" />
                    <span className="absolute bottom-1 right-1 text-xs">
                      {preset.emoji}
                    </span>
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1 mb-0.5">
                      <h4 className="font-display font-bold text-sm text-[#F5F2EB] group-hover:text-[#F4D779] transition-colors truncate">
                        {preset.title}
                      </h4>
                      <span className="text-[10px] font-mono font-medium text-[#F4D779] bg-[#F4D779]/10 px-2 py-0.5 rounded-full shrink-0">
                        {preset.target_time}
                      </span>
                    </div>

                    <p className="text-[11px] text-[#A5A39D] line-clamp-1 mb-1.5">
                      {preset.description}
                    </p>

                    {/* Ingredient preview tags */}
                    <div className="flex flex-wrap gap-1">
                      {preset.ingredients.slice(0, 4).map((ing, i) => (
                        <span
                          key={i}
                          className="text-[9px] font-medium px-1.5 py-0.5 rounded bg-[#292929] text-[#A5A39D]"
                        >
                          {ing}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="text-[#A5A39D] group-hover:text-[#F4D779] transition-colors pl-1">
                    <ChevronRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 2: Custom Fridge Scavenger */}
      {activeTab === 'scavenger' && (
        <div className="space-y-4 animate-in fade-in duration-200">
          {/* Active Pan Tray */}
          <div className="bg-[#202020] p-3.5 rounded-2xl border border-white/[0.07]">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-[#F5F2EB] flex items-center gap-1.5">
                <span>🍳 In Your Pan</span>
                <span className="text-[11px] font-mono text-[#F4D779]">
                  ({selectedIngredients.length} items)
                </span>
              </span>
              {selectedIngredients.length > 0 && (
                <button
                  type="button"
                  onClick={onClearIngredients}
                  className="text-[10px] text-[#A5A39D] hover:text-red-400 flex items-center gap-1 transition-colors cursor-pointer"
                >
                  <Trash2 className="w-3 h-3" />
                  <span>Clear</span>
                </button>
              )}
            </div>

            {selectedIngredients.length === 0 ? (
              <div className="py-3 text-center text-xs text-[#A5A39D]/60 italic">
                Pan is empty. Tap ingredients below or type what's in your fridge.
              </div>
            ) : (
              <div className="flex flex-wrap gap-1.5">
                {selectedIngredients.map((ing) => (
                  <span
                    key={ing}
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-[#292929] text-[#F5F2EB] border border-[#F4D779]/30 text-xs font-medium"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-[#F4D779]" />
                    <span>{ing}</span>
                    <button
                      type="button"
                      onClick={() => onRemoveIngredient(ing)}
                      className="text-[#A5A39D] hover:text-[#F5F2EB] p-0.5 rounded-full hover:bg-white/[0.1] transition-colors cursor-pointer"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Quick Custom Input Bar */}
          <form onSubmit={handleAddCustom} className="flex gap-2">
            <input
              type="text"
              value={customInput}
              onChange={(e) => setCustomInput(e.target.value)}
              placeholder="Add item (e.g. leftover kimchi, feta)..."
              className="flex-1 px-3.5 py-2 rounded-xl border border-white/[0.1] bg-[#202020] text-xs text-[#F5F2EB] placeholder:text-[#A5A39D]/40 focus:outline-none focus:border-[#F4D779]/60"
            />
            <button
              type="submit"
              className="px-3.5 py-2 rounded-xl bg-[#292929] hover:bg-[#333] text-[#F5F2EB] text-xs font-semibold flex items-center gap-1 cursor-pointer border border-white/[0.08]"
            >
              <Plus className="w-3.5 h-3.5 text-[#F4D779]" />
              <span>Add</span>
            </button>
          </form>

          {/* Category Filter Pills */}
          <div>
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 mb-2.5 scrollbar-none">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-medium whitespace-nowrap transition-all cursor-pointer ${
                    selectedCategory === cat.id
                      ? 'bg-[#F4D779] text-[#181818] font-bold'
                      : 'bg-[#202020] text-[#A5A39D] hover:text-[#F5F2EB]'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>

            {/* Scavenged Staples Grid */}
            <div className="flex flex-wrap gap-1.5 max-h-44 overflow-y-auto pr-1">
              {filteredCatalog.map((item) => {
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
                    className={`px-2.5 py-1 rounded-xl text-xs font-medium border transition-all cursor-pointer flex items-center gap-1 ${
                      isSelected
                        ? 'bg-[#F4D779] text-[#181818] border-[#F4D779] font-bold shadow-xs'
                        : 'bg-[#202020] hover:bg-[#292929] text-[#A5A39D] hover:text-[#F5F2EB] border-white/[0.06]'
                    }`}
                  >
                    {isSelected && <Check className="w-3 h-3 stroke-[3]" />}
                    <span>{item}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* The Sloth Contract (Integrated Effort Bounds) */}
      <div className="border-t border-white/[0.07] pt-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-[#A5A39D] flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-[#F4D779]" />
            <span>The Sloth Contract</span>
          </span>
          <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
            Strict 1-Pan Bound
          </span>
        </div>

        {/* Time and Vessel controls */}
        <div className="grid grid-cols-2 gap-2.5 mb-2.5">
          {/* Active Time */}
          <div className="bg-[#202020] p-2.5 rounded-xl border border-white/[0.06]">
            <div className="flex items-center justify-between text-[11px] text-[#A5A39D] mb-1.5">
              <span>Max Time</span>
              <span className="font-mono font-bold text-[#F5F2EB]">
                {contract.maxActiveMinutes}m
              </span>
            </div>
            <div className="flex gap-1">
              {[3, 5, 8].map((mins) => (
                <button
                  key={mins}
                  type="button"
                  onClick={() => updateContract({ maxActiveMinutes: mins })}
                  className={`flex-1 py-1 text-[11px] font-semibold rounded-lg transition-all cursor-pointer ${
                    contract.maxActiveMinutes === mins
                      ? 'bg-[#F4D779] text-[#181818]'
                      : 'bg-[#292929] text-[#A5A39D] hover:text-[#F5F2EB]'
                  }`}
                >
                  {mins}m
                </button>
              ))}
            </div>
          </div>

          {/* Preferred Vessel */}
          <div className="bg-[#202020] p-2.5 rounded-xl border border-white/[0.06]">
            <div className="flex items-center justify-between text-[11px] text-[#A5A39D] mb-1.5">
              <span>Vessel Cap</span>
              <span className="text-[10px] font-mono text-emerald-400">1 Item</span>
            </div>
            <div className="flex gap-1">
              {VESSEL_OPTIONS.map((v) => (
                <button
                  key={v.full}
                  type="button"
                  onClick={() => onVesselChange(v.full)}
                  className={`flex-1 py-1 text-[11px] font-semibold rounded-lg transition-all flex items-center justify-center gap-1 cursor-pointer ${
                    vesselPreference === v.full
                      ? 'bg-[#F4D779] text-[#181818]'
                      : 'bg-[#292929] text-[#A5A39D] hover:text-[#F5F2EB]'
                  }`}
                  title={v.full}
                >
                  <span>{v.icon}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Switches */}
        <div className="grid grid-cols-2 gap-2">
          {/* Microwave Only */}
          <div
            onClick={() => updateContract({ microwaveOnly: !contract.microwaveOnly })}
            className="bg-[#202020] p-2.5 rounded-xl border border-white/[0.06] flex items-center justify-between cursor-pointer hover:border-white/[0.12] transition-all select-none"
          >
            <span className="text-[11px] text-[#F5F2EB] flex items-center gap-1.5">
              <Zap className="w-3 h-3 text-[#F4D779]" />
              <span>Microwave Only</span>
            </span>
            <div
              className={`w-7 h-4 rounded-full transition-colors flex items-center p-0.5 ${
                contract.microwaveOnly ? 'bg-[#F4D779]' : 'bg-[#333]'
              }`}
            >
              <div
                className={`w-3 h-3 rounded-full bg-[#181818] shadow transition-transform ${
                  contract.microwaveOnly ? 'translate-x-3' : 'translate-x-0'
                }`}
              />
            </div>
          </div>

          {/* Zero-Knife Prep */}
          <div
            onClick={() => updateContract({ minimalChopping: !contract.minimalChopping })}
            className="bg-[#202020] p-2.5 rounded-xl border border-white/[0.06] flex items-center justify-between cursor-pointer hover:border-white/[0.12] transition-all select-none"
          >
            <span className="text-[11px] text-[#F5F2EB] flex items-center gap-1.5">
              <Scissors className="w-3 h-3 text-[#F4D779]" />
              <span>Zero-Knife Prep</span>
            </span>
            <div
              className={`w-7 h-4 rounded-full transition-colors flex items-center p-0.5 ${
                contract.minimalChopping ? 'bg-[#F4D779]' : 'bg-[#333]'
              }`}
            >
              <div
                className={`w-3 h-3 rounded-full bg-[#181818] shadow transition-transform ${
                  contract.minimalChopping ? 'translate-x-3' : 'translate-x-0'
                }`}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Primary Action Button */}
      <div className="pt-2">
        <button
          type="button"
          onClick={onGenerate}
          disabled={selectedIngredients.length === 0 || isLoading}
          className={`w-full py-3.5 px-6 rounded-2xl font-display font-bold text-sm flex items-center justify-center gap-2.5 transition-all shadow-xl cursor-pointer ${
            selectedIngredients.length === 0 || isLoading
              ? 'bg-[#292929] text-[#A5A39D]/40 border border-white/[0.05] cursor-not-allowed shadow-none'
              : 'bg-[#F4D779] hover:bg-[#E8CA6B] text-[#181818] shadow-[#F4D779]/15 active:scale-98'
          }`}
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-[#181818]/30 border-t-[#181818] rounded-full animate-spin" />
              <span>TabPFN-3.5 Evaluating Flavor Synergy...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 text-[#181818]" />
              <span>Synthesize Sloth Meal (1 Pan)</span>
            </>
          )}
        </button>

        <div className="flex items-center justify-between mt-2.5 px-1 text-[11px] text-[#A5A39D]">
          <span>{selectedIngredients.length} ingredients queued</span>
          <span className="text-[#F4D779] font-medium">
            TabPFN in-context Bayesian model ready
          </span>
        </div>
      </div>
    </div>
  );
};
