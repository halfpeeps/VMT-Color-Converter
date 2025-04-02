import tkinter as tk
from tkinter import messagebox
import webbrowser
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

boost_factor = 2.1

def perceptual_color_to_color2(r, g, b, boost=2.1):
    def adjust(c):
        normalized = c / 255
        boosted = pow(normalized, 1 / boost)
        return round(min(boosted, 1.0), 3)
    return tuple(adjust(c) for c in (r, g, b))

def color2_to_perceptual_color(r_norm, g_norm, b_norm, boost=2.1):
    def reverse_adjust(c):
        boosted = pow(c, boost) * 255
        return int(min(255, max(0, round(boosted))))
    return tuple(reverse_adjust(c) for c in (r_norm, g_norm, b_norm))

def convert_color(event=None):
    r, g, b = safe_get_rgb()
    color2 = perceptual_color_to_color2(r, g, b, boost_factor)
    result_var.set(f'$color2 "[{color2[0]} {color2[1]} {color2[2]}]"')
    update_color_preview(r, g, b, color2)
    update_vmt_snippet(color2)

def convert_backwards():
    try:
        r = float(entry_c2_r.get())
        g = float(entry_c2_g.get())
        b = float(entry_c2_b.get())
        r, g, b = max(0, min(r, 1)), max(0, min(g, 1)), max(0, min(b, 1))
        color = color2_to_perceptual_color(r, g, b, boost_factor)
        entry_r.delete(0, tk.END)
        entry_g.delete(0, tk.END)
        entry_b.delete(0, tk.END)
        entry_r.insert(0, str(color[0]))
        entry_g.insert(0, str(color[1]))
        entry_b.insert(0, str(color[2]))
        convert_color()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid $color2 float values (0–1)")

def update_color_preview(r, g, b, color2):
    def unboost(c):
        return int(min(255, pow(c, boost_factor) * 255))
    c2_rgb = tuple(unboost(c) for c in color2)
    output_color = f'#{c2_rgb[0]:02x}{c2_rgb[1]:02x}{c2_rgb[2]:02x}'
    color_preview.config(bg=output_color)
    color_preview.after(10, lambda: color_preview.config(highlightbackground=output_color))

def update_boost(val):
    global boost_factor
    boost_factor = float(val)
    convert_color()

def copy_to_clipboard():
    result = result_var.get()
    if result.startswith("$color2"):
        root.clipboard_clear()
        root.clipboard_append(result)
        clipboard_message.config(text="Copied!", fg="lime")
        root.after(2000, lambda: clipboard_message.config(text=""))

def safe_get_rgb():
    try:
        r = int(entry_r.get()) if entry_r.get() else 0
        g = int(entry_g.get()) if entry_g.get() else 0
        b = int(entry_b.get()) if entry_b.get() else 0
        return max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255))
    except:
        return 0, 0, 0

def update_vmt_snippet(color2):
    vmt_text = f'''VertexLitGeneric
{{
    $basetexture "models/debug/debugwhite"
    $color2 "[{color2[0]} {color2[1]} {color2[2]}]"
    $model 1
}}'''
    vmt_box.config(state="normal")
    vmt_box.delete("1.0", tk.END)
    vmt_box.insert(tk.END, vmt_text)
    vmt_box.config(state="disabled")

def toggle_advanced():
    if advanced_var.get():
        boost_slider.grid()
        reverse_label.grid()
        entry_c2_r.grid()
        entry_c2_g.grid()
        entry_c2_b.grid()
        reverse_button.grid()
    else:
        boost_slider.grid_remove()
        reverse_label.grid_remove()
        entry_c2_r.grid_remove()
        entry_c2_g.grid_remove()
        entry_c2_b.grid_remove()
        reverse_button.grid_remove()

def open_about():
    about = tk.Toplevel(root)
    about.title("About")
    about.resizable(False, False)
    about.configure(bg=dark_bg)
    tk.Label(about, text="Created by peeps", fg=light_fg, bg=dark_bg).pack(pady=(10, 0))
    tk.Label(about, text="Version: 0.0.7", fg=light_fg, bg=dark_bg).pack(pady=(10, 0))
    tk.Label(about, text="Contact:", fg=light_fg, bg=dark_bg).pack()
    btn_frame = tk.Frame(about, bg=dark_bg)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Steam", width=12, command=lambda: webbrowser.open("https://steamcommunity.com/id/halfpeeps/")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Forums", width=12, command=lambda: webbrowser.open("https://perpheads.com/members/peeps.10255/")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="GitHub", width=12, command=lambda: webbrowser.open("https://github.com/halfpeeps/VMT-Color-Converter")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Web Version", width=12, command=lambda: webbrowser.open("https://halfpeeps.github.io/VMT-Color-Converter/")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Addon Version", width=12, command=lambda: webbrowser.open("https://steamcommunity.com/sharedfiles/filedetails/?id=3456942097")).pack(side="left", padx=5)

#tooltip
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + cy + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#333", foreground="#fff",
            relief="solid", borderwidth=1,
            font=("TkDefaultFont", 9), padx=5, pady=2
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


# GUI setup
dark_bg = "#1e1e1e"
light_fg = "#f0f0f0"
entry_bg = "#2c2c2c"
button_bg = "#3a3a3a"
outline = "#555"

