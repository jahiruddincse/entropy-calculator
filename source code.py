import tkinter as tk
from tkinter import ttk, messagebox
import math

class EntropyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Entropy Change Calculator")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Global style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fa")
        style.configure("TLabel", background="#f5f7fa", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#1a3d7c")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("Result.TLabel", background="#ffffff", relief="solid", padding=10)

        # Constants
        self.R = 8.314  

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)

        self.setup_phase_tab()
        self.setup_heating_tab()
        self.setup_expansion_tab()
        self.setup_spontaneity_tab()

    # ----------------------- Helper Methods -----------------------
    def create_input_row(self, parent, label, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=8)
        entry = ttk.Entry(parent, font=("Segoe UI", 11))
        entry.grid(row=row, column=1, sticky='ew', padx=10)
        parent.columnconfigure(1, weight=1)
        return entry

    def get_float(self, entry):
        try:
            return float(entry.get())
        except:
            return None

    def to_kelvin(self, temp, unit_var):
        return temp + 273.15 if unit_var.get() == "Celsius" else temp

    # ----------------------- Phase Change -----------------------
    def setup_phase_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Phase Change")
        frame = ttk.Frame(tab, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ΔS = ΔH / T", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        self.ph_dh = self.create_input_row(frame, "Enthalpy ΔH (kJ/mol):", 1)

        ttk.Label(frame, text="Temperature:").grid(row=2, column=0, sticky='w', pady=8)
        self.ph_t = ttk.Entry(frame)
        self.ph_t.grid(row=2, column=1, sticky='ew', padx=10)

        self.ph_unit = tk.StringVar(value="Celsius")
        ttk.OptionMenu(frame, self.ph_unit, "Celsius", "Celsius", "Kelvin").grid(row=3, column=1, sticky='w', pady=5)

        ttk.Button(frame, text="Calculate ΔS", command=self.calc_phase).grid(row=4, column=0, columnspan=2, pady=15, sticky='ew')
        self.ph_result = tk.StringVar()
        ttk.Label(frame, textvariable=self.ph_result, style="Result.TLabel").grid(row=5, column=0, columnspan=2, sticky='nsew', pady=10)

    def calc_phase(self):
        dh = self.get_float(self.ph_dh)
        t = self.get_float(self.ph_t)
        if dh is None or t is None:
            messagebox.showerror("Error", "Enter valid numbers.")
            return
        t_k = self.to_kelvin(t, self.ph_unit)
        dh_j = dh * 1000
        ds = dh_j / t_k
        self.ph_result.set(f"Temperature: {t_k:.2f} K\nΔH: {dh_j:.2f} J/mol\nΔS = {ds:.4f} J/(mol·K)")

    # ----------------------- Heating -----------------------
    def setup_heating_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Heating")
        frame = ttk.Frame(tab, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ΔS = nC ln(T₂/T₁)", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        self.heat_n = self.create_input_row(frame, "Moles (n):", 1)
        self.heat_c = self.create_input_row(frame, "Heat Capacity C (J/mol·K):", 2)

        ttk.Label(frame, text="Initial Temp T₁:").grid(row=3, column=0, pady=8)
        self.heat_t1 = ttk.Entry(frame)
        self.heat_t1.grid(row=3, column=1, sticky='ew', padx=10)

        ttk.Label(frame, text="Final Temp T₂:").grid(row=4, column=0, pady=8)
        self.heat_t2 = ttk.Entry(frame)
        self.heat_t2.grid(row=4, column=1, sticky='ew', padx=10)

        self.heat_unit = tk.StringVar(value="Celsius")
        ttk.OptionMenu(frame, self.heat_unit, "Celsius", "Celsius", "Kelvin").grid(row=5, column=1, sticky='w', pady=5)

        ttk.Button(frame, text="Calculate ΔS", command=self.calc_heating).grid(row=6, column=0, columnspan=2, pady=15, sticky='ew')
        self.heat_result = tk.StringVar()
        ttk.Label(frame, textvariable=self.heat_result, style="Result.TLabel").grid(row=7, column=0, columnspan=2, sticky='nsew', pady=10)

    def calc_heating(self):
        n = self.get_float(self.heat_n)
        c = self.get_float(self.heat_c)
        t1 = self.get_float(self.heat_t1)
        t2 = self.get_float(self.heat_t2)
        if None in [n,c,t1,t2]:
            messagebox.showerror("Error","Invalid input.")
            return
        t1_k = self.to_kelvin(t1,self.heat_unit)
        t2_k = self.to_kelvin(t2,self.heat_unit)
        ds = n*c*math.log(t2_k/t1_k)
        self.heat_result.set(f"T₁ = {t1_k:.2f} K\nT₂ = {t2_k:.2f} K\nΔS = {ds:.4f} J/K")

    # ----------------------- Expansion -----------------------
    def setup_expansion_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Expansion")
        frame = ttk.Frame(tab, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ΔS = nR ln(V₂/V₁)", style="Header.TLabel").grid(row=0,column=0,columnspan=2,pady=10)
        self.exp_n = self.create_input_row(frame, "Moles (n):",1)
        self.exp_v1 = self.create_input_row(frame, "Initial Volume V₁:",2)
        self.exp_v2 = self.create_input_row(frame, "Final Volume V₂:",3)
        ttk.Button(frame,text="Calculate ΔS", command=self.calc_expansion).grid(row=4,column=0,columnspan=2,pady=15,sticky='ew')
        self.exp_result = tk.StringVar()
        ttk.Label(frame,textvariable=self.exp_result, style="Result.TLabel").grid(row=5,column=0,columnspan=2,sticky='nsew', pady=10)

    def calc_expansion(self):
        n = self.get_float(self.exp_n)
        v1 = self.get_float(self.exp_v1)
        v2 = self.get_float(self.exp_v2)
        if None in [n,v1,v2] or v1<=0 or v2<=0:
            messagebox.showerror("Error","Volumes must be positive.")
            return
        ds = n*self.R*math.log(v2/v1)
        self.exp_result.set(f"V₂/V₁={v2/v1:.2f}\nΔS={ds:.4f} J/K")

    # ----------------------- Spontaneity -----------------------
    def setup_spontaneity_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Spontaneity")
        frame = ttk.Frame(tab, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ΔG = ΔH - TΔS", style="Header.TLabel").grid(row=0,column=0,columnspan=2,pady=10)
        self.spon_dh = self.create_input_row(frame,"ΔH (kJ):",1)
        self.spon_ds = self.create_input_row(frame,"ΔS (J/K):",2)
        ttk.Label(frame,text="Temperature:").grid(row=3,column=0,pady=8)
        self.spon_t = ttk.Entry(frame)
        self.spon_t.grid(row=3,column=1,sticky='ew', padx=10)
        self.spon_unit = tk.StringVar(value="Celsius")
        ttk.OptionMenu(frame,self.spon_unit,"Celsius","Celsius","Kelvin").grid(row=4,column=1,sticky='w', pady=5)
        ttk.Button(frame,text="Check Spontaneity",command=self.calc_spontaneity).grid(row=5,column=0,columnspan=2,pady=15,sticky='ew')
        self.spon_result = tk.StringVar()
        ttk.Label(frame,textvariable=self.spon_result, style="Result.TLabel").grid(row=6,column=0,columnspan=2,sticky='nsew', pady=10)

    def calc_spontaneity(self):
        dh_kj = self.get_float(self.spon_dh)
        ds = self.get_float(self.spon_ds)
        t = self.get_float(self.spon_t)
        if None in [dh_kj, ds, t]:
            messagebox.showerror("Error","Invalid input.")
            return
        t_k = self.to_kelvin(t,self.spon_unit)
        dh_j = dh_kj*1000
        dg = dh_j - t_k*ds
        if dg<0:
            status="SPONTANEOUS"; bg="#b9f5c0"
        elif dg>0:
            status="NON-SPONTANEOUS"; bg="#ffbdbd"
        else:
            status="EQUILIBRIUM"; bg="#d9d9d9"
        self.spon_result.set(f"ΔH={dh_j:.2f} J\nT={t_k:.2f} K\nΔG={dg:.2f} J\nResult:{status}")

# ----------------------- Run App -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EntropyGUI(root)
    root.mainloop()
