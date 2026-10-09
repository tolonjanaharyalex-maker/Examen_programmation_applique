# Module math: ampiasaina amin'ny kajy matematika.
import math

# Lisitry ny karazana fonctions sy ny paramètres default.
FONCTIONS={
"Affine":{"formula":"f(x) = ax + b","params":[("a","coefficient directeur",2),("b","ordonnée à l'origine",1)]},
"Linéaire":{"formula":"f(x) = ax","params":[("a","coefficient",2)]},
"Polynôme":{"formula":"f(x) = ax² + bx + c","params":[("a","coefficient de x²",1),("b","coefficient de x",0),("c","constante",-1)]},
"Puissance":{"formula":"f(x) = a × xⁿ","params":[("a","coefficient",1),("n","exposant",2)]},
"Exponentielle":{"formula":"f(x) = a × bˣ","params":[("a","coefficient",1),("b","base",2)]},
"Logarithme":{"formula":"f(x) = a × log_b(x)","params":[("a","coefficient",1),("b","base",2)]}
}

# Mandinika ny fonction voafidy ary mamerina ny fonction sy ny valiny.
def analyser_fonction(n,p):
    # Fonction affine: f(x) = ax + b.
    if n=="Affine":
        a,b=p["a"],p["b"]
        def f(x): return a*x+b
        d=f"FONCTION AFFINE\n\nf(x) = {a:g}x + {b:g}\nf(0) = {b:g}\n"
        if a: d+=f"Zéro : {-b/a:g}\n"+("Variation : croissante\n" if a>0 else "Variation : décroissante\n")
        else: d+="Fonction constante.\n"
        return {"fonction":f,"details":d}
    # Fonction linéaire: f(x) = ax.
    if n=="Linéaire":
        a=p["a"]
        def f(x): return a*x
        d=f"FONCTION LINÉAIRE\n\nf(x) = {a:g}x\nZéro : 0\n"
        d+=("Variation : croissante\n" if a>0 else "Variation : décroissante\n" if a<0 else "Fonction nulle.\n")
        return {"fonction":f,"details":d}
    # Polynôme du second degré.
    if n=="Polynôme":
        a,b,c=p["a"],p["b"],p["c"]
        if a==0: return analyser_fonction("Affine",{"a":b,"b":c})
        def f(x): return a*x*x+b*x+c
        delta=b*b-4*a*c; d=f"POLYNÔME DU SECOND DEGRÉ\n\nf(x) = {a:g}x² + {b:g}x + {c:g}\nΔ = {delta:g}\n"
        if delta>0: d+=f"x₁ = {(-b-math.sqrt(delta))/(2*a):g}\nx₂ = {(-b+math.sqrt(delta))/(2*a):g}\n"
        elif delta==0: d+=f"Racine double : {-b/(2*a):g}\n"
        else: d+="Aucune racine réelle.\n"
        sx=-b/(2*a); d+=f"Sommet : S({sx:g} ; {f(sx):g})\n"
        return {"fonction":f,"details":d}
    # Fonction puissance.
    if n=="Puissance":
        a,k=p["a"],p["n"]
        def f(x):
            if x<0 and not float(k).is_integer(): return float("nan")
            return a*x**k
        return {"fonction":f,"details":f"FONCTION PUISSANCE\n\nf(x) = {a:g} × x^{k:g}\n"}
    # Fonction exponentielle.
    if n=="Exponentielle":
        a,b=p["a"],p["b"]
        if b<=0 or b==1: raise ValueError("La base b doit être > 0 et différente de 1.")
        def f(x): return a*b**x
        return {"fonction":f,"details":f"FONCTION EXPONENTIELLE\n\nf(x) = {a:g} × {b:g}ˣ\nf(0) = {a:g}\n"+("Croissante.\n" if b>1 else "Décroissante.\n")}
    # Fonction logarithmique.
    if n=="Logarithme":
        a,b=p["a"],p["b"]
        if b<=0 or b==1: raise ValueError("La base b doit être > 0 et différente de 1.")
        def f(x): return float("nan") if x<=0 else a*math.log(x,b)
        return {"fonction":f,"details":f"FONCTION LOGARITHME\n\nf(x) = {a:g} × log_{b:g}(x)\nDomaine : x > 0\nZéro : x = 1\n"}