font_main = ("Segoe UI", 11)
font_heading = ("Segoe UI", 12, "bold")

root = tk.Tk()
root.title("VMT $color Converter")
root.iconbitmap(resource_path("vmt_color_converter.ico"))
root.configure(bg=dark_bg)
root.resizable(False, False)

frame = tk.Frame(root, bg=dark_bg, padx=20, pady=20)
frame.pack()

for i, channel in enumerate("RGB"):
    tk.Label(frame, text=channel, bg=dark_bg, fg=light_fg, font=("Segoe UI", 14)).grid(row=0, column=i, padx=10)

entry_r = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg,
                   justify="center", relief="flat", font=font_main, highlightthickness=1, highlightbackground=outline)
entry_g = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg,
                   justify="center", relief="flat", font=font_main, highlightthickness=1, highlightbackground=outline)
entry_b = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg,
                   justify="center", relief="flat", font=font_main, highlightthickness=1, highlightbackground=outline)
entry_r.grid(row=1, column=0, padx=10)
entry_g.grid(row=1, column=1, padx=10)
entry_b.grid(row=1, column=2, padx=10)

for entry in (entry_r, entry_g, entry_b):
    entry.bind("<KeyRelease>", convert_color)
    entry.bind("<Return>", convert_color)

tk.Label(frame, text="$color2", fg=light_fg, bg=dark_bg, font=font_heading).grid(row=2, column=0, columnspan=3, pady=(20, 0))
result_var = tk.StringVar()
tk.Entry(frame, textvariable=result_var, width=35, state="readonly", justify="center",
         bg=entry_bg, fg=light_fg, readonlybackground=entry_bg, relief="flat",
         font=font_main, highlightthickness=1, highlightbackground=outline).grid(row=3, column=0, columnspan=3, pady=5)

clipboard_message = tk.Label(frame, text="", fg="lime", bg=dark_bg, font=font_main)
clipboard_message.grid(row=4, column=0, columnspan=3)

#copy
tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard, bg=button_bg, fg=light_fg,
          relief="flat", font=font_main, activebackground=button_bg).grid(row=5, column=0, columnspan=3, pady=(5, 15))

#snippit
tk.Label(frame, text="VMT SNIPPET", fg=light_fg, bg=dark_bg, font=font_heading).grid(row=6, column=0, columnspan=3)

vmt_box = tk.Text(frame, height=6, width=35, wrap="none", bg=entry_bg, fg=light_fg,
                 relief="flat", font=("Consolas", 10), highlightthickness=1, highlightbackground=outline)
vmt_box.grid(row=7, column=0, columnspan=3, pady=5)
vmt_box.config(state="disabled")

color_preview = tk.Label(frame, text="PREVIEW", font=("Segoe UI", 20, "bold"), width=20, height=10,
                         bg=dark_bg, fg=light_fg, relief="flat", bd=2, highlightthickness=2, highlightbackground=outline)
color_preview.grid(row=0, column=3, rowspan=8, padx=(40, 0), pady=10)

#advanced check
advanced_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Advanced", variable=advanced_var, command=toggle_advanced,
               bg=dark_bg, fg=light_fg, selectcolor=dark_bg, relief="flat", font=font_main).grid(row=8, column=0, columnspan=2, sticky="w")

boost_slider = tk.Scale(frame, from_=1.0, to=3.0, resolution=0.05, orient="horizontal", command=update_boost,
                        bg=dark_bg, fg=light_fg, highlightbackground=dark_bg, relief="flat")
boost_slider.set(boost_factor)
boost_slider.grid(row=9, column=0, columnspan=3)
boost_slider.grid_remove()
ToolTip(boost_slider, text="How much the intensity is boosted to match the color between shaders (default: 2.1)")

tk.Button(frame, text="ABOUT", command=open_about, bg=button_bg, fg=light_fg,
          relief="flat", font=font_main, activebackground=button_bg).grid(row=9, column=3, sticky="e")

#reverse
reverse_label = tk.Label(frame, text="Reverse: $color2 → $color", fg=light_fg, bg=dark_bg, font=font_heading)
reverse_label.grid(row=10, column=0, columnspan=3, pady=(20, 0))
reverse_label.grid_remove()

entry_c2_r = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg,
                      justify="center", relief="flat", font=font_main, highlightthickness=1, highlightbackground=outline)
entry_c2_g = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg,
                      justify="center", relief="flat", font=font_main, highlightthickness=1, highlightbackground=outline)
entry_c2_b = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg,
                      justify="center", relief="flat", font=font_main, highlightthickness=1, highlightbackground=outline)
entry_c2_r.grid(row=11, column=0, padx=10)
entry_c2_g.grid(row=11, column=1, padx=10)
entry_c2_b.grid(row=11, column=2, padx=10)
entry_c2_r.grid_remove()
entry_c2_g.grid_remove()
entry_c2_b.grid_remove()

reverse_button = tk.Button(frame, text="Convert to $color", command=convert_backwards, bg=button_bg, fg=light_fg,
          relief="flat", font=font_main, activebackground=button_bg)
reverse_button.grid(row=12, column=0, columnspan=3, pady=10)
reverse_button.grid_remove()

entry_r.focus()
root.mainloop()
