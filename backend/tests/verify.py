"""Local script to verify FastAPI endpoints and validation logic."""

import sys
from fastapi.testclient import TestClient

# Ensure backend directory is in python path
sys.path.append(".")

from app.main import app

client = TestClient(app)


def test_root_endpoints():
    """Test GET / and GET /health root endpoints."""
    print("Testing root endpoints...")
    
    r_index = client.get("/")
    assert r_index.status_code == 200, f"Expected 200, got {r_index.status_code}"
    assert "Welcome" in r_index.json().get("message", ""), "Welcome message not found"
    
    r_health = client.get("/health")
    assert r_health.status_code == 200, f"Expected 200, got {r_health.status_code}"
    assert r_health.json() == {"status": "healthy"}, "Health status mismatch"
    print("✅ Root endpoints verified successfully!")


def test_booking_happy_path():
    """Test successful booking transaction validation."""
    print("\nTesting booking happy path...")
    payload = {
        "call_id": "call_12345",
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john.doe@example.com",
        "service": "Dental Cleaning",
        "appointment_date": "2026-10-15",  # Future date
        "appointment_time": "14:30",        # Within working hours
        "notes": "Patient molar sensitivity"
    }
    
    response = client.post("/api/v1/appointments/book", json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert "booking_id" in data
    assert data["summary"]["patient"] == "John Doe"
    assert data["summary"]["service"] == "Dental Cleaning"
    print("✅ Booking happy path verified successfully!")


def test_booking_validation_failures():
    """Test booking validation failures for incorrect inputs."""
    print("\nTesting booking validation failures...")
    
    # 1. Invalid phone number (not 10 digits)
    payload_bad_phone = {
        "caller_name": "John Doe",
        "phone_number": "555-123",  # invalid length
        "email": "john@example.com",
        "service": "Dental Cleaning",
        "appointment_date": "2026-10-15",
        "appointment_time": "14:30"
    }
    r = client.post("/api/v1/appointments/book", json=payload_bad_phone)
    assert r.status_code == 422, f"Expected 422 for phone, got {r.status_code}"
    
    # 2. Invalid email address
    payload_bad_email = {
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john-invalid",  # invalid format
        "service": "Dental Cleaning",
        "appointment_date": "2026-10-15",
        "appointment_time": "14:30"
    }
    r = client.post("/api/v1/appointments/book", json=payload_bad_email)
    assert r.status_code == 422, f"Expected 422 for email, got {r.status_code}"
    
    # 3. Invalid service name
    payload_bad_service = {
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john@example.com",
        "service": "Dental Implant",  # unsupported service
        "appointment_date": "2026-10-15",
        "appointment_time": "14:30"
    }
    r = client.post("/api/v1/appointments/book", json=payload_bad_service)
    assert r.status_code == 422, f"Expected 422 for service, got {r.status_code}"
    
    # 4. Past date
    payload_past_date = {
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john@example.com",
        "service": "Dental Cleaning",
        "appointment_date": "2020-01-01",  # past
        "appointment_time": "14:30"
    }
    r = client.post("/api/v1/appointments/book", json=payload_past_date)
    assert r.status_code == 422, f"Expected 422 for past date, got {r.status_code}"
    
    # 5. Sunday appointment
    payload_sunday = {
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john@example.com",
        "service": "Dental Cleaning",
        "appointment_date": "2026-07-12",  # Sunday
        "appointment_time": "14:30"
    }
    r = client.post("/api/v1/appointments/book", json=payload_sunday)
    assert r.status_code == 422, f"Expected 422 for Sunday, got {r.status_code}"
    
    # 6. Outside working hours (early)
    payload_early = {
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john@example.com",
        "service": "Dental Cleaning",
        "appointment_date": "2026-10-15",
        "appointment_time": "08:30"  # before 9 AM
    }
    r = client.post("/api/v1/appointments/book", json=payload_early)
    assert r.status_code == 422, f"Expected 422 for outside hours, got {r.status_code}"

    # 7. Outside working hours (late)
    payload_late = {
        "caller_name": "John Doe",
        "phone_number": "5550199000",
        "email": "john@example.com",
        "service": "Dental Cleaning",
        "appointment_date": "2026-10-15",
        "appointment_time": "18:30"  # after 6 PM
    }
    r = client.post("/api/v1/appointments/book", json=payload_late)
    assert r.status_code == 422, f"Expected 422 for outside hours, got {r.status_code}"
    
    print("✅ Booking validation failure cases verified successfully!")


if __name__ == "__main__":
    try:
        test_root_endpoints()
        test_booking_happy_path()
        test_booking_validation_failures()
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
    except AssertionError as e:
        print(f"\n❌ TEST FAILURE: {e}")
        sys.exit(1)
