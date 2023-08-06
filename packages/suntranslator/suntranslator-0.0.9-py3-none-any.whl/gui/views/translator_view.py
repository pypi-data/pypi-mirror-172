import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from translator.translate import Translator


class EntryView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.translator = Translator()
        self.translate_font = self.set_translated_font(16)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Entry box whose text will be translated
        self.textEntry = tk.Text(self)
        self.textEntry.grid(row=0, column=1,
                            sticky=tk.N+tk.S+tk.E+tk.W)
        self.textEntry.configure(font=("Times", 16),
                                 wrap=tk.WORD, width=75)

        # Entry box to display the translated text
        self.translatedText = tk.Text(self)
        self.translatedText.grid(row=0, column=2,
                                 sticky=tk.N+tk.S+tk.E+tk.W)
        self.translatedText.configure(font=self.translate_font,
                                      wrap=tk.WORD, width=75)
        self.translatedText.configure(state=tk.DISABLED)

        # Buttons
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.buttonFrame.grid(row=0, column=0)

        self.translateButton = ttk.Button(self.buttonFrame, text="Translate",
                                          command=self.translate)
        self.translateButton.grid(row=0, column=0,
                                  sticky=tk.N+tk.E+tk.W)

        self.saveButton = ttk.Button(self.buttonFrame, text="Save",
                                     command=self.save)
        self.saveButton.grid(row=1, column=0,
                             sticky=tk.N+tk.E+tk.W)

        self.textEntry.bind("<Return>", self.__translate)

    def __translate(self, event):
        self.translateButton.invoke()

    def set_translated_font(self, f_size):
        if "SUN7_8_1210" in font.families():
            return ("SUN7_8_1210", f_size)
        else:
            messagebox.showwarning("Sun Language Not Installed",
                                   "The Sun language font is either not \
                                   installed or not on your system's font \
                                   path. Will continue using the default \
                                   font.")
            return ("TkDefaultFont", f_size)

    def translate(self):
        text = self.textEntry.get('1.0', 'end')

        translated = self.translator.translateText(text)

        self.translatedText.configure(state=tk.NORMAL)
        self.translatedText.delete('1.0', 'end')
        self.translatedText.insert('1.0', translated)
        self.translatedText.configure(state=tk.DISABLED)

    def save(self):
        filename = filedialog.asksaveasfilename(filetypes=[("PDF", "*.pdf")],
                                                defaultextension='.pdf',
                                                title="Save As")
        text = self.translatedText.get('1.0', 'end')
        self.translator.saveToPdf(text, filename)
