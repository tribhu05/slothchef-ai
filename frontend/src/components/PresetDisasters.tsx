import React from 'react';
import { PresetDisaster } from '../types';
import { Flame, Clock, Sparkles } from 'lucide-react';

interface PresetDisastersProps {
  presets: PresetDisaster[];
  selectedId: string | null;
  onSelect: (preset: PresetDisaster) => void;
  isLoading: boolean;
}

export const PresetDisasters: React.FC<PresetDisastersProps> = ({
  presets,
  selectedId,
  onSelect,
  isLoading
}) => {
  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-amber-600" />
          <h2 className="text-sm font-bold uppercase tracking-wider text-amber-900/80 font-display">
            The Desperation Menu (1-Click Judge Presets)
          </h2>
        </div>
        <span className="text-xs text-amber-700/70 italic hidden sm:inline">
          Click any preset to instantly test TabPFN + Gemma
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
        {presets.map((preset) => {
          const isSelected = selectedId === preset.id;
          return (
            <button
              key={preset.id}
              onClick={() => onSelect(preset)}
              disabled={isLoading}
              className={`text-left p-3 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'bg-amber-100 border-amber-500 shadow-sm ring-2 ring-amber-400/40'
                  : 'bg-white/80 hover:bg-white border-amber-200/80 hover:border-amber-300 hover:shadow-xs'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-1">
                  <div className="flex items-center gap-1.5 font-bold text-sm text-stone-800">
                    <span className="text-base">{preset.emoji}</span>
                    <span>{preset.title}</span>
                  </div>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-100/80 text-amber-800 border border-amber-200">
                    {preset.target_time}
                  </span>
                </div>
                <p className="text-xs text-stone-600 line-clamp-2 mb-2 leading-relaxed">
                  {preset.description}
                </p>
              </div>

              <div className="flex flex-wrap gap-1 mt-auto pt-1 border-t border-amber-100/80">
                {preset.ingredients.map((ing, i) => (
                  <span
                    key={i}
                    className="text-[10px] font-medium px-1.5 py-0.5 rounded-md bg-stone-100 text-stone-600 border border-stone-200"
                  >
                    {ing}
                  </span>
                ))}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
