import tkinter as tk
from tkinter import messagebox
import webbrowser

boost_factor = 2.1

def perceptual_color_to_color2(r, g, b, boost=2.1):
    def adjust(c):
        normalized = c / 255
        boosted = pow(normalized, 1 / boost)
        return round(min(boosted, 1.0), 3)
    return tuple(adjust(c) for c in (r, g, b))

def convert_color(event=None):
    try:
        r = int(entry_r.get())
        g = int(entry_g.get())
        b = int(entry_b.get())
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError
        color2 = perceptual_color_to_color2(r, g, b, boost_factor)
        result_var.set(f'$color2 "[{color2[0]} {color2[1]} {color2[2]}]"')
        update_color_previews(r, g, b, color2)
        update_vmt_snippet(color2)
    except ValueError:
        result_var.set("Invalid input. RGB must be 0–255.")
        update_color_previews(None, None, None, None)

def update_color_previews(r, g, b, color2):
    try:
        #input color (brush)
        input_color = f'#{r:02x}{g:02x}{b:02x}'
        input_color_preview.config(bg=input_color)

        #output color (model)
        def unboost(c):
            return int(min(255, pow(c, boost_factor) * 255))

        c2_rgb = tuple(unboost(c) for c in color2)
        output_color = f'#{c2_rgb[0]:02x}{c2_rgb[1]:02x}{c2_rgb[2]:02x}'
        output_color_preview.config(bg=output_color)

    except:
        input_color_preview.config(bg=dark_bg)
        output_color_preview.config(bg=dark_bg)

def copy_to_clipboard():
    result = result_var.get()
    if result.startswith("$color2"):
        root.clipboard_clear()
        root.clipboard_append(result)
        clipboard_message.config(text="Copied!", fg="lime")
        root.after(2000, lambda: clipboard_message.config(text=""))
    else:
        clipboard_message.config(text="Invalid input", fg="orange")
        root.after(2000, lambda: clipboard_message.config(text=""))

def update_boost(val):
    global boost_factor
    boost_factor = float(val)

    try:
        r = int(entry_r.get())
        g = int(entry_g.get())
        b = int(entry_b.get())
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError

        color2 = perceptual_color_to_color2(r, g, b, boost_factor)

        result_var.set(f'$color2 "[{color2[0]} {color2[1]} {color2[2]}]"')
        update_color_previews(r, g, b, color2)
        update_vmt_snippet(color2)

    except ValueError:
        result_var.set("Invalid input.")
        update_color_previews(None, None, None, None)

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
    else:
        boost_slider.grid_remove()

def open_about():
    about = tk.Toplevel(root)
    about.title("About")
    about.resizable(False, False)
    about.configure(bg=dark_bg)
    tk.Label(about, text="Created by peeps", fg=light_fg, bg=dark_bg).pack(pady=(10, 0))
    tk.Label(about, text="Contact:", fg=light_fg, bg=dark_bg).pack()

    button_frame = tk.Frame(about, bg=dark_bg)
    button_frame.pack(pady=5)

    def open_link(url): webbrowser.open(url)

    tk.Button(button_frame, text="Steam", width=10, command=lambda: open_link("https://steamcommunity.com/id/halfpeeps/")).pack(side="left", padx=5)
    tk.Button(button_frame, text="Forums", width=10, command=lambda: open_link("https://perpheads.com/members/peeps.10255/")).pack(side="left", padx=5)
    tk.Button(button_frame, text="GitHub", width=10, command=lambda: open_link("https://github.com/halfpeeps/VMT-Color-Converter")).pack(side="left", padx=5)

#colors
dark_bg = "#1e1e1e"
light_fg = "#f0f0f0"
accent_color = "#3c8dbc"
entry_bg = "#2a2a2a"

#gui
root = tk.Tk()
root.title("VMT $color Converter")
root.configure(bg=dark_bg)
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20, bg=dark_bg)
frame.pack()

tk.Label(frame, text="RGB Input (0–255):", bg=dark_bg, fg=light_fg).grid(row=0, column=0, columnspan=3)

entry_r = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
entry_g = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
entry_b = tk.Entry(frame, width=5, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
entry_r.grid(row=1, column=0, padx=5)
entry_g.grid(row=1, column=1, padx=5)
entry_b.grid(row=1, column=2, padx=5)

entry_r.bind("<Return>", convert_color)
entry_g.bind("<Return>", convert_color)
entry_b.bind("<Return>", convert_color)

tk.Button(frame, text="Convert", command=convert_color).grid(row=2, column=0, columnspan=3, pady=10)

result_var = tk.StringVar()
tk.Entry(frame, textvariable=result_var, width=40, state="readonly", justify="center",
         bg=entry_bg, fg=light_fg, readonlybackground=entry_bg).grid(row=3, column=0, columnspan=3, pady=5)

clipboard_message = tk.Label(frame, text="", fg="lime", bg=dark_bg)
clipboard_message.grid(row=4, column=0, columnspan=3)

tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=5, column=0, columnspan=3, pady=5)

tk.Label(frame, text="Brush $color", bg=dark_bg, fg=light_fg).grid(row=6, column=0)
tk.Label(frame, text="Model $color2", bg=dark_bg, fg=light_fg).grid(row=6, column=2)

input_color_preview = tk.Label(frame, width=10, height=2, bg=dark_bg, relief='sunken')
output_color_preview = tk.Label(frame, width=10, height=2, bg=dark_bg, relief='sunken')
input_color_preview.grid(row=7, column=0, pady=5)
output_color_preview.grid(row=7, column=2, pady=5)

advanced_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Advanced", variable=advanced_var, command=toggle_advanced, bg=dark_bg, fg=light_fg, activebackground=dark_bg, activeforeground=light_fg, selectcolor=dark_bg).grid(row=8, column=0, columnspan=3)

boost_slider = tk.Scale(frame, from_=1.0, to=3.0, resolution=0.05,
                        orient="horizontal", command=update_boost,
                        bg=dark_bg, fg=light_fg, highlightbackground=dark_bg)
boost_slider.set(boost_factor)
boost_slider.grid(row=9, column=0, columnspan=3)
boost_slider.grid_remove()

tk.Label(frame, text="VMT Snippet", bg=dark_bg, fg=light_fg).grid(row=10, column=0, columnspan=3, pady=(10, 0))
vmt_box = tk.Text(frame, height=6, width=42, wrap="none", bg=entry_bg, fg=light_fg)
vmt_box.grid(row=11, column=0, columnspan=3, pady=5)
vmt_box.config(state="disabled")

tk.Button(frame, text="About", command=open_about).grid(row=12, column=0, columnspan=3, pady=(0, 5))

entry_r.focus()
root.mainloop()
