"""
Calendar service implementing Backend Proxy Pattern.

Flow:
1. ElevenLabs agent calls tool endpoint
2. This service receives the call
3. Calls our Calendar API endpoints
4. Returns results to ElevenLabs agent
"""

import requests
from datetime import datetime
from typing import Optional, Dict, List, Any

# Base URL for our Calendar API (running on same machine)
CALENDAR_API_BASE_URL = "http://localhost:8000"


class CalendarServiceError(Exception):
    """Raised when calendar operations fail"""
    pass


def call_calendar_api(
    method: str,
    endpoint: str,
    json_data: dict = None,
    params: dict = None
) -> Dict[str, Any]:
    """
    Make HTTP request to our Calendar API.
    
    Args:
        method: HTTP method (GET, POST, PATCH, DELETE)
        endpoint: API endpoint (e.g., "/api/calendar/check-availability")
        json_data: JSON body for POST/PATCH requests
        params: Query parameters for GET requests
    
    Returns:
        dict: API response
    """
    url = f"{CALENDAR_API_BASE_URL}{endpoint}"
    
    try:
        response = requests.request(
            method=method,
            url=url,
            json=json_data,
            params=params,
            timeout=10
        )
        
        data = response.json()
        
        if response.status_code >= 400:
            raise CalendarServiceError(data.get("detail", "API error"))
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise CalendarServiceError(f"Failed to connect to Calendar API: {e}")


def check_availability(
    date: str,
    duration_minutes: Optional[int] = None
) -> Dict[str, Any]:
    """
    Check doctor's calendar availability for a given date.
    
    Called by ElevenLabs agent tool: check_calendar_availability
    
    Args:
        date: Date to check (YYYY-MM-DD or natural language like "tomorrow")
        duration_minutes: Optional appointment duration
    
    Returns:
        dict: Available slots or error
    """
    try:
        body = {"date": date}
        if duration_minutes:
            body["duration_minutes"] = duration_minutes
        
        result = call_calendar_api(
            method="POST",
            endpoint="/api/calendar/check-availability",
            json_data=body
        )
        
        slots = result.get("available_slots", [])
        
        return {
            "success": True,
            "date": result.get("date"),
            "formatted_date": result.get("formatted_date"),
            "available_slots": [
                {"time": slot["formatted_time"], "start": slot["start"]}
                for slot in slots
            ],
            "total_slots": len(slots),
            "message": result.get("message")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}


def check_availability_range(
    dates: List[str],
    duration_minutes: Optional[int] = None
) -> Dict[str, Any]:
    """
    Check availability across multiple dates.
    
    Args:
        dates: List of dates to check (e.g., ["tomorrow", "next monday"])
        duration_minutes: Optional appointment duration
    
    Returns:
        dict: Available slots for each date
    """
    try:
        body = {"dates": dates}
        if duration_minutes:
            body["duration_minutes"] = duration_minutes
        
        result = call_calendar_api(
            method="POST",
            endpoint="/api/calendar/check-availability-range",
            json_data=body
        )
        
        return {
            "success": True,
            "dates": result.get("dates", []),
            "total_slots": result.get("total_slots", 0),
            "message": result.get("message")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}


def book_appointment(
    patient_name: str,
    patient_phone: str,
    appointment_datetime: str,
    patient_email: Optional[str] = None,
    appointment_type: str = "checkup",
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Book an appointment.
    
    Called by ElevenLabs agent tool: book_appointment
    
    Args:
        patient_name: Patient's full name
        patient_phone: Patient's phone number
        appointment_datetime: ISO format datetime (e.g., "2026-02-15T14:00:00-05:00")
        patient_email: Optional email
        appointment_type: Type of appointment (checkup, consultation, follow_up)
        notes: Optional notes
    
    Returns:
        dict: Booking confirmation
    """
    try:
        body = {
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "appointment_datetime": appointment_datetime,
            "appointment_type": appointment_type
        }
        if patient_email:
            body["patient_email"] = patient_email
        if notes:
            body["notes"] = notes
        
        result = call_calendar_api(
            method="POST",
            endpoint="/api/calendar/appointments",
            json_data=body
        )
        
        appointment = result.get("appointment", {})
        
        return {
            "success": True,
            "confirmation_id": result.get("confirmation_id"),
            "appointment_date": appointment.get("formatted_date"),
            "appointment_time": appointment.get("formatted_time"),
            "message": result.get("message")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}


def cancel_appointment(appointment_id: str) -> Dict[str, Any]:
    """
    Cancel an appointment.
    
    Args:
        appointment_id: The appointment/event ID to cancel
    
    Returns:
        dict: Cancellation result
    """
    try:
        result = call_calendar_api(
            method="DELETE",
            endpoint=f"/api/calendar/appointments/{appointment_id}"
        )
        
        return {
            "success": True,
            "message": result.get("message", "Appointment cancelled successfully")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}


def reschedule_appointment(
    appointment_id: str,
    new_datetime: str
) -> Dict[str, Any]:
    """
    Reschedule an appointment to a new time.
    
    Args:
        appointment_id: The appointment/event ID to reschedule
        new_datetime: New ISO format datetime
    
    Returns:
        dict: Rescheduling result
    """
    try:
        result = call_calendar_api(
            method="PATCH",
            endpoint=f"/api/calendar/appointments/{appointment_id}",
            json_data={"new_datetime": new_datetime}
        )
        
        appointment = result.get("appointment", {})
        
        return {
            "success": True,
            "new_date": appointment.get("formatted_date"),
            "new_time": appointment.get("formatted_time"),
            "message": result.get("message")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}


def get_upcoming_appointments(hours_ahead: Optional[int] = None) -> Dict[str, Any]:
    """
    Get upcoming appointments.
    
    Args:
        hours_ahead: Optional filter for appointments within N hours
    
    Returns:
        dict: List of upcoming appointments
    """
    try:
        params = {}
        if hours_ahead:
            params["hours_ahead"] = hours_ahead
        
        result = call_calendar_api(
            method="GET",
            endpoint="/api/calendar/appointments",
            params=params
        )
        
        appointments = result.get("appointments", [])
        
        return {
            "success": True,
            "appointments": [
                {
                    "id": apt.get("id"),
                    "patient_name": apt.get("patient", {}).get("name"),
                    "date": apt.get("formatted_date"),
                    "time": apt.get("formatted_time"),
                    "status": apt.get("status")
                }
                for apt in appointments
            ],
            "total": len(appointments)
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e), "appointments": []}


def mark_reminder_sent(appointment_id: str) -> Dict[str, Any]:
    """
    Mark that a reminder was sent for an appointment.
    
    Args:
        appointment_id: The appointment ID
    
    Returns:
        dict: Result
    """
    try:
        result = call_calendar_api(
            method="PATCH",
            endpoint=f"/api/calendar/appointments/{appointment_id}/remind"
        )
        
        return {
            "success": True,
            "message": result.get("message")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}


def mark_no_show(appointment_id: str) -> Dict[str, Any]:
    """
    Mark an appointment as no-show.
    
    Args:
        appointment_id: The appointment ID
    
    Returns:
        dict: Result
    """
    try:
        result = call_calendar_api(
            method="PATCH",
            endpoint=f"/api/calendar/appointments/{appointment_id}/no-show"
        )
        
        return {
            "success": True,
            "status": "no_show",
            "message": result.get("message")
        }
        
    except CalendarServiceError as e:
        return {"success": False, "error": str(e)}