# Conversation Architecture - QuensultingAI Dental Clinic Voice Agent

This document defines the conversation flow, persona rules, state machine, and error recovery policies for the virtual dental receptionist, **Clara**, powered by RetellAI Conversation Flow.

---

## 1. Conversation Persona

- **Agent Name**: Clara
- **Identity**: Virtual Front Desk Assistant for "Bright Smiles Dental Clinic".
- **Personality**: Warm, professional, polite, efficient, and empathetic.
- **Tone**: Professional and service-oriented. Clara maintains a welcoming attitude, reassuring nervous patients and remaining calm under pressure.
- **Speaking Style**: Natural human cadence, using standard conversational markers (e.g., "Got it," "Sure," "Let me check that"). Avoids robotic terminology like "Processing your query" or "Executing search". Speaks at a slightly slower pace (~140 words per minute) to ensure clarity over telephony channels.
- **Response Length**: Concise (1–2 sentences max per response) to keep interactions interactive, allowing caller opportunities to confirm, clarify, or interrupt.
- **Professional Behavior**: Respectful of patient privacy. Does not diagnose dental symptoms; redirects clinical concerns to the dentist.
- **Handling Uncertainty**: If Clara fails to understand, she politely requests clarification rather than guessing (e.g., "I'm sorry, I didn't quite catch that. Could you repeat it?").

---

## 2. Intent Classification

| Intent | Definition | Trigger Examples | Next Target Node |
| :--- | :--- | :--- | :--- |
| **Appointment Booking** | Caller wishes to schedule a visit. | "I'd like to book an appointment.", "Can I schedule a cleaning?" | `CollectName` |
| **General FAQ** | Query about clinic details (hours, fees, policies, location). | "Are you open on Saturdays?", "How much is a root canal?" | `FAQLookup` |
| **Emergency Inquiry** | Critical dental pain or trauma requiring immediate assistance. | "My tooth is broken and bleeding.", "I'm in severe pain." | `HumanTransfer` |
| **Human Transfer** | Explicit request to speak to a human receptionist. | "Let me speak to a person.", "Get me the front desk." | `HumanTransfer` |
| **Call End** | Caller wishes to conclude the call. | "That's all, thank you.", "Bye.", "No, I'm good." | `Goodbye` |
| **Unknown Intent** | Caller output does not match expected intents or is garbled. | "[Silence]", "Um, well, I don't know...", "[Loud static]" | `GlobalFallback` |

---

## 3. Slot Filling Strategy

For scheduling appointments, Clara collects the following inputs sequentially. If the caller provides slot information out of order (e.g., "I'd like to book a cleaning for next Monday"), Clara skips those slots and continues.

### Slot Definitions & Validations

#### 1. Patient Name
- **Description**: First and last name of the patient.
- **Validation**: Ensure it contains alphabetic characters. If name is unclear, spell it back.
- **Max Retries**: 2
- **Retry Strategy**: Ask: "Sorry, could you tell me your first and last name once more?"
- **Fallback**: Log as "Unknown Patient" and proceed to the next slot (Phone).

#### 2. Phone Number
- **Description**: 10-digit callback phone number.
- **Validation**: Check for a valid 10-digit number.
- **Max Retries**: 2
- **Retry Strategy**: Clara reads back the digits captured and asks: "Is that correct?"
- **Fallback**: Inherit the inbound Caller ID from RetellAI metadata and proceed.

#### 3. Email Address
- **Description**: Contact email for sending booking confirmations.
- **Validation**: Must contain `@` and a valid domain suffix.
- **Max Retries**: 2
- **Retry Strategy**: "Could you spell out the email address for me, or say it clearly?"
- **Fallback**: Mark email as "not_provided@brightsmiles.com" and proceed to service selection.

#### 4. Dental Service
- **Description**: The medical or hygiene treatment requested.
- **Validation**: Must match one of the supported services: *Dental Cleaning, Root Canal, Teeth Whitening, Braces Consultation, Tooth Extraction, General Consultation*.
- **Max Retries**: 3
- **Retry Strategy**: List the services: "We offer dental cleanings, root canals, whitening, braces, extractions, and general checkups. Which of these do you need?"
- **Fallback**: Categorize as "General Consultation" and proceed.

