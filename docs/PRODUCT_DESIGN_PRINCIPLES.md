# Product Design Principles — InfoClar model applications

These are product-design preferences for the suite. They govern how validated scientific results are exposed to users; they do **not** authorize changing scientific results, validation gates, model equations, scenario values or evidence status.

## Canonical priority

**User usefulness > internal model structure.**

**Information a user can learn > software metadata.**

**Model results > registries, contracts and gate codes.**

**Clear explanations > implementation jargon.**

**Progressive disclosure > information crowding.**

**Model-specific product design > rigid layout templates.**

The frontend should always be audited by asking: **“What can a user learn now?”**

## Information order

The preferred information hierarchy is:

1. **What can I learn?** — the important results, turning points, balances, mechanisms or other conclusions produced by this specific model.
2. **Why does it happen?** — the mechanisms and scenario differences needed to interpret those results.
3. **How robust, sensitive or uncertain is it?** — uncertainty must be explained in plain language, including what it does and does not mean.
4. **How does the model work?** — the full theory, variables, feedbacks, assumptions and boundaries needed for independent understanding.
5. **Methodological / technical provenance** — validation details, software internals, registries, hashes and other technical metadata, available on demand rather than dominating the normal product surface.

This hierarchy can be adapted when a model-specific use case requires it, but it must not be inverted merely because internal metadata already exists in the repository.

## Model results as product objects

An application exists to help the user learn something. Primary indicators must therefore represent important outputs of the model rather than development metadata or arbitrary convenient values.

For World3, turning-point timing is more useful than a software version or a value selected only because it is easy to calculate. For another model, the canonical result may instead be a flow, balance-sheet exposure, causal mechanism, risk concentration or another model-specific object.

The visualization should be designed around that object. A shared visual language is useful, but a fixed dashboard or 2×2 template must never override the model’s actual purpose.

## Theory is a product feature

Theory / Learn must be sufficient for a user without prior specialist knowledge to understand the model, its scenarios, mechanisms, assumptions and interpretation boundaries. Contextual explanations may accompany a selected variable, but they supplement rather than replace a coherent full manual.

Each complex control must explain:

- what it shows;
- what changes when it is enabled;
- what it does **not** mean.

Technical codes should be translated into user language on normal product surfaces. Internal identifiers remain available in scientific or technical provenance only when useful.

## Uncertainty and evidence

Uncertainty must be explained, not merely drawn. A confidence interval, sensitivity envelope, scenario spread, Monte Carlo distribution and predictive probability are different concepts and must not share labels unless their statistical interpretation genuinely matches.

Observed data, modelled historical values, scenario projections, forecasts and probabilities must remain visually and semantically distinct.

Evidence & Limits should explain provenance, vintage, fit, backtesting, validation and limitations in natural language. It is important but normally secondary to the model result the user came to understand.

## Responsive and accessible product quality

Responsive layout is a functional requirement. Normal desktop, laptop, tablet and mobile surfaces must not contain horizontal page scrolling, overlapping panels, clipped cards or off-screen tooltips. Flexible container-based grids (`auto-fit`, `minmax`, appropriate breakpoints) are preferred to fixed column counts when content width is variable.

Accessibility, keyboard interaction, EN/RO language parity where promised, and progressive disclosure are part of product correctness rather than optional polish.

## Visual inspection is a gate

Automated tests can prove contracts and detect many layout failures; they cannot prove that the product is understandable. Every significant product recovery must therefore include rendered screenshots at representative viewports and direct visual inspection.

**CI green ≠ useful product.**

A release should not be integrated until both software/scientific non-regression gates and a model-specific usefulness gate pass.

## Scientific integrity

Product design must never alter model outputs to produce a more compelling story. If a desired metric cannot be derived legitimately, the product should say **“Not yet estimated”** and explain what evidence or model capability is missing.

Scientific status belongs to the science. Product design decides how to make that status intelligible and useful without overstating it.
