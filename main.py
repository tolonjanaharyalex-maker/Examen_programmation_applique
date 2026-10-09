# Tkinter: mamorona ny interface graphique.
import tkinter as tk
# Outils ho an'ny boutons, messages ary fichiers.
from tkinter import ttk, messagebox, filedialog
import math
# NumPy: kajy sy tableaux de valeurs.
import numpy as np
# Matplotlib: manao ny courbes.
import matplotlib.pyplot as plt
# Mampiditra Matplotlib ao anatin'ny Tkinter.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# Maka ny fonctions avy amin'ny fonctions.py.
from fonctions import analyser_fonction, FONCTIONS

# ===== THÈME MATHLAB EN COULEUR =====
BG = "#101827"
CARD = "#09378D"
CARD2 = "#EC0B16"
TEXT = "#F3F6FA"
MUTED = "#AEBACB"
ACCENT = "#B9F319"

style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass
style.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 10))
style.configure("TFrame", background=BG)
style.configure("TLabel", background=BG, foreground=TEXT)
style.configure("TButton", background=CARD2, foreground=TEXT,
                padding=8, font=("Segoe UI", 10, "bold"))
style.map("TButton", background=[("active", ACCENT)],
          foreground=[("active", "#07111F")])
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=CARD2, foreground=TEXT,
                padding=(18, 10), font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", background=[("selected", ACCENT)],
          foreground=[("selected", "#07111F")])
style.configure("TCombobox", fieldbackground=CARD2, background=CARD2,
                foreground=TEXT)
style.configure("TLabelframe", background=BG, foreground=ACCENT)
style.configure("TLabelframe.Label", background=BG, foreground=ACCENT,
                font=("Segoe UI", 10, "bold"))

