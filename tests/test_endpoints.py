"""
CallPilot Service Integration Tests

Tests the service.py functions that ElevenLabs will call.
Make sure FastAPI server is running: python3 -m uvicorn main:app --reload --port 8000

Run with: python3 tests/test_service_integration.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calendar.service import (
    check_availability,
    check_availability_range,
    book_appointment,
    get_upcoming_appointments,
    reschedule_appointment,
    mark_reminder_sent,
    mark_no_show,
    cancel_appointment
)

# Store data between tests
test_data = {
    "appointment_id": None,
    "booking_slot": None,
    "reschedule_slot": None
}


def print_result(test_name, passed, details=None, error=None):
    status = "PASS" if passed else "FAIL"
    print(f"\n[{status}] {test_name}")
    if details:
        print(f"    {details}")
    if error:
        print(f"    Error: {error}")


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ============== Availability Tests ==============

def test_check_availability_today():
    try:
        result = check_availability("today")
        passed = result.get("success") == True and "available_slots" in result
        
        print_result(
            "check_availability('today')",
            passed,
            f"Found {result.get('total_slots', 0)} slots on {result.get('formatted_date')}"
        )
        return passed
    except Exception as e:
        print_result("check_availability('today')", False, error=str(e))
        return False


def test_check_availability_tomorrow():
    try:
        result = check_availability("tomorrow")
        passed = result.get("success") == True and "available_slots" in result
        
        print_result(
            "check_availability('tomorrow')",
            passed,
            f"Found {result.get('total_slots', 0)} slots on {result.get('formatted_date')}"
        )
        return passed
    except Exception as e:
        print_result("check_availability('tomorrow')", False, error=str(e))
        return False


def test_check_availability_next_monday():
    global test_data
    try:
        result = check_availability("next monday")
        passed = result.get("success") == True
        
        # Store slot for booking test
        if passed and result.get("available_slots"):
            slots = result["available_slots"]
            test_data["booking_slot"] = slots[0] if len(slots) > 0 else None
        
        print_result(
            "check_availability('next monday')",
            passed,
            f"Found {result.get('total_slots', 0)} slots on {result.get('formatted_date')}"
        )
        return passed
    except Exception as e:
        print_result("check_availability('next monday')", False, error=str(e))
        return False


def test_check_availability_next_wednesday():
    global test_data
    try:
        result = check_availability("next wednesday")
        passed = result.get("success") == True
        
        # Store slot for reschedule test
        if passed and result.get("available_slots"):
            slots = result["available_slots"]
            test_data["reschedule_slot"] = slots[0] if len(slots) > 0 else None
        
        print_result(
            "check_availability('next wednesday')",
            passed,
            f"Found {result.get('total_slots', 0)} slots on {result.get('formatted_date')}"
        )
        return passed
    except Exception as e:
        print_result("check_availability('next wednesday')", False, error=str(e))
        return False


def test_check_availability_specific_date():
    try:
        result = check_availability("2026-02-20")
        passed = result.get("success") == True
        
        print_result(
            "check_availability('2026-02-20')",
            passed,
            f"Date: {result.get('formatted_date')}, Slots: {result.get('total_slots', 0)}"
        )
        return passed
    except Exception as e:
        print_result("check_availability('2026-02-20')", False, error=str(e))
        return False


def test_check_availability_past_date():
    try:
        result = check_availability("2020-01-01")
        # Should succeed but return 0 slots
        passed = result.get("success") == True and result.get("total_slots", 0) == 0
        
        print_result(
            "check_availability('2020-01-01') - past date",
            passed,
            f"Correctly returned 0 slots for past date"
        )
        return passed
    except Exception as e:
        print_result("check_availability() past date", False, error=str(e))
        return False


def test_check_availability_range():
    try:
        dates = ["next monday", "next tuesday", "next wednesday", "next thursday", "next friday"]
        result = check_availability_range(dates)
        passed = result.get("success") == True and len(result.get("dates", [])) == 5
        
        print_result(
            "check_availability_range() - 5 weekdays",
            passed,
            f"Total slots across 5 days: {result.get('total_slots', 0)}"
        )
        return passed
    except Exception as e:
        print_result("check_availability_range()", False, error=str(e))
        return False


def test_check_availability_custom_duration():
    try:
        result = check_availability("next tuesday", duration_minutes=60)
        passed = result.get("success") == True
        
        print_result(
            "check_availability() with 60 min duration",
            passed,
            f"Found {result.get('total_slots', 0)} slots (fewer due to longer duration)"
        )
        return passed
    except Exception as e:
        print_result("check_availability() custom duration", False, error=str(e))
        return False


# ============== Booking Tests ==============

def test_book_appointment_next_monday():
    global test_data
    try:
        if not test_data.get("booking_slot"):
            print_result("book_appointment() on next monday", False, error="No available slot from previous test")
            return False
        
        slot = test_data["booking_slot"]
        
        result = book_appointment(
            patient_name="Alice Johnson",
            patient_phone="+1555123456",
            appointment_datetime=slot["start"],
            patient_email="alice.johnson@example.com",
            appointment_type="checkup",
            notes="New patient checkup"
        )
        
        passed = result.get("success") == True and result.get("confirmation_id")
        
        if passed:
            test_data["appointment_id"] = result.get("confirmation_id")
        
        print_result(
            "book_appointment() on next monday",
            passed,
            f"Booked: {result.get('appointment_date')} at {result.get('appointment_time')}, ID: {result.get('confirmation_id')}"
        )
        return passed
    except Exception as e:
        print_result("book_appointment()", False, error=str(e))
        return False


def test_book_duplicate_should_fail():
    global test_data
    try:
        if not test_data.get("booking_slot"):
            print_result("book_appointment() duplicate", False, error="No slot data")
            return False
        
        slot = test_data["booking_slot"]
        
        result = book_appointment(
            patient_name="Bob Smith",
            patient_phone="+1555987654",
            appointment_datetime=slot["start"],
            appointment_type="consultation"
        )
        
        passed = result.get("success") == False
        
        print_result(
            "book_appointment() duplicate (should fail)",
            passed,
            "Correctly rejected duplicate booking" if passed else "Should have been rejected"
        )
        return passed
    except Exception as e:
        print_result("book_appointment() duplicate", False, error=str(e))
        return False


def test_book_with_different_types():
    try:
        # First get a slot on next thursday
        avail = check_availability("next thursday")
        if not avail.get("available_slots"):
            print_result("book_appointment() consultation type", False, error="No slots on thursday")
            return False
        
        slot = avail["available_slots"][0]
        
        result = book_appointment(
            patient_name="Carol Davis",
            patient_phone="+1555222333",
            appointment_datetime=slot["start"],
            appointment_type="consultation",
            notes="Follow-up consultation"
        )
        
        passed = result.get("success") == True
        
        # Cancel it right away to clean up
        if passed and result.get("confirmation_id"):
            cancel_appointment(result.get("confirmation_id"))
        
        print_result(
            "book_appointment() with consultation type",
            passed,
            f"Booked consultation on {result.get('appointment_date')}"
        )
        return passed
    except Exception as e:
        print_result("book_appointment() consultation", False, error=str(e))
        return False


# ============== Get Appointments Tests ==============

def test_get_upcoming_appointments():
    global test_data
    try:
        result = get_upcoming_appointments()
        passed = result.get("success") == True and "appointments" in result
        
        our_apt_found = False
        if test_data.get("appointment_id"):
            for apt in result.get("appointments", []):
                if apt.get("id") == test_data["appointment_id"]:
                    our_apt_found = True
                    break
        
        print_result(
            "get_upcoming_appointments()",
            passed,
            f"Total: {result.get('total', 0)}, Our monday appointment found: {our_apt_found}"
        )
        return passed
    except Exception as e:
        print_result("get_upcoming_appointments()", False, error=str(e))
        return False


def test_get_upcoming_24_hours():
    try:
        result = get_upcoming_appointments(hours_ahead=24)
        passed = result.get("success") == True
        
        print_result(
            "get_upcoming_appointments(hours_ahead=24)",
            passed,
            f"Found {result.get('total', 0)} appointments in next 24 hours"
        )
        return passed
    except Exception as e:
        print_result("get_upcoming_appointments(hours_ahead=24)", False, error=str(e))
        return False


def test_get_upcoming_one_week():
    try:
        result = get_upcoming_appointments(hours_ahead=168)  # 7 days
        passed = result.get("success") == True
        
        print_result(
            "get_upcoming_appointments(hours_ahead=168) - 1 week",
            passed,
            f"Found {result.get('total', 0)} appointments in next week"
        )
        return passed
    except Exception as e:
        print_result("get_upcoming_appointments() 1 week", False, error=str(e))
        return False


# ============== Reschedule Tests ==============

def test_reschedule_to_wednesday():
    global test_data
    try:
        if not test_data.get("appointment_id"):
            print_result("reschedule_appointment()", False, error="No appointment ID")
            return False
        
        if not test_data.get("reschedule_slot"):
            print_result("reschedule_appointment()", False, error="No wednesday slot available")
            return False
        
        new_slot = test_data["reschedule_slot"]
        
        result = reschedule_appointment(
            appointment_id=test_data["appointment_id"],
            new_datetime=new_slot["start"]
        )
        
        passed = result.get("success") == True
        
        print_result(
            "reschedule_appointment() monday -> wednesday",
            passed,
            f"Rescheduled to: {result.get('new_date')} at {result.get('new_time')}"
        )
        return passed
    except Exception as e:
        print_result("reschedule_appointment()", False, error=str(e))
        return False


def test_reschedule_to_past_should_fail():
    global test_data
    try:
        if not test_data.get("appointment_id"):
            print_result("reschedule to past", False, error="No appointment ID")
            return False
        
        result = reschedule_appointment(
            appointment_id=test_data["appointment_id"],
            new_datetime="2020-01-01T10:00:00-05:00"
        )
        
        passed = result.get("success") == False
        
        print_result(
            "reschedule_appointment() to past (should fail)",
            passed,
            f"Correctly rejected: {result.get('error', 'Invalid date')}" if passed else "Should have been rejected"  # ← CHANGED THIS LINE
        )
        return passed
    except Exception as e:
        print_result("reschedule to past", False, error=str(e))
        return False

# ============== Reminder & No-Show Tests ==============

def test_mark_reminder_sent():
    global test_data
    try:
        if not test_data.get("appointment_id"):
            print_result("mark_reminder_sent()", False, error="No appointment ID")
            return False
        
        result = mark_reminder_sent(test_data["appointment_id"])
        passed = result.get("success") == True
        
        print_result(
            "mark_reminder_sent()",
            passed,
            result.get("message")
        )
        return passed
    except Exception as e:
        print_result("mark_reminder_sent()", False, error=str(e))
        return False


def test_mark_no_show():
    global test_data
    try:
        if not test_data.get("appointment_id"):
            print_result("mark_no_show()", False, error="No appointment ID")
            return False
        
        result = mark_no_show(test_data["appointment_id"])
        passed = result.get("success") == True and result.get("status") == "no_show"
        
        print_result(
            "mark_no_show()",
            passed,
            f"Status changed to: {result.get('status')}"
        )
        return passed
    except Exception as e:
        print_result("mark_no_show()", False, error=str(e))
        return False


# ============== Cancel Tests ==============

def test_cancel_appointment():
    global test_data
    try:
        if not test_data.get("appointment_id"):
            print_result("cancel_appointment()", False, error="No appointment ID")
            return False
        
        result = cancel_appointment(test_data["appointment_id"])
        passed = result.get("success") == True
        
        print_result(
            "cancel_appointment()",
            passed,
            result.get("message")
        )
        return passed
    except Exception as e:
        print_result("cancel_appointment()", False, error=str(e))
        return False


def test_cancel_nonexistent():
    try:
        result = cancel_appointment("fake-id-that-does-not-exist-12345")
        passed = result.get("success") == False
        
        print_result(
            "cancel_appointment() nonexistent (should fail)",
            passed,
            "Correctly returned error" if passed else "Should have failed"
        )
        return passed
    except Exception as e:
        print_result("cancel_appointment() nonexistent", False, error=str(e))
        return False


def test_cancel_already_cancelled():
    global test_data
    try:
        if not test_data.get("appointment_id"):
            print_result("cancel already cancelled", False, error="No appointment ID")
            return False
        
        # Try to cancel again - keeping idempotent behavior (success expected)
        result = cancel_appointment(test_data["appointment_id"])
        
        # Test that it succeeds (idempotent)
        passed = result.get("success") == True  # ← CHANGED: Actually test the result
        
        print_result(
            "cancel_appointment() already cancelled (idempotent)",  # ← CHANGED: Clarify it's testing idempotency
            passed,  # ← CHANGED: Use actual test result
            f"Idempotent behavior confirmed: {result.get('message', '')}"  # ← CHANGED: Better message
        )
        return passed  # ← CHANGED: Return actual result instead of always True
    except Exception as e:
        print_result("cancel already cancelled", False, error=str(e))
        return False


# ============== Run All Tests ==============

def run_all_tests():
    print("\n" + "="*60)
    print("  CallPilot Service Integration Tests")
    print("="*60)
    print("\nMake sure FastAPI is running on http://localhost:8000")
    
    results = []
    
    # Availability - multiple days and scenarios
    print_section("Availability Functions")
    results.append(("check_availability('today')", test_check_availability_today()))
    results.append(("check_availability('tomorrow')", test_check_availability_tomorrow()))
    results.append(("check_availability('next monday')", test_check_availability_next_monday()))
    results.append(("check_availability('next wednesday')", test_check_availability_next_wednesday()))
    results.append(("check_availability('2026-02-20')", test_check_availability_specific_date()))
    results.append(("check_availability() past date", test_check_availability_past_date()))
    results.append(("check_availability_range() 5 days", test_check_availability_range()))
    results.append(("check_availability() 60 min", test_check_availability_custom_duration()))
    
    # Booking - different scenarios
    print_section("Booking Functions")
    results.append(("book_appointment() next monday", test_book_appointment_next_monday()))
    results.append(("book_appointment() duplicate", test_book_duplicate_should_fail()))
    results.append(("book_appointment() consultation", test_book_with_different_types()))
    
    # Get appointments
    print_section("Get Appointments")
    results.append(("get_upcoming_appointments()", test_get_upcoming_appointments()))
    results.append(("get_upcoming() 24 hours", test_get_upcoming_24_hours()))
    results.append(("get_upcoming() 1 week", test_get_upcoming_one_week()))
    
    # Reschedule
    print_section("Reschedule")
    results.append(("reschedule monday -> wednesday", test_reschedule_to_wednesday()))
    results.append(("reschedule to past (fail)", test_reschedule_to_past_should_fail()))
    
    # Reminder & No-Show
    print_section("Reminder & No-Show")
    results.append(("mark_reminder_sent()", test_mark_reminder_sent()))
    results.append(("mark_no_show()", test_mark_no_show()))
    
    # Cancel
    print_section("Cancel")
    results.append(("cancel_appointment()", test_cancel_appointment()))
    results.append(("cancel nonexistent (fail)", test_cancel_nonexistent()))
    results.append(("cancel already cancelled", test_cancel_already_cancelled()))
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, p in results if p)
    failed = sum(1 for _, p in results if not p)
    total = len(results)
    
    print(f"\n  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {total}")
    
    if failed > 0:
        print(f"\n  Failed tests:")
        for name, result in results:
            if not result:
                print(f"    - {name}")
    
    print(f"\n  {'All tests passed!' if failed == 0 else 'Some tests failed'}")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    run_all_tests()