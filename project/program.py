from tkinter import *
import tkinter.font as tkFont
from project import model, logger


class Application(Frame):
    ''' GUI Application to KK24 beverage scanner '''

    def __init__(self, master):
        ''' Creating Frames and placing widgets '''
        # Full screen window
        master.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        # master.geometry('400x300')
        # Window title
        master.title('KK24 - Beverage buyer')

        # determine fonts and font sizes
        default_font = "Segoe UI"

        entry_font_size = 10
        entry_font = tkFont.Font(family=default_font, size=entry_font_size)

        info_font_size = 12
        info_font = tkFont.Font(family=default_font, size=info_font_size, weight="bold")

        warning_font_size = 16
        warning_font = tkFont.Font(family=default_font, size=warning_font_size, weight="bold")

        # Main frame
        main_frame = Frame(master)
        main_frame.pack(padx=5, pady=5)

        # Validate command for Entry
        vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # Adding Entry widget
        # self.barcode = Entry(main_frame, validate='key', validatecommand=vcmd, bg='lightgrey', font=entry_font)
        self.barcode = Entry(main_frame, bg='lightgrey', font=entry_font)
        self.barcode.focus_set()
        self.barcode.bind("<Return>", self.buy_beverage)
        self.barcode.grid(row=0, column=0, columnspan=1, sticky='EWNS')

        ''' No need for button when we use the scanner '''
        # Adding Button widget
        self.button = Button(main_frame, text='Submit', command=self.buy_beverage)
        self.button.grid(columnspan=2, row=1)

        # Adding Labels
        self.label_info = Label(main_frame, text='', font=info_font)
        self.label_info.grid(row=1, column=0, columnspan=1, sticky='EWNS')

        self.label_warning = Label(main_frame, text='', font=warning_font)
        self.label_warning.grid(row=2, column=0, columnspan=1, sticky='EWNS')

    # Validates input
    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def buy_beverage(self, event=None):
        ''' Function that handles the beverage
         purchase and calls the API methods '''

        if root.user_id == 0:
            # Assign user ID to var
            root.user_id = self.barcode.get()
            root.user_name = model.get_user(user_id=root.user_id)

            # Printing user to GUI
            self.label_info.config(text="User: " + root.user_name)
            self.label_warning.config(text='')
        else:
            # Assign beverage ID to var
            root.beverage_id = self.barcode.get()
            root.beverage_name = model.get_beverage_name(beverage_id=root.beverage_id)

            # Printing result to GUI
            try:
                self.label_info.config(text="User: " + root.user_name + "\nBeverage: " + root.beverage_name)
            except TypeError as e:
                logger.logger_error(str(e), 'TypeError')

            # Calls API methods and stores response
            status = model.call_buy_beverage(user_id=root.user_id, beverage_id=root.beverage_id)

            if status == 400:
                self.label_warning.config(text="Purchase was unsuccessful \nPlease contact an administrator", fg='red')
            else:
                self.label_warning.config(text="Purchase was successful", fg='green')

            # Resetting ID's to 0
            root.user_id = 0
            root.beverage_id = 0

        self.barcode.delete(0, 'end')


root = Tk()

# Initializing 'GLOBAL' variables
root.user_id = 0
root.beverage_id = 0
root.user_name = ' '
root.beverage_name = ' '

app = Application(root)

root.mainloop()
