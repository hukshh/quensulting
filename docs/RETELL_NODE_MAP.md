# RetellAI Node Map

This document lists every logical node within Clara's conversational state machine, mapped directly to their configurations in the RetellAI Flow Builder.

---

## 1. node_greeting
- **Node Type**: Greeting Node
- **Purpose**: Initiate the call, welcome the caller, and classify initial intent.
- **Inputs**: Call Connection Trigger.
- **Outputs**: Greeting speech payload.
- **Variables Updated**: None.
- **Transition Conditions**:
  - Directs to `node_col_name` if booking request is detected.
  - Directs to `node_faq_lookup` if FAQ question is asked.
  - Directs to `node_human_transfer` if emergency or human requested.
- **Retry Logic**: If silence is detected for 3 seconds, Clara prompts again (up to 2 times).
- **Webhook Trigger**: None.
- **Failure Behavior**: If silent for 2 consecutive prompts, transfers to `node_human_transfer`.

---

## 2. node_faq_lookup
- **Node Type**: Knowledge Base Lookup Node
- **Purpose**: Answer general questions about hours, location, services, and fees.
- **Inputs**: User's question text.
- **Outputs**: Retrieved answer matching FAQ database.
- **Variables Updated**: `intent` ("faq"), `confidence_score`.
- **Transition Conditions**:
  - Returns to the calling node in the booking process (e.g. `node_col_email` or `node_col_date`).
  - If no booking was active, prompts: "Is there anything else I can help you with today?" and routes to `node_greeting`.
- **Retry Logic**: If Clara is unsure of the question, she asks the user to rephrase once.
- **Webhook Trigger**: None.
- **Failure Behavior**: If Clara cannot resolve the question twice, she routes to `node_human_transfer` (Complex FAQ escalation).

---

## 3. node_col_name
- **Node Type**: Slot Gathering Node (Name)
- **Purpose**: Capture the first and last name of the patient.
- **Inputs**: Natural speech containing caller name.
- **Outputs**: Voice prompt asking for name.
- **Variables Updated**: `caller_name`, `retry_count`.
- **Transition Conditions**:
  - Transitions to `node_col_phone` once a name is extracted and validated.
- **Retry Logic**: If name is not captured or empty:
  - Clara: "I'm sorry, I didn't catch that name. Can you please tell me your first and last name?" (Increment `retry_count`).
- **Webhook Trigger**: None.
- **Failure Behavior**: If `retry_count` > 2, defaults to "Unknown Patient" and transitions to `node_col_phone`.

---

## 4. node_col_phone
- **Node Type**: Slot Gathering Node (Phone)
- **Purpose**: Capture the patient's 10-digit callback phone number.
- **Inputs**: Spoken numbers.
- **Outputs**: Voice prompt.
- **Variables Updated**: `phone_number`, `retry_count`.
- **Transition Conditions**:
  - Transitions to `node_col_email` once a valid 10-digit number is captured.
- **Retry Logic**: If formatting validation fails (not 10 digits):
  - Clara reads back digits captured: "Is your number [captured_digits], or is it different?"
- **Webhook Trigger**: None.
- **Failure Behavior**: If `retry_count` > 2, inherits Caller ID from Retell metadata and proceeds to `node_col_email`.

---

## 5. node_col_email
- **Node Type**: Slot Gathering Node (Email)
- **Purpose**: Capture email address for confirmation.
- **Inputs**: Spoken email.
- **Outputs**: Voice prompt.
- **Variables Updated**: `email`, `retry_count`.
- **Transition Conditions**:
  - Transitions to `node_col_service` once valid email or skip instruction is captured.
- **Retry Logic**: If no `@` or domain match found:
  - Clara: "Could you spell that email for me, or say it again clearly?"
- **Webhook Trigger**: None.
- **Failure Behavior**: If `retry_count` > 2, stores "not_provided@brightsmiles.com" and transitions.

---

## 6. node_col_service
- **Node Type**: Slot Gathering Node (Service)
- **Purpose**: Capture the type of treatment requested.
- **Inputs**: Dental service name.
- **Outputs**: Voice prompt listing services.
- **Variables Updated**: `service`, `retry_count`.
- **Transition Conditions**:
  - Transitions to `node_col_date` once matched against catalog.
