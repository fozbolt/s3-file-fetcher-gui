import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("s3 file fetcher.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)  # Ensure the sidebar frame can expand

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="History", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")

        # create scrollable frame inside the sidebar
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.sidebar_frame, label_text="Downloads", width=140, label_anchor="w")
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=3)  # Ensure scrollable frame gets more space

        # Add buttons in the scrollable frame
        self.sidebar_frame_switches = []
        for i in range(20):  # Reduced to avoid too much content
            button = customtkinter.CTkButton(master=self.scrollable_frame, text=f"CTkButton {i}")
            button.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.sidebar_frame_switches.append(button)

        # appearance mode selection
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", height=20)
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(0, 0), sticky="w")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event, height=20)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 5), sticky="w")

        # scaling option selection
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", height=20)
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event, height=20)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 20), sticky="w")

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250, anchor="w")
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Daily bucket")  # First tab
        self.tabview.add("Store bucket")  # Second tab
        self.tabview.tab("Store bucket").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Daily bucket").grid_columnconfigure(0, weight=1)

       # Create a frame in the first tab for radio buttons
        self.radio_frame = customtkinter.CTkFrame(self.tabview.tab("Daily bucket"))
        self.radio_frame.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")

        # Create radio buttons and place them in the radio_frame
        self.radio_var = customtkinter.StringVar(value="prod")
        self.radio1 = customtkinter.CTkRadioButton(self.radio_frame, text="Prod", variable=self.radio_var, value="prod", height=20, width=50, radiobutton_height=15)
        self.radio1.grid(row=0, column=0, padx=2, pady=5, sticky="w")
        self.radio2 = customtkinter.CTkRadioButton(self.radio_frame, text="Store", variable=self.radio_var, value="store", height=20)
        self.radio2.grid(row=0, column=1, padx=2, pady=5, sticky="w")
        self.radio3 = customtkinter.CTkRadioButton(self.radio_frame, text="Dev", variable=self.radio_var, value="dev", height=20)
        self.radio3.grid(row=0, column=2, padx=2, pady=5, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Daily bucket"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Daily bucket"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Daily bucket"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # Move the CTkTextbox into the first tab of the tabview
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("Daily bucket"), width=250)
        self.textbox.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Add a label to the second tab
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Store bucket"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 10)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
