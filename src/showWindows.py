import uiautomation as ui
import psutil as ps
import re

TIMEOUT_SET = 0.00001
class showWindows:
    # tabList[i] = (control, procName)
    tabList = {}
    def __init__(self):
        ui.SetGlobalSearchTimeout(TIMEOUT_SET)
        
    def showWindow(self, control: ui.WindowControl):
        # print(
        #     f"X\tWnd name : {control.Name}\tCls name : {control.ClassName}\tPID : {control.ProcessId}"
        # )
        processName = ps.Process(control.ProcessId).name()
        self.tabList[control.Name] = (control, processName)
        if(control.Name == 'Advanced Alt - Tab by THLee'):
            control.SetFocus()
        return None

    def getTab(self, control: ui.WindowControl, tabList: dict):
        # Tab implementaion lacks standardization.
        # should implement one by one?

        # Chrome based
        rootClassName = control.ClassName
        processName = ps.Process(control.ProcessId).name()
        if rootClassName == "Chrome_WidgetWin_1":
            
            if processName == "msedge.exe":
                # for Edge
                container = ui.PaneControl(control, ClassName="TabContainerImpl")
                if container and container.Exists(TIMEOUT_SET):
                    tab = container.GetFirstChildControl()
                    while tab:
                        if tab.Name:
                            # print(f"\t\t└Tab name : {tab.Name} ")
                            tabList[tab.Name] = (tab, processName)
                        tab = tab.GetNextSiblingControl()
                    return None
                
            elif processName == "Code.exe":
                # for VScode
                # container = ui.TabControl(control, AriaRole='tablist', foundIndex=2)
                container = control.GetFirstChildControl()
                container = ui.TabControl(container, AriaRole="tablist", foundIndex=2)
                if container and container.Exists(TIMEOUT_SET):
                    tab = container.GetFirstChildControl()
                    while tab:
                        if tab.Name:
                            # print(f"\t\t└Tab name : {tab.Name} ")
                            tabList[tab.Name] = (tab, processName)
                        tab = tab.GetNextSiblingControl()
                    return None

        # NOT CRHOME
        
        elif rootClassName == "CabinetWClass":
            # Windows Explorer
            container = ui.ListControl(
                control, searchDepth=4, AutomationId="TabListView", foundIndex=1
            )
            if container and container.Exists(TIMEOUT_SET):
                tab = container.GetFirstChildControl()
                while tab:
                    if tab.Name:
                        # print(f"\t\t└Tab name : {tab.Name} ")
                            tabList[tab.Name] = (tab, processName)
                    tab = tab.GetNextSiblingControl()
                return None

        return None


################################# main ##################################
    def getTabList(self):
        # Sould be revised. more directly!
        # It fails when no windows present(?)
        self.tabList = {}
        root = ui.WindowControl(searchFromControl=None, searchDepth=1).GetParentControl()
        wnd = root.GetFirstChildControl()
        while wnd:
            self.showWindow(wnd)
            self.getTab(wnd, self.tabList)
            wnd = wnd.GetNextSiblingControl()
    
    def searchTabs(self, keyword:str) -> [ui.WindowControl]:
        res = []
        regex = keyword
        p = re.compile(regex, flags= re.IGNORECASE)
        keys = self.tabList.keys()
        for key in keys:
            if p.search(key) or p.search( self.tabList[key][1] ):   # procName search
                res.append(key)
        return res

    def focusTab(self, name:str):
        if name in self.tabList.keys():
            control:ui.WindowControl = self.tabList[name][0]
            control.SetFocus()
            return None
        else:
            print("no such tab exist.")
            return None