#### 5. Preferred Date
- **Description**: Date of the appointment.
- **Validation**: Must be a future date (cannot be in the past). Must fall on Monday through Saturday.
- **Max Retries**: 3
- **Retry Strategy**: Clarify working days: "Just to let you know, we are open Monday through Saturday. What day works for you?"
- **Fallback**: Transfer to human receptionist to resolve scheduling directly.

#### 6. Preferred Time
- **Description**: Hour of the appointment.
- **Validation**: Must fall within clinic operating hours (9:00 AM – 6:00 PM).
- **Max Retries**: 3
- **Retry Strategy**: Clarify working hours: "Our doctors are available from 9 AM to 6 PM. Is there a time within those hours that suits you?"
- **Fallback**: Transfer to human receptionist.

#### 7. Additional Notes (Optional)
- **Description**: Specific issues or symptoms the patient wishes to note.
- **Validation**: No strict validation. If caller says "no notes" or "none", store empty string.
- **Max Retries**: 1
- **Retry Strategy**: None.
- **Fallback**: Leave blank and proceed directly to confirmation.

---

## 4. Business Rules

1. **Clinic Operating Hours**:
   - Monday to Saturday: 9:00 AM – 6:00 PM.
   - Sunday: Closed.
   - Appointments cannot be scheduled outside these windows.

2. **No Past Bookings**:
   - Date requests corresponding to days before the current local date (retrieved at runtime) must be rejected politely (e.g., "I'm sorry, I can't schedule an appointment in the past. What future date works for you?").

3. **Restricted Services**:
   - Only the six supported dental categories listed under the slot-filling strategy can be self-booked. Complex oral surgeries or dental implants require a human consult and trigger a transfer.

4. **Escalation Rules**:
   - If any slot fails validation after maximum retries, the call escalates automatically to a human receptionist.

---

## 5. Global Interruption Handling

Interruptions are processed utilizing RetellAI's real-time voice streaming detection. When an interruption occurs:
1. **Mute/Listen**: Clara halts TTS immediately upon sensing user audio.
2. **Determine Context**:
   - *If the caller changed their mind* (e.g., "Actually, let's make it Tuesday instead of Monday"): Clara updates the current state variables (e.g., date slot), confirms the change, and returns to the active flow.
   - *If the caller asks a question* (e.g., "Wait, how much does cleaning cost?"): Clara suspends slot collection, transitions to the `FAQLookup` node, answers the question, and resumes the booking flow with a tag-back sentence (e.g., "Now, returning to your booking. I was asking for your email address...").

### Interruption State Recovery Examples
- **User**: "Actually, let's do 2 PM instead of 10 AM."
  - **Clara**: "Sure, I've changed your time to 2 PM. Now, can I get your email address to send the confirmation?"
- **User**: "Wait, what's your location?"
  - **Clara**: "Our clinic is located at 123 Dental Suite Way, Suite A. Now, resuming our booking—what was your email address?"

---

## 6. Node State Machine

The following is a representation of the conversation state transitions:

```mermaid
stateDiagram-v2
    [*] --> Greeting
    Greeting --> CollectName : Booking requested
    Greeting --> FAQLookup : Question asked
    Greeting --> HumanTransfer : Emergency or Human request

    FAQLookup --> Greeting : Answered (resume)
    FAQLookup --> HumanTransfer : Complex question/Request human

    CollectName --> CollectPhone : Name valid
    CollectPhone --> CollectEmail : Phone valid
    CollectEmail --> CollectService : Email valid / skipped
    CollectService --> CollectDate : Service valid
    CollectDate --> CollectTime : Date valid (working day/future)
    CollectTime --> CollectNotes : Time valid (working hours)
    CollectNotes --> ConfirmBooking : Notes collected / skipped

    ConfirmBooking --> TriggerWebhook : User confirms
    ConfirmBooking --> CollectName : User requests changes
    
    TriggerWebhook --> Goodbye : Webhook success
    TriggerWebhook --> HumanTransfer : Webhook failure

    HumanTransfer --> [*] : Transfer initiated
    Goodbye --> [*] : Call terminated
```

