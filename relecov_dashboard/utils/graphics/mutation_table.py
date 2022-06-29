# Dash libs
import dash
import dash_table
from dash.dependencies import Input, Output
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html

# Other libs
import pandas as pd
import json
import urllib.request as urlreq

"""
Mutaciones asociadas a linajes, con sus frecuencias

- Generar script
- Leer json/csv
- Generar dataframe
- Tabla auxiliar al needle plot
    - needle plot encima
    - debajo una tabla para que se pueda filtrar, viendo frecuencia de una mutación en linaje
    
"""
