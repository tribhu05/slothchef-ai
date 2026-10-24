# SlothChef AI — Master Video Storyboard & Shot List
### *Competition-Quality Production Storyboard for DEV Hacktoberfest 2026: Week 3 (Slow and Steady)*

* **Total Runtime**: 2 minutes 50 seconds (170.0s)
* **Resolution**: 1920×1080 (16:9 Landscape Full HD)
* **Framerate**: 30.0 fps (5,100 total frames)
* **Audio Track**: 48.0 kHz Stereo (Narrator Dialogue + Sub-bass Ambient Pad + Microwave Chime SFX)
* **Core Brand Identity**: Charcoal `#181818`, Surface `#202020`, Butter Gold `#F4D779`, Cream White `#F5F2EB`

---

## Shot-by-Shot Production Breakdown

### Scene 1 — The Midnight Crisis | 0:00 – 0:18 (18.0s / Frames 0 – 539)
* **Objective**: Establish immediate emotional resonance with exhausted developers. Hook the viewer before introducing the brand.
* **Visual Asset**: `card_scene1_hook.png`
* **Shot Composition**: 
  - Top: Dark terminal mock at 02:47 AM displaying `CrashLoopBackOff` on `api-gateway` and `cat /dev/fridge` inventory output.
  - Center/Bottom: High-contrast gold hook card with rounded corners and glowing border.
  - On-Screen Text: `"PRODUCTION IS BROKEN. DINNER SHOULDN'T BE."`
  - Badges: `[8 HOURS DEBUGGING]` (Red) • `[4 SAD INGREDIENTS]` (Gold) • `[0 COOKING ENERGY]` (Gray) • `[SOLUTION: RADICAL SLOTH HEURISTICS]` (Green)
* **Camera Movement**: Subtle slow zoom (1.0x to 1.04x) focusing into the gold headline.
* **Audio Cue**: 
  - 0:00 – 0:00.5: Low sub-bass ambient hum fade-in.
  - 0:00.5 – 0:14.8: Narration: *"Production is broken. Dinner shouldn't be. You've spent eight hours debugging, your brain is running on fumes, and your fridge has four ingredients that don't look like a meal. The last thing you need is a recipe that demands another hour of work."*
  - 0:14.8 – 0:18.0: Audio pause / breathing room. Soft synth beat drop.
* **Transition to Scene 2**: Clean straight cut with 0.3s audio crossfade.

---

### Scene 2 — Meet SlothChef | 0:18 – 0:38 (20.0s / Frames 540 – 1139)
* **Objective**: Introduce the brand philosophy, the DEV Hacktoberfest Week 3 theme ("Slow and Steady"), and the four strict bounds of the Sloth Contract.
* **Visual Assets**: 
  - 0:18 – 0:28 (10s): `card_scene2_sloth_contract.png`
  - 0:28 – 0:38 (10s): `shot_live_loaded.png` (Live UI overview)
* **Shot Composition**:
  - Part A (0:18 - 0:28): The 4 Sloth Contract Bounds displayed as editorial dark glass cards:
    1. `1 VESSEL`: Strict 1-vessel cap (skillet, pot, or microwave bowl).
    2. `O(< 5m)`: Active standing bound (maximum 5 minutes on feet).
    3. `1 UTENSIL`: Eat directly from the pan with 1 fork.
    4. `0 BOARDS`: Zero cutting boards (crush garlic with coffee mug, tear greens with bare hands).
  - Part B (0:28 - 0:38): Cut to the live web interface showing the clean UI, the Scavenger input, and vessel selectors.
* **Camera Movement**: Static high-clarity presentation with subtle card emphasis.
* **Audio Cue**:
  - 0:18.5 – 0:33.8: Narration: *"Meet SlothChef: an extreme low-effort cooking companion built for people who want dinner, not a second project. Give it what you've got. The Sloth Contract enforces strictly one cooking vessel, zero cutting boards, and under five minutes on your feet."*
  - 0:33.8 – 0:38.0: Visual pacing pause allowing viewer to inspect the live interface.
* **Transition to Scene 3**: Direct transition to live screen recording.

---

