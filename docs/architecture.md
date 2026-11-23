# Architecture

Static Vite frontend → `genlayer-js` → Studionet contract. Browser wallets sign writes; Studio built-in accounts sign inside Studio through the documented preparation workflow. Both paths return transaction hashes that can be tracked in the dashboard.

The contract stores canonical strings in TreeMaps: issuer-attested permits, immutable event plans, latest assessment pointers, bounded attempt counters, pending challenge pointers, permit revocation records, and an append-only global event chain. Latest pointers do not erase older events.

Lifecycle: register_permit → submit_plan → assess → challenge → assess. Issuer revocation overrides every linked plan at any time. Future amendments use new IDs. There is no unbounded reassessment or ability to mutate source evidence.

Deterministic fields: declared attendance/capacity, venue equality, interval containment, address roles, hashes, byte lengths, timing and retry bounds. Nondeterministic fields: documentary metadata consistency and each restriction's SATISFIED / VIOLATED / UNKNOWN classification. The leader's normalized interpretation is stored only after network consensus; intermediate validator answers are not stored or presented as a vote transcript.

Every non-UNKNOWN finding contains distinct quotes from permit and plan. Literal substring checks run in code; independent model auditing checks whether the full source context supports the proposed interpretation. Model knowledge cannot invent legal conditions or authenticate an issuing authority.

Receipts use canonical JSON (`sort_keys=True`, compact separators, ASCII escapes) and SHA-256. Receipt hash excludes only its own event_hash field. The previous hash, monotonically increasing sequence, chain ID and contract address bind ordering and deployment.
