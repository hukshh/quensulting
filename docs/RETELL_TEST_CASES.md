# RetellAI Simulator Test Cases

Use the following conversational test scripts in the RetellAI Web Simulator to verify routing, validation rules, and variable capture.

---

## Test Case 1: Happy Path (Standard Booking)
- **Goal**: Verify successful capture of all slots, confirmation, and webhook dispatch.
- **Script**:
  - **Clara**: "Hello, thanks for calling Bright Smiles Dental! This is Clara. How can I help you today?"
  - **User**: "Hi, I'd like to book an appointment."
  - **Clara**: "I'd be happy to help you book that. Can I please start with your first and last name?"
  - **User**: "My name is Alice Smith."
  - **Clara**: "Great. What is the best phone number to reach you if we need to get in touch?"
  - **User**: "It's 555-019-9000."
  - **Clara**: "Thank you. And what is your email address? We'll use this to send your confirmation."
  - **User**: "alice.smith@example.com"
  - **Clara**: "What type of appointment are you looking to schedule?"
  - **User**: "I just need a dental cleaning."
  - **Clara**: "What day works best for you?"
  - **User**: "Next Tuesday, July 14th."
  - **Clara**: "And what time of day works for you? Our slots are from 9 AM to 6 PM."
  - **User**: "Is 2 PM available?"
  - **Clara**: "Yes, we can do 2 PM. Is there any symptom or note you'd like me to add for the dentist?"
  - **User**: "No, just a standard cleaning."
  - **Clara**: "Got it. Let me verify: I have you down as Alice Smith, booking a Dental Cleaning on July 14th at 2:00 PM. Is that all correct?"
  - **User**: "Yes, that's correct."
  - **Clara**: "Perfect! Your appointment is locked in..." *(Webhook executes successfully)*

---

## Test Case 2: Interruption and FAQ handling
- **Goal**: Verify Clara answers an FAQ mid-booking and returns to the active slot.
- **Script**:
  - **Clara**: "I'd be happy to help you book that. Can I please start with your first and last name?"
  - **User**: "My name is Bob Jones."
  - **Clara**: "Great. What is the best phone number to reach you?"
  - **User**: "Wait, before that, where is your clinic located?"
  - **Clara**: "Our clinic is located at 123 Dental Suite Way, Suite A. We have free parking in front. Now, resuming our booking—what was your phone number?"
  - **User**: "Ah, okay. It's 555-019-9111."

---

## Test Case 3: Emergency Handoff
- **Goal**: Verify immediate human transfer when critical symptoms are mentioned.
- **Script**:
  - **Clara**: "Hello, thanks for calling Bright Smiles Dental! This is Clara..."
  - **User**: "Help! My tooth broke and my gum is bleeding heavily."
  - **Clara**: "I understand. Let me transfer you directly to our front desk receptionist so they can assist you right away. One moment please." *(Initiates transfer call)*
