export interface TabPFNPrediction {
  harmony_score: number;
  confidence: number;
  effort_class: string;
  dish_count: number;
  active_standing_minutes: number;
  total_minutes: number;
  flavor_balance: Record<string, number>;
  pairing_synergies: string[];
  model_version: string;
}

export interface MissingIngredientSuggestion {
  ingredient_name: string;
  canonical_id: string;
  reason: string;
  unlocks_recipe_title: string;
  substitutes: string[];
}

export interface SlothRecipe {
  id: string;
  title: string;
  subtitle: string;
  tagline: string;
  sloth_efficiency: string;
  sloth_score?: number;
  image_url?: string;
  vessel_type: string;
  utensil: string;
  dishes_to_wash: number;
  active_standing_minutes: number;
  total_minutes: number;
  harmony_score: number;
  ingredients_used: string[];
  sloth_shortcuts: string[];
  steps: string[];
  cleanup_audit: string;
  open_weights_rationale: string;
  tabpfn_evidence: TabPFNPrediction;
  status?: "READY" | "NEEDS_INGREDIENTS" | "NO_GOOD_MATCH";
  decision_message?: string;
  missing_suggestions?: MissingIngredientSuggestion[];
  safety_warnings?: string[];
  fit_explanation?: string;
}

export interface PresetDisaster {
  id: string;
  title: string;
  emoji: string;
  description: string;
  ingredients: string[];
  vessel_preference: string;
  target_time: string;
  image_url?: string;
}

export interface SlothContractState {
  maxActiveMinutes: number;
  maxCookwareCount: number;
  maxUtensilCount: number;
  microwaveOnly: boolean;
  minimalChopping: boolean;
}
