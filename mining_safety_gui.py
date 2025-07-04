import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import csv
import sys

class SafetySensor:
    def __init__(self, sensor_id, location, threshold, critical_threshold=None):
        self.sensor_id = sensor_id
        self.location = location
        self.threshold = threshold
        self.critical_threshold = critical_threshold
        self.current_value = 0
    
    def update_reading(self, new_value):
        self.current_value = new_value
    
    def check_status(self):
        if self.critical_threshold and self.current_value > self.critical_threshold:
            return "CRITICAL"
        elif self.current_value > self.threshold:
            return "WARNING"
        else:
            return "NORMAL"

class AlertSystem:
    def __init__(self):
        self.alerts = []
        self.critical_count = 0
        self.warning_count = 0
    
    def add_alert(self, sensor):
        status = sensor.check_status()
        if status == "CRITICAL":
            alert_msg = f"🚨 CRITICAL: {sensor.sensor_id} at {sensor.location} ({sensor.current_value})"
            self.alerts.append(("CRITICAL", alert_msg))
            self.critical_count += 1
        elif status == "WARNING":
            alert_msg = f"⚠️ WARNING: {sensor.sensor_id} at {sensor.location} ({sensor.current_value})"
            self.alerts.append(("WARNING", alert_msg))
            self.warning_count += 1
    
    def clear_alerts(self):
        self.alerts = []
        self.critical_count = 0
        self.warning_count = 0

