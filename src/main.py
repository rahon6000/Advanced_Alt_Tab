import tkinter as tk
from tkinter import ttk
import keyboard
import showWindows


# GUI components
root = tk.Tk()
root.title("Advanced Alt - Tab by THLee")

maxWidth = 640
maxHeight = 400
root.geometry("+" + str(maxWidth // 2) + "+" + "100")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0)  # Set invisible
root.resizable(0, 0)
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Adv. Alt Tab").grid(column=0, row=0)
textbox = tk.Entry(
    frm,
    width= 100,
)
textbox.grid(column=0, row=1)
alpha = 0.7
sw = showWindows.showWindows()
tabNames = []
isDisplayed = False


# Events
def keyInputManager(key: keyboard.KeyboardEvent) -> None:
    if key.name == "esc":
        textbox.delete(0,"end")
        textbox.config(state="disable")
        root.wm_attributes("-alpha", 0)
    elif key.name == "enter":
        tabNames = sw.searchTabs(textbox.get())
        if(len(tabNames)):
            sw.focusWindowByName(tabNames[0])
            textbox.delete(0,"end")
            textbox.config(state="disabled")
            root.wm_attributes("-alpha", 0)
            
    return None

def showApp() -> None:
    root.wm_attributes("-alpha", alpha)
    textbox.config(state="normal")
    sw.getTabList()
    textbox.focus_force() # dCurrently not working as wanted.
    return None

# Loops
keyboard.on_press(keyInputManager)
keyboard.add_hotkey("ctrl+`", showApp)
root.mainloop()
