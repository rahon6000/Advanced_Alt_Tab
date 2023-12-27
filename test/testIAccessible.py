import uiautomation as ui

    
def enum(wnd : ui.WindowControl, depth: int ) -> None:
    ia = wnd.GetLegacyIAccessiblePattern()
    tabs = " " * depth
    if (ia and ia.Role == 37 and ia.State == 3145728) or ui.IsTopLevelWindow(wnd.NativeWindowHandle) :   ## 0x300000 == focusable, selectable.
        namePresnet = wnd.Name
        namePresnet = namePresnet.ljust(20) if len(namePresnet) < 20 else namePresnet[:20]
        print( f"{tabs}└{namePresnet} | {ui.IsTopLevelWindow(wnd.NativeWindowHandle)}" + 
              f"|{hex(ia.State)}")
    arr = wnd.GetChildren()
    for i in arr:
        enum(i, depth + 1)
    return None

ui.SetGlobalSearchTimeout(0.1)
testWnd = ui.ControlFromHandle(ui.GetForegroundWindow())
while testWnd.GetParentControl():
    testWnd = testWnd.GetParentControl()
print(testWnd)
enum(testWnd, 0 )
print('hello world!')