- **Retry Logic**: If service does not match the 6 catalog services:
  - Clara: "We currently offer cleanings, root canals, whitening, braces consults, extractions, and general consultations. Which of those do you need?"
- **Webhook Trigger**: None.
- **Failure Behavior**: If `retry_count` > 2, defaults to "General Consultation" and transitions.

---

## 7. node_col_date
- **Node Type**: Slot Gathering Node (Date)
- **Purpose**: Capture preferred date of the appointment.
- **Inputs**: Date descriptions (e.g. "next Friday", "July 12th").
- **Outputs**: Voice prompt.
- **Variables Updated**: `appointment_date`, `retry_count`.
- **Transition Conditions**:
  - Transitions to `node_col_time` once a valid future date on Monday-Saturday is verified.
- **Retry Logic**: If date is Sunday or in the past:
  - Clara explains: "We are open Monday through Saturday. What other date works for you?"
- **Webhook Trigger**: None.
- **Failure Behavior**: If `retry_count` > 3, escalates to `node_human_transfer`.

---

## 8. node_col_time
- **Node Type**: Slot Gathering Node (Time)
- **Purpose**: Capture preferred time of the appointment.
- **Inputs**: Spoken time.
- **Outputs**: Voice prompt.
- **Variables Updated**: `appointment_time`, `retry_count`.
- **Transition Conditions**:
  - Transitions to `node_col_notes` once valid time between 9:00 AM – 6:00 PM is verified.
- **Retry Logic**: If time falls outside business hours:
  - Clara: "Our slots are from 9 AM to 6 PM. What time in that range works best?"
- **Webhook Trigger**: None.
- **Failure Behavior**: If `retry_count` > 3, escalates to `node_human_transfer`.

---

## 9. node_col_notes
- **Node Type**: Slot Gathering Node (Notes)
- **Purpose**: Optional comments about symptoms or health history.
- **Inputs**: Caller comments or "none".
- **Outputs**: Voice prompt.
- **Variables Updated**: `notes`.
- **Transition Conditions**:
  - Transitions to `node_confirm_booking`.
- **Retry Logic**: None (1 attempt only).
- **Webhook Trigger**: None.
- **Failure Behavior**: Defaults to empty string and transitions.

---

## 10. node_confirm_booking
- **Node Type**: Confirmation Node
- **Purpose**: Final verification of all gathered slots.
- **Inputs**: Yes/No affirmation.
- **Outputs**: Summary statement synthesis.
- **Variables Updated**: None.
- **Transition Conditions**:
  - Transitions to `node_webhook_trigger` if caller confirms details.
  - Transitions back to specific slot node if caller requests changes.
- **Retry Logic**: Clara repeats the prompt once if user provides ambiguous response.
- **Webhook Trigger**: None.
- **Failure Behavior**: If ambiguous/silent twice, transfers to `node_human_transfer`.

---

## 11. node_webhook_trigger
- **Node Type**: Webhook API Dispatcher Node
- **Purpose**: Send booking transaction details to the backend API.
- **Inputs**: System variables collection.
- **Outputs**: API success/failure response envelope.
- **Variables Updated**: `conversation_state`.
- **Transition Conditions**:
  - Transitions to `node_goodbye` on HTTP success code.
  - Transitions to `node_human_transfer` on HTTP failure or timeout.
- **Retry Logic**: None (handled by network timeout rules).
- **Webhook Trigger**: Expatches HTTP POST call.
- **Failure Behavior**: Transitions to `node_human_transfer`.

---

## 12. node_human_transfer
- **Node Type**: Telephony Transfer Node
- **Purpose**: Transfer call to human operator.
- **Inputs**: None.
- **Outputs**: "Let me transfer you to our clinic receptionist now."
- **Variables Updated**: `conversation_state` ("transferred").
- **Transition Conditions**: Initiates telephony transfer trunk trigger.
- **Retry Logic**: None.
- **Webhook Trigger**: None.
- **Failure Behavior**: Hangs up if transfer trunk fails.

---

## 13. node_goodbye
- **Node Type**: Goodbye Node
- **Purpose**: End the call.
- **Inputs**: None.
- **Outputs**: Farewell speech.
- **Variables Updated**: `conversation_state` ("completed").
- **Transition Conditions**: Telephony disconnect trigger.
- **Retry Logic**: None.
- **Webhook Trigger**: None.
- **Failure Behavior**: Immediately forces disconnect.
