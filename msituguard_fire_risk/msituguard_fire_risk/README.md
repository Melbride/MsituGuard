# MsituGuard · Fire Risk (Django)

A minimal, data-driven fire risk dashboard for MsituGuard. It auto-detects user location in the browser, fetches live weather from OpenWeather, (optionally) checks recent fires (NASA FIRMS), and computes an interpretable fire risk score with colored categories. Predictions are stored for history & trends.

## Features
- One-click **Use my location** (HTML5 Geolocation).
- Live weather via **OpenWeather** (temperature, humidity, wind, recent rain estimate).
- Optional hook for **NASA FIRMS** recent fire proximity.
- Optional NDVI integration placeholder via **Google Earth Engine**.
- Heuristic **risk score** (0–1) and **levels** (LOW/MODERATE/HIGH/EXTREME).
- Persists predictions to SQLite, lists recent history.
- Simple citizen **Community Report** form (smoke/heat/flames/smell/other).

## Quickstart

1) Create a virtualenv and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) Configure environment:
```bash
cp .env.example .env
# Edit .env and set OPENWEATHER_API_KEY
```

3) Initialize DB and run:
```bash
python manage.py migrate
python manage.py runserver
```

4) Open http://127.0.0.1:8000 and click **Use my location**.

## Notes

- **OpenWeather**: We use the `/data/2.5/weather` endpoint. Rainfall for the last 24h is estimated from 1h/3h fields if available (simple multiplier).
- **NASA FIRMS**: Function is stubbed to `0` unless you add your FIRMS API details in `risk/utils.py`.
- **NDVI (GEE)**: `risk/utils.py:get_ndvi` returns `None`. Replace it with your Google Earth Engine implementation once you have credentials.
- **Security**: This demo uses `DEBUG=1`. Do not deploy like this.

## Admin
Create a superuser to view logs in the admin:
```bash
python manage.py createsuperuser
```

## Roadmap
- Real NDVI via GEE or Sentinel Hub.
- Proper FIRMS proximity using user radius and date window.
- Forecast risk (next 24–72h) using OpenWeather One Call.
- Charts for trends.