### Scene 3 — The Real Product Demo | 0:38 – 1:23 (45.0s / Frames 1140 – 2489)
* **Objective**: The central anchor of the video. Demonstrate 100% genuine live interaction on `slothchef-ai.onrender.com` from raw scavenged pantry to generated meal, Cook-Along mode, and TabPFN telemetry.
* **Visual Assets**:
  - 0:38 – 1:12 (34s): `live_demo_raw.webm` (Authentic 1080p screen recording)
  - 1:12 – 1:20 (8s): `shot_cook_along.png` (Cook-Along hands-free view)
  - 1:20 – 1:23 (3s): `shot_tabpfn_modal.png` (TabPFN Math Radar)
* **Action Breakdown**:
  1. Cursor hovers over "1-Click Disasters (6)" button and clicks.
  2. Drawer opens; user selects "Post-Deploy Desperation" (`Ramen noodles`, `Peanut butter`, `Sriracha`, `Soy sauce`).
  3. Vessel set to "One Skillet", max standing time "3 mins".
  4. Clicks "Synthesize Sloth Meal (1 Pan)".
  5. Loading state runs: TabPFN chemical analysis and Gemma synthesis.
  6. Recipe Card populates: **Midnight Dan-Dan Rescue**.
  7. Smooth scroll through "Ingredients in this Pan", radical shortcuts ("Crush garlic flat with coffee mug"), and cleanup audit ("1 Skillet, 1 Fork, 0 Prep Bowls").
  8. Cut to Cook-Along Mode: Large legible step-by-step display.
  9. Cut to TabPFN Math modal: Flavor radar displaying Umami (88%), Richness (85%), Acidity (74%), Salt (92%), and 94% overall synergy.
* **Audio Cue**:
  - 0:38.5 – 1:07.8: Narration: *"Let's test the post-deploy pantry: instant ramen, peanut butter, soy sauce, and sriracha. SlothChef turns those ingredients into a practical starting point, with no imaginary pantry and no elaborate workflow. It synthesizes the Midnight Dan-Dan Rescue: one skillet, one fork, and three minutes of active cooking. With radical shortcuts: crush garlic flat with a coffee mug, tear greens with bare hands. And Cook-Along mode reads each step aloud with an audible timer."*
  - 1:14.5 – 1:15.5: **SFX Microwave Chime Bell** (`microwave_chime.wav`) dings at 587Hz -> 880Hz to signal timer completion.
  - 1:15.5 – 1:23.0: Ambient music continues during flavor radar showcase.
* **Transition to Scene 4**: Wipe transition into technical architecture.

---

### Scene 4 — How It Works (Dual-Engine AI Architecture) | 1:23 – 1:58 (35.0s / Frames 2490 – 3539)
* **Objective**: Explain why generic LLMs fail at cooking bounds and how SlothChef decouples culinary prediction into TabPFN-3.5 and Google Gemma 2.
* **Visual Asset**: `card_scene4_architecture.png`
* **Shot Composition**:
  - Stage 1: Ingestion (React 19, 3-5 Scavenged items, Strict 1-vessel cap).
  - Stage 2: Prior Labs TabPFN-3.5 Foundation Model (Continuous In-Context Bayesian Inference, <45ms latency, Umami/Lipid/Acidity/Salt vector scoring).
  - Stage 3: Google Gemma 2 (Local Open-Weight SLM, Sloth tone, sequential steps, cleanup audit).
  - Stage 4: User Experience (React 19 SPA, Cook-Along voice, microwave chime).
* **On-Screen Text**: `"KEY TAKEAWAY: TabPFN-3.5 guarantees mathematical food chemistry before Gemma 2 writes a single word."`
* **Camera Movement**: Subtle pan across the 4 stages from left to right.
* **Audio Cue**:
  - 1:23.5 – 1:50.4: Narration: *"Behind the interface is a decoupled dual-AI pipeline. First, Prior Labs' TabPFN tabular foundation model evaluates continuous chemical flavor vectors: umami, salt, acidity, and lipids, in a single Bayesian forward pass under 45 milliseconds. It quantifies synergy before generating text. Then, Google's open-weight Gemma 2 SLM translates those exact bounds into sequential, zero-friction cooking instructions."*
  - 1:50.4 – 1:58.0: Pacing hold on the architecture diagram.
* **Transition to Scene 5**: Clean cut to cloud deployment & open innovation.

