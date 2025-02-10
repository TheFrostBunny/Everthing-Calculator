import os, sys, math, numpy as np, sympy as sp, customtkinter as ctk, matplotlib.pyplot as plt
from PIL import Image 
from customtkinter import CTkImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry 


class Hovedmeny(ctk.CTkFrame):
    """Hovedmenyramme med navigasjon til kalkulatorer."""
    
    def __init__(self, master, 
                 prosent_callback=None, 
                 kalkulator_callback=None, 
                 graf_callback=None, 
                 konvertering_callback=None, 
                 TrigonometryCalculator_callback=None, 
                 Tidskalkulator_callback=None,
                 FinansKalkulator_callback=None):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self, text="Velg en kalkulator", font=("Arial", 20))
        label.grid(row=0, column=2, pady=20)

        # Ikoner
        prosent_icon = self.load_icon("Icons/prosent_icon.png")
        kalkulator_icon = self.load_icon("Icons/kalkulkator_icon.png")
        graf_icon = self.load_icon("Icons/icon_graf.png")
        Data_icon = self.load_icon("Icons/icon_data.png")
        Trig_icon = self.load_icon("Icons/icon_trigonometry.png")
        Tidskalkulatorer_icon = self.load_icon("Icons/icon_Tid.png")
        Soon_icon = self.load_icon("Icons/Icon_soon.png")
        Icon_penger = self.load_icon("Icons/Icon_penger.png")

        # Knapper
        ctk.CTkButton(
            self, text="Prosentkalkulator", command=prosent_callback,
            image=prosent_icon, compound="top", width=150, fg_color="#cf1e91", hover_color="#951671"
        ).grid(row=1, column=1, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Kalkulator", command=kalkulator_callback,
            image=kalkulator_icon, compound="top", width=150, fg_color="#7652c7"
        ).grid(row=1, column=2, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Graf kalkulator", command=graf_callback,
            image=graf_icon, compound="top", width=150, fg_color="#e3cd93"
        ).grid(row=1, column=3, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Konverteringskalkulator", command=konvertering_callback,
            image=Data_icon, compound="top", width=150, fg_color="#bf35a3"
        ).grid(row=2, column=1, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Trig kalkulatoren", command=TrigonometryCalculator_callback,
            image=Trig_icon, compound="top", width=150, fg_color="#896dcd"
        ).grid(row=2, column=2, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Tidskalkulatorer", command=Tidskalkulator_callback,
            image=Tidskalkulatorer_icon, compound="top", width=150, fg_color="#f78759"
        ).grid(row=2, column=3, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Finans Kalkulator", command=FinansKalkulator_callback,
            image=Icon_penger, compound="top", width=150, fg_color="#b043b4"
        ).grid(row=3, column=1, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Kommer Straks",
            image=Soon_icon, compound="top", width=150, fg_color="#9e85d3"
        ).grid(row=3, column=2, pady=10, padx=5)

        ctk.CTkButton(
            self, text="Kommer Straks",
            image=Soon_icon, compound="top", width=150, fg_color="#fc0007"
        ).grid(row=3, column=3, pady=10, padx=5)

        ctk.CTkLabel(
            self, text="Laget Av David :) Klasse: 1IM1", width=250
        ).grid(row=4, column=2, pady=10, padx=5)

    @staticmethod
    def load_icon(file_path):
        """Last inn et ikon fra fil. Returner et bildeobjekt eller et standardikon hvis filen ikke finnes."""
        if os.path.exists(file_path):
            img = Image.open(file_path)
            return CTkImage(light_image=img, dark_image=img)
        else:
            # Returner et standardikon hvis filen ikke finnes
            return None


