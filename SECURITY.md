# Security and limits

- No payments, escrow, tokens, secrets, backend signing keys or deposits. Never enter a private key into the application.
- The contract authenticates issuer and organizer **accounts**, not government agencies, document issuers, signatures on PDFs, event safety or factual accuracy of submitted statements. Independent external issuer verification is required.
- Documents are bounded to 14,000 UTF-8 bytes each and hash/byte verified. Duplicate JSON keys, invalid identifiers, extra fields, booleans masquerading as integers and oversized inputs are rejected. Up to eight restrictions are allowed.
- Permit and plan records cannot be overwritten. Conditions, source text, organizer and scope are locked. Existing plan submissions cannot add evidence during a challenge: corrections require a new record.
- Prompts treat every document, URL, rule and challenge as untrusted data. Models independently interpret evidence; an additional audit checks quotation relevance and exceptions. Prompt injection and model error remain risks, not solved problems.
- No supplied URL is retrieved, preventing user-controlled URL fetching/SSRF. Provenance URLs are not authenticity proof. No automatic live permit revocation registry is queried; the registered issuer must revoke on-chain.
- Party roles limit assessment, challenge and revocation. Revocation cannot be undone. Both issuer and organizer may be the same address in a synthetic demo; a real pilot should use distinct accounts and verify their identities externally.
- At most three assessments per plan; a challenge must precede reassessment; transactions after event start are rejected for assessment and challenge. A terminal third assessment can retain unresolved issues requiring external official review.
- Effective status overrides historical receipts after challenge/revocation/start. On-chain clocks are used for this, not the browser clock.
- Audit events include chain ID, contract address, actor, time, sequence, previous hash, payload and event hash. SHA-256 uses canonical ASCII-escaped JSON with sorted keys and compact separators. This detects alterations to an exported chain; independent chain reads are needed to detect a forged complete export.
- Frontend renders user content with `textContent`, never HTML. It rechecks wallet network before sending, clears account state on wallet/network changes, distinguishes failed FINALIZED receipts from successful ones, and never retries writes automatically.
- Receipt tracking is bounded. Pending transaction hashes are kept in browser localStorage for recovery. No account or wallet key is saved. RPC requests for a real signer require its signature; a typed address is never treated as connected.
- Public test-network text is permanent and visible. Do not submit private documents, personal information or commercial secrets. The deployed walkthrough is synthetic.
- Availability, gas, simulator outages, LLM availability and network consensus are outside the app's control. Unit test mocks are not evidence of successful live AI execution.

Report defects through repository issues without including private documents or wallet secrets.
