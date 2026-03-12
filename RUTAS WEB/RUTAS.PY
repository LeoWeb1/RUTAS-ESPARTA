from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_excel("RUTAS.xlsx")

dias = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO"]

def espejo(ruta):
    ruta = str(ruta)
    if ruta.startswith("1"):
        return "2" + ruta[1:]
    if ruta.startswith("2"):
        return "1" + ruta[1:]
    return ruta

def buscar_info_ruta(ruta):
    for _, fila in df.iterrows():
        for d in dias:
            if str(fila[d]) == str(ruta):
                return fila["VENDEDOR"], d
    return "NO ENCONTRADO","-"

@app.route("/", methods=["GET","POST"])
def index():
    resultados = []
    
    if request.method == "POST":
        vendedor = request.form.get("vendedor", "")
        ruta_buscar = request.form.get("ruta", "")
        dia = request.form["dia"]
        
        # Filtrar por vendedor si se ingresó
        if vendedor:
            filtro = df[df["VENDEDOR"].str.contains(vendedor, case=False, na=False)]
        else:
            filtro = df
        
        for _, fila in filtro.iterrows():
            
            # Si se busca por RUTA, buscar en todos los días
            if ruta_buscar:
                for d in dias:
                    ruta = str(fila[d])
                    
                    if ruta == str(ruta_buscar):
                        ruta_espejo = espejo(ruta)
                        vendedor_espejo, dia_espejo = buscar_info_ruta(ruta_espejo)
                        
                        resultados.append({
                            "nombre": fila["VENDEDOR"],
                            "ruta_general": fila["RUTA GENERAL"],
                            "ruta": ruta,
                            "dia": d,
                            "espejo": ruta_espejo,
                            "dia_espejo": dia_espejo,
                            "vendedor_espejo": vendedor_espejo
                        })
            else:
                # Si solo busca por vendedor, usar el día seleccionado
                ruta = str(fila[dia])
                ruta_espejo = espejo(ruta)
                vendedor_espejo, dia_espejo = buscar_info_ruta(ruta_espejo)
                
                resultados.append({
                    "nombre": fila["VENDEDOR"],
                    "ruta_general": fila["RUTA GENERAL"],
                    "ruta": ruta,
                    "dia": dia,
                    "espejo": ruta_espejo,
                    "dia_espejo": dia_espejo,
                    "vendedor_espejo": vendedor_espejo
                })
    
    return render_template("index.html", dias=dias, resultados=resultados)

app.run(host="0.0.0.0", port=5000, debug=True)
    