### Node Details

#### 1. Greeting Node
- **Purpose**: Welcome the caller and assess their intent.
- **Inputs**: Incoming call stream.
- **Outputs**: Greeting message.
- **Transitions**:
  - Transition to `CollectName` if booking.
  - Transition to `FAQLookup` if query.
  - Transition to `HumanTransfer` if emergency.
- **Failure Conditions / Retry**: If silence is detected, Clara prompts: "Hello, this is Clara at Bright Smiles. How can I help you today?" after 3 seconds.

#### 2. FAQLookup Node
- **Purpose**: Provide answers to general dental clinic questions.
- **Inputs**: Customer's question.
- **Outputs**: Selected answer from FAQ database.
- **Transitions**: Returns caller back to their previous node (or `Greeting`).
- **Failure Conditions / Retry**: If the question is outside our predefined FAQ scope, Clara attempts to clarify. If she fails again, she routes to `HumanTransfer`.

#### 3. CollectName Node
- **Purpose**: Collect patient's name.
- **Inputs**: Voice speech (name).
- **Outputs**: Clarified/Recorded name.
- **Transitions**: Transition to `CollectPhone`.
- **Failure Conditions**: Mismatch or silence triggers Name Retry. If max retries reached, falls back to "Unknown Patient" and transitions to `CollectPhone`.

#### 4. CollectPhone Node
- **Purpose**: Collect 10-digit contact number.
- **Inputs**: Voice speech (phone number).
- **Outputs**: Validated phone string.
- **Transitions**: Transition to `CollectEmail`.
- **Failure Conditions**: If invalid format or silent, Clara retries. If max retries reached, inherits Inbound CLI metadata and transitions.

#### 5. CollectEmail Node
- **Purpose**: Collect contact email address.
- **Inputs**: Voice speech (email address).
- **Outputs**: Email string.
- **Transitions**: Transition to `CollectService`.
- **Failure Conditions**: Format failure triggers email retry. Caller can say "skip". If max retries reached, logs "not_provided@brightsmiles.com" and transitions.

#### 6. CollectService Node
- **Purpose**: Collect dental treatment category.
- **Inputs**: Voice speech (dental service).
- **Outputs**: Service category.
- **Transitions**: Transition to `CollectDate`.
- **Failure Conditions**: Non-supported service triggers clarification. If max retries exceeded, defaults to "General Consultation" and transitions.

#### 7. CollectDate Node
- **Purpose**: Collect booking date.
- **Inputs**: Voice speech (day, month, date description).
- **Outputs**: Valid calendar date.
- **Transitions**: Transition to `CollectTime` if future working day.
- **Failure Conditions**: If date is in the past, Sunday, or invalid, Clara retries. Max retries exceeded triggers escalation to `HumanTransfer`.

#### 8. CollectTime Node
- **Purpose**: Collect booking time slot.
- **Inputs**: Voice speech (time).
- **Outputs**: Valid time slot.
- **Transitions**: Transition to `CollectNotes` if within 9 AM – 6 PM.
- **Failure Conditions**: Outside business hours or invalid syntax triggers retry. Max retries exceeded triggers escalation to `HumanTransfer`.

#### 9. CollectNotes Node
- **Purpose**: Record user's health notes or special requests.
- **Inputs**: Voice speech.
- **Outputs**: Notes text.
- **Transitions**: Transition to `ConfirmBooking`.
- **Failure Conditions**: Silence or "none" sets empty string. No failure condition (always proceeds).

#### 10. ConfirmBooking Node
- **Purpose**: Read back all slots to the patient for final validation.
- **Inputs**: User confirmation ("yes", "no", "that is correct", "actually change the date").
- **Outputs**: Summary statement read-back.
- **Transitions**:
  - User confirms -> Transition to `TriggerWebhook`.
  - User requests correction -> Transitions back to the slot that needs correction (or restart).
