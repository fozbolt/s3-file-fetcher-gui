import customtkinter
from src.backend.backendHelperFunctions import getSortedBucketFileNames, deleteBucketHistory, generateDailyBucketParams
from src.backend import dailyBucket
import os
import subprocess

class DailyBucketTab:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app
        self.createWidgets()
        self.createMainWidgets()
        self.sidebarFrameSwitches = []

    def createSidebarButtons(self, scrollableFrame, folderName):
        dailyBucketFileNames = getSortedBucketFileNames(folderName)
        
        for i, fileName in enumerate(dailyBucketFileNames):
            button = customtkinter.CTkButton(
                master=scrollableFrame, 
                text=fileName, 
                command=lambda name=fileName: self.openFile(name, folderName)
            )
            button.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.sidebarFrameSwitches.append(button)

    def createWidgets(self):
        self.tab.grid_rowconfigure(11, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

        self.dailyRadioVar = customtkinter.StringVar(value="prod")
        # self.dailyRadioVar.trace_add("write", self.onRadioChange)
        self.createDailyRadioFrame(self.tab, self.dailyRadioVar, [("Prod", "prod"), ("Stage", "stage"), ("Dev", "dev")])

        self.dailyEntryDisplay = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.dailyEntryDisplay.grid(row=2, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dailyUrlWithBody = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.dailyUrlWithBody.grid(row=4, column=0, padx=(25, 0), pady=(2, 10), sticky="w")

        self.dailyBucketPopupButton = customtkinter.CTkButton(self.tab, text="Show all", command=self.showDailyBucketPopup)
        self.dailyBucketPopupButton.grid(row=4, column=0, padx=(350, 0), pady=(2, 10), sticky="w")  # Positioned next to dailyUrlWithBody

        self.dailyEntryDisplay1 = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.dailyEntryDisplay1.grid(row=6, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dailyEntryDisplay2 = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.dailyEntryDisplay2.grid(row=8, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dailyEntryDisplay3 = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.dailyEntryDisplay3.grid(row=10, column=0, padx=(25, 5), pady=(2, 10), sticky="w")
        
        self.createDailyBucketLabelsAndEntries()

        self.dailyTextbox = customtkinter.CTkTextbox(self.tab, width=250, height=150)
        self.dailyTextbox.configure(state="disabled")
        self.dailyTextbox.grid(row=11, column=0, padx=20, pady=(50, 10), sticky="nsew")

    def createMainWidgets(self):
        # Adjust the width attribute to make the entryInput thinner
        self.entryInput = customtkinter.CTkEntry(self.tab, placeholder_text="url", width=150)
        self.entryInput.grid(row=12, column=0, padx=(20, 5), pady=(20, 5), sticky="ew")
        self.entryInput.bind("<KeyRelease>", self.updateEntries)

        self.dateInput = customtkinter.CTkEntry(self.tab, placeholder_text="date as YYYYMMDD", width=150)
        self.dateInput.grid(row=12, column=1, padx=(5, 10), pady=(20, 5), sticky="ew")
        self.dateInput.bind("<KeyRelease>", self.updateEntries)

        # Configure column weights to ensure they expand properly
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=1)


        self.mainButton = customtkinter.CTkButton(self.tab, text="Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.submit)
        self.mainButton.grid(row=12, column=2, padx=(20, 20), pady=(20, 5), sticky="nsew")

    def createDailyRadioFrame(self, tab, variable, options):
        self.dailyRadioFrame = customtkinter.CTkFrame(tab)
        self.dailyRadioFrame.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")
        for i, (text, value) in enumerate(options):
            radio = customtkinter.CTkRadioButton(self.dailyRadioFrame, text=text, variable=variable, value=value, height=20, width=60, radiobutton_width=10, radiobutton_height=10)
            radio.grid(row=0, column=i, padx=2, pady=5, sticky="w")

    def createDailyBucketLabelsAndEntries(self):
        self.tab.grid_rowconfigure((0,10), weight=0)
        self.tab.grid_rowconfigure(11, weight=1)

        #TODO change names to sth descriptive
        dailyLabel1 = customtkinter.CTkLabel(self.tab, text="1. url:", anchor="w")
        dailyLabel1.grid(row=1, column=0, padx=(25, 5), pady=(20, 2), sticky="w")

        dailyLabel2 = customtkinter.CTkLabel(self.tab, text="2. url with body (htttps..._undefined or body), create pop to see it...", anchor="w")
        dailyLabel2.grid(row=3, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        dailyLabel3 = customtkinter.CTkLabel(self.tab, text="3. hashed url and body", anchor="w")
        dailyLabel3.grid(row=5, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        dailyLabel4 = customtkinter.CTkLabel(self.tab, text="4. date/hashed url with body...", anchor="w")
        dailyLabel4.grid(row=7, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        dailyLabel5 = customtkinter.CTkLabel(self.tab, text="Reverse check terminal command", anchor="w")
        dailyLabel5.grid(row=9, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

    def setDefaulDailyBucketEntryValues(self):
        self.dailyEntryDisplay.configure(state="normal")
        self.dailyEntryDisplay.delete(0, 'end')
        self.dailyEntryDisplay.insert(0, "Paste the url at the bottom input to view")
        self.dailyEntryDisplay.configure(state="readonly")

    # def onRadioChange(self, *args):
    #     self.updateEntry(self.reverseCheckCmdEntry, backendHelperFunctions.createReverseCheckStoreCmd(self.storeRadioVar.get(), self.convertedStoreIdPlaceholder.get()))

    def updateEntries(self, event=None):
        urlWithBody = self.dailyEntryDisplay.get()
        url, vehicleUrlBody = (urlWithBody.rsplit("_", 1) if "_" in urlWithBody else (urlWithBody, 'undefined')) #TODO this is bad practice, improve
        dateInput = self.dateInput.get()
        self.updateEntry(self.dailyEntryDisplay, url)
        # i tu stao 
        vehicleUrlWithBody = f"{url}_{vehicleUrlBody}" #ovo staviti u backend funkciju zbog logike s undefiend?
    
        self.updateEntry(self.dailyUrlWithBody, vehicleUrlWithBody)
        #tu stao
        #
        ##tu dobijem hashed url..
        entryInputChangeThisName = generateDailyBucketParams(url, vehicleUrlBody, dateInput)
        print(entryInputChangeThisName)
        # self.updateEntry(self.dailyUrlWithBody, )

        # TODO fix this
        # self.updateEntry(self.dailyUrlWithBody, backendHelperFunctions.generateDailyBucketParams(inputText))

        if not urlWithBody:
            self.updateTextboxDaily('', '')

    def updateEntry(self, entry, text):
        entry.configure(state="normal")
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.configure(state="readonly")

    def updateTextboxDaily(self, message, status):
        self.dailyTextbox.configure(state="normal")
        self.dailyTextbox.delete("1.0", customtkinter.END)

        if status == "success":
            self.dailyTextbox.configure(text_color="green")
        else:
            self.dailyTextbox.configure(text_color="red")

        self.dailyTextbox.insert(customtkinter.END, message)
        self.dailyTextbox.configure(state="disabled")


    def openFile(self, fileName, folder):
        ## add here logic for sending tab info and showing tab info...
        try:
            # Get the directory where the current script (app.py) is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            
            # Construct the relative file path based on the script's location
            filePath = os.path.join(script_dir, folder, fileName)

            subprocess.Popen(['open', filePath])

            with open(filePath, 'r') as file:
                content = file.read()
                # Display the content in the daily tab's textbox or wherever appropriate
                self.updateTextboxDaily(content, "success")

        except Exception as e:
            print(f"Error handling file {fileName}: {str(e)}")
            self.updateTextboxDaily(f"Error handling file {fileName}", "error")


    def showDailyBucketPopup(self):
        dailyBucketEntryText = self.dailyUrlWithBody.get()
        popup = customtkinter.CTkToplevel(self.tab)
        popup.geometry("400x200")
        popup.title("URL with Body")

        message_label = customtkinter.CTkLabel(popup, text=dailyBucketEntryText, wraplength=350)
        message_label.pack(padx=20, pady=20)

    def deleteDailyBucketHistory(self, folderName, scrollableFrame):
        result = deleteBucketHistory(self, folderName)
        self.updateTextboxDaily(result['message'], result['status'])

        if (result["status"] == "success"):
            self.createSidebarButtons(scrollableFrame, folderName)

    def submit(self):
        urlWithBody = self.dailyEntryDisplay.get()
        url, vehicleUrlBody = (urlWithBody.rsplit("_", 1) if "_" in urlWithBody else (urlWithBody, None))
        environmentName = self.dailyRadioVar.get()
        date = self.dateInput.get()

        result = dailyBucket.fetchVehicleRawResponse(environmentName, date, url, vehicleUrlBody) #test what happens if no date is entered, possibly create restriction
        self.updateTextboxDaily(result["message"], result["status"])

