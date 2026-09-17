import time
import urllib.parse
import threading
import os
import sys
import keyboard
import pyperclip
import tkinter as tk
import winreg
import webview
import pystray
from PIL import Image, ImageDraw

def get_system_theme():
    """Detects Windows device default theme (Dark or Light) automatically."""
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
        return "light" if value == 1 else "dark"
    except Exception:
        return "dark"  # Fallback default

def handle_hotkey():
    """Triggers when Win + / is pressed: releases Win key lock, copies real selection, and opens WinUI 3 prompt."""
    try:
        time.sleep(0.05)
        
        # Force-release Windows key to prevent blocking Ctrl+C
        for key in ('windows', 'left windows', 'right windows', 'win'):
            try:
                keyboard.release(key)
            except:
                pass
                
        time.sleep(0.05)
        pyperclip.copy("")
        
        # Simulate Ctrl+C to grab highlighted text
        keyboard.send('ctrl+c')
        time.sleep(0.2)
        
        selected_text = pyperclip.paste().strip()
        if not selected_text:
            selected_text = "(No text detected. Ensure text is highlighted and try again.)"
            
        root.after(0, lambda: show_prompt_dialog(selected_text))
    except Exception as e:
        print(f"Error capturing text: {e}")

def show_prompt_dialog(selected_text):
    """Creates a native Windows 11 WinUI 3 Fluent Design floating dialog with acrylic styling & smooth feedback."""
    dialog = tk.Toplevel(root)
    dialog.title("Ask AI Assistant")
    dialog.attributes('-topmost', True)
    dialog.geometry("500x280")
    dialog.resizable(False, False)
    
    # State for theme management
    current_theme = tk.StringVar(value=get_system_theme())
    
    # WinUI 3 / Windows 11 Fluent Design System Color Palettes
    themes = {
        "light": {
            "bg": "#f3f3f3",             # Mica Alt Light
            "card": "#ffffff",           # Acrylic Card Fill
            "text": "#191919",           # Text Primary
            "subtext": "#5f5f5f",        # Text Secondary
            "accent": "#0067c0",         # Windows Accent Blue
            "accent_hover": "#005fb8",
            "accent_click": "#004386",
            "entry_bg": "#ffffff",       # Control Fill Default
            "entry_fg": "#191919",
            "border": "#e5e5e5"          # Control Border
        },
        "dark": {
            "bg": "#202020",             # Mica Alt Dark
            "card": "#2c2c2c",           # Acrylic Card Fill Dark
            "text": "#ffffff",           # Text Primary
            "subtext": "#ababab",        # Text Secondary
            "accent": "#60cdff",         # Windows Accent Light Blue
            "accent_hover": "#35b1ff",
            "accent_click": "#0098ff",
            "entry_bg": "#2d2d2d",       # Control Fill Default Dark
            "entry_fg": "#ffffff",
            "border": "#3b3b3b"          # Control Border Dark
        }
    }
    
    main_frame = tk.Frame(dialog)
    main_frame.pack(fill="both", expand=True)
    
    def apply_theme():
        th = themes[current_theme.get()]
        dialog.configure(bg=th["bg"])
        main_frame.configure(bg=th["bg"])
        
        for widget in widget_registry:
            w_type = widget.winfo_class()
            if w_type == 'Frame':
                widget.configure(bg=th["card"] if widget == card_frame else th["bg"])
            elif w_type == 'Label':
                widget.configure(
                    bg=th["card"] if widget.master == card_frame or widget == header_frame else th["bg"],
                    fg=th["text"] if widget in (title_lbl, snippet_lbl) else th["subtext"]
                )
            elif w_type == 'Entry':
                is_ph = entry.get() == placeholder_text and entry.cget('fg') == th["subtext"]
                widget.configure(
                    bg=th["entry_bg"], 
                    fg=th["subtext"] if is_ph else th["entry_fg"], 
                    insertbackground=th["text"]
                )
            elif w_type == 'Button':
                if widget == toggle_btn:
                    toggle_btn.configure(
                        bg=th["entry_bg"], fg=th["text"], 
                        activebackground=th["border"], activeforeground=th["text"]
                    )
                elif widget == submit_btn:
                    submit_btn.configure(
                        bg=th["accent"], fg="#ffffff" if current_theme.get() == "light" else "#000000", 
                        activebackground=th["accent_hover"], activeforeground="#ffffff"
                    )

    def trigger_animation(btn, target_color, original_color):
        """Provides tactile WinUI button press feedback animation."""
        btn.configure(bg=target_color)
        dialog.after(120, lambda: btn.configure(bg=original_color))

    def toggle_theme():
        th_name = current_theme.get()
        new_th = "dark" if th_name == "light" else "light"
        current_theme.set(new_th)
        
        th = themes[new_th]
        toggle_btn.configure(text="Dark Mode 🌙" if new_th == "light" else "Light Mode ☀️")
        trigger_animation(toggle_btn, th["border"], th["entry_bg"])
        apply_theme()

    # WinUI 3 App Header Bar
    header_frame = tk.Frame(main_frame)
    header_frame.pack(fill="x", padx=16, pady=(16, 4))
    
    title_lbl = tk.Label(header_frame, text="✨ Ask AI Assistant", font=("Segoe UI Variable Display", 12, "bold"))
    title_lbl.pack(side="left")
    
    initial_toggle_text = "Dark Mode 🌙" if current_theme.get() == "light" else "Light Mode ☀️"
    toggle_btn = tk.Button(
        header_frame, text=initial_toggle_text, command=toggle_theme,
        font=("Segoe UI Variable", 9), relief="flat", padx=10, pady=4, cursor="hand2"
    )
    toggle_btn.pack(side="right")

    # WinUI 3 Acrylic Card Container for Captured Context
    card_frame = tk.Frame(main_frame, bd=1, relief="solid")
    card_frame.pack(fill="x", padx=16, pady=4)
    
    preview_title = tk.Label(card_frame, text="CAPTURED CONTEXT", font=("Segoe UI Variable", 7, "bold"))
    preview_title.pack(anchor="w", padx=12, pady=(10, 2))
    
    snippet = selected_text[:95] + "..." if len(selected_text) > 95 else selected_text
    snippet_lbl = tk.Label(card_frame, text=snippet, font=("Segoe UI Variable", 9), wraplength=440, justify="left")
    snippet_lbl.pack(anchor="w", padx=12, pady=(0, 10))

    # WinUI 3 Outlined Input Field Section
    input_frame = tk.Frame(main_frame)
    input_frame.pack(fill="x", padx=16, pady=(6, 0))
    
    prompt_lbl = tk.Label(input_frame, text="Prompt to ask AI", font=("Segoe UI Variable", 9, "bold"))
    prompt_lbl.pack(anchor="w", pady=(0, 4))
    
    placeholder_text = "Type instructions or questions about this text..."
    entry = tk.Entry(input_frame, font=("Segoe UI Variable", 10), relief="flat", bd=6)
    entry.pack(fill="x", ipady=4)
    
    def on_focus_in(event):
        th = themes[current_theme.get()]
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg=th["entry_fg"])

    def on_focus_out(event):
        th = themes[current_theme.get()]
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg=th["subtext"])

    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
    # Ensure entry box gets immediate, reliable focus right as window opens
    dialog.after(80, lambda: entry.focus_force())
    
    def on_submit(event=None):
        th = themes[current_theme.get()]
        trigger_animation(submit_btn, th["accent_click"], th["accent"])
        
        user_prompt = entry.get()
        if user_prompt == placeholder_text:
            user_prompt = ""
            
        dialog.destroy()
        
        # Combine selected text inside parentheses with user prompt
        combined_query = f"({selected_text}) {user_prompt}".strip()
        encoded_query = urllib.parse.quote(combined_query)
        target_url = f"http://google.com/ai?q={encoded_query}"
        
        # Open floating web window in 485x475 dimension with text selection & right-click menu enabled (DevTools auto-launch blocked)
        webview.create_window(
            "Ask AI Results", 
            target_url, 
            width=485, 
            height=475, 
            text_select=True
        )
        webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False
        webview.start(debug=True)

    entry.bind("<Return>", on_submit)
    
    # WinUI 3 Action Button Layout
    action_frame = tk.Frame(main_frame)
    action_frame.pack(fill="x", padx=16, pady=12)
    
    submit_btn = tk.Button(
        action_frame, text="Ask AI ➔", command=on_submit,
        font=("Segoe UI Variable", 9, "bold"), relief="flat", cursor="hand2", padx=16, pady=6
    )
    submit_btn.pack(side="right")

    # Global Escape key handler to close popup smoothly
    dialog.bind("<Escape>", lambda e: dialog.destroy())

    widget_registry = [
        main_frame, header_frame, card_frame, input_frame, action_frame,
        title_lbl, preview_title, snippet_lbl, prompt_lbl, entry, toggle_btn, submit_btn
    ]
    
    apply_theme()
    entry.config(fg=themes[current_theme.get()]["subtext"])

