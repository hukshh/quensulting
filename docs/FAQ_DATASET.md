# Dental Clinic FAQ Dataset

This dataset maps common questions asked by patients to Clara, detailing canonical answers, alternative phrasing, synonyms, and escalation thresholds.

---

## 1. Clinic Timings
- **Question**: "What are your hours of operation?"
- **Canonical Answer**: "We are open Monday through Saturday, from 9:00 AM to 6:00 PM. We are closed on Sundays."
- **Alternative Phrasings**:
  - "When do you guys open?"
  - "Are you open on Saturdays?"
  - "What are your working hours?"
- **Synonyms**: Timings, operating hours, schedule, opening times.
- **Escalation Conditions**: Escalate to a human if the user insists on booking outside these hours or requests holiday schedules not covered here.

---

## 2. Consultation Fee
- **Question**: "How much does a checkup cost?"
- **Canonical Answer**: "Our general consultation fee is $50. This covers the oral examination and a discussion of any treatments you might need. X-rays or cleanings are priced separately."
- **Alternative Phrasings**:
  - "What is your consultation fee?"
  - "How much is it to just see the dentist?"
  - "What do you charge for a first visit?"
- **Synonyms**: Price, cost, fees, rates, payment.
- **Escalation Conditions**: Escalate if the patient asks about insurance coverage, payment plans, or sliding scale pricing.

---

## 3. Walk-in Policy
- **Question**: "Can I just walk in?"
- **Canonical Answer**: "We highly recommend scheduling an appointment to minimize your wait time, but we do accept walk-in patients on a first-come, first-served basis, depending on doctor availability."
- **Alternative Phrasings**:
  - "Do you take walk-ins?"
  - "Can I come by without an appointment?"
  - "Do I need to book in advance?"
- **Synonyms**: Walk-in, unscheduled visit, drop-in.
- **Escalation Conditions**: None.

---

## 4. Emergency Appointments
- **Question**: "Do you handle emergencies?"
- **Canonical Answer**: "Yes, we prioritize dental emergencies, such as severe pain, swelling, or a knocked-out tooth. Please come in immediately or let me transfer you to our main desk right now."
- **Alternative Phrasings**:
  - "I have a toothache emergency."
  - "Can you see me today for a broken tooth?"
  - "My gum is bleeding heavily."
- **Synonyms**: Emergency, urgent, severe pain, bleeding, broken tooth.
- **Escalation Conditions**: Trigger immediate transfer to `node_human_transfer` upon classification of any active trauma or bleeding.

---

## 5. Clinic Location
- **Question**: "Where are you located?"
- **Canonical Answer**: "Our clinic is located at 123 Dental Suite Way, Suite A. We have free parking directly in front of the building."
- **Alternative Phrasings**:
  - "What is your address?"
  - "How do I get to your clinic?"
  - "Where is Bright Smiles Dental located?"
- **Synonyms**: Address, location, directions, street, coordinates.
- **Escalation Conditions**: None.

---

## 6. Payment Methods
- **Question**: "What payment methods do you accept?"
- **Canonical Answer**: "We accept all major credit cards, debit cards, cash, and Apple Pay. We can also provide itemized receipts if you wish to file a claim with your dental insurance."
- **Alternative Phrasings**:
  - "Can I pay with credit card?"
  - "Do you take check or cash?"
  - "Do you accept Apple Pay?"
- **Synonyms**: Payments, visa, mastercard, cash, credit, invoice.
- **Escalation Conditions**: Escalate if the caller asks about specific insurance providers (e.g. Delta Dental, MetLife) or financing options.

---

## 7. Service Specific FAQs

### Dental Cleaning
- **Question**: "How much is a basic cleaning?"
- **Canonical Answer**: "A standard professional dental cleaning is $90. It typically takes about 45 minutes and includes plaque removal and teeth polishing."
- **Alternative Phrasings**: "I want to clean my teeth," "What is the cleaning charge?"

### Root Canal
- **Question**: "How much is a root canal?"
- **Canonical Answer**: "A root canal treatment typically starts at $600, depending on which tooth requires the procedure. We recommend a general consultation first to get an accurate estimate."
- **Alternative Phrasings**: "Do you do root canals?", "My nerve is hurting."

### Teeth Whitening
- **Question**: "How much is teeth whitening?"
- **Canonical Answer**: "We offer professional in-office whitening for $250. This provides immediate results in a single, one-hour session."
- **Alternative Phrasings**: "I want to whiten my teeth," "What is bleaching price?"

### Braces Consultation
- **Question**: "Can I get a quote for braces?"
- **Canonical Answer**: "Our orthodontist offers free initial braces consultations to evaluate your alignment options and draft a custom pricing plan."
- **Alternative Phrasings**: "Do you do Invisalign?", "How much are braces?"

### Tooth Extraction
- **Question**: "How much to pull a tooth?"
- **Canonical Answer**: "A simple tooth extraction is $150. Surgical or wisdom teeth extractions can be higher. A checkup is required beforehand to evaluate the tooth."
- **Alternative Phrasings**: "I need a tooth pulled," "What is the extraction cost?"

### General Consultation
- **Question**: "What is included in a checkup?"
- **Canonical Answer**: "A general consultation is $50 and includes a comprehensive oral exam by the dentist. X-rays, if needed, are additional."
- **Alternative Phrasings**: "I just need a dental checkup," "Can I see the dentist for an exam?"
