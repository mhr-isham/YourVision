import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class YourVisionLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("YourVision - Computer Vision Games & Tools")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="YourVision", 
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Computer Vision Games & Tools",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Applications list
        self.apps = [
            {
                "name": "BlurFace",
                "file": "BlurFace.py",
                "description": "Privacy tool that detects and blurs faces in real-time",
                "icon": "🎭"
            },
            {
                "name": "HandMouse",
                "file": "HandMouse.py",
                "description": "Control your mouse using hand gestures",
                "icon": "👆"
            },
            {
                "name": "DanceWithMe",
                "file": "DanceWithMe.py",
                "description": "Your dance moves mimicked by a stickman",
                "icon": "💃"
            },
            {
                "name": "FoodEater",
                "file": "FoodEater.py",
                "description": "Eat foods by opening your mouth - a fun game!",
                "icon": "🍕"
            },
            {
                "name": "MyAvatar",
                "file": "MyAvatar.py",
                "description": "Create cartoonized or stylized avatars",
                "icon": "🎨"
            },
            {
                "name": "Red Light Green Light",
                "file": "Red_Light_Green_Light.py",
                "description": "Squid Game inspired movement detection game",
                "icon": "🚦"
            }
        ]
        
        # Create buttons for each app
        for app in self.apps:
            self.create_app_button(main_frame, app)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, pady=(20, 0))
        
        info_label = tk.Label(
            footer_frame,
            text="Tip: Make sure your camera is connected and accessible",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        info_label.pack()
        
        exit_btn = ttk.Button(
            footer_frame,
            text="Exit",
            command=self.root.quit,
            width=15
        )
        exit_btn.pack(pady=(10, 0))
    
    def create_app_button(self, parent, app):
        # Container for each app button
        btn_frame = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Make the frame clickable
        btn_frame.bind("<Button-1>", lambda e: self.launch_app(app))
        btn_frame.bind("<Enter>", lambda e: btn_frame.config(bg="#ecf0f1"))
        btn_frame.bind("<Leave>", lambda e: btn_frame.config(bg="white"))
        
        # Icon and name
        header_frame = tk.Frame(btn_frame, bg="white")
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        header_frame.bind("<Button-1>", lambda e: self.launch_app(app))
        
        icon_label = tk.Label(
            header_frame,
            text=app["icon"],
            font=("Arial", 20),
            bg="white"
        )
        icon_label.pack(side=tk.LEFT)
        icon_label.bind("<Button-1>", lambda e: self.launch_app(app))
        
        name_label = tk.Label(
            header_frame,
            text=app["name"],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        name_label.pack(side=tk.LEFT, padx=(10, 0))
        name_label.bind("<Button-1>", lambda e: self.launch_app(app))
        
        # Description
        desc_label = tk.Label(
            btn_frame,
            text=app["description"],
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
            anchor="w"
        )
        desc_label.pack(fill=tk.X, padx=10, pady=(0, 5))
        desc_label.bind("<Button-1>", lambda e: self.launch_app(app))
    
    def launch_app(self, app):
        try:
            # Check if file exists
            if not os.path.exists(app["file"]):
                messagebox.showerror(
                    "Error",
                    f"Could not find {app['file']}\nMake sure all files are in the same directory."
                )
                return
            
            # Launch the application
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, app["file"]], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, app["file"]])
            
            messagebox.showinfo(
                "Launching",
                f"{app['name']} is starting...\nCheck the new window that opened."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {app['name']}:\n{str(e)}")

def main():
    root = tk.Tk()
    app = YourVisionLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
