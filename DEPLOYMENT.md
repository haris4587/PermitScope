# Deployment

Contract: `0xe78dC7a94f12575D7D2f1Dd7C8e3760C77a6cfbA` on Studionet (61999).
Explorer: https://explorer-studio.genlayer.com/address/0xe78dC7a94f12575D7D2f1Dd7C8e3760C77a6cfbA
RPC: https://studio.genlayer.com/api
SDK runner: pinned in the contract header, GenVM v0.2.16.

## Reproduce

1. Run `genvm-lint check contracts/permit_scope.py` and the tests.
2. Add this exact source to GenLayer Studio; select **Normal (Full Consensus)**. There are no constructor parameters.
3. Deploy with a Studio built-in account. Save its transaction hash and returned address; wait for FINALIZED, successful execution and majority agreement.
4. Update `web/deployment.js` and `evidence/deployment.json` for a new instance. Do not upgrade the reviewed instance silently.
5. Register `fixtures/permit.json` using `register_permit(permit_json: str)`. The sending account becomes issuer; use the fixture's organizer account to submit the plan.
6. Call `submit_plan(plan_json: str)`, then `assess(plan_id: str)`, `challenge(plan_id: str, reason: str)`, and `assess(plan_id: str)` again.
7. For revocation use `revoke_permit(permit_id: str, reason: str)`. Prefer a separate demonstration permit if retaining an active COMPLIANT example.
8. Export finalized receipts with `npm run verify:live`. This verifies deployed code bytes, consensus receipts and the event hash chain, rather than trusting UI status alone.

Browser wallets sign actual contract calls through `genlayer-js`. **Prepare in Studio** only downloads JSON inputs; it does not claim to connect to Studio's wallet or submit a transaction. Studio's private keys never leave Studio. `eth_sendTransaction` with a pasted address is not available on this RPC. MetaMask itself is not installed in the automation browser; mocked provider tests exercise network switch, add-chain, rejection and missing-account handling.

Website builds with `npm run build`. Hosting is ChatGPT Sites with static output in `dist/`; `.openai/hosting.json` records the Site identity. No Vercel hosting is configured.