def create_tray_image():
    """Generates the Outline Auto Awesome (✨) vector icon precisely mapped for the system tray."""
    # Create a 64x64 high-resolution transparent canvas for crisp rendering
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    # Draw Outline Auto Awesome (✨) paths scaled cleanly onto 64x64 grid from 24x24 specs
    # Primary large sparkle star
    star_1 = [
        (50.6, 24.0), (33.3, 20.0), (29.3, 2.7), (25.3, 20.0), 
        (8.0, 24.0), (25.3, 28.0), (29.3, 45.3), (33.3, 28.0), (50.6, 24.0)
    ]
    # Secondary smaller sparkle star
    star_2 = [
        (30.6, 40.0), (26.6, 32.0), (18.6, 28.0), (26.6, 24.0), 
        (30.6, 16.0), (34.6, 24.0), (42.6, 28.0), (34.6, 32.0), (30.6, 40.0)
    ]
    
    dc.polygon(star_1, fill=(0, 103, 192, 255)) # Windows Accent Blue fill
    dc.polygon(star_2, fill=(96, 205, 255, 255)) # Secondary highlight fill
    
    return image

def setup_tray():
    """Initializes and runs the system tray background service."""
    def on_force_close(icon, item):
        icon.stop()
        os._exit(0)

    tray_menu = pystray.Menu(
        pystray.MenuItem("Force to close this app", on_force_close)
    )
    
    icon = pystray.Icon(
        "AskAIAssistant", 
        create_tray_image(), 
        "AI Text Asker", 
        tray_menu
    )
    icon.run()

# Background service bootstrap
root = tk.Tk()
root.withdraw() 

# Register global shortcut (Win + /)
keyboard.add_hotkey('windows + /', handle_hotkey)

# Start system tray with Auto Awesome icon in a background thread
threading.Thread(target=setup_tray, daemon=True).start()

print("AI Text Asker are running, please keep this terminal open. Highlight text & press Win + /...")

root.mainloop()