class Prosentkalkulator(ctk.CTkFrame):
    """Prosentkalkulator med tre funksjoner."""
    def __init__(self, master, tilbake_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Konfigurer grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Hovedramme
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Topprad med tilbakeknapp og overskrift
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            top_frame, 
            text="← Tilbake", 
            command=tilbake_callback,
            width=100,
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            top_frame, 
            text="Prosentkalkulator", 
            font=("Helvetica", 24, "bold")
        ).grid(row=0, column=1, pady=10)

        # Velg kalkulatortype
        self.kalkulator_type = ctk.CTkSegmentedButton(
            main_frame,
            values=["Beregn %", "Finn %", "Reduser %"],
            command=self.bytt_kalkulator,
            height=40,
            font=("Helvetica", 14)
        )
        self.kalkulator_type.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.kalkulator_type.set("Beregn %")

        # Opprett rammer for hver kalkulator
        self.beregn_frame = self.lag_beregn_prosent()
        self.finn_frame = self.lag_finn_prosent()
        self.reduser_frame = self.lag_reduser_prosent()
        
        # Start med beregn prosent
        self.aktiv_frame = self.beregn_frame
        self.beregn_frame.grid(row=2, column=0, sticky="nsew")
        self.finn_frame.grid_forget()
        self.reduser_frame.grid_forget()

        # Legg til Enter-binding for beregn prosent
        self.entry_total_1.bind('<Return>', lambda event: self.beregn_prosent())
        self.entry_total_1.bind('<KP_Enter>', lambda event: self.beregn_prosent())
        self.entry_prosent_1.bind('<Return>', lambda event: self.beregn_prosent())
        self.entry_prosent_1.bind('<KP_Enter>', lambda event: self.beregn_prosent())

        # Legg til Enter-binding for finn prosent
        self.entry_total_2.bind('<Return>', lambda event: self.finn_prosent())
        self.entry_total_2.bind('<KP_Enter>', lambda event: self.finn_prosent())
        self.entry_belop_2.bind('<Return>', lambda event: self.finn_prosent())
        self.entry_belop_2.bind('<KP_Enter>', lambda event: self.finn_prosent())

        # Legg til Enter-binding for reduser prosent
        self.entry_total_3.bind('<Return>', lambda event: self.reduser_prosent())
        self.entry_total_3.bind('<KP_Enter>', lambda event: self.reduser_prosent())
        self.entry_prosent_3.bind('<Return>', lambda event: self.reduser_prosent())
        self.entry_prosent_3.bind('<KP_Enter>', lambda event: self.reduser_prosent())

    def lag_beregn_prosent(self):
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Input-felt
        input_frame = ctk.CTkFrame(frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Total beløp
        ctk.CTkLabel(
            input_frame, 
            text="Total beløp:", 
            font=("Helvetica", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_total_1 = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 1000",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry_total_1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Prosent
        ctk.CTkLabel(
            input_frame, 
            text="Prosent:", 
            font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_prosent_1 = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 10",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry_prosent_1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Beregn-knapp
        ctk.CTkButton(
            frame, 
            text="Beregn", 
            command=self.beregn_prosent,
            height=45,
            font=("Helvetica", 16, "bold"),
            fg_color="#cf1e91",
            hover_color="#951671"
        ).grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        # Resultatramme
        result_frame = ctk.CTkFrame(frame)
        result_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        result_frame.grid_columnconfigure(0, weight=1)

        self.resultat_1 = ctk.CTkLabel(
            result_frame, 
            text="Resultat vil vises her",
            font=("Helvetica", 14)
        )
        self.resultat_1.grid(row=0, column=0, pady=10)

        return frame

    def bytt_kalkulator(self, valg):
        self.aktiv_frame.grid_forget()
        if valg == "Beregn %":
            self.aktiv_frame = self.beregn_frame
        elif valg == "Finn %":
            self.aktiv_frame = self.finn_frame
        else:
            self.aktiv_frame = self.reduser_frame
        self.aktiv_frame.grid(row=2, column=0, sticky="nsew")

    def beregn_prosent(self, event=None):
        """Beregn prosent av beløp."""
        try:
            total = float(self.entry_total_1.get())
            prosent = float(self.entry_prosent_1.get())
            resultat = (prosent / 100) * total
            self.resultat_1.configure(text=f"Resultat: {resultat:.2f}")
        except ValueError:
            self.resultat_1.configure(text="Ugyldige tall!")

    def lag_finn_prosent(self):
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Input-felt
        input_frame = ctk.CTkFrame(frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Total beløp
        ctk.CTkLabel(
            input_frame, 
            text="Total beløp:", 
            font=("Helvetica", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_total_2 = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 1000",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry_total_2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Beløp
        ctk.CTkLabel(
            input_frame, 
            text="Beløp:", 
            font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_belop_2 = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 250",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry_belop_2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Beregn-knapp
        ctk.CTkButton(
            frame, 
            text="Beregn prosent", 
            command=self.finn_prosent,
            height=45,
            font=("Helvetica", 16, "bold"),
            fg_color="#cf1e91",
            hover_color="#951671"
        ).grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        # Resultatramme
        result_frame = ctk.CTkFrame(frame)
        result_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        result_frame.grid_columnconfigure(0, weight=1)

        self.resultat_2 = ctk.CTkLabel(
            result_frame, 
            text="Prosent vil vises her",
            font=("Helvetica", 14)
        )
        self.resultat_2.grid(row=0, column=0, pady=10)

        return frame

    def finn_prosent(self, event=None):
        """Finn prosentverdien."""
        try:
            total = float(self.entry_total_2.get())
            belop = float(self.entry_belop_2.get())
            prosent = (belop / total) * 100
            self.resultat_2.configure(text=f"Prosent: {prosent:.2f}%")
        except ValueError:
            self.resultat_2.configure(text="Ugyldige tall!")

    def lag_reduser_prosent(self):
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Input-felt
        input_frame = ctk.CTkFrame(frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Total beløp
        ctk.CTkLabel(
            input_frame, 
            text="Total beløp:", 
            font=("Helvetica", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_total_3 = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 1000",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry_total_3.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Prosent
        ctk.CTkLabel(
            input_frame, 
            text="Prosent:", 
            font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_prosent_3 = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 20",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry_prosent_3.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Beregn-knapp
        ctk.CTkButton(
            frame, 
            text="Beregn redusert beløp", 
            command=self.reduser_prosent,
            height=45,
            font=("Helvetica", 16, "bold"),
            fg_color="#cf1e91",
            hover_color="#951671"
        ).grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        # Resultatramme
        result_frame = ctk.CTkFrame(frame)
        result_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        result_frame.grid_columnconfigure(0, weight=1)

        self.resultat_3 = ctk.CTkLabel(
            result_frame, 
            text="Redusert beløp vil vises her",
            font=("Helvetica", 14)
        )
        self.resultat_3.grid(row=0, column=0, pady=10)

        return frame

    def reduser_prosent(self, event=None):
        """Reduser beløp med prosent."""
        try:
            total = float(self.entry_total_3.get())
            prosent = float(self.entry_prosent_3.get())
            redusert_belop = total - (prosent / 100) * total
            self.resultat_3.configure(text=f"Redusert beløp: {redusert_belop:.2f}")
        except ValueError:
            self.resultat_3.configure(text="Ugyldige tall!")
class Kalkulator(ctk.CTkFrame):
    """Standard kalkulator."""
    def __init__(self, master, tilbake_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Konfigurer grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Hovedramme
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Topprad med tilbakeknapp og overskrift
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            top_frame, 
            text="← Tilbake", 
            command=tilbake_callback,
            width=100,
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            top_frame, 
            text="Kalkulator", 
            font=("Helvetica", 24, "bold")
        ).grid(row=0, column=1, pady=10)

        # Display
        self.display = ctk.CTkEntry(
            main_frame, 
            font=("Helvetica", 24),
            justify="right",
            height=60
        )
        self.display.grid(row=1, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="ew")

        # Knapperad
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=2, column=0, sticky="nsew", padx=20)
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Knappekonfigurasjon
        buttons = [
            ('7', '#4a4a4a', '#363636'), ('8', '#4a4a4a', '#363636'), ('9', '#4a4a4a', '#363636'), ('/', '#2f2f2f', '#1f1f1f'),
            ('4', '#4a4a4a', '#363636'), ('5', '#4a4a4a', '#363636'), ('6', '#4a4a4a', '#363636'), ('*', '#2f2f2f', '#1f1f1f'),
            ('1', '#4a4a4a', '#363636'), ('2', '#4a4a4a', '#363636'), ('3', '#4a4a4a', '#363636'), ('-', '#2f2f2f', '#1f1f1f'),
            ('0', '#4a4a4a', '#363636'), ('.', '#4a4a4a', '#363636'), ('=', '#1f6aa5', '#144d75'), ('+', '#2f2f2f', '#1f1f1f')
        ]

        row = 0
        col = 0
        for (text, fg_color, hover_color) in buttons:
            cmd = self.calculate_result if text == '=' else lambda x=text: self.add_to_display(x)
            ctk.CTkButton(
                button_frame,
                text=text,
                command=cmd,
                width=80,
                height=60,
                font=("Helvetica", 18, "bold"),
                fg_color=fg_color,
                hover_color=hover_color
            ).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Clear knapp
        ctk.CTkButton(
            button_frame,
            text="C",
            command=self.clear_display,
            width=80,
            height=60,
            font=("Helvetica", 18, "bold"),
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Legg til binding for Enter-tasten i display
        self.display.bind('<Return>', lambda event: self.calculate_result())
        self.display.bind('<KP_Enter>', lambda event: self.calculate_result())  # For numerisk tastatur

    def add_to_display(self, value):
        current = self.display.get()
        self.display.delete(0, "end")
        self.display.insert("end", current + value)

    def clear_display(self):
        self.display.delete(0, "end")

    def calculate_result(self, event=None):
        try:
            result = eval(self.display.get())
            self.display.delete(0, "end")
            self.display.insert(0, str(result))
        except Exception:
            self.display.delete(0, "end")
            self.display.insert(0, "Feil")
class GrafKalkulator(ctk.CTkFrame):
    """Grafkalkulator som plotter matematiske funksjoner."""
    def __init__(self, master, tilbake_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Konfigurer grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Hovedramme
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Topprad med tilbakeknapp og overskrift
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            top_frame, 
            text="← Tilbake", 
            command=tilbake_callback,
            width=100,
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            top_frame, 
            text="Grafkalkulator", 
            font=("Helvetica", 24, "bold")
        ).grid(row=0, column=1, pady=10)

        # Input-ramme
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Funksjonsinput
        ctk.CTkLabel(
            input_frame,
            text="Funksjon f(x):",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, pady=10, padx=(10, 5), sticky="w")

        self.display = ctk.CTkEntry(
            input_frame,
            placeholder_text="f.eks. x**2 eller sin(x)",
            height=35,
            font=("Helvetica", 14)
        )
        self.display.grid(row=0, column=1, pady=10, padx=(5, 10), sticky="ew")

        # Knapperad
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Plot-knapp
        self.plot_button = ctk.CTkButton(
            button_frame,
            text="Plot Graf",
            command=self.plot_function,
            width=150,
            height=40,
            font=("Helvetica", 14, "bold"),
            fg_color="#896dcd",
            hover_color="#7652c7"
        )
        self.plot_button.grid(row=0, column=0, padx=5, pady=10)

        # Lagre-knapp
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Lagre Graf",
            command=self.save_plot,
            width=150,
            height=40,
            font=("Helvetica", 14),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.save_button.grid(row=0, column=1, padx=5, pady=10)

        # Graf-ramme
        plot_frame = ctk.CTkFrame(main_frame)
        plot_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        plot_frame.grid_columnconfigure(0, weight=1)
        plot_frame.grid_rowconfigure(0, weight=1)

        # Opprett figur og canvas
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.figure.patch.set_facecolor('#2b2b2b')  # Mørk bakgrunn
        self.ax.set_facecolor('#2b2b2b')  # Mørk bakgrunn for plotteområdet
        
        # Stil for aksene
        self.ax.grid(True, color='#555555')
        self.ax.spines['bottom'].set_color('#ffffff')
        self.ax.spines['top'].set_color('#ffffff')
        self.ax.spines['right'].set_color('#ffffff')
        self.ax.spines['left'].set_color('#ffffff')
        self.ax.tick_params(axis='x', colors='#ffffff')
        self.ax.tick_params(axis='y', colors='#ffffff')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Legg til Enter-binding
        self.display.bind('<Return>', lambda event: self.plot_function())
        self.display.bind('<KP_Enter>', lambda event: self.plot_function())

    def plot_function(self, event=None):
        """Plotter funksjonen som er skrevet inn i displayet."""
        function_text = self.display.get()
        function_text = function_text.replace(' ', '').replace('^', '**')
        if '=' in function_text:
            function_text = function_text.split('=')[1]

        x = np.linspace(-10, 10, 400)
        try:
            # Rens plottet
            self.ax.clear()
            
            # Stil for nytt plott
            self.ax.grid(True, color='#555555')
            self.ax.set_facecolor('#2b2b2b')
            self.ax.spines['bottom'].set_color('#ffffff')
            self.ax.spines['top'].set_color('#ffffff')
            self.ax.spines['right'].set_color('#ffffff')
            self.ax.spines['left'].set_color('#ffffff')
            self.ax.tick_params(axis='x', colors='#ffffff')
            self.ax.tick_params(axis='y', colors='#ffffff')
            
            # Plot funksjonen
            expr = sp.sympify(function_text)
            y = sp.lambdify(sp.symbols('x'), expr, modules=['numpy'])(x)
            self.ax.plot(x, y, color='#896dcd', linewidth=2)
            
            # Sett tittel
            self.ax.set_title(f"f(x) = {function_text}", color='#ffffff', pad=10)
            
            # Oppdater canvas
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Feil", f"Kunne ikke plotte funksjonen:\n{str(e)}")

    def save_plot(self):
        """Lagrer grafen som et bilde."""
        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPG Files", "*.jpg")]
        )
        if file_path:
            try:
                self.figure.savefig(file_path, 
                                  facecolor=self.figure.get_facecolor(), 
                                  edgecolor='none', 
                                  bbox_inches='tight')
                messagebox.showinfo("Suksess", "Grafen ble lagret!")
            except Exception as e:
                messagebox.showerror("Feil", f"Kunne ikke lagre grafen:\n{str(e)}")
class ConversionCalculator(ctk.CTkFrame):
    def __init__(self, master, tilbake_callback, konvertering_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Konfigurer grid weights for hovedrammen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Hovedramme
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(5, weight=1)  # La resultatrammen ekspandere
        main_frame.grid_columnconfigure(0, weight=1)

        # Topprad med tilbakeknapp og overskrift
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            top_frame, 
            text="← Tilbake", 
            command=tilbake_callback,
            width=100,
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            top_frame, 
            text="Konverteringskalkulator", 
            font=("Helvetica", 24, "bold")
        ).grid(row=0, column=1, pady=10)

        # Velg konverteringstype
        type_frame = ctk.CTkFrame(main_frame)
        type_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        type_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            type_frame,
            text="Velg konverteringstype:",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, padx=10, sticky="w")

        self.convert_type = ctk.CTkOptionMenu(
            type_frame,
            values=["Temperatur", "Lengde", "Vekt", "Dataenheter", "Valuta", "Hastighet", "Areal", "Volum"],
            command=self.update_fields,
            width=200,
            height=35,
            font=("Helvetica", 14)
        )
        self.convert_type.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.convert_type.set("Temperatur")

        # Input ramme
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Fra-enhet
        ctk.CTkLabel(
            input_frame,
            text="Fra:",
            font=("Helvetica", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.from_unit = ctk.CTkOptionMenu(
            input_frame,
            values=[],
            width=200,
            height=35,
            font=("Helvetica", 14)
        )
        self.from_unit.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Til-enhet
        ctk.CTkLabel(
            input_frame,
            text="Til:",
            font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.to_unit = ctk.CTkOptionMenu(
            input_frame,
            values=[],
            width=200,
            height=35,
            font=("Helvetica", 14)
        )
        self.to_unit.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Verdi input
        ctk.CTkLabel(
            input_frame,
            text="Verdi:",
            font=("Helvetica", 14)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.input_value = ctk.CTkEntry(
            input_frame,
            placeholder_text="Skriv inn verdi",
            width=200,
            height=35,
            font=("Helvetica", 14)
        )
        self.input_value.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Knapper
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_frame,
            text="Konverter",
            command=self.convert,
            width=150,
            height=40,
            font=("Helvetica", 14, "bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).grid(row=0, column=0, padx=5, pady=10)

        ctk.CTkButton(
            button_frame,
            text="Nullstill",
            command=self.clear_fields,
            width=150,
            height=40,
            font=("Helvetica", 14),
            fg_color="#FF9800",
            hover_color="#F57C00"
        ).grid(row=0, column=1, padx=5, pady=10)

        # Resultatramme
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)
        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(
            result_frame,
            text="Resultat vil vises her",
            font=("Helvetica", 16)
        )
        self.result_label.grid(row=0, column=0, pady=20)

        # Initialiser konverteringsenheter
        self.conversion_units = {
            "Temperatur": ["Celsius", "Fahrenheit", "Kelvin"],
            "Lengde": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Fot", "Tommer"],
            "Vekt": ["Kilogram", "Gram", "Milligram", "Pund", "Ounce", "Tonn"],
            "Dataenheter": ["Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte", "Petabyte"],
            "Valuta": ["NOK", "USD", "EUR", "GBP", "SEK", "DKK"],
            "Hastighet": ["km/t", "m/s", "mph", "knop"],
            "Areal": ["m²", "km²", "cm²", "mm²", "hektar", "acre"],
            "Volum": ["m³", "liter", "milliliter", "gallon", "kubikkfot"]
        }

        # Initialiser feltene
        self.update_fields("Temperatur")

        # Legg til Enter-binding
        self.input_value.bind('<Return>', lambda event: self.convert())
        self.input_value.bind('<KP_Enter>', lambda event: self.convert())

    def update_fields(self, selected_type):
        """Oppdater enhetsvalgene basert på valgt konverteringstype"""
        units = self.conversion_units.get(selected_type, [])
        self.from_unit.configure(values=units)
        self.to_unit.configure(values=units)
        if units:
            self.from_unit.set(units[0])
            self.to_unit.set(units[1] if len(units) > 1 else units[0])

    def convert(self, event=None):
        """Utfør konverteringen"""
        try:
            value = float(self.input_value.get().replace(",", "."))
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            conv_type = self.convert_type.get()

            result = self.perform_conversion(value, from_unit, to_unit, conv_type)
            
            if result is not None:
                self.result_label.configure(
                    text=f"{value} {from_unit} = {result:.4f} {to_unit}"
                )
            else:
                self.result_label.configure(
                    text="Kunne ikke utføre konverteringen"
                )

        except ValueError:
            self.result_label.configure(
                text="Vennligst skriv inn et gyldig tall"
            )

    def perform_conversion(self, value, from_unit, to_unit, conv_type):
        """Utfør selve konverteringen basert på type og enheter"""
        # Temperaturkonverteringer
        if conv_type == "Temperatur":
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                return (value - 32) * 5/9
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                return value + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                return value - 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32

        # Lengdekonverteringer
        elif conv_type == "Lengde":
            # Konverter alt til meter først
            meters = {
                "Meter": value,
                "Kilometer": value * 1000,
                "Centimeter": value / 100,
                "Millimeter": value / 1000,
                "Mile": value * 1609.344,
                "Yard": value * 0.9144,
                "Fot": value * 0.3048,
                "Tommer": value * 0.0254
            }
            
            # Konverter fra meter til målenheten
            conversions = {
                "Meter": 1,
                "Kilometer": 0.001,
                "Centimeter": 100,
                "Millimeter": 1000,
                "Mile": 1/1609.344,
                "Yard": 1/0.9144,
                "Fot": 1/0.3048,
                "Tommer": 1/0.0254
            }
            
            return meters[from_unit] * conversions[to_unit]

        # Vektkonverteringer
        elif conv_type == "Vekt":
            # Konverter alt til gram først
            grams = {
                "Kilogram": value * 1000,
                "Gram": value,
                "Milligram": value / 1000,
                "Pund": value * 453.59237,
                "Ounce": value * 28.349523125,
                "Tonn": value * 1000000
            }
            
            # Konverter fra gram til målenheten
            conversions = {
                "Kilogram": 0.001,
                "Gram": 1,
                "Milligram": 1000,
                "Pund": 1/453.59237,
                "Ounce": 1/28.349523125,
                "Tonn": 0.000001
            }
            
            return grams[from_unit] * conversions[to_unit]

        # Dataenheter
        elif conv_type == "Dataenheter":
            # Konverter alt til bytes først
            bytes_value = {
                "Byte": value,
                "Kilobyte": value * 1024,
                "Megabyte": value * 1024**2,
                "Gigabyte": value * 1024**3,
                "Terabyte": value * 1024**4,
                "Petabyte": value * 1024**5
            }
            
            # Konverter fra bytes til målenheten
            conversions = {
                "Byte": 1,
                "Kilobyte": 1/1024,
                "Megabyte": 1/1024**2,
                "Gigabyte": 1/1024**3,
                "Terabyte": 1/1024**4,
                "Petabyte": 1/1024**5
            }
            
            return bytes_value[from_unit] * conversions[to_unit]

        # Hastighet
        elif conv_type == "Hastighet":
            # Konverter alt til m/s først
            ms_value = {
                "km/t": value / 3.6,
                "m/s": value,
                "mph": value / 2.237,
                "knop": value / 1.944
            }
            
            # Konverter fra m/s til målenheten
            conversions = {
                "km/t": 3.6,
                "m/s": 1,
                "mph": 2.237,
                "knop": 1.944
            }
            
            return ms_value[from_unit] * conversions[to_unit]

        # Areal
        elif conv_type == "Areal":
            # Konverter alt til m² først
            m2_value = {
                "m²": value,
                "km²": value * 1000000,
                "cm²": value / 10000,
                "mm²": value / 1000000,
                "hektar": value * 10000,
                "acre": value * 4046.86
            }
            
            # Konverter fra m² til målenheten
            conversions = {
                "m²": 1,
                "km²": 0.000001,
                "cm²": 10000,
                "mm²": 1000000,
                "hektar": 0.0001,
                "acre": 1/4046.86
            }
            
            return m2_value[from_unit] * conversions[to_unit]

        # Volum
        elif conv_type == "Volum":
            # Konverter alt til m³ først
            m3_value = {
                "m³": value,
                "liter": value / 1000,
                "milliliter": value / 1000000,
                "gallon": value / 264.172,
                "kubikkfot": value / 35.3147
            }
            
            # Konverter fra m³ til målenheten
            conversions = {
                "m³": 1,
                "liter": 1000,
                "milliliter": 1000000,
                "gallon": 264.172,
                "kubikkfot": 35.3147
            }
            
            return m3_value[from_unit] * conversions[to_unit]

        return None

    def clear_fields(self):
        """Nullstill alle felt"""
        self.input_value.delete(0, "end")
        self.result_label.configure(text="Resultat vil vises her")
class TrigonometryCalculator(ctk.CTkFrame):
    def __init__(self, master, tilbake_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Konfigurer grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Hovedramme
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Topprad med tilbakeknapp og overskrift
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            top_frame, 
            text="← Tilbake", 
            command=tilbake_callback,
            width=100,
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            top_frame, 
            text="Trigonometrisk Kalkulator", 
            font=("Helvetica", 24, "bold")
        ).grid(row=0, column=1, pady=10)

        # Input-ramme
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Vinkel input
        ctk.CTkLabel(
            input_frame, 
            text="Vinkel i grader:",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, pady=10, padx=(10, 5), sticky="w")

        self.entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 30 eller 45",
            height=35,
            font=("Helvetica", 14)
        )
        self.entry.grid(row=0, column=1, pady=10, padx=(5, 10), sticky="ew")

        # Operasjonsvalg
        ctk.CTkLabel(
            input_frame, 
            text="Velg funksjon:",
            font=("Helvetica", 14, "bold")
        ).grid(row=1, column=0, pady=10, padx=(10, 5), sticky="w")

        self.operation_var = ctk.StringVar(value="Sin")
        self.operation_menu = ctk.CTkOptionMenu(
            input_frame,
            variable=self.operation_var,
            values=["Sin", "Cos", "Tan", "Sec", "Csc", "Cot"],
            width=200,
            height=35,
            font=("Helvetica", 14),
            fg_color="#896dcd",
            button_color="#7652c7",
            button_hover_color="#5b3e9e"
        )
        self.operation_menu.grid(row=1, column=1, pady=10, padx=(5, 10), sticky="ew")

        # Beregn-knapp
        ctk.CTkButton(
            main_frame,
            text="Beregn",
            command=self.calculate,
            width=200,
            height=45,
            font=("Helvetica", 16, "bold"),
            fg_color="#896dcd",
            hover_color="#7652c7"
        ).grid(row=2, column=0, pady=20)

        # Resultatramme
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        result_frame.grid_columnconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(
            result_frame,
            text="Resultat vil vises her",
            font=("Helvetica", 16),
            height=40
        )
        self.result_label.grid(row=0, column=0, pady=15)

        # Tøm-knapp
        ctk.CTkButton(
            main_frame,
            text="Tøm",
            command=self.clear_inputs,
            width=200,
            height=40,
            font=("Helvetica", 14),
            fg_color="#DB4437",
            hover_color="#B33225"
        ).grid(row=4, column=0, pady=(0, 20))

        # Legg til Enter-binding
        self.entry.bind('<Return>', lambda event: self.calculate())
        self.entry.bind('<KP_Enter>', lambda event: self.calculate())

    def calculate(self, event=None):
        try:
            angle = self.entry.get().strip()
            if not angle:
                self.result_label.configure(text="Vennligst skriv inn en vinkel")
                return
            angle = float(angle)
            
            operation = self.operation_var.get()
            
            # Utfør beregningen
            if operation == "Sin":
                result = math.sin(math.radians(angle))
            elif operation == "Cos":
                result = math.cos(math.radians(angle))
            elif operation == "Tan":
                result = math.tan(math.radians(angle))
            elif operation == "Sec":
                result = 1 / math.cos(math.radians(angle))
            elif operation == "Csc":
                result = 1 / math.sin(math.radians(angle))
            elif operation == "Cot":
                result = 1 / math.tan(math.radians(angle))
            
            self.result_label.configure(
                text=f"{operation}({angle}°) = {result:.6f}",
                font=("Helvetica", 16, "bold")
            )

        except ValueError:
            self.result_label.configure(
                text="Ugyldig verdi for vinkel",
                font=("Helvetica", 16)
            )
        except ZeroDivisionError:
            self.result_label.configure(
                text="Matematisk feil: Deling på null",
                font=("Helvetica", 16)
            )

    def clear_inputs(self):
        self.entry.delete(0, ctk.END)
        self.operation_var.set("Sin")
        self.result_label.configure(
            text="Resultat vil vises her",
            font=("Helvetica", 16)
        )
class Tidskalkulator(ctk.CTkFrame):
    """Tidskalkulator med start- og sluttdato og tid."""
    def __init__(self, master, tilbake_callback=None, tidskalkulator_callback=None):
        super().__init__(master)

        self.configure_grid()

        if tilbake_callback:
            ctk.CTkButton(self, text="Tilbake", command=tilbake_callback).grid(row=0, column=0, pady=10)

        self.setup_ui()

    def configure_grid(self):
        """Sett opp grid-konfigurasjon."""
        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def setup_ui(self):
        """Konfigurer brukergrensesnitt."""
        header_label = ctk.CTkLabel(self, text="Tidskalkulator", font=("Helvetica", 24, "bold"))
        header_label.grid(row=1, column=0, columnspan=2, pady=20)

        start_frame = ctk.CTkFrame(self)
        start_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        ctk.CTkLabel(start_frame, text="Startdato:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_date_entry = DateEntry(start_frame, date_pattern="yyyy-mm-dd", width=18)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(start_frame, text="Starttid (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.start_time_entry = ctk.CTkEntry(start_frame, width=30, font=("Helvetica", 14), justify="center")
        self.start_time_entry.grid(row=1, column=1, padx=10, pady=5)

        end_frame = ctk.CTkFrame(self)
        end_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ctk.CTkLabel(end_frame, text="Sluttdato:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.end_date_entry = DateEntry(end_frame, date_pattern="yyyy-mm-dd", width=18)
        self.end_date_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(end_frame, text="Slutttid (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.end_time_entry = ctk.CTkEntry(end_frame, width=30, font=("Helvetica", 14), justify="center")
        self.end_time_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text="Beregn tid", command=self.calculate_time, fg_color="#1f6aa5", hover_color="#144d75").grid(row=4, column=0, columnspan=2, pady=20)

        result_frame = ctk.CTkFrame(self)
        result_frame.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")
        self.result_label = ctk.CTkLabel(result_frame, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=10)

        # Legg til en nullstillingsknapp
        ctk.CTkButton(self, text="Nullstill", command=self.clear_fields, fg_color="#FF9800", hover_color="#F57C00").grid(row=4, column=1, pady=20)

        # Legg til en dropdown-meny for tidsformat
        self.time_format_var = ctk.StringVar(value="Timer")  # Standardverdi
        time_format_menu = ctk.CTkOptionMenu(
            self,
            variable=self.time_format_var,
            values=["Sekunder", "Minutter", "Timer"],
            command=self.update_time_format
        )
        time_format_menu.grid(row=4, column=0, pady=10)

        # Legg til en knapp for å beregne tid i timer, minutter og sekunder
        ctk.CTkButton(self, text="Beregn tid i timer/minutter/sekunder", command=self.calculate_time_units).grid(row=6, column=0, columnspan=2, pady=20)

    def calculate_time(self):
        """Beregn tid mellom to datoer/klokkeslett."""
        try:
            # Hent verdier fra input-feltene
            start_date = self.start_date_entry.get()
            start_time = self.start_time_entry.get()
            end_date = self.end_date_entry.get()
            end_time = self.end_time_entry.get()

            # Kombiner dato og tid til datetime-objekter
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

            # Valider at sluttdato er etter startdato
            if end_datetime < start_datetime:
                messagebox.showerror("Feil", "Sluttdato må være etter startdato!")
                return

            # Beregn forskjellen
            time_difference = end_datetime - start_datetime

            # Vis resultatet i henhold til valgt format
            total_seconds = time_difference.total_seconds()
            if self.time_format_var.get() == "Sekunder":
                result_text = f"Forskjell: {total_seconds:.0f} sekunder"
            elif self.time_format_var.get() == "Minutter":
                result_text = f"Forskjell: {total_seconds / 60:.0f} minutter"
            else:  # Timer
                days, seconds = time_difference.days, time_difference.seconds
                hours, minutes = divmod(seconds, 3600)
                minutes //= 60
                result_text = f"Forskjell: {days} dager, {hours} timer, {minutes} minutter"

            self.result_label.configure(text=result_text)
        except ValueError:
            messagebox.showerror("Feil", "Vennligst skriv inn dato og tid i riktig format!\nFormat: YYYY-MM-DD for dato og HH:MM for tid.")

    def update_time_format(self, selected_format):
        """Oppdaterer visningen basert på valgt tidsformat."""
        self.calculate_time()  # Kall beregningsmetoden for å oppdatere resultatet

    def copy_result(self):
        """Kopier resultatet til utklippstavlen."""
        result_text = self.result_label.cget("text")
        if result_text:
            self.clipboard_clear()  # Tøm utklippstavlen
            self.clipboard_append(result_text)  # Legg til resultatet
            messagebox.showinfo("Kopiert", "Resultatet er kopiert til utklippstavlen!")
        else:
            messagebox.showwarning("Ingen data", "Ingen resultat å kopiere.")

    def clear_fields(self):
        """Nullstill alle felt."""
        self.start_date_entry.delete(0, "end")
        self.start_time_entry.delete(0, "end")
        self.end_date_entry.delete(0, "end")
        self.end_time_entry.delete(0, "end")
        self.result_label.configure(text="")

    def calculate_time_units(self):
        """Beregn tid mellom to datoer/klokkeslett i timer, minutter og sekunder."""
        try:
            # Hent verdier fra input-feltene
            start_date = self.start_date_entry.get()
            start_time = self.start_time_entry.get()
            end_date = self.end_date_entry.get()
            end_time = self.end_time_entry.get()

            # Kombiner dato og tid til datetime-objekter
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

            # Valider at sluttdato er etter startdato
            if end_datetime < start_datetime:
                messagebox.showerror("Feil", "Sluttdato må være etter startdato!")
                return

            # Beregn forskjellen
            time_difference = end_datetime - start_datetime

            # Vis resultatet i timer, minutter og sekunder
            total_seconds = time_difference.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            result_text = f"Forskjell: {int(hours)} timer, {int(minutes)} minutter, {int(seconds)} sekunder"
            self.result_label.configure(text=result_text)
        except ValueError:
            messagebox.showerror("Feil", "Vennligst skriv inn dato og tid i riktig format!\nFormat: YYYY-MM-DD for dato og HH:MM for tid.")

class FinansKalkulator(ctk.CTkFrame):
    def __init__(self, master, tilbake_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Konfigurer grid weights for hovedrammen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Hovedramme - oppdater grid-konfigurasjon
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)  # La innholdet ekspandere
        main_frame.grid_columnconfigure(0, weight=1)

        # Topprad med tilbakeknapp og overskrift
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            top_frame, 
            text="← Tilbake", 
            command=tilbake_callback,
            width=100,
            fg_color="#DB4437",  # Rød farge
            hover_color="#B33225"
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            top_frame, 
            text="Finansiell Kalkulator", 
            font=("Helvetica", 24, "bold")
        ).grid(row=0, column=1, pady=10)

        # Velg kalkulatortype med større og tydeligere knapper
        self.kalkulator_type = ctk.CTkSegmentedButton(
            main_frame,
            values=["Lånekalkulator", "Sparekalkulator"],
            command=self.bytt_kalkulator,
            height=40,
            font=("Helvetica", 14)
        )
        self.kalkulator_type.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.kalkulator_type.set("Lånekalkulator")

        # Opprett rammer for hver kalkulator
        self.lane_frame = self.opprett_lane_frame()
        self.spare_frame = self.opprett_spare_frame()
        
        # Start med lånekalkulatoren
        self.aktiv_frame = self.lane_frame
        self.lane_frame.grid(row=2, column=0, sticky="nsew")
        self.spare_frame.grid_forget()

        # Legg til Enter-binding for lånekalkulator
        self.loan_amount_entry.bind('<Return>', lambda event: self.calculate_loan())
        self.loan_amount_entry.bind('<KP_Enter>', lambda event: self.calculate_loan())
        self.interest_rate_entry.bind('<Return>', lambda event: self.calculate_loan())
        self.interest_rate_entry.bind('<KP_Enter>', lambda event: self.calculate_loan())
        self.years_entry.bind('<Return>', lambda event: self.calculate_loan())
        self.years_entry.bind('<KP_Enter>', lambda event: self.calculate_loan())

        # Legg til Enter-binding for sparekalkulator
        self.monthly_savings_entry.bind('<Return>', lambda event: self.calculate_savings())
        self.monthly_savings_entry.bind('<KP_Enter>', lambda event: self.calculate_savings())
        self.savings_rate_entry.bind('<Return>', lambda event: self.calculate_savings())
        self.savings_rate_entry.bind('<KP_Enter>', lambda event: self.calculate_savings())
        self.savings_years_entry.bind('<Return>', lambda event: self.calculate_savings())
        self.savings_years_entry.bind('<KP_Enter>', lambda event: self.calculate_savings())

    def opprett_lane_frame(self):
        """Oppretter ramme for lånekalkulatoren"""
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(2, weight=1)  # La resultatrammen ekspandere
        frame.grid_columnconfigure(0, weight=1)

        # Input-felt med bedre spacing og design
        input_frame = ctk.CTkFrame(frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Lånebeløp
        ctk.CTkLabel(
            input_frame, 
            text="Lånebeløp (NOK):", 
            font=("Helvetica", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.loan_amount_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 2 000 000",
            height=35,
            font=("Helvetica", 14)
        )
        self.loan_amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Rentesats
        ctk.CTkLabel(
            input_frame, 
            text="Årlig rente (%):", 
            font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.interest_rate_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 3.5",
            height=35,
            font=("Helvetica", 14)
        )
        self.interest_rate_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Nedbetalingstid
        ctk.CTkLabel(
            input_frame, 
            text="Nedbetalingstid (år):", 
            font=("Helvetica", 14)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.years_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 25",
            height=35,
            font=("Helvetica", 14)
        )
        self.years_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Beregn-knapp
        ctk.CTkButton(
            frame, 
            text="Beregn lån", 
            command=self.calculate_loan,
            height=45,
            font=("Helvetica", 16, "bold"),
            fg_color="#b043b4",
            hover_color="#863389"
        ).grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        # Resultatramme med bedre visuell presentasjon
        result_frame = ctk.CTkFrame(frame)
        result_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        result_frame.grid_columnconfigure(0, weight=1)

        # Legg til resultat-etiketter
        self.monthly_payment_label = ctk.CTkLabel(
            result_frame, 
            text="Månedlig betaling: --- NOK",
            font=("Helvetica", 14)
        )
        self.monthly_payment_label.grid(row=0, column=0, pady=10)

        self.total_payment_label = ctk.CTkLabel(
            result_frame, 
            text="Totalt beløp: --- NOK",
            font=("Helvetica", 14)
        )
        self.total_payment_label.grid(row=1, column=0, pady=10)

        self.total_interest_label = ctk.CTkLabel(
            result_frame, 
            text="Total rentekostnad: --- NOK",
            font=("Helvetica", 14)
        )
        self.total_interest_label.grid(row=2, column=0, pady=10)

        return frame

    def bytt_kalkulator(self, valg):
        """Bytter mellom låne- og sparekalkulator"""
        self.aktiv_frame.grid_forget()
        if valg == "Lånekalkulator":
            self.aktiv_frame = self.lane_frame
        else:
            self.aktiv_frame = self.spare_frame
        self.aktiv_frame.grid(row=2, column=0, sticky="nsew")

    def calculate_loan(self, event=None):
        """Beregn lånedetaljer"""
        try:
            loan_amount = float(self.loan_amount_entry.get().replace(" ", ""))
            annual_rate = float(self.interest_rate_entry.get().replace(",", "."))
            years = float(self.years_entry.get())

            monthly_rate = annual_rate / 100 / 12
            total_months = int(years * 12)

            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)
            else:
                monthly_payment = loan_amount / total_months

            total_payment = monthly_payment * total_months
            total_interest = total_payment - loan_amount

            self.monthly_payment_label.configure(text=f"Månedlig betaling: {monthly_payment:,.2f} NOK".replace(",", " "))
            self.total_payment_label.configure(text=f"Totalt beløp: {total_payment:,.2f} NOK".replace(",", " "))
            self.total_interest_label.configure(text=f"Total rentekostnad: {total_interest:,.2f} NOK".replace(",", " "))

        except ValueError:
            messagebox.showerror(
                "Feil", 
                "Vennligst fyll inn gyldige tall!\n\n"
                "Lånebeløp: Helt tall uten desimaler\n"
                "Rente: Tall med eller uten desimaler (bruk punktum)\n"
                "År: Helt tall eller desimaltall"
            )

    def calculate_savings(self, event=None):
        """Beregn sparedetaljer"""
        try:
            monthly_savings = float(self.monthly_savings_entry.get().replace(" ", ""))
            annual_rate = float(self.savings_rate_entry.get().replace(",", "."))
            years = float(self.savings_years_entry.get())

            monthly_rate = annual_rate / 100 / 12
            total_months = int(years * 12)

            # Beregn total sparing med rentes rente
            total_savings = 0
            for month in range(total_months):
                total_savings += monthly_savings
                total_savings *= (1 + monthly_rate)

            total_contributions = monthly_savings * total_months
            total_interest = total_savings - total_contributions

            self.total_savings_label.configure(text=f"Total sparing: {total_savings:,.2f} NOK".replace(",", " "))
            self.total_interest_earned_label.configure(text=f"Total renteinntekt: {total_interest:,.2f} NOK".replace(",", " "))
            self.monthly_needed_label.configure(text=f"Månedlig sparing: {monthly_savings:,.2f} NOK".replace(",", " "))

        except ValueError:
            messagebox.showerror(
                "Feil",
                "Vennligst fyll inn gyldige tall!\n\n"
                "Månedlig sparing: Helt tall uten desimaler\n"
                "Rente: Tall med eller uten desimaler (bruk punktum)\n"
                "År: Helt tall eller desimaltall"
            )

    def opprett_spare_frame(self):
        """Oppretter ramme for sparekalkulator"""
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure(2, weight=1)  # La resultatrammen ekspandere
        frame.grid_columnconfigure(0, weight=1)

        # Input-felt
        input_frame = ctk.CTkFrame(frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        input_frame.grid_columnconfigure(1, weight=1)

        # Månedlig sparing
        ctk.CTkLabel(
            input_frame, 
            text="Månedlig sparing (NOK):", 
            font=("Helvetica", 14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.monthly_savings_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 5000",
            height=35,
            font=("Helvetica", 14)
        )
        self.monthly_savings_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Rentesats
        ctk.CTkLabel(
            input_frame, 
            text="Årlig rente (%):", 
            font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.savings_rate_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 3.5",
            height=35,
            font=("Helvetica", 14)
        )
        self.savings_rate_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Spareperiode
        ctk.CTkLabel(
            input_frame, 
            text="Spareperiode (år):", 
            font=("Helvetica", 14)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.savings_years_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="f.eks. 10",
            height=35,
            font=("Helvetica", 14)
        )
        self.savings_years_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Beregn-knapp
        ctk.CTkButton(
            frame, 
            text="Beregn sparing", 
            command=self.calculate_savings,
            height=45,
            font=("Helvetica", 16, "bold"),
            fg_color="#b043b4",
            hover_color="#863389"
        ).grid(row=1, column=0, pady=20, padx=20, sticky="ew")

        # Resultatramme
        result_frame = ctk.CTkFrame(frame)
        result_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        result_frame.grid_columnconfigure(0, weight=1)

        self.total_savings_label = ctk.CTkLabel(
            result_frame, 
            text="Total sparing: --- NOK",
            font=("Helvetica", 14)
        )
        self.total_savings_label.grid(row=0, column=0, pady=10)

        self.total_interest_earned_label = ctk.CTkLabel(
            result_frame, 
            text="Total renteinntekt: --- NOK",
            font=("Helvetica", 14)
        )
        self.total_interest_earned_label.grid(row=1, column=0, pady=10)

        self.monthly_needed_label = ctk.CTkLabel(
            result_frame, 
            text="Månedlig sparing: --- NOK",
            font=("Helvetica", 14)
        )
        self.monthly_needed_label.grid(row=2, column=0, pady=10)

        return frame


class App(ctk.CTk):
    """Hovedapplikasjonen."""
    def __init__(self):
        super().__init__()
        self.title("RegneGeniet")
        self.geometry("575x570")
        self.resizable(False, False)

        # Bestem stien til ikonet
        if getattr(sys, 'frozen', False):
            # Koden kjører fra en frossen .exe
            icon_path = os.path.join(sys._MEIPASS, 'Icons/icon_app.ico')
        else:
            # Koden kjører fra en vanlig Python-fil
            icon_path = 'Icons/icon_app.ico'

        # Bruk icon_path i stedet for den faste stien
        self.iconbitmap(icon_path)

        # Initialize all frames
        self.hovedmeny = Hovedmeny(
            self, 
            self.vis_prosentkalkulator, 
            self.vis_kalkulator, 
            self.vis_grafkalkulator, 
            self.vis_konverteringskalkulator, 
            self.vis_Trigonometry, 
            self.vis_Tidskalkulator,
            self.vis_finanskalkulator  # Legg til denne linjen
        )
        self.prosentkalkulator = Prosentkalkulator(self, self.vis_hovedmeny)
        self.kalkulator = Kalkulator(self, self.vis_hovedmeny)
        self.grafkalkulator = GrafKalkulator(self, self.vis_hovedmeny)
        self.konverteringskalkulator = ConversionCalculator(self, self.vis_hovedmeny, self.konvertering_callback)
        self.Tidskalkulator = Tidskalkulator(self, self.vis_hovedmeny, self.vis_Tidskalkulator)
        self.trigonometry_calculator = TrigonometryCalculator(self, self.vis_hovedmeny)
        self.finanskalkulator = FinansKalkulator(self, self.vis_hovedmeny)

        self.vis_hovedmeny()

    def vis_hovedmeny(self):
        self.hovedmeny.tkraise()

    def vis_prosentkalkulator(self):
        self.prosentkalkulator.tkraise()

    def vis_kalkulator(self):
        self.kalkulator.tkraise()

    def vis_grafkalkulator(self):
        self.grafkalkulator.tkraise()

    def vis_konverteringskalkulator(self):
        self.konverteringskalkulator.tkraise()

    def vis_Trigonometry(self):
        self.trigonometry_calculator.tkraise()
    
    def vis_Tidskalkulator(self):
        self.Tidskalkulator.tkraise()

    def konvertering_callback(self, conversion_type, value, result):
        """Callback to handle conversion result."""
        print(f"Conversion Type: {conversion_type}, Value: {value}, Result: {result}")

    def vis_finanskalkulator(self):
        self.finanskalkulator.tkraise()

def on_closing():
    sys.exit()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()