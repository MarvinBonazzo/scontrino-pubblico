#!/usr/bin/env python3
"""Ricostruisce comuni-12mesi.json dai dati open di SIOPE.

Prende gli ultimi 12 mesi chiusi di pagamenti (uscite) e incassi (entrate)
di tutti i Comuni italiani, li raggruppa nelle voci dello scontrino e scrive
un file JSON che la pagina index.html carica quando si sceglie un Comune.

Uso:
    python3 scripts/aggiorna_comuni.py              # scarica i file da siope.it
    python3 scripts/aggiorna_comuni.py --raw data/raw   # usa zip già scaricati
    python3 scripts/aggiorna_comuni.py --fine 2026-09   # sceglie l'ultimo mese

Formato di ogni riga del JSON (stesso ordine delle voci C_OUT e C_IN in index.html):
    [nome, provincia, regione, residenti,
     uscite[29], entrate[17],
     partite_giro_uscite, partite_giro_entrate,
     movimenti_finanziari_uscite, movimenti_finanziari_entrate]
Tutti gli importi sono in euro, arrotondati.
"""
import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
import unicodedata
import urllib.request
import zipfile
from pathlib import Path

BASE = "https://www.siope.it/documenti/siope2/open/last/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
N_OUT, N_IN = 29, 17


# ---------- download ----------

def get_zip(name, raw_dir):
    """Restituisce il contenuto di uno zip SIOPE, dalla cartella locale o da siope.it."""
    if raw_dir:
        p = Path(raw_dir) / name
        if p.exists():
            return p.read_bytes()
    print(f"  scarico {name}…", file=sys.stderr)
    req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read()
    except Exception as e:
        sys.exit(f"Non riesco a scaricare {name}: {e}\n"
                 f"Scaricalo a mano da {BASE}{name} e mettilo in data/raw, poi usa --raw data/raw")
    if raw_dir:
        Path(raw_dir).mkdir(parents=True, exist_ok=True)
        (Path(raw_dir) / name).write_bytes(data)
    return data


