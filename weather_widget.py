import tkinter as tk
import requests
import datetime

def get_weather():
    try:
        # Step 1: Get your location from IP
        loc = requests.get("https://ipapi.co/json/").json()
        city = loc.get("city", "Unknown")
        lat  = loc.get("latitude")
        lon  = loc.get("longitude")

        # Step 2: Get temperature from Open-Meteo (free, no API key!)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather = requests.get(url).json()
        temp = weather["current_weather"]["temperature"]

        return city, temp
    except:
        return "Unknown", "--"

def update():
    city, temp = get_weather()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    date = datetime.datetime.now().strftime("%d %b %Y")

    time_label.config(text=f"🕐 {now}")
    date_label.config(text=f"📅 {date}")
    temp_label.config(text=f"🌡️ {temp}°C")
    city_label.config(text=f"📍 {city}")

    # Refresh every 60 seconds
    root.after(60000, update)

# --- Window setup ---
root = tk.Tk()
root.title("Weather Widget")
root.overrideredirect(True)          # Remove title bar
root.attributes("-topmost", True)    # Always on top
root.attributes("-alpha", 0.85)      # Slight transparency
root.configure(bg="#1e1e2e")

# --- Position: Bottom-right corner ---
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry(f"200x130+{sw-220}+{sh-160}")

# --- Labels ---
time_label = tk.Label(root, text="🕐 --:--:--", bg="#1e1e2e", fg="white",  font=("Segoe UI", 12, "bold"))
date_label = tk.Label(root, text="📅 --",       bg="#1e1e2e", fg="#aaaaaa", font=("Segoe UI", 9))
temp_label = tk.Label(root, text="🌡️ --°C",     bg="#1e1e2e", fg="#ff9f43", font=("Segoe UI", 14, "bold"))
city_label = tk.Label(root, text="📍 --",       bg="#1e1e2e", fg="#54a0ff", font=("Segoe UI", 9))

time_label.pack(pady=(10,0))
date_label.pack()
temp_label.pack(pady=4)
city_label.pack()

# --- Close on right-click ---
root.bind("<Button-3>", lambda e: root.destroy())

update()
root.mainloop()