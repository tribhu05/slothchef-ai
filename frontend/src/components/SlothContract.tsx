import React from 'react';
import { SlothContractState } from '../types';
import { ShieldCheck, Clock, Flame, Utensils, Zap, Scissors } from 'lucide-react';

interface SlothContractProps {
  contract: SlothContractState;
  onChange: (contract: SlothContractState) => void;
  vesselPreference: string;
  onVesselChange: (vessel: string) => void;
}

export const SlothContract: React.FC<SlothContractProps> = ({
  contract,
  onChange,
  vesselPreference,
  onVesselChange,
}) => {
  const updateContract = (updates: Partial<SlothContractState>) => {
    onChange({ ...contract, ...updates });
  };

  return (
    <div className="bg-[#181818] rounded-3xl p-5 border border-white/[0.07] shadow-lg mb-6">
      <div className="flex items-center justify-between gap-2 mb-4 pb-3 border-b border-white/[0.06]">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-[#F4D779]" />
          <h2 className="font-display font-semibold text-sm tracking-wide text-[#F5F2EB] uppercase">
            The Sloth Contract
          </h2>
        </div>
        <span className="text-[11px] font-mono text-[#A5A39D]">
          Radical Effort Bounds
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {/* Active Time Limit */}
        <div className="bg-[#202020] p-3.5 rounded-2xl border border-white/[0.06] flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-[#A5A39D] mb-2">
            <span className="flex items-center gap-1.5 font-medium">
              <Clock className="w-3.5 h-3.5 text-[#F4D779]" />
              <span>Max Active Time</span>
            </span>
            <span className="font-mono font-bold text-[#F5F2EB]">
              {contract.maxActiveMinutes} mins
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            {[3, 5, 8].map((mins) => (
              <button
                key={mins}
                type="button"
                onClick={() => updateContract({ maxActiveMinutes: mins })}
                className={`flex-1 py-1.5 text-xs font-medium rounded-xl transition-all cursor-pointer ${
                  contract.maxActiveMinutes === mins
                    ? 'bg-[#F4D779] text-[#181818] font-bold shadow-xs'
                    : 'bg-[#292929] hover:bg-[#333] text-[#A5A39D] hover:text-[#F5F2EB]'
                }`}
              >
                {mins}m
              </button>
            ))}
          </div>
        </div>

        {/* Cookware & Utensil Vessel */}
        <div className="bg-[#202020] p-3.5 rounded-2xl border border-white/[0.06] flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-[#A5A39D] mb-2">
            <span className="flex items-center gap-1.5 font-medium">
              <Utensils className="w-3.5 h-3.5 text-[#F4D779]" />
              <span>Preferred Vessel</span>
            </span>
            <span className="text-[11px] font-mono text-[#A5A39D]">1 Vessel</span>
          </div>
          <div className="flex items-center gap-1.5">
            {["One Skillet", "Single Pot", "Microwave Bowl"].map((v) => (
              <button
                key={v}
                type="button"
                onClick={() => onVesselChange(v)}
                className={`flex-1 py-1.5 text-[11px] font-medium rounded-xl transition-all truncate px-1 cursor-pointer ${
                  vesselPreference === v
                    ? 'bg-[#F4D779] text-[#181818] font-bold shadow-xs'
                    : 'bg-[#292929] hover:bg-[#333] text-[#A5A39D] hover:text-[#F5F2EB]'
                }`}
                title={v}
              >
                {v.replace("One ", "").replace("Single ", "").replace(" Safe", "")}
              </button>
            ))}
          </div>
        </div>

        {/* Toggles: Microwave-Only & Minimal Chopping */}
        <div className="bg-[#202020] p-3.5 rounded-2xl border border-white/[0.06] flex flex-col justify-around gap-2 sm:col-span-2 lg:col-span-1">
          {/* Microwave Only Mode */}
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="text-xs text-[#A5A39D] group-hover:text-[#F5F2EB] flex items-center gap-1.5 transition-colors">
              <Zap className="w-3.5 h-3.5 text-[#F4D779]" />
              <span>Microwave Only</span>
            </span>
            <input
              type="checkbox"
              checked={contract.microwaveOnly}
              onChange={(e) => updateContract({ microwaveOnly: e.target.checked })}
              className="accent-[#F4D779] w-4 h-4 rounded cursor-pointer"
            />
          </label>

          {/* Minimal Chopping Mode */}
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="text-xs text-[#A5A39D] group-hover:text-[#F5F2EB] flex items-center gap-1.5 transition-colors">
              <Scissors className="w-3.5 h-3.5 text-[#F4D779]" />
              <span>Zero-Knife Prep</span>
            </span>
            <input
              type="checkbox"
              checked={contract.minimalChopping}
              onChange={(e) => updateContract({ minimalChopping: e.target.checked })}
              className="accent-[#F4D779] w-4 h-4 rounded cursor-pointer"
            />
          </label>
        </div>
      </div>
    </div>
  );
};
