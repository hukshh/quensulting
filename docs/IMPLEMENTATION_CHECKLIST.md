# RetellAI Flow Builder Implementation Checklist

This checklist guides the engineering implementation of Clara's conversation flow directly in the RetellAI Console interface.

---

## Step 1: Initialize Agent Configuration
- [ ] Create a new voice agent profile inside the RetellAI dashboard.
- [ ] Choose the preferred synthetic voice (e.g., standard professional warm female voice).
- [ ] Set dynamic interruption sensitivity threshold to `Medium-High` to catch user overrides without false triggering on breathing or noise.
- [ ] Configure ambient noise cancellation settings.

## Step 2: Set Up Flow Variables
- [ ] Initialize variables in the agent state catalog matching names and default values in [RETELL_VARIABLES.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/RETELL_VARIABLES.md):
  - `caller_name` (String, default: "Unknown Patient")
  - `phone_number` (String)
  - `email` (String)
  - `service` (String)
  - `appointment_date` (String)
  - `appointment_time` (String)
  - `notes` (String)
  - `retry_count` (Integer, default: 0)

## Step 3: Author Conversational Nodes
- [ ] Construct the nodes mapped in [RETELL_NODE_MAP.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/RETELL_NODE_MAP.md).
- [ ] Copy-paste prompt templates and guidelines from [RETELL_NODE_PROMPTS.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/RETELL_NODE_PROMPTS.md).

## Step 4: Configure Branching & Transitions
- [ ] Set up state transitions using Retell's visual routing:
  - Connect node outcomes to the next slot-collection step.
  - Link global fallback pathways to `node_human_transfer` if retries exceed boundaries.

## Step 5: Connect Provisional Webhook
- [ ] Link `node_webhook_trigger` API endpoint to the provisional URL:
  - URL: `https://api.brightsmiles.quensulting.ai/api/v1/appointments/book` *(Provisional path)*
  - Method: `POST`
  - Map body variables (Name, Phone, Email, Service, Date, Time, Notes).

## Step 6: Define Knowledge Base FAQ Repository
- [ ] Upload the canonical dental FAQs text defined in [FAQ_DATASET.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/FAQ_DATASET.md) into the Retell Knowledge Base settings.
- [ ] Configure the fallback lookup node to automatically reference this repository when standard intents fail to trigger.

## Step 7: Verify via Simulator
- [ ] Launch Simulator testing mode.
- [ ] Run through Test Case 1, 2, and 3 defined in [RETELL_TEST_CASES.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/RETELL_TEST_CASES.md).
- [ ] Inspect session variable updates on the dashboard debugger panel to verify slots align correctly.
