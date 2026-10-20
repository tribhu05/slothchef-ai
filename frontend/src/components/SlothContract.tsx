import React from 'react';
import { SlothContractState } from '../types';
import { ShieldCheck, Clock, Utensils, Zap, Scissors } from 'lucide-react';

interface SlothContractProps {
  contract: SlothContractState;
  onChange: (contract: SlothContractState) => void;
  vesselPreference: string;
  onVesselChange: (vessel: string) => void;
}

const VESSEL_OPTIONS = [
  { label: 'Skillet', full: 'One Skillet', icon: '🍳' },
  { label: 'Pot', full: 'Single Pot', icon: '🍲' },
  { label: 'Microwave', full: 'Microwave Bowl', icon: '⚡' },
];

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
      {/* Header */}
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

      {/* Row 1: Time & Vessel */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
        {/* Active Time Limit */}
        <div className="bg-[#202020] p-3.5 rounded-2xl border border-white/[0.06] flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-[#A5A39D] mb-2.5">
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
                className={`flex-1 py-1.5 text-xs font-semibold rounded-xl transition-all cursor-pointer ${
                  contract.maxActiveMinutes === mins
                    ? 'bg-[#F4D779] text-[#181818] shadow-xs'
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
          <div className="flex items-center justify-between text-xs text-[#A5A39D] mb-2.5">
            <span className="flex items-center gap-1.5 font-medium">
              <Utensils className="w-3.5 h-3.5 text-[#F4D779]" />
              <span>Preferred Vessel</span>
            </span>
            <span className="text-[11px] font-mono text-emerald-400">1 Vessel Cap</span>
          </div>
          <div className="flex items-center gap-1.5">
            {VESSEL_OPTIONS.map((v) => (
              <button
                key={v.full}
                type="button"
                onClick={() => onVesselChange(v.full)}
                className={`flex-1 py-1.5 text-xs font-semibold rounded-xl transition-all flex items-center justify-center gap-1 cursor-pointer ${
                  vesselPreference === v.full
                    ? 'bg-[#F4D779] text-[#181818] shadow-xs'
                    : 'bg-[#292929] hover:bg-[#333] text-[#A5A39D] hover:text-[#F5F2EB]'
                }`}
              >
                <span>{v.icon}</span>
                <span>{v.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Row 2: Premium Switches for Microwave & Zero-Knife */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {/* Microwave Only Mode Switch */}
        <div
          onClick={() => updateContract({ microwaveOnly: !contract.microwaveOnly })}
          className="bg-[#202020] p-3 rounded-2xl border border-white/[0.06] flex items-center justify-between cursor-pointer hover:border-white/[0.12] transition-all select-none"
        >
          <span className="text-xs text-[#F5F2EB] flex items-center gap-2">
            <Zap className="w-3.5 h-3.5 text-[#F4D779]" />
            <span>Microwave Only</span>
          </span>
          <button
            type="button"
            role="switch"
            aria-checked={contract.microwaveOnly}
            className={`relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
              contract.microwaveOnly ? 'bg-[#F4D779]' : 'bg-[#333]'
            }`}
          >
            <span
              className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-[#181818] shadow-md ring-0 transition duration-200 ease-in-out ${
                contract.microwaveOnly ? 'translate-x-4' : 'translate-x-0'
              }`}
            />
          </button>
        </div>

        {/* Zero-Knife Prep Switch */}
        <div
          onClick={() => updateContract({ minimalChopping: !contract.minimalChopping })}
          className="bg-[#202020] p-3 rounded-2xl border border-white/[0.06] flex items-center justify-between cursor-pointer hover:border-white/[0.12] transition-all select-none"
        >
          <span className="text-xs text-[#F5F2EB] flex items-center gap-2">
            <Scissors className="w-3.5 h-3.5 text-[#F4D779]" />
            <span>Zero-Knife Prep</span>
          </span>
          <button
            type="button"
            role="switch"
            aria-checked={contract.minimalChopping}
            className={`relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
              contract.minimalChopping ? 'bg-[#F4D779]' : 'bg-[#333]'
            }`}
          >
            <span
              className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-[#181818] shadow-md ring-0 transition duration-200 ease-in-out ${
                contract.minimalChopping ? 'translate-x-4' : 'translate-x-0'
              }`}
            />
          </button>
        </div>
      </div>
    </div>
  );
};