# Classe mitantana ny calculatrice scientifique.
class ScientificCalculator:
    # Classe mitantana ny calculatrice scientifique.
    def __init__(self, parent):
        self.parent = parent
        self.degrees = True
        self.build()

    # Mamorona ny écran sy ny boutons.
    def build(self):
        f = ttk.Frame(self.parent, padding=15)
        f.pack(fill="both", expand=True)

        ttk.Label(
            f, text="CALCULATRICE SCIENTIFIQUE",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # Écran: mampiasa Entry mivantana mba hahafahana mamafa tsara.
        self.display = tk.Entry(
            f, font=("Consolas", 20, "bold"),
            justify="right", bg="#0B1220", fg=TEXT,
            insertbackground=ACCENT, relief="flat"
        )
        self.display.pack(fill="x", ipady=10, pady=8)
        self.display.bind("<Return>", lambda e: self.calculate())
        self.display.bind("<Escape>", lambda e: self.clear())

        top = ttk.Frame(f)
        top.pack(fill="x")

        self.mode = ttk.Button(top, text="DEGRÉS", command=self.toggle)
        self.mode.pack(side="left", padx=3)

        ttk.Button(top, text="⌫", command=self.back).pack(side="left", padx=3)
        ttk.Button(top, text="C", command=self.clear).pack(side="left", padx=3)
        ttk.Button(top, text="=", command=self.calculate).pack(side="right", padx=3)

        grid = ttk.Frame(f)
        grid.pack(fill="both", expand=True, pady=10)

        keys = [
            ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
            ("log", "log("), ("ln", "ln("),
            ("asin", "asin("), ("acos", "acos("), ("atan", "atan("),
            ("√", "sqrt("), ("x²", "**2"),
            ("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("(", "("),
            ("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), (")", ")"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("−", "-"), ("^", "**"),
            ("0", "0"), (".", "."), ("π", "pi"), ("e", "e"), ("+", "+")
        ]

        for c in range(5):
            grid.columnconfigure(c, weight=1)
        for r in range(6):
            grid.rowconfigure(r, weight=1)

        for i, (label, value) in enumerate(keys):
            r, c = divmod(i, 5)
            ttk.Button(
                grid, text=label,
                command=lambda v=value: self.insert(v)
            ).grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

        ttk.Label(
            f,
            text="Exemples : 2+3*4  |  sin(30)  |  sqrt(25)  |  log(100)  |  2**5",
            foreground=MUTED
        ).pack(pady=5)

    # Manampy isa na symbole eo amin'ny toerana misy ny curseur.
    def insert(self, value):
        self.display.insert(tk.INSERT, value)
        self.display.focus_set()

    # Mamafa tanteraka izay ao amin'ny écran.
    def clear(self):
        self.display.delete(0, tk.END)
        self.display.focus_set()

    # Mamafa caractère iray any ankavian'ny curseur.J W²²²²Q²²²²²²²²²²²²
    def back(self):
        try:
            pos = self.display.index(tk.INSERT)
            if pos > 0:
                self.display.delete(pos - 1, pos)
        except tk.TclError:
            self.display.delete(0, tk.END)
        self.display.focus_set()

    # Manova degrés <-> radians.
    def toggle(self):
        self.degrees = not self.degrees
        self.mode.config(text="DEGRÉS" if self.degrees else "RADIANS")

    # Manao ny calcul ary mametraka ny résultat eo amin'ny écran.
    def calculate(self):
        expression = self.display.get().strip()

        if not expression:
            return

        try:
            env = {
                "pi": math.pi,
                "e": math.e,
                "sqrt": math.sqrt,
                "log": lambda x: math.log10(x),
                "ln": math.log,
                "abs": abs,
                "exp": math.exp
            }

            if self.degrees:
                env.update({
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                    "asin": lambda x: math.degrees(math.asin(x)),
                    "acos": lambda x: math.degrees(math.acos(x)),
                    "atan": lambda x: math.degrees(math.atan(x))
                })
            else:
                env.update({
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "asin": math.asin,
                    "acos": math.acos,
                    "atan": math.atan
                })

            # Avela ihany ireo opérations/fonctions voafaritra ao amin'ny env.
            result = eval(expression, {"__builtins__": {}}, env)

            if isinstance(result, float):
                if not math.isfinite(result):
                    raise ValueError("Résultat tsy voafaritra.")
                result_text = f"{result:.12g}"
            else:
                result_text = str(result)

            self.display.delete(0, tk.END)
            self.display.insert(0, result_text)
            self.display.icursor(tk.END)

        except ZeroDivisionError:
            messagebox.showerror("Erreur", "Tsy azo zaraina amin'ny zéro.")
        except (ValueError, SyntaxError, TypeError, NameError):
            messagebox.showerror(
                "Erreur",
                "Expression tsy mety.\n\n"
                "Ohatra: 2+3*4, sin(30), sqrt(25), log(100)"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Calcul tsy azo atao.\n{e}")

class FunctionResolver:
    # Classe mitantana ny choix de fonction, calcul, tableau ary courbe.
    def __init__(self, parent):
        self.parent = parent
        self.entries = {}
        self.build()

    # Mamorona ny interface.
    def build(self):
        pan = ttk.PanedWindow(self.parent, orient="horizontal")
        pan.pack(fill="both", expand=True, padx=15, pady=15)

        left = ttk.Frame(pan, padding=12)
        right = ttk.Frame(pan, padding=8)
        pan.add(left, weight=0)
        pan.add(right, weight=1)

        box = ttk.LabelFrame(left, text="Type de fonction", padding=10)
        box.pack(fill="x")

        self.choice = tk.StringVar(value="Affine")
        self.combo = ttk.Combobox(
            box, textvariable=self.choice,
            values=list(FONCTIONS), state="readonly", width=25
        )
        self.combo.pack(fill="x")
        # Synchronisation robuste: ny valeur asehon'ilay liste no tena ampiasaina.
        self.combo.bind("<<ComboboxSelected>>", self.on_function_change)
        self.choice.trace_add("write", lambda *_: self.on_function_change())

        self.formula = ttk.Label(
            box, text="", font=("Arial", 11, "italic")
        )
        self.formula.pack(anchor="w", pady=8)

        self.params = ttk.LabelFrame(left, text="Paramètres", padding=10)
        self.params.pack(fill="x", pady=10)

        inter = ttk.LabelFrame(left, text="Intervalle", padding=10)
        inter.pack(fill="x")
        ttk.Label(inter, text="X min").grid(row=0, column=0)
        self.xmin = ttk.Entry(inter, width=9)
        self.xmin.grid(row=0, column=1)
        self.xmin.insert(0, "-10")

        ttk.Label(inter, text="X max").grid(row=0, column=2)
        self.xmax = ttk.Entry(inter, width=9)
        self.xmax.grid(row=0, column=3)
        self.xmax.insert(0, "10")

        ttk.Button(
            left, text="CALCULER ET TRACER",
            command=self.calculate
        ).pack(fill="x", pady=4)

        ttk.Button(
            left, text="RÉINITIALISER",
            command=self.reset
        ).pack(fill="x", pady=4)

        ttk.Button(
            left, text="ENREGISTRER LA COURBE",
            command=self.save
        ).pack(fill="x", pady=4)

        rf = ttk.LabelFrame(left, text="Résultats", padding=6)
        rf.pack(fill="both", expand=True, pady=8)
        self.result = tk.Text(
            rf, font=("Consolas", 10), bg="#0B1220",
            fg=TEXT, insertbackground=TEXT, relief="flat",
            padx=10, pady=10
        )
        self.result.pack(fill="both", expand=True)

        gf = ttk.LabelFrame(right, text="Courbe", padding=5)
        gf.pack(fill="both", expand=True)

        self.fig, self.ax = plt.subplots(
            figsize=(7, 5), dpi=100, facecolor=CARD
        )
        self.canvas = FigureCanvasTkAgg(self.fig, master=gf)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        NavigationToolbar2Tk(self.canvas, gf).update()

        self.fields()
        self.empty()

    # Rehefa misafidy fonction vaovao dia ovaina avy hatrany ny paramètres.
    def on_function_change(self, event=None):
        # Alaina mivantana avy amin'ny Combobox ny choix, fa tsy miantehitra amin'ny ancien value.
        name = self.combo.get().strip()
        if name in FONCTIONS:
            self.choice.set(name)
            self.fields(name)
            self.result.delete("1.0", tk.END)
            self.empty()

    # Mamorona ny champs mifanaraka amin'ilay fonction voafidy.
    def fields(self, selected_name=None):
        for w in self.params.winfo_children():
            w.destroy()

        self.entries = {}
        name = selected_name or self.combo.get().strip() or self.choice.get()

        if name not in FONCTIONS:
            return

        data = FONCTIONS[name]
        self.formula.config(text=data["formula"])

        for i, (key, label, default) in enumerate(data["params"]):
            ttk.Label(
                self.params, text=key + ":"
            ).grid(row=i, column=0, sticky="w", pady=4)

            e = ttk.Entry(self.params, width=12)
            e.grid(row=i, column=1, pady=4)
            e.insert(0, str(default))
            self.entries[key] = e

            ttk.Label(
                self.params, text=label
            ).grid(row=i, column=2, padx=6, sticky="w")

    # Manao ny calcul sy mametraka ny courbe mifanaraka amin'ny fonction.
    def calculate(self):
        try:
            # Ny Combobox no loharano tokana hahazoana ny fonction voafidy.
            name = self.combo.get().strip()

            # Hamarino fa tena fonction voafidy izy.
            if name not in FONCTIONS:
                raise ValueError("Misafidiana karazana fonction aloha.")

            params = {
                key: float(entry.get())
                for key, entry in self.entries.items()
            }

            xmin = float(self.xmin.get())
            xmax = float(self.xmax.get())

            if xmin >= xmax:
                raise ValueError("X min doit être inférieur à X max.")

            # Mamorona fonction vaovao miaraka amin'ireo paramètres vaovao.
            result = analyser_fonction(name, params)
            fn = result["fonction"]

            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, result["details"])
            self.result.insert(
                tk.END,
                f"\nIntervalle : [{xmin:g} ; {xmax:g}]\n\n"
                f"TABLEAU\n{'-' * 35}\n"
                f"{'x':>10} | {'f(x)':>15}\n"
                f"{'-' * 35}\n"
            )

            for x in np.linspace(xmin, xmax, 11):
                try:
                    y = fn(float(x))
                    value = f"{y:.5f}" if np.isfinite(y) else "non défini"
                except Exception:
                    value = "non défini"

                self.result.insert(
                    tk.END, f"{x:10.3f} | {value:>15}\n"
                )

            # Zava-dehibe: plot vaovao no ampiasaina isaky ny calcul.
            self.plot(fn, name, xmin, xmax)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # Manadio sy mamerina manoritra ny courbe vaovao.
    def plot(self, fn, name, xmin, xmax):
        x = np.linspace(xmin, xmax, 2000)
        y = np.full_like(x, np.nan, dtype=float)

        for i, value in enumerate(x):
            try:
                result = fn(float(value))
                if np.isfinite(result):
                    y[i] = result
            except Exception:
                pass

        self.ax.clear()
        self.ax.set_facecolor("#0B1220")
        self.ax.plot(x, y, label=name, linewidth=2.5)
        self.ax.axhline(0, linewidth=0.8)
        self.ax.axvline(0, linewidth=0.8)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Courbe : " + name)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.legend()
        self.fig.tight_layout()

        # Force l'affichage du nouveau graphique.
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def empty(self):
        self.ax.clear()
        self.ax.set_facecolor("#0B1220")
        self.ax.set_title("Choisis une fonction puis calcule")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")]
        )
        if path:
            self.fig.savefig(path, dpi=200, bbox_inches="tight")

    # Mamerina amin'ny Affine sy valeurs voalohany.
    def reset(self):
        self.combo.set("Affine")
        self.choice.set("Affine")
        self.xmin.delete(0, tk.END)
        self.xmin.insert(0, "-10")
        self.xmax.delete(0, tk.END)
        self.xmax.insert(0, "10")
        self.fields()
        self.result.delete("1.0", tk.END)
        self.empty()
        self.combo.focus_set()

root=tk.Tk()
root.title("MathLab - Calculatrice scientifique & fonctions")
root.geometry("1300x850")
root.minsize(1050,700)

# Bandeau titre.
header=tk.Frame(root,bg="#0B1220",height=72)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header,text="MATHLAB",bg="#0B1220",fg=ACCENT,
         font=("Segoe UI",24,"bold")).pack(side="left",padx=24,pady=12)
tk.Label(header,text="Calculatrice scientifique  •  Fonctions  •  Courbes",
         bg="#0B1220",fg=MUTED,font=("Segoe UI",11)).pack(side="left",padx=8)
nb=ttk.Notebook(root); nb.pack(fill="both",expand=True,padx=10,pady=10)
calc=ttk.Frame(nb); funcs=ttk.Frame(nb)
nb.add(calc,text="🧮 Calculatrice scientifique"); nb.add(funcs,text="📈 Fonctions & courbes")
ScientificCalculator(calc); FunctionResolver(funcs)
root.mainloop()