class MiningSafetyApp:
    def __init__(self, root):
        self.root = root
        self.setup_emoji_support()
        self.root.title("⛏️ Mining Safety Monitoring 🚨")
        self.root.geometry("900x650")
        
        # Initialize sensors
        self.methane_sensor = SafetySensor("CH4-001", "Tunnel A", 1.0, 2.0)
        self.temp_sensor = SafetySensor("TEMP-001", "Tunnel B", 40, 45)
        self.air_sensor = SafetySensor("AIR-001", "Tunnel C", 19, 17)
        self.sensors = [self.methane_sensor, self.temp_sensor, self.air_sensor]
        self.alert_system = AlertSystem()
        
        self.create_widgets()
    
    def setup_emoji_support(self):
        """Configure emoji fonts for different operating systems"""
        if sys.platform == 'win32':
            self.emoji_font = ('Segoe UI Emoji', 12)
        elif sys.platform == 'darwin':  # Mac
            self.emoji_font = ('Apple Color Emoji', 12) 
        else:  # Linux
            self.emoji_font = ('Noto Color Emoji', 12)
        
        # Testing
        try:
            test_label = tk.Label(self.root, text="🚨⚠️✅", font=self.emoji_font)
            test_label.pack()
            self.root.after(100, test_label.destroy)
            self.use_emojis = True
        except:
            self.emoji_font = ('Arial', 12)
            self.use_emojis = False
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = "⛏️ Mining Safety Monitoring System 🚨" if self.use_emojis else "Mining Safety Monitoring System"
        ttk.Label(main_frame, text=title, font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Sensor displays
        self.sensor_frames = []
        for i, sensor in enumerate(self.sensors):
            frame = ttk.LabelFrame(main_frame, text=f"{sensor.sensor_id} - {sensor.location}")
            frame.grid(row=1, column=i, padx=10, pady=10, sticky="nsew")
            
            ttk.Label(frame, text="Current Value:").pack()
            value_label = ttk.Label(frame, text="0", font=('Helvetica', 14))
            value_label.pack()
            
            ttk.Label(frame, text="Status:").pack()
            status_label = tk.Label(frame, text="NORMAL", font=self.emoji_font)
            status_label.pack()
            
            self.sensor_frames.append({
                'frame': frame,
                'value_label': value_label,
                'status_label': status_label
            })
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, 
                  text="⚡ Run Simulation" if self.use_emojis else "Run Simulation", 
                  command=self.run_simulation).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="📋 View Alerts" if self.use_emojis else "View Alerts", 
                  command=self.view_alerts).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="💾 Export Logs" if self.use_emojis else "Export Logs", 
                  command=self.export_logs).pack(side=tk.LEFT, padx=5)
        
        # Alert display
        self.alert_text = tk.Text(main_frame, height=10, width=80, state=tk.DISABLED, font=self.emoji_font)
        self.alert_text.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Configure grid columns
        for i in range(3):
            main_frame.columnconfigure(i, weight=1)
    
    def update_sensor_display(self):
        for i, sensor in enumerate(self.sensors):
            status = sensor.check_status()
            self.sensor_frames[i]['value_label'].config(text=f"{sensor.current_value}")
            
            # status
            if self.use_emojis:
                status_emoji = {
                    "CRITICAL": "🔴 CRITICAL",
                    "WARNING": "🟠 WARNING",
                    "NORMAL": "🟢 NORMAL"
                }.get(status, "❓ UNKNOWN")
            else:
                status_emoji = status
            
            self.sensor_frames[i]['status_label'].config(
                text=status_emoji,
                foreground='red' if status == "CRITICAL" else 
                          'orange' if status == "WARNING" else 'green'
            )
    
    def run_simulation(self):
        self.alert_system.clear_alerts()
        
        # Generate random readings
        self.methane_sensor.update_reading(round(random.uniform(0.5, 2.5), 2))
        self.temp_sensor.update_reading(random.randint(35, 47))
        self.air_sensor.update_reading(random.randint(16, 21))
        
        # Check sensors
        for sensor in self.sensors:
            self.alert_system.add_alert(sensor)
        
        self.update_sensor_display()
        self.update_alert_display()
        
        # Show critical alerts
        if self.alert_system.critical_count > 0:
            self.show_critical_alert()
    
    def update_alert_display(self):
        self.alert_text.config(state=tk.NORMAL)
        self.alert_text.delete(1.0, tk.END)
        
        if not self.alert_system.alerts:
            status_msg = "✅ All systems normal" if self.use_emojis else "All systems normal"
            self.alert_text.insert(tk.END, status_msg)
        else:
            # Headers
            crit_header = f"🚨 CRITICAL alerts: {self.alert_system.critical_count}\n" if self.use_emojis else f"CRITICAL alerts: {self.alert_system.critical_count}\n"
            warn_header = f"⚠️ WARNING alerts: {self.alert_system.warning_count}\n\n" if self.use_emojis else f"WARNING alerts: {self.alert_system.warning_count}\n\n"
            
            self.alert_text.insert(tk.END, crit_header)
            self.alert_text.insert(tk.END, warn_header)
            
            # Individual alerts
            for severity, alert in self.alert_system.alerts:
                if severity == "CRITICAL":
                    prefix = "🚨 " if self.use_emojis else "CRITICAL: "
                else:
                    prefix = "⚠️ " if self.use_emojis else "WARNING: "
                self.alert_text.insert(tk.END, prefix + alert + "\n")
        
        self.alert_text.config(state=tk.DISABLED)
    
    def show_critical_alert(self):
        popup = tk.Toplevel()
        popup.title("‼️ CRITICAL ALERT ‼️" if self.use_emojis else "CRITICAL ALERT")
        
        # Main warning
        if self.use_emojis:
            tk.Label(popup, text="🚨🚨🚨", font=('Segoe UI Emoji', 48)).pack(pady=10)
        
        tk.Label(popup, 
                text="DANGEROUS CONDITIONS DETECTED!", 
                font=('Helvetica', 14, 'bold')).pack()
        
        # Affected sensors
        for severity, alert in self.alert_system.alerts:
            if severity == "CRITICAL":
                tk.Label(popup, text=alert, font=('Helvetica', 12)).pack()
        
        # Action required
        if self.use_emojis:
            tk.Label(popup, text="👉 Evacuate immediately 👈", font=self.emoji_font).pack(pady=10)
        else:
            tk.Label(popup, text="Evacuate immediately", font=('Helvetica', 12)).pack(pady=10)
        
        # Close button
        btn_text = "🆗 Acknowledge" if self.use_emojis else "Acknowledge"
        ttk.Button(popup, text=btn_text, command=popup.destroy).pack(pady=10)
    
    def view_alerts(self):
        if not self.alert_system.alerts:
            messagebox.showinfo("Alerts", "No active alerts")
        else:
            self.update_alert_display()
    
    def export_logs(self):
        filename = "mining_alerts.csv"
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for severity, alert in self.alert_system.alerts:
                    
                    clean_alert = alert.replace("🚨", "").replace("⚠️", "").strip()
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        severity,
                        clean_alert
                    ])
            messagebox.showinfo("Success", f"Alerts exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs: {str(e)}")

if __name__ == "__main__":
    
    if sys.platform == 'win32':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    
    root = tk.Tk()
    app = MiningSafetyApp(root)
    root.mainloop()