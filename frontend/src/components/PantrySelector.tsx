import React, { useState } from 'react';
import { Plus, X, Sparkles, Check, Search, Tag } from 'lucide-react';

interface PantrySelectorProps {
  catalog: string[];
  selectedIngredients: string[];
  onAddIngredient: (name: string) => void;
  onRemoveIngredient: (name: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
}

export const PantrySelector: React.FC<PantrySelectorProps> = ({
  catalog,
  selectedIngredients,
  onAddIngredient,
  onRemoveIngredient,
  onGenerate,
  isLoading
}) => {
  const [customInput, setCustomInput] = useState('');
  const [filterQuery, setFilterQuery] = useState('');

  const handleAddCustom = (e: React.FormEvent) => {
    e.preventDefault();
    if (customInput.trim()) {
      onAddIngredient(customInput.trim());
      setCustomInput('');
    }
  };

  const filteredCatalog = catalog.filter((item) =>
    item.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div className="bg-[#181818] rounded-3xl p-5 sm:p-6 border border-white/[0.07] shadow-xl mb-7">
      <div className="mb-4">
        <h2 className="font-display font-bold text-lg text-[#F5F2EB] flex items-center gap-2">
          <span>What sad items are in your fridge right now?</span>
        </h2>
        <p className="text-xs text-[#A5A39D] mt-0.5">
          Type whatever random ingredients you have left or pick from common staples below.
        </p>
      </div>

      {/* Selected Ingredients Tag Cloud */}
      <div className="min-h-[58px] p-3 rounded-2xl bg-[#202020] border border-white/[0.07] flex flex-wrap items-center gap-2 mb-4">
        {selectedIngredients.length === 0 ? (
          <div className="text-xs text-[#A5A39D]/60 italic flex items-center gap-1.5 px-2">
            <Tag className="w-3.5 h-3.5" />
            <span>No ingredients selected yet. Add 2–4 items to begin...</span>
          </div>
        ) : (
          selectedIngredients.map((ing) => (
            <span
              key={ing}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#292929] text-[#F5F2EB] border border-white/[0.1] text-xs font-medium hover:border-[#F4D779]/40 transition-colors animate-in fade-in zoom-in duration-150"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-[#F4D779]" />
              <span>{ing}</span>
              <button
                type="button"
                onClick={() => onRemoveIngredient(ing)}
                className="hover:bg-white/[0.1] text-[#A5A39D] hover:text-[#F5F2EB] rounded-full p-0.5 transition-colors cursor-pointer"
                title={`Remove ${ing}`}
              >
                <X className="w-3 h-3" />
              </button>
            </span>
          ))
        )}
      </div>

      {/* Custom Input Bar */}
      <form onSubmit={handleAddCustom} className="flex gap-2.5 mb-5">
        <div className="relative flex-1">
          <input
            type="text"
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            placeholder="Type ingredient (e.g. half a zucchini, leftover curry paste, feta)..."
            className="w-full px-4 py-2.5 rounded-2xl border border-white/[0.1] bg-[#202020] text-sm text-[#F5F2EB] placeholder:text-[#A5A39D]/50 focus:outline-none focus:border-[#F4D779]/60 focus:ring-1 focus:ring-[#F4D779]/40 transition-all"
          />
        </div>
        <button
          type="submit"
          className="px-5 py-2.5 rounded-2xl bg-[#292929] hover:bg-[#333] text-[#F5F2EB] border border-white/[0.08] text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4 text-[#F4D779]" />
          <span>Add</span>
        </button>
      </form>

      {/* Quick Select Staples */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2.5">
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#A5A39D] block">
            Common Scavenged Staples
          </span>
          <div className="relative w-36 sm:w-48">
            <input
              type="text"
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              placeholder="Filter staples..."
              className="w-full px-2.5 py-1 text-[11px] rounded-lg bg-[#202020] border border-white/[0.08] text-[#F5F2EB] placeholder:text-[#A5A39D]/40 focus:outline-none focus:border-[#F4D779]/50"
            />
          </div>
        </div>

        <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto pr-1">
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
                className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-[#F4D779] text-[#181818] border-[#F4D779] font-bold shadow-xs'
                    : 'bg-[#202020] hover:bg-[#292929] text-[#A5A39D] hover:text-[#F5F2EB] border-white/[0.06]'
                }`}
              >
                {isSelected && <Check className="w-3 h-3 inline mr-1 stroke-[3]" />}
                {item}
              </button>
            );
          })}
        </div>
      </div>

      {/* Primary Action Button */}
      <div className="flex items-center justify-between pt-4 border-t border-white/[0.07]">
        <div className="text-xs text-[#A5A39D]">
          <span className="font-semibold text-[#F5F2EB]">{selectedIngredients.length}</span> items queued for TabPFN pairing
        </div>

        <button
          type="button"
          onClick={onGenerate}
          disabled={selectedIngredients.length === 0 || isLoading}
          className={`px-7 py-3 rounded-2xl font-display font-bold text-sm flex items-center gap-2.5 transition-all shadow-md cursor-pointer ${
            selectedIngredients.length === 0 || isLoading
              ? 'bg-[#292929] text-[#A5A39D]/40 border border-white/[0.05] cursor-not-allowed shadow-none'
              : 'bg-[#F4D779] hover:bg-[#E8CA6B] text-[#181818] shadow-[#F4D779]/10 active:scale-98'
          }`}
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-[#181818]/30 border-t-[#181818] rounded-full animate-spin" />
              <span>Prior Labs TabPFN-3.5 + Gemma 2 Thinking...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 text-[#181818]" />
              <span>Synthesize Sloth Recipe</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
