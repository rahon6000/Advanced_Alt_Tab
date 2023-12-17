import uiautomation as ui
import psutil as ps
import re

def showWindow(control: ui.WindowControl, tabList: dict):
    print(f'X\tWnd name : {control.Name}\tCls name : {control.ClassName}\tPID : {control.ProcessId}')
    tabList[control.Name] = control
    return None

def getTabs(control: ui.WindowControl, tabList: dict):
    # Tab implementaion lacks standardization.
    # should implement one by one?
    
    # Chrome based
    rootClassName = control.ClassName
    processName = ps.Process(control.ProcessId).name()
    if( rootClassName == 'Chrome_WidgetWin_1'):
        if(processName == 'msedge.exe'):
            # for Edge
            container = ui.PaneControl(control, ClassName='TabContainerImpl')
            if(container and container.Exists(0.0001)):
                tab = container.GetFirstChildControl()
                while(tab):
                    if(tab.Name):
                        print(f'\t\t└Tab name : {tab.Name} ')
                        tabList[tab.Name] = tab
                    tab = tab.GetNextSiblingControl()
                return None
        elif(processName == 'Code.exe'):    
            # for VScode
            # container = ui.TabControl(control, AriaRole='tablist', foundIndex=2)
            container = control.GetFirstChildControl()
            
            container = ui.TabControl(container, AriaRole='tablist', foundIndex=2)
            
            if(container and container.Exists(0.0001)):
                tab = container.GetFirstChildControl()
                while(tab):
                    if(tab.Name):
                        print(f'\t\t└Tab name : {tab.Name} ')
                        tabList[tab.Name] = tab
                    tab = tab.GetNextSiblingControl()
                return None
        
    # NOT CRHOME
    elif (rootClassName == 'CabinetWClass'):
        # Windows Explorer
        container = ui.ListControl(control, searchDepth=4, AutomationId='TabListView', foundIndex=1)
        if(container and container.Exists(0.0001)):
            tab = container.GetFirstChildControl()
            while(tab):
                if(tab.Name):
                    print(f'\t\t└Tab name : {tab.Name} ')
                    tabList[tab.Name] = tab
                tab = tab.GetNextSiblingControl()
            return None
    
    
    return None

################################# main ##################################

ui.SetGlobalSearchTimeout(0.0001)

# Sould be revised. more directly!
# It fails when no windows present(?)
root = ui.WindowControl(searchFromControl=None, searchDepth=1).GetParentControl()
wnd = root.GetFirstChildControl()
tabList = {}
while wnd:
    showWindow(wnd, tabList)
    getTabs(wnd, tabList)
    wnd = wnd.GetNextSiblingControl()


# 한글 못찾는디...
searchName = '탭'
regex = searchName
p = re.compile(regex)

target:ui.WindowControl
keys = tabList.keys()
foundList = []
for key in keys:
    if p.search(key):
        foundList.append(key)

print(foundList)

# target = tabList[searchName]
# target.SetFocus()
# IT WORKS! HORAY~