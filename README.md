# PermitScope

**Event permit compliance verification with immutable evidence and independent GenLayer validators.**

An organizer and a permit issuer often interpret the same event restrictions differently. PermitScope locks the exact permit and plan before assessment, checks measurable limits in code, and uses GenLayer consensus to interpret activity restrictions and exceptions. Its receipts show what evidence was assessed, which conditions were satisfied or violated, and what remains unresolved.

- Website: https://permitscope.mohamedansaf222.chatgpt.site (public; no sign-in required)
- Contract: [Studionet explorer](https://explorer-studio.genlayer.com/address/0xe78dC7a94f12575D7D2f1Dd7C8e3760C77a6cfbA)
- Network: GenLayer Studionet, chain **61999**. This is a test-network application.
- Demo plan: `DEMO-PLAN-001`. All walkthrough documents are explicitly synthetic.

## Use the app

1. Open the overview to read the finalized demonstration plan without connecting a wallet.
2. Choose **Connect account**. Use a browser wallet on Studionet, or choose **Prepare in Studio** to download exact call inputs and sign with GenLayer Studio's built-in wallet.
3. As issuer, register a permit: organizer account, venue, UTC interval, capacity, activity restrictions and exact permit text with its source reference.
4. As that organizer, submit a future event plan and exact supporting text. The app computes UTF-8 byte length and SHA-256 before submission.
5. Request an assessment. The website genuinely invokes `writeContract` for browser wallets, tracks submitted/accepted/finalized states, verifies successful execution and majority agreement, and refreshes finalized records. Studio signatures happen in Studio; paste their hash into the same receipt tracker.
6. Challenge a questionable finding before the event starts. Its effective status becomes `OFFICIAL_REVIEW_REQUIRED` until reassessed. Up to three assessments are allowed per plan. Amendments need a new immutable record.
7. The issuer can revoke a permit. Every linked plan's effective status immediately becomes `REVOKED`; earlier receipts stay accessible.

## Trust boundary and authoritative data

The permit's source is the **account that registers and attests the exact document**, with an on-chain issuer address, document hash and provenance URL. There is no built-in issuer accreditation registry: a user must confirm that this address belongs to the relevant issuing authority outside the app. Registration by an arbitrary account does not prove government approval. The demo issuer is a Studio account, not a government agency.

No live government facts are asserted. URLs are provenance references and are not fetched. Hashes bind the exact uploaded text, not an original PDF or authenticated web response. Structured capacity, dates, venue and activities are checked against both documents by validators; contradictory/missing metadata prevents a clean result. Use actual authoritative permit documents and an independently verified issuer account for a real pilot. PermitScope does not issue permits, establish legal compliance, or guarantee physical event safety.

## Consensus, not formatting

`assess` uses `gl.vm.run_nondet_unsafe` with separate leader and validator functions. Each validator reruns interpretation independently, compares integrity and every condition's status, then performs an independent contextual grounding audit of the proposed quotes. Merely matching JSON shape is insufficient. Exact quoted wording need not match between models, but proposed quotes must occur in the correct document and entail the finding in context.

Malformed/unavailable model output is normalized to UNKNOWN. Validators may reject it if their independent review disagrees. A failed or undetermined consensus transaction makes no state change; it is never a fabricated INCONCLUSIVE receipt.

## Outcomes

| Outcome | Deterministic aggregation |
|---|---|
| VIOLATION | Any capacity, date or venue breach, revocation, or critical condition violation |
| INCONCLUSIVE | Otherwise any missing/contradictory metadata or UNKNOWN condition |
| CONDITIONAL | Otherwise any noncritical condition violation |
| COMPLIANT | All checks and conditions satisfied |

`effective_status` also exposes UNASSESSED, OFFICIAL_REVIEW_REQUIRED, REVOKED and EVENT_STARTED. A historical COMPLIANT receipt must not be displayed as current after challenge, revocation or event start. There is no automatic official adjudicator integration: the challenge mechanism is a bounded second documentary review.

## Run locally

Node 22+ and Python 3.12+:

```sh
npm ci
npm run dev
npm run build
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest -q
node --test tests/transactions.test.mjs
.venv/bin/genvm-lint check contracts/permit_scope.py
npm run verify:live
```

The Python tests use GenLayer's direct VM and mocked LLM responses to test contract logic and independent validator behavior. They do not claim live consensus. Live receipt/code verification is separate. See [EVIDENCE.md](EVIDENCE.md), [SECURITY.md](SECURITY.md), [DEPLOYMENT.md](DEPLOYMENT.md), [SUBMISSION.md](SUBMISSION.md), and [architecture](docs/architecture.md).

## Continued use

The same immutable permit can support multiple separately locked plans. Recurring organizers can compare findings across plans and export audit records for authority review. A production pilot needs an authority-controlled signer, issuer identity verification, a supported production network and jurisdiction-specific document ingestion, rather than extending this test deployment's claims.
