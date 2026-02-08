# MomMode Doctor Dashboard

MomMode is an AI calling system for small doctor clinics. This repository contains a doctor-only
dashboard built with React 18, Vite, TypeScript, Tailwind CSS, and React Router. The frontend app
lives in the `frontend/` directory, and the FastAPI backend provides calendar integration and appointment management.

## Features

- Landing, login, and Google Calendar connection screens for clinic onboarding
- Doctor dashboard with live call queue and appointment summaries
- Patients, appointments, and call history views
- Settings area for clinic configuration
- Healthcare-focused color palette and layout

## Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite + Tailwind CSS
- React Router
- Lucide React icons
- Axios for API wiring

**Backend:**
- FastAPI (Python)
- Google Calendar API integration
- OAuth 2.0 authentication

## Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Build for production:

```bash
cd frontend
npm run build
```

Preview the production build:

```bash
cd frontend
npm run preview
```

### Backend

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Configure Google OAuth:
   - Create a project in Google Cloud Console
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials
   - Add `http://localhost:8000/api/auth/google/callback` as an authorized redirect URI
   - Set environment variables:
     ```bash
     export GOOGLE_CLIENT_ID="your-client-id"
     export GOOGLE_CLIENT_SECRET="your-client-secret"
     ```

3. Run the API server:

```bash
python3 -m src.api.main
# or
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

