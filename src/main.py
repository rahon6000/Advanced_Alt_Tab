import tkinter as tk
from tkinter import ttk
# import pystray
# from PIL import Image
import os
import keyboard
import showWindows


# parameters
mainAppTitle = "Advanced Alt - Tab by THLee"

maxWidth = 640
maxHeight = 400
alpha = 0.8
sw = showWindows.showWindows()
searchResult = []
cursor = 0
targetLabel:tk.Label

# Events
def keyInputManager(key: keyboard.KeyboardEvent) -> None:
    global cursor
    global targetLabel
    global textbox
    # print(keyboard._hotkeys['ctrl+`'])
    if ( keyboard.is_pressed('ctrl+`') ):
        showApp()
        return None
    if ( textbox["state"] == "disabled"):
        return None
    if key.name == "esc":
        ## hide 
        textbox.delete(0,"end")
        textbox.config(state="disabled")
        root.wm_attributes("-alpha", 0)
        
    elif key.name == "enter":
        try:
            name = targetLabel["text"]
            if(len(name)):
                sw.focusTab(name)
                textbox.delete(0,"end")
                textbox.config(state="disabled")
                root.wm_attributes("-alpha", 0)
        except(NameError):
            return None
            
    elif key.name =="down":
        refreshCursor( +1 )
    elif key.name == "up":
        refreshCursor( -1 )
    
    return None

def quitApp(*args ):
    root.quit()
    return None

def showApp() -> None:
    # global icon
    # icon.stop()
    global searchResult
    root.wm_attributes("-alpha", alpha)
    textbox.config(state="normal")
    sw.getTabList()
    searchResult= sw.searchTabs( textbox.get() )
    root.deiconify()
    root.focus_force()
    textbox.focus_force()
    return None

def getMatchings(*args):
    global entryVar
    global searchResult
    global cursor
    
    searchResult= sw.searchTabs( entryVar.get() )
    refreshSelection()
    return None

def refreshSelection():
    global cursor
    global searchResult
    global previewFrame
    length = len(searchResult)
    cursor = 0
    for ch in previewFrame.winfo_children():
        ch.destroy()
    if(length == 0):
        return None
    for i, tabs in enumerate(searchResult):
        lab = ttk.Label(previewFrame, text=tabs, justify="left")
        lab.grid(column=0, row=i)
    refreshCursor( 0 )
    return None

def refreshCursor(dir: int):
    global cursor
    global searchResult
    global previewFrame
    global targetLabel
    length  = len(searchResult)
    if( length == 0):
        return None
    cursor %= length
    prevLabel = previewFrame.winfo_children()[cursor]
    cursor += dir
    cursor %= length
    targetLabel = previewFrame.winfo_children()[cursor]
    prevLabel["relief"] = ""
    targetLabel["relief"] = "solid" 
    return None

# Main frame
root = tk.Tk()
root.title(mainAppTitle)
root.geometry(""                 # width x height
              + "+" + str(maxWidth // 2)    # x position
              + "+" + "100")                # y position
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0)  # Set invisible
root.resizable(0, 0)
frm = ttk.Frame(root, padding=10)
frm.grid()

# Title label
ttk.Label(frm, text="Adv. Alt Tab", width= 100).grid(column=0, row=0)

# Quit button
ttk.Button(frm, text="X", command=quitApp, width=10).grid(column=1, row=0)

# Search box
entryVar = tk.StringVar()
textbox = ttk.Entry(
    frm,
    state="disabled",
    textvariable=entryVar,
)
textbox.grid(column=0, row=1, columnspan=2, sticky='we')


previewFrame = ttk.Frame(frm)
previewFrame.grid(column=0, row=2)
previewFrame.grid()
# previewLabel = tk.Label(textbox, text = "test")
# previewLabel.pack(anchor="s", )

# faviconImage=Image.open( os.path.split(__file__)[0] +  "\\favicon.ico")
# menu=(pystray.MenuItem('Quit', quitApp),
#         pystray.MenuItem('Show', showApp))
# icon=pystray.Icon("name", faviconImage, "My System Tray Icon", menu)


# Loops
keyboard.on_press(keyInputManager)
entryVar.trace_add(mode="write", callback=getMatchings)
root.mainloop()