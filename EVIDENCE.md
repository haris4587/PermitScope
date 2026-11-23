# Verification evidence

Verified on 23 November 2026. The fixtures are synthetic and do not represent a government-issued permit.

- Contract: [0xe78dC7a94f12575D7D2f1Dd7C8e3760C77a6cfbA](https://explorer-studio.genlayer.com/address/0xe78dC7a94f12575D7D2f1Dd7C8e3760C77a6cfbA)
- Deployed source SHA-256: `f9129ca10aafe34d8a34bbb46bfe3ead045863974c6b7a5cbe77ec50efe011f9`.
- Deployment finalized with SUCCESS, MAJORITY_AGREE and `leader_only=false`.
- The corrected permit is DEMO-PERMIT-002, the plan is DEMO-PLAN-001. Both independent assessments finalized COMPLIANT with grounded permit and plan quotations. Between them, the challenge produced OFFICIAL_REVIEW_REQUIRED; reassessment cleared the challenge.
- 44 direct-VM contract tests pass, including independent validator acceptance/rejection, malformed model output, document hash/UTF-8 bytes, timing, access control, immutability, challenge limits, effective revocation and receipt-chain integrity.
- 10 frontend transaction/provider tests pass. Pending/accepted are not success; FINALIZED with execution ERROR is not success; wallet rejection, missing accounts, chain switching and chain addition are covered.
- GenVM lint and semantic/schema validation pass: 11 methods (6 views, 5 writes). The official runner header is pinned to v0.2.16.
- Desktop browser QA exercised real finalized plan reads, absent-wallet feedback, Studio preparation, permit form population, document hashing and transaction review/download, and display of a real finalized rejected call as ERROR. The public dashboard also tracked the successful reassessment as FINALIZED / SUCCESS and refreshed the current COMPLIANT state. A MetaMask extension is not installed in this automation browser; no real MetaMask signature is claimed.
- Responsive breakpoints are implemented; mobile device QA was not performed.

Machine-verifiable live actions are recorded in `evidence/deployment.json`. Run `npm run verify:live` and `python scripts/verify-chain.py` to fetch current state, compare exact deployed source bytes, verify full-consensus successful execution, and verify every event's hash linkage against the live head. `evidence/verified-live.json`, `records-live.json` and `events-live.json` contain the exported results. Individual transaction files are reduced to public verification fields, not complete RPC debug logs.

## Rejected setup transactions

The first synthetic permit accidentally designated an address with `...d52e...` instead of the Studio sender's actual `...d52f...`. The contract rejected the unauthorized plan submission and subsequent calls referencing its missing plan. These are retained as rejected setup evidence, never counted as successful lifecycle actions. Because records are immutable, a corrected permit was registered under a new ID. The old permit is not used by the active demonstration plan.

## Hosting

ChatGPT Sites is configured for public access at the user's request. The public website was published successfully and opened in the browser with live finalized data. No Vercel deployment or public social post is made. See SUBMISSION.md for reviewer instructions and accurate trust limitations.

## Finalized live walkthrough

All eight calls below have SUCCESS execution, MAJORITY_AGREE and `leader_only=false`. The event chain contains seven entries and every SHA-256 link matches the live head. The three rejected setup calls are listed separately in `evidence/rejected-live.json`.

| Action | Transaction |
|---|---|
| deploy | [0x31a728db…](https://explorer-studio.genlayer.com/transactions/0x31a728db56dba503e8c9ac05fe2022fa826ade60e9d7b3cfbb0cd2bafe0c38f9) |
| register permit | [0xdc837496…](https://explorer-studio.genlayer.com/transactions/0xdc837496d51f8a41839ed155ca249a40d6a15deb7c1247aeec5860af16c07112) |
| register corrected permit | [0xc3a3e127…](https://explorer-studio.genlayer.com/transactions/0xc3a3e1279533d10774210f7e334ad0fea6a75bf0d8c55da6053e41320c7e1f61) |
| submit corrected plan | [0xd8805b2f…](https://explorer-studio.genlayer.com/transactions/0xd8805b2f095e4290ee734d50306db1be812f8d0028107ac40f027aa884ccd435) |
| assess corrected plan | [0x01178645…](https://explorer-studio.genlayer.com/transactions/0x011786457938cc53b6e1edf87e7f2433d1e7571e125b8df8203401adb2abb40b) |
| challenge | [0x0b8bbdae…](https://explorer-studio.genlayer.com/transactions/0x0b8bbdae0bfc493839fab3b78cf8d2b79e95b140aa06203618d1f9b550ea2d76) |
| reassess | [0xf38730eb…](https://explorer-studio.genlayer.com/transactions/0xf38730eb360dda3a8cc53144711f44b90d91c9b26b08f643eb9d76e8d7ee56ce) |
| revoke unused permit | [0xbd2d1581…](https://explorer-studio.genlayer.com/transactions/0xbd2d158179df9de5f98b0f6dc6077e8d9e460aeeeb2d0939a55503f4df6584b1) |

Revocation withdrew the unused setup permit DEMO-PERMIT-001. It did not revoke the active DEMO-PERMIT-002. Linked-plan revocation overrides are additionally covered in direct-VM tests.
