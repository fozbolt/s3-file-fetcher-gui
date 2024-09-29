import customtkinter
from src.frontend import dailyBucketTab, storeBucketTab

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.configureWindow()
        self.createTabview()
        self.createSidebarFrame()
        self.createSidebarOptions()
        self.setDefaultValues()

        self.currTabName = self.tabview.get()
        self.checkTabName() 

    def configureWindow(self):
        self.title("s3 file fetcher.py")
        self.geometry(f"{1500}x{800}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def createTabview(self):
        self.tabview = customtkinter.CTkTabview(self, width=250, anchor="w")
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Daily bucket")
        self.tabview.add("Store bucket")

        dailyTab = self.tabview.tab("Daily bucket")
        storeTab = self.tabview.tab("Store bucket")

        self.dailyTab = dailyBucketTab.DailyBucketTab(dailyTab, self)
        self.storeTab = storeBucketTab.StoreBucketTab(storeTab, self)

    def createSidebarFrame(self):
        self.sidebarFrame = customtkinter.CTkFrame(self, width=400, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)

        self.logoLabel = customtkinter.CTkLabel(self.sidebarFrame, text="History", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logoLabel.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.deleteButton = customtkinter.CTkButton(self.sidebarFrame, text="Delete", fg_color="dark red", corner_radius=20, width=70, command=self.deleteHistory)
        self.deleteButton.grid(row=0, column=0, sticky="e", padx=(0,25), pady=(25,0))

        self.scrollableFrame = customtkinter.CTkScrollableFrame(self.sidebarFrame, label_text="Downloads", width=400, label_anchor="w")
        self.scrollableFrame.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.scrollableFrame.grid_columnconfigure(0, weight=1)
        self.sidebarFrame.grid_rowconfigure(1, weight=3)

       # Initial population of sidebar buttons
        self.updateSidebarButtons()

    def createSidebarOptions(self):
        self.appearanceModeLabel = customtkinter.CTkLabel(self.sidebarFrame, text="Appearance Mode:", anchor="w", height=20)
        self.appearanceModeLabel.grid(row=5, column=0, padx=20, pady=(0, 0), sticky="w")
        self.appearanceModeOptionMenu = customtkinter.CTkOptionMenu(self.sidebarFrame, values=["Light", "Dark", "System"], command=self.changeAppearanceModeEvent, height=20)
        self.appearanceModeOptionMenu.grid(row=6, column=0, padx=20, pady=(5, 5), sticky="w")

        self.scalingLabel = customtkinter.CTkLabel(self.sidebarFrame, text="UI Scaling:", anchor="w", height=20)
        self.scalingLabel.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.scalingOptionMenu = customtkinter.CTkOptionMenu(self.sidebarFrame, values=["80%", "90%", "100%", "110%", "120%"], command=self.changeScalingEvent, height=20)
        self.scalingOptionMenu.grid(row=8, column=0, padx=20, pady=(5, 20), sticky="w")


    # temporary solution because CTk library doesn't have event listener on tab click
    def checkTabName(self):
        newTabName = self.tabview.get()

        if newTabName != self.currTabName:
            self.currTabName = newTabName
            self.updateSidebarButtons()
        
        self.after(2500, self.checkTabName)


    ## change buttons on tab change
    def updateSidebarButtons(self):
        for button in self.dailyTab.sidebarFrameSwitches:
            button.destroy()

        for button in self.storeTab.sidebarFrameSwitches:
            button.destroy()

        currTabName = getattr(self, 'currTabName', 'Daily bucket')
        currTabViewSlug = 'dailyBucket' if currTabName == 'Daily bucket' else 'storeBucket'

        if currTabName == 'Daily bucket':
            self.dailyTab.createSidebarButtons(self.scrollableFrame, currTabViewSlug)
        elif currTabName == 'Store bucket':
            self.storeTab.createSidebarButtons(self.scrollableFrame, currTabViewSlug)
        else: self.dailyTab.createSidebarButtons(self.scrollableFrame, currTabViewSlug)


    def setDefaultValues(self):
        self.appearanceModeOptionMenu.set("Dark")
        self.scalingOptionMenu.set("100%")
        self.dailyTab.setDefaulDailyBucketEntryValues()
        self.storeTab.setDefaultstoreBucketEntryValues()

    def changeAppearanceModeEvent(self, newAppearanceMode: str):
        customtkinter.set_appearance_mode(newAppearanceMode)

    def changeScalingEvent(self, newScaling: str):
        newScalingFloat = float(newScaling.strip('%')) / 100
        customtkinter.set_widget_scaling(newScalingFloat)

    def deleteHistory(self):
        newTabName = self.tabview.get()

        if newTabName == 'Daily bucket':
            self.dailyTab.deleteDailyBucketHistory('dailyBucket', self.scrollableFrame)
        else:
            self.storeTab.deleteStoreBucketHistory('storeBucket', self.scrollableFrame)

        self.updateSidebarButtons()

if __name__ == "__main__":
    app = App()
    app.mainloop()
