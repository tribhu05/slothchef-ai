import React from 'react';
import { PresetDisaster } from '../types';
import { Sparkles, Clock, ArrowRight } from 'lucide-react';

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
  // Focus primarily on the 3 core featured presets as requested in prompt, plus secondary presets
  return (
    <div className="mb-7">
      <div className="flex items-center justify-between mb-3.5 px-1">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-[#F4D779]" />
          <h2 className="text-xs font-bold uppercase tracking-wider text-[#A5A39D] font-display">
            Fridge Disasters (Curated Presets)
          </h2>
        </div>
        <span className="text-xs text-[#A5A39D]/70 hidden sm:inline">
          1-Click test with TabPFN + Gemma
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {presets.slice(0, 3).map((preset) => {
          const isSelected = selectedId === preset.id;
          return (
            <button
              key={preset.id}
              onClick={() => onSelect(preset)}
              disabled={isLoading}
              className={`group text-left rounded-3xl overflow-hidden border transition-all duration-200 cursor-pointer flex flex-col justify-between relative ${
                isSelected
                  ? 'bg-[#202020] border-[#F4D779] shadow-lg shadow-[#F4D779]/5 ring-1 ring-[#F4D779]/40'
                  : 'bg-[#181818] hover:bg-[#202020] border-white/[0.08] hover:border-white/[0.15]'
              }`}
            >
              {/* Preset Food Imagery Header */}
              <div className="h-32 w-full relative overflow-hidden bg-[#242424]">
                <img
                  src={preset.image_url || "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80"}
                  alt={preset.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105 filter brightness-90"
                  onError={(e) => {
                    e.currentTarget.src = "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80";
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#181818] via-[#181818]/40 to-transparent" />
                
                {/* Time Badge */}
                <div className="absolute top-3 right-3 flex items-center gap-1 px-2.5 py-1 rounded-full bg-[#181818]/85 backdrop-blur-md border border-white/[0.1] text-[11px] font-mono text-[#F4D779]">
                  <Clock className="w-3 h-3 text-[#F4D779]" />
                  <span>{preset.target_time}</span>
                </div>

                {/* Emoji badge */}
                <div className="absolute bottom-2 left-4 text-2xl">
                  {preset.emoji}
                </div>
              </div>

              {/* Content Body */}
              <div className="p-4 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="font-display font-bold text-base text-[#F5F2EB] group-hover:text-[#F4D779] transition-colors mb-1">
                    {preset.title}
                  </h3>
                  <p className="text-xs text-[#A5A39D] leading-relaxed line-clamp-2 mb-3">
                    {preset.description}
                  </p>
                </div>

                <div>
                  {/* Ingredients Preview */}
                  <div className="flex flex-wrap gap-1.5 pt-2 border-t border-white/[0.06]">
                    {preset.ingredients.map((ing, i) => (
                      <span
                        key={i}
                        className="text-[10px] font-medium px-2 py-0.5 rounded-lg bg-[#292929] text-[#A5A39D] border border-white/[0.05]"
                      >
                        {ing}
                      </span>
                    ))}
                  </div>

                  {/* Select CTA */}
                  <div className="mt-3 flex items-center justify-between text-[11px] font-semibold text-[#F4D779] pt-1">
                    <span>Cook This Disaster</span>
                    <ArrowRight className="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