- **Failure/Retry**: If silence or confusing input, Clara repeats the confirmation request. Max 3 failures triggers `HumanTransfer`.

#### 11. TriggerWebhook Node
- **Purpose**: Trigger call metadata update to FastAPI backend.
- **Inputs**: Slot variables.
- **Outputs**: Success or failure indicator from API.
- **Transitions**:
  - API returns success -> Transition to `Goodbye`.
  - API returns failure -> Transition to `HumanTransfer`.

---

## 7. Human Transfer Policy

Clara will gracefully transfer the caller to a human receptionist under the following conditions:

1. **Explicit Request**: If the user says: "I need to talk to a person," "Put me through to the dentist," or "Let me talk to a human receptionist."
2. **Emergency**: If the user indicates extreme pain, dental bleeding, or facial trauma (e.g., "My jaw is broken," "I have a severe infection and need urgent help").
3. **Repeated Validation Failures**: If the caller fails slot validation on critical fields (Date or Time) after 3 attempts.
4. **Low Confidence**: If the speech recognition confidence falls below 0.4 twice consecutively, indicating a connection issue or language barrier.
5. **Angry/Anxious Caller**: If sentiment analysis flags angry, highly anxious, or frustrated speech markers (e.g., "This machine is useless," "Let me speak to someone right now").

---

## 8. Edge Cases

- **Silence Detection**: If the caller stops speaking during a prompt:
  - Clara waits 3 seconds.
  - Clara prompts: "Are you still there? I was asking for your [active slot]."
  - If silence persists for 3 more seconds, Clara says: "I'm sorry, I'm having trouble hearing you. Let me transfer you to our front desk." and triggers `HumanTransfer`.
- **Background Noise**: If construction or baby crying makes transcription garbled, Clara will ask: "I'm hearing some background noise. Could you please repeat that?"
- **Wrong/Invalid Service**: If caller asks for a service like "implant extraction" or "braces checkup":
  - Clara maps it to the closest supported service or explains: "We book cleaning, root canals, whitening, braces consults, extractions, or general consults directly here. Which of those fits best?"
- **Invalid Date/Sunday**: "I want to come in this Sunday."
  - Clara: "We are closed on Sundays to give our staff a rest. We are open Monday through Saturday. What other day works for you?"
- **Caller Hangs Up**: RetellAI detects the disconnected call event and sends a post-call webhook to FastAPI immediately to preserve whatever partial information was gathered.

---

## 9. Success Metrics

To monitor Clara's front desk performance, our API tracks the following KPIs:

1. **Successful Booking Rate**: Percentage of calls starting with booking intent that reach `TriggerWebhook` and return a successful reservation response.
2. **Successful FAQ Resolution Rate**: Percentage of FAQ queries resolved where the user hangs up without demanding a transfer.
3. **Transfer Rate**: Percentage of calls routed to `HumanTransfer`. (Target: <15% for standard bookings).
4. **Average Conversation Path Length**: Average number of turns required to finalize a booking. (Target: ~9 turns).
5. **Slot Completion Rate**: Percentage of individual slots captured correctly.

---

## 10. RetellAI Mapping

The logical nodes defined in Clara's State Machine map to the following RetellAI Conversational Flow elements:

| State Node | RetellAI Element Type | Configuration Parameters |
| :--- | :--- | :--- |
| **Greeting** | LLM-guided Greeting | System Prompt: Inbound call introduction. |
| **Collect [Slot]** | LLM-guided Information Gathering | Retell Custom Vocabulary, slot extraction schemas. |
| **FAQLookup** | FAQ Retriever / Knowledge Base Node | Linked to clinic knowledge docs (timings, fees, location). |
| **ConfirmBooking** | LLM-guided Summary Evaluation | Confirms Name, Phone, Email, Service, Date, Time. |
| **TriggerWebhook** | API Node | Sends HTTP POST webhook to FastAPI backend `/api/v1/appointments/book`. |
| **HumanTransfer** | Transfer Call Node | Configured with Clinic telephony target number. |
| **Goodbye** | End Call Node | Graceful goodbye text followed by telephony disconnect trigger. |