def csv_rows(zip_bytes, prefix=""):
    """Legge le righe dei CSV dentro uno zip (codifica latin-1, campi tra virgolette)."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        for info in z.infolist():
            if not info.filename.startswith(prefix):
                continue
            with z.open(info) as f:
                yield from csv.reader(io.TextIOWrapper(f, encoding="latin-1", newline=""))


# ---------- regole di raggruppamento ----------
# Le stesse usate per costruire la versione pubblicata. -1 = partite di giro, -2 = movimenti finanziari.

def sw(c, *p):
    return c.startswith(p)


def g_out_base(c, d):
    if sw(c, "7."): return -1
    if sw(c, "1.01."): return 0
    if sw(c, "4.", "1.07."): return 10
    if sw(c, "1.02.", "1.10.03."): return 14
    if sw(c, "1.03.02.01."): return 15
    if c == "1.03.02.99.999": return 4
    if re.search(r"rifiut", d): return 1
    if re.search(r"scolast|istruzione|universit", d): return 9
    if re.search(r"trasport|mezzi di", d): return 3
    if re.search(r"strad|sistemazione del suolo|infrastrutture idrauliche|opere per la", d): return 2
    if re.search(r"asil|social|assistenz|famiglie|sussid|disabil|anzian", d): return 5
    if re.search(r"sport|muse|teatr|bibliotec|cultur|culto|storico|artistic|librar|bibliograf", d): return 6
    if re.search(r"illuminazione|energia elettrica|^gas$|acqua|telefon|utenze|riscaldamento|combustib", d): return 8
    if re.search(r"manutenzione ordinaria", d): return 12
    if re.search(r"software|informatic|hardware|ict|telematic|postazioni|applicazioni|sistemi e relativa", d): return 13
    if sw(c, "2.02.01.09.") or re.search(r"fabbricat|immobil|cimiter", d): return 7
    if sw(c, "1.04.", "2.03."): return 11
    return 16


def g_out_altro(c, d):
    if sw(c, "7."): return -1
    if sw(c, "5.", "3.", "0."): return -2
    g = g_out_base(c, d)
    if g != 16: return g
    if sw(c, "1.03.02.11.006", "1.03.02.99.002", "1.03.02.99.001", "1.10.05."): return 18
    if sw(c, "1.03.02.15."): return 16
    if sw(c, "1.03.02.10.", "1.03.02.11.", "1.03.02.12.", "2.02.03.05."): return 17
    if sw(c, "1.03.02.13."): return 19
    if sw(c, "1.03.02.99.009", "2.02.02."): return 20
    if sw(c, "1.03.02.03."): return 21
    if sw(c, "1.03.01.", "2.02.01.03.", "2.02.01.04.", "2.02.01.05.", "2.02.01.99.", "2.02.01.06.", "2.02.01.08."): return 22
    if sw(c, "1.03.02.02.", "1.03.02.99.011"): return 23
    if sw(c, "1.10.04."): return 24
    if sw(c, "1.09.", "2.05.04."): return 25
    if sw(c, "1.03.02.16.", "1.03.02.17.", "1.03.02.99.003", "1.03.02.99.004", "1.03.02.99.005"): return 26
    return 27


def g_out(c, d):
    if sw(c, "1.03.02.99.999", "2.05.99.99.999", "1.10.99.99.999"): return 4
    g = g_out_altro(c, d)
    if sw(c, "1.03.02.06.", "1.03.02.07.", "1.03.02.08.", "2.02.03.06.") and g == 27: return 28
    return g


def g_in_base(c):
    if sw(c, "9.", "0."): return -1
    if sw(c, "1.01.01.06."): return 2
    if sw(c, "1.01.01.51.", "1.01.01.61."): return 4
    if sw(c, "1.01.01.41."): return 5
    if sw(c, "1.01.01.16."): return 7
    if sw(c, "1.03.", "2.01.01.01.", "4.02.01.01."): return 0
    if sw(c, "2.01.01.02.", "4.02.01.02."): return 3
    if sw(c, "3.02."): return 6
    if sw(c, "3.01.", "4.05."): return 1
    return 8


def g_in(c):
    if sw(c, "9."): return -1
    if sw(c, "7.", "5.", "0."): return -2
    if sw(c, "4.03.10.01."): return 0
    if sw(c, "4.03.10.02."): return 3
    g = g_in_base(c)
    if g != 8: return g
    if sw(c, "6."): return 9
    if sw(c, "4.04."): return 10
    if sw(c, "3.03.", "3.04."): return 11
    if sw(c, "3.05.02."): return 12
    if sw(c, "4.02.05.", "2.01.05.", "4.03.11."): return 13
    if sw(c, "1."): return 14
    if sw(c, "4.02.03.", "4.02.04.", "4.03.12.", "4.03.13.", "2.01.03.", "2.01.04.", "4.03.14."): return 15
    if sw(c, "3.05.99.99.999"): return 16
    return 8


# ---------- periodo ----------

def mesi_finestra(fine):
    """I 12 mesi che finiscono con `fine` (anno, mese), come insieme di (anno, mese)."""
    a, m = fine
    out = []
    for _ in range(12):
        out.append((a, m))
        m -= 1
        if m == 0:
            a, m = a - 1, 12
    return set(out)


def nome_mese(a, m):
    nomi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
            "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    return f"{nomi[m - 1]} {a}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", default="data/raw", help="cartella dove tenere gli zip SIOPE (default data/raw)")
    ap.add_argument("--fine", help="ultimo mese da includere, AAAA-MM (default: il mese scorso)")
    ap.add_argument("--out", default="comuni-12mesi.json")
    args = ap.parse_args()

    if args.fine:
        a, m = map(int, args.fine.split("-"))
    else:
        oggi = dt.date.today().replace(day=1) - dt.timedelta(days=1)
        a, m = oggi.year, oggi.month
    mesi = mesi_finestra((a, m))
    anni = sorted({x[0] for x in mesi})
    inizio = min(mesi)
    print(f"Periodo: {nome_mese(*inizio)} – {nome_mese(a, m)}", file=sys.stderr)

    # Anagrafiche: comuni, province, descrizioni dei codici
    anag = get_zip("SIOPE_ANAGRAFICHE.zip", args.raw)
    prov = {r[3]: (r[4], r[2]) for r in csv_rows(anag, "ANAG_REG_PROV") if len(r) >= 5}
    inizio_str = f"{inizio[0]}-{inizio[1]:02d}-01"
    comuni = {}
    for r in csv_rows(anag, "ANAG_ENTI_SIOPE"):
        if len(r) >= 9 and r[8] == "COMUNE" and r[2] >= inizio_str:
            p = prov.get(r[6], ("", ""))
            try:
                pop = int(r[7])
            except ValueError:
                pop = 0
            comuni[r[0]] = {"n": re.sub(r"^COMUNE DI ", "", r[4]), "p": p[0], "r": p[1], "pop": pop}
    desc_out = {r[0]: r[2].lower() for r in csv_rows(anag, "ANAG_CODGEST_USCITE") if len(r) >= 3 and r[1] == "PRO"}

    # Movimenti
    agg = {}
    gruppi_out, gruppi_in = {}, {}
    for tipo in ("USCITE", "ENTRATE"):
        for anno in anni:
            zb = get_zip(f"SIOPE_{tipo}.{anno}.zip", args.raw)
            for r in csv_rows(zb):
                if len(r) < 5 or r[0] not in comuni:
                    continue
                if (int(r[1]), int(r[2])) not in mesi:
                    continue
                c, v = r[3], int(r[4]) / 100
                a_ = agg.setdefault(r[0], {"o": [0.0] * N_OUT, "i": [0.0] * N_IN, "go": 0.0, "gi": 0.0, "fo": 0.0, "fi": 0.0})
                if tipo == "USCITE":
                    g = gruppi_out.get(c)
                    if g is None:
                        g = gruppi_out[c] = g_out(c, desc_out.get(c, ""))
                    if g == -1: a_["go"] += v
                    elif g == -2: a_["fo"] += v
                    else: a_["o"][g] += v
                else:
                    g = gruppi_in.get(c)
                    if g is None:
                        g = gruppi_in[c] = g_in(c)
                    if g == -1: a_["gi"] += v
                    elif g == -2: a_["fi"] += v
                    else: a_["i"][g] += v

    rows = []
    for cid, a_ in agg.items():
        c = comuni[cid]
        if c["pop"] <= 1:  # popolazione mancante o errata nell'anagrafica
            continue
        rows.append([c["n"], c["p"], c["r"], c["pop"],
                     [round(x) for x in a_["o"]], [round(x) for x in a_["i"]],
                     round(a_["go"]), round(a_["gi"]), round(a_["fo"]), round(a_["fi"])])
    key = lambda r: unicodedata.normalize("NFD", r[0]).encode("ascii", "ignore").decode()
    rows.sort(key=key)

    Path(args.out).write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Scritti {len(rows)} Comuni in {args.out}", file=sys.stderr)
    print(f"Ricorda di aggiornare in index.html il periodo: {nome_mese(*inizio)} – {nome_mese(a, m)}", file=sys.stderr)


if __name__ == "__main__":
    main()
