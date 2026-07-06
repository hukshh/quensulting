# RetellAI Variables Definition

This document lists and defines all conversation variables stored in the active session context during a call. These variables are referenced within Clara's prompt nodes and dispatched in the final webhook payload.

---

| Variable Name | Data Type | Required | Default Value | Validation Criteria | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`caller_name`** | `String` | Yes | `"Unknown Patient"` | Minimum length of 2 characters. Only alphabet letters and spaces allowed. | `"John Doe"` |
| **`phone_number`** | `String` | Yes | `""` | Must be a valid 10-digit number. Characters like `-`, `(`, `)` are stripped. | `"5550199000"` |
| **`email`** | `String` | Yes | `"not_provided@brightsmiles.com"` | Regular expression: `^[^@]+@[^@]+\.[^@]+$`. Must contain `@` and domain structure. | `"john.doe@example.com"` |
| **`service`** | `String` | Yes | `"General Consultation"` | Must match one of the 6 supported dental services exactly. | `"Dental Cleaning"` |
| **`appointment_date`** | `String` | Yes | `""` | ISO-8601 formatted date string (`YYYY-MM-DD`). Must be a future date on Monday-Saturday. | `"2026-07-10"` |
| **`appointment_time`** | `String` | Yes | `""` | Time string in 24-hour structure (`HH:MM`). Must fall between `09:00` and `18:00`. | `"14:30"` |
| **`notes`** | `String` | No | `""` | Free-form text capture. Max length 500 characters. | `"Has mild gum sensitivity."` |
| **`intent`** | `String` | Yes | `"unknown"` | Allowed values: `booking`, `faq`, `emergency`, `transfer`, `end_call`, `unknown`. | `"booking"` |
| **`confidence_score`** | `Float` | Yes | `1.0` | Range `0.0` to `1.0`. Measures transcript and intent extraction confidence. | `0.92` |
| **`retry_count`** | `Integer` | Yes | `0` | Increments on slot parsing validation failures. Reset upon successful slot save. | `1` |
| **`conversation_state`** | `String` | Yes | `"greeting"` | Allowed values: `greeting`, `collecting_info`, `confirming`, `sending_data`, `transferred`, `completed`. | `"collecting_info"` |
