import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
import os
import keyboard
import showWindows


# parameters
mainAppTitle = "Advanced Alt - Tab by THLee"

maxWidth = 640
maxHeight = 400
alpha = 0.7
sw = showWindows.showWindows()
searchResult = []
cursor = 0

# Events
def keyInputManager(key: keyboard.KeyboardEvent) -> None:
    global cursor
    if key.name == "esc":
        ## hide 
        textbox.delete(0,"end")
        textbox.config(state="disable")
        root.wm_attributes("-alpha", 0)
        # root.withdraw()
        # global icon
        # icon.run() # this block events....
        
    elif key.name == "enter":
        ## focus wanted tab
        name = textbox.get()
        if(len(name)):
            print(name)
            sw.focusTab(name)
            textbox.delete(0,"end")
            textbox.config(state="disabled")
            root.wm_attributes("-alpha", 0)
            
    elif key.name =="down":
        cursor += 1
    elif key.name == "up":
        cursor -= 1
    else:
        return None
    refreshSelection()
    return None

def quitApp():
    root.quit()
    return None

def showApp() -> None:
    # TODO: focus is currently NOT set properly.
    # global icon
    # icon.stop()
    root.wm_attributes("-alpha", alpha)
    textbox.config(state="normal")
    sw.getTabList()
    root.deiconify()
    root.focus_force()
    textbox.focus_force()
    return None

def getMatchings(dummy):
    # check the key is just alphabet.
    global textbox
    global searchResult
    global cursor
    searchResult= sw.searchTabs( textbox.get() )
    if len(searchResult) == 0:
        return None
    # textbox["values"] = searchResult
    # textbox.event_generate('<Down>')
    text = ''
    for tabName in searchResult:
        text += tabName + '\n'
    refreshSelection()
    return None

def refreshSelection():
    global cursor
    global searchResult
    global previewFrame
    length = len(searchResult)
    print(cursor, length)
    cursor %= length
    for ch in previewFrame.winfo_children():
        ch.destroy()
    
    if(length == 0):
        return None
    
    for i, tabs in enumerate(searchResult):
        if( i == cursor):
            print(tabs)
            lab = ttk.Label(previewFrame, text=tabs, borderwidth=3, relief= "flat") # why no effect?
        else:
            lab = ttk.Label(previewFrame, text=tabs, )
            
        lab.grid(column=0, row=i)
    
    #TODO
    
    
    return None

root = tk.Tk()
root.title(mainAppTitle)
root.geometry("+" + str(maxWidth // 2) + "+" + "100")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0)  # Set invisible
root.resizable(0, 0)
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Adv. Alt Tab").grid(column=0, row=0)
textbox = ttk.Entry(
    frm,
    width= 100,
    # values=searchResult,
)
textbox.grid(column=0, row=1)

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
keyboard.add_hotkey("ctrl+`", showApp)
textbox.bind("<KeyRelease>", getMatchings)
root.mainloop()