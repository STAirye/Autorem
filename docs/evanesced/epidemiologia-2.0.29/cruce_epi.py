import sys, re, difflib
sys.path.insert(0, '.')
import pandas as pd, openpyxl
from programas.rem_utils import norm

m = pd.read_csv('catalogos/maestro_slim.csv.gz')
m['A'] = m['ACTIVIDAD'].map(norm)
g = (m.groupby('A').agg(ACT=('ACTIVIDAD', 'first'),
                        NUMREM=('NUM REM', lambda s: sorted(set(map(str, s.dropna())))),
                        SEC=('NUM SECCION', lambda s: sorted(set(map(str, s.dropna())))),
                        REM=('REM', lambda s: sorted(set(map(str, s.dropna())))),
                        N=('INSTRUMENTO ASOCIADO', 'nunique'),
                        INSTR=('INSTRUMENTO ASOCIADO', lambda s: sorted(set(map(str, s.dropna()))))))
claves = list(g.index)

print('=== Maestro: NUM REM A04, secciones P-U ===')
a4 = m[m['NUM REM'].astype(str).str.contains('A04', na=False)
       & m['NUM SECCION'].astype(str).str.strip().str.match(r'^[P-U]\b', na=False)]
for (act, sec), d in a4.groupby(['ACTIVIDAD', 'NUM SECCION']):
    print(f'  [{sec}] {act}  | {d["NUM REM"].iloc[0]} | estamentos={d["INSTRUMENTO ASOCIADO"].nunique()}')

print('\n=== Maestro: actividades con EPIDEMIOL / QUIMIOPROFILAXIS / BUSQUEDA ACTIVA / CONTACTOS ===')
pat = r'EPIDEMIOL|QUIMIOPROF|BUSQUEDA ACTIVA|CONTACTOS/|NOTIFICACION|\bENO\b|COVID|VIRUELA|AGOTAMIENTO|INMUNIZACION|HISOPADO|ANTIGENO'
for k in claves:
    if re.search(pat, k):
        r = g.loc[k]
        print(f'  {r.ACT}  | {r.NUMREM} | sec={r.SEC} | {r.REM} | n_estam={r.N}')

wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
ws = wb.active
print('\n=== Tabla epi -> Maestro ===')
for col in 'CG':
    for fila in range(7, ws.max_row + 1):
        v = ws[f'{col}{fila}'].value
        if not v or not str(v).strip():
            continue
        k = norm(str(v).replace('\xa0', ' '))
        k = re.sub(r'\s+', ' ', k).strip()
        if k in g.index:
            r = g.loc[k]; print(f'{col}{fila} EXACTO  {v!r} -> {r.NUMREM} sec={r.SEC} {r.REM} n_estam={r.N}')
            continue
        cand = difflib.get_close_matches(k, claves, n=3, cutoff=0.6)
        print(f'{col}{fila} NO-EXACTO {v!r}')
        for c in cand:
            r = g.loc[c]
            print(f'      ~ {r.ACT!r} {difflib.SequenceMatcher(None, k, c).ratio():.2f} -> {r.NUMREM} sec={r.SEC} {r.REM} n_estam={r.N}')
