CallPilot - AI Voice Agent for Medical Appointments
Overview
CallPilot is a voice-first AI assistant powered by ElevenLabs that handles medical appointment scheduling through natural phone conversations. Patients call to book, cancel, or reschedule appointments. All data is stored directly in Google Calendar events.

Features
Patient Features (Voice Interface)

📞 Schedule Appointment - Call and book with natural conversation
❌ Cancel Appointment - Call to cancel existing appointments
🔄 Reschedule Appointment - Change appointment times via phone
⏰ Automated Reminders - Receive AI call 3 hours before appointment

Doctor Features (Google Calendar)

📅 Manage Availability - Set available hours in Google Calendar
👀 View Appointments - See all bookings in Google Calendar
⚠️ Mark No-Shows - Update event status to trigger follow-up

Booking flow

1. Patient calls Twilio number
   ↓
2. Twilio forwards to ElevenLabs agent
   ↓
3. Agent: "How can I help you?"
   Patient: "I need to book an appointment"
   ↓
4. Agent asks: "What date works for you?"
   Patient: "Next Tuesday"
   ↓
5. Agent calls: check_availability(date="2026-02-11")
   ↓
6. Backend queries Google Calendar Free/Busy
   ↓
7. Returns available slots: [2:00 PM, 3:00 PM, 4:00 PM]
   ↓
8. Agent: "I have 2 PM, 3 PM, or 4 PM"
   Patient: "2 PM"
   ↓
9. Agent calls: book_appointment(name, phone, datetime)
   ↓
10. Backend creates Google Calendar event with patient details
    ↓
11. Backend sends SMS confirmation via Twilio
    ↓
12. Agent: "You're all set! Check your texts for confirmation"

Reminder flow

1. Cron job runs every 15 minutes
   ↓
2. Queries Google Calendar for events 3 hours ahead
   ↓
3. Finds appointment: John Doe at 2:00 PM
   ↓
4. Extracts phone number from event metadata
   ↓
5. Triggers ElevenLabs outbound call
   ↓
6. Patient answers phone
   ↓
7. Agent: "Hi John, reminder about your 2 PM appointment today"
   ↓
8. Patient: "Yes, I'll be there"
   ↓
9. Agent: "Great! See you then"
   ↓
10. Backend updates event description: "Reminder Sent: true"

How It Works
Data Storage in Google Calendar
Available Slots:

Doctor blocks "Available for Appointments" in calendar
System queries free/busy status

Booked Appointments:
Event Title: "Appointment: John Doe"
Start Time: 2:00 PM
Duration: 30 minutes
Description:
Patient: John Doe
Phone: +1234567890
Type: Checkup
Status: scheduled
Reminder Sent: false
1. Patient Books Appointment
   Patient calls → ElevenLabs agent → Queries Google Calendar free/busy → Shows available slots → Patient selects → Creates calendar event with patient details → SMS confirmation
2. Automated 3-Hour Reminder
   Cron job runs every 15 minutes → Queries Google Calendar events 3 hours ahead → Triggers outbound call → Patient confirms/reschedules → Updates event metadata
3. Doctor Manages Schedule
   Doctor uses Google Calendar → Blocks available hours → System respects free/busy times → All bookings appear as calendar events
4. No-Show Handling
   Doctor updates event description to "Status: no_show" → System detects change → Automatically calls patient to reschedule → Deletes/updates event
