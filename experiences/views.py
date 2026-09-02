from django.shortcuts import render

def app_view(request):
    return render(request, "app.html")

def manifest_view(request):
    return render(request, "manifest.json", content_type="application/manifest+json")

def service_worker_view(request):
    # Served at the root path (not /static/) so its scope covers the whole app —
    # a service worker can only control paths at or below the URL it's served from.
    return render(request, "sw.js", content_type="application/javascript")
