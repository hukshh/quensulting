# RetellAI Webhook Specification

> [!WARNING]
> The webhook URL and JSON payload contracts defined below are **provisional placeholders** to guide the initial RetellAI node mapping setup. The final API implementation details and JSON request/response models will be established during Phase 4 (Backend Integration).

---

## 1. HTTP Endpoint Details

- **Provisional Webhook URL**: `https://api.brightsmiles.quensulting.ai/api/v1/appointments/book` *(Provisional path, subject to change in Phase 4)*
- **HTTP Method**: `POST`
- **Headers**:
  ```http
  Content-Type: application/json
  X-Retell-Signature: v1=f72e9a5c889f07a2d82914197e88c031c360a0f5123d45ef8890bc1c2789e02c
  ```
  *(The `X-Retell-Signature` header is used for validating webhook calls locally to ensure payloads originate from Retell).*

---

## 2. Request Payload (Retell → FastAPI)

RetellAI transfers variables accumulated in the session state within the JSON body:

```json
{
  "call_id": "call_987654321_abc123",
  "caller_name": "John Doe",
  "phone_number": "5550199000",
  "email": "john.doe@example.com",
  "service": "Dental Cleaning",
  "appointment_date": "2026-07-10",
  "appointment_time": "14:30",
  "notes": "Patient reports minor sensitivity on the upper left molar.",
  "confidence_score": 0.94
}
```

---

## 3. Response Schema (FastAPI → Retell)

### Success Response (HTTP 200/201 OK)
Returned when the backend API successfully validates inputs, writes the booking log to Google Sheets, and schedules the email dispatch queue.

```json
{
  "status": "success",
  "booking_id": "bk_20260710_001",
  "message": "Appointment booked successfully",
  "summary": {
    "patient": "John Doe",
    "service": "Dental Cleaning",
    "datetime": "2026-07-10T14:30:00"
  }
}
```

### Failure Response (HTTP 400 Bad Request / 500 Server Error)
Returned if validation parameters fail backend audits, sheets lock conflicts arise, or database limits expire.

```json
{
  "status": "error",
  "code": "SLOT_CONFLICT",
  "message": "The requested appointment time slot is no longer available. Please select another time."
}
```

---

## 4. Connection Policies

- **Timeout Limit**: `5000ms` (5 seconds). If our server does not respond within this window, the Retell node treats the attempt as failed.
- **Retry Strategy**: None in real-time. Since a human caller is waiting on the line, retrying background APIs repeatedly would result in silence. The system must transition directly to `node_human_transfer` if a timeout or server error occurs.
