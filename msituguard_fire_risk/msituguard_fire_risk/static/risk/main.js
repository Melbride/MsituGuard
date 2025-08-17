const detectBtn = document.getElementById("detectBtn");
if (detectBtn) {
  detectBtn.addEventListener("click", () => {
    if (!navigator.geolocation) {
      alert("Geolocation not supported by your browser.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        const url = `/?lat=${latitude}&lon=${longitude}`;
        window.location.href = url;
      },
      (err) => {
        console.error(err);
        alert("Could not get your location. Please allow location access and try again.");
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  });
}
