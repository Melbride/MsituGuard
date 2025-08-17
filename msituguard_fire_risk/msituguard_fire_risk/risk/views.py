from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.db.models import Avg
from .forms import CitizenReportForm
from .models import PredictionLog, CitizenReport
from .utils import get_openweather, get_recent_fires_count, get_ndvi, compute_fire_risk, categorize_risk

def health(request):
    return JsonResponse({"ok": True})

def index(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    context = {
        "has_location": False,
        "prediction": None,
    }

    if lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return HttpResponseBadRequest("Invalid coordinates")

        context["has_location"] = True
        # Fetch data
        weather = get_openweather(lat, lon)
        ndvi = get_ndvi(lat, lon)
        recent_fires = get_recent_fires_count(lat, lon)

        score = compute_fire_risk(
            temp_c=weather["temp_c"],
            humidity=weather["humidity"],
            wind_speed_ms=weather["wind_speed_ms"],
            rainfall_mm_24h=weather["rainfall_mm_24h"],
            ndvi=ndvi,
            recent_fires=recent_fires
        )
        level, color = categorize_risk(score)

        # Persist
        log = PredictionLog.objects.create(
            lat=lat, lon=lon,
            temperature_c=weather["temp_c"],
            humidity=weather["humidity"],
            wind_speed_ms=weather["wind_speed_ms"],
            rainfall_mm_24h=weather["rainfall_mm_24h"],
            ndvi=ndvi,
            recent_fires=recent_fires,
            risk_score=score,
            risk_level=level
        )

        context["prediction"] = {
            "lat": lat, "lon": lon,
            "weather": weather,
            "ndvi": ndvi,
            "recent_fires": recent_fires,
            "score": round(score, 3),
            "level": level,
            "color": color,
            "timestamp": log.timestamp,
        }
        context["report_form"] = CitizenReportForm(initial={"lat": lat, "lon": lon})

    return render(request, "risk/index.html", context)

def history(request):
    logs = PredictionLog.objects.order_by("-timestamp")[:200]
    # Simple aggregates for the last 7 days
    last7 = PredictionLog.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))
    agg = last7.aggregate(avg_score=Avg("risk_score"))
    return render(request, "risk/history.html", {"logs": logs, "agg": agg})

def submit_report(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    form = CitizenReportForm(request.POST)
    if form.is_valid():
        CitizenReport.objects.create(**form.cleaned_data)
        return redirect("index")
    return HttpResponseBadRequest("Invalid form")