---

### Scene 5 — Open Innovation & Render Deployment | 1:58 – 2:23 (25.0s / Frames 3540 – 4289)
* **Objective**: Answer the DEV challenge prompt: *"Why does open innovation matter for what you built?"* and verify live Render infrastructure.
* **Visual Asset**: `card_scene5_deployment.png`
* **Shot Composition**:
  - Top: Deployed live on Render banner + Live URL `https://slothchef-ai.onrender.com`.
  - Three Open Innovation Pillar Cards:
    1. **Private Fridge Telemetry**: Kitchen logs reveal intimate health & lifestyle data; local open models keep telemetry on-device.
    2. **True Offline Resilience**: 100% operational in campervans, off-grid cabins, or during power/internet outages.
    3. **Zero Token Anxiety**: Runs 24/7 as an ambient kitchen assistant without monthly subscriptions or API meter panic.
  - Bottom: Render hosting verification (`render.yaml` 1-click blueprint, multi-stage Docker build, `/api/health` 200 OK monitoring).
* **Audio Cue**:
  - 1:58.5 – 2:19.5: Narration: *"SlothChef is deployed live on Render via a multi-stage Docker container with automated health monitoring. Why does open innovation matter here? Because midnight pantry habits are intensely personal. Running open-weight models locally keeps private fridge telemetry on your device. It works 100% offline with zero token anxiety and zero cloud lock-in."*
  - 2:19.5 – 2:23.0: 3.5s hold on Render deployment verification.
* **Transition to Scene 6**: Cinematic dip to dark followed by warm, appetizing food reveal.

---

### Scene 6 — The Payoff | 2:23 – 2:42 (19.0s / Frames 4290 – 4859)
* **Objective**: Reward the viewer with appetizing sensory payoff and tangible, quantitative time and dish savings.
* **Visual Asset**: `card_scene6_payoff.png`
* **Shot Composition**:
  - Right: High-resolution hero photograph of Midnight Dan-Dan Noodles (warm, savory noodles with chili oil, scallions, and crushed peanuts).
  - Left: Quantitative life metrics:
    - `+38 MIN`: Life reclaimed vs standard recipe prep.
    - `6 FEWER`: Dirty dishes and prep bowls eliminated.
    - `1 SKILLET`: Cooked and eaten straight from the pan.
    - `94% SCORE`: TabPFN mathematical flavor harmony.
  - Bottom Quote: *"Conservation of energy is the supreme evolutionary virtue."*
* **Camera Movement**: Subtle pan from left metrics to luscious noodles.
* **Audio Cue**:
  - 2:23.5 – 2:40.5: Narration: *"The result? A steaming bowl of rich, spicy Dan-Dan noodles. Thirty-eight minutes reclaimed, six fewer dishes to wash, and an edible victory when energy was at absolute zero. Because conservation of energy isn't laziness: it's the supreme evolutionary virtue."*
  - 2:40.5 – 2:42.0: Satisfying musical resolution.
* **Transition to Scene 7**: Fade into the final closing card.

---

### Scene 7 — Closing & Call to Action | 2:42 – 2:50 (8.0s / Frames 4860 – 5099)
* **Objective**: Deliver a memorable final impression with clear links to the live application and GitHub repository.
* **Visual Asset**: `card_scene7_endcard.png`
* **Shot Composition**:
  - Header: `DEV HACKTOBERFEST 2026: WEEK 3`
  - Hero Brand: `SlothChef AI`
  - Core Creative Line: `"Production is broken. Dinner shouldn't be."`
  - Action Block 1: `TRY THE LIVE APP: https://slothchef-ai.onrender.com`
  - Action Block 2: `FORK ON GITHUB: https://github.com/tribhu05/slothchef-ai`
  - Footer Badges: `[100% OPEN SOURCE (MIT)]` • `[PRIOR LABS TABPFN-3.5]` • `[GOOGLE GEMMA 2]`
* **Audio Cue**:
  - 2:42.2 – 2:49.2: Narration: *"Production is broken. Dinner shouldn't be. Try SlothChef on Render, or fork it on GitHub."*
  - 2:49.2 – 2:50.0: Ambient track gentle fade to complete silence.
* **End of Video**: Exactly 170.0 seconds (2:50).
