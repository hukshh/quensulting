# RetellAI Edge Cases & Recovery Prompts

This document lists specific edge-case scenarios occurring during patient calls, detailing Clara's recovery responses and routing rules.

---

## 1. Speech Mismatch & Spelling Verification
- **Scenario**: The caller has a unique name or accent, and the transcriber gets it wrong.
- **Recovery Prompt**:
  > "I want to make sure I spell that correctly. Could you please spell your name out for me?"
- **Action**: Update `caller_name` using letter-by-letter spelling extraction rules.

---

## 2. Telephony Background Static or Traffic Noise
- **Scenario**: The caller is driving or in a noisy public space, causing garbled transcripts.
- **Recovery Prompt**:
  > "I'm sorry, I'm hearing a bit of background noise and want to make sure I get your details right. Could you please repeat that?"
- **Action**: Clara prompts once more. If transcript confidence remains below `0.40`, trigger `node_human_transfer`.

---

## 3. Requesting a Sunday Appointment
- **Scenario**: Patient requests a booking on a Sunday.
- **Recovery Prompt**:
  > "We are closed on Sundays to rest our staff, but we are open Monday through Saturday from 9 AM to 6 PM. What other day would you prefer?"
- **Action**: Return to date input phase.

---

## 4. Date Requested is in the Past
- **Scenario**: Caller requests "yesterday" or a date that has already passed.
- **Recovery Prompt**:
  > "It looks like that date has already passed. Could we choose a future date instead?"
- **Action**: Return to date input phase.

---

## 5. Unrecognized Dental Treatment Category
- **Scenario**: User asks for an unsupported service (e.g. "implants" or "veneers").
- **Recovery Prompt**:
  > "We don't schedule cosmetic implants through this automated line, but I can book you for cleanings, root canals, whitening, braces consults, extractions, or checkups. Which of those sounds like what you need?"
- **Action**: If they insist on a service outside this list, transfer to a human.

---

## 6. Middle-of-Sentence Call Disconnection (Hang-ups)
- **Scenario**: Call drops mid-booking before confirmation.
- **Action**: RetellAI triggers the post-call Webhook indicating `"call_status": "disconnected"`. FastAPI should log the partial parameters, but does NOT save to Google Sheets or send emails to avoid incomplete records.
