# 📞 MomMode

**AI Voice Agent for Medical Appointment Scheduling**

CallPilot is an AI-powered voice agent that enables patients to schedule, reschedule, cancel, and manage medical appointments through natural phone conversations — 24/7, with zero setup required.

## 🎯 Features

- **Check Availability** — Query open slots using natural language dates
- **Book Appointments** — Schedule visits with real-time conflict detection
- **Reschedule Appointments** — Move existing bookings seamlessly
- **Cancel Appointments** — Remove bookings with voice confirmation
- **View Upcoming Appointments** — List scheduled visits (patient & staff)
- **Mark No-Show** — Staff-facing operation for missed appointments

## 🏗️ Architecture

```
Patient (Voice Call)
       ↓
ElevenLabs Conversational AI (STT → NLU → Tool Calling → TTS)
       ↓
FastAPI Backend Proxy
       ↓
Google Calendar API (OAuth 2.0)
       ↓
Google Calendar Storage
```

## 🔧 System Architecture Diagram: 
<img src="res/System-diag.png" alt="System Architecture" width="600"/>

## 🎭 Use Case Diagram: 
<img src="res/use-case-diag.png" alt="System Architecture"/>

## 🛠️ Tech Stack

| Technology | Role |
|-----------|------|
| **ElevenLabs Conversational AI** | Speech-to-text, NLU, tool calling, text-to-speech |
| **FastAPI** | Backend proxy exposing scheduling functions as callable tools |
| **Google Calendar API** | Real-time availability, event CRUD, conflict detection |
| **OAuth 2.0** | Secure Google Calendar authentication |
| **dateparser** | Natural language date parsing |
| **Python 3.10+** | Core language |

## 📄 API Endpoints

### Auth
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calendar/status` | GET | Check Google Calendar connection status |
| `/api/calendar/auth-url` | GET | Get Google OAuth authorization URL |
| `/api/calendar/auth-callback` | POST/GET | Handle OAuth callback and exchange code for tokens |
| `/api/calendar/disconnect` | DELETE | Disconnect Google Calendar |

### Availability
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calendar/check-availability` | POST | Check open slots for a single date (supports natural language) |
| `/api/calendar/check-availability-range` | POST | Check available slots across multiple dates |

### Appointments
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calendar/appointments` | POST | Book a new appointment |
| `/api/calendar/appointments` | GET | List upcoming appointments (optional `hours_ahead` filter) |
| `/api/calendar/appointments/{id}` | GET | Get a specific appointment |
| `/api/calendar/appointments/{id}` | PATCH | Reschedule an existing appointment |
| `/api/calendar/appointments/{id}` | DELETE | Cancel an appointment |
| `/api/calendar/appointments/{id}/remind` | PATCH | Mark reminder sent |
| `/api/calendar/appointments/{id}/no-show` | PATCH | Mark appointment as no-show |

### Raw Events
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calendar/events` | GET | Get raw calendar events (optional `time_min`/`time_max` filters) |

## 📋 Prerequisites

- Python 3.10+
- Google Cloud project with Calendar API enabled
- Google OAuth 2.0 credentials (`credentials.json`)
- ElevenLabs API key with Conversational AI access

## 🚀 Setup

### 1. Clone and install
```bash
git clone https://github.com/<your-username>/mommode.git
cd callpilot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
Create a `.env` file in the project root:
```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key
GOOGLE_CALENDAR_ID=your_calendar_id
```

### 3. Set up Google OAuth
Place your `credentials.json` from Google Cloud Console in the project root. On first run, you'll be prompted to authorize — this generates `token.json`.

### 4. Run
```bash
uvicorn service:app --reload --port 8000
```
