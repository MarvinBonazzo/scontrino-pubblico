# Scontrino pubblico

Pagina web che mostra, come uno scontrino, quanto spende il settore pubblico per ogni residente e da dove arrivano i soldi. Parte dall'Italia intera; in fondo un pulsante apre una finestra per scegliere uno dei circa 7.900 Comuni.

Progetto gemello dello "Scontrino delle tasse" (stipendio, repo `scontrino-stipendio`): stesso stile, stessa logica a tre schermate. Si completano: lo stipendio mostra cosa paghi tu e dove va; questo mostra quanti soldi arrivano in tutto allo Stato, da dove, e come vengono spesi. Le due pagine si linkano a vicenda.

## File

- `index.html`: la pagina completa in un solo file (stile, markup, script) e i dati dell'Italia.
- `comuni-12mesi.json`: i dati dei Comuni, caricati con `fetch` quando si apre la finestra di scelta.
- `scripts/aggiorna_comuni.py`: rifà `comuni-12mesi.json` dai file open di SIOPE.
- `data/raw/`: gli zip SIOPE scaricati dallo script (non serve committarli, sono grandi).
- `wrapped/`: il Wrapped dello Stato, versione a storie per ragazzi. Regole e struttura in `wrapped/CLAUDE.md`. Se cambiano i dati di `ITALIA`, vanno ricalcolate anche le cifre scritte a mano lì.

## Vedere la pagina in locale

Il doppio clic su `index.html` non basta: il browser blocca il `fetch` del JSON da una pagina aperta come file.

```
python3 -m http.server 8000
```
poi aprire http://localhost:8000

## Struttura dello script in index.html

- `ITALIA`: dati dell'Italia, scritti a mano. Spesa per funzione da Eurostat COFOG (`gov_10a_exp`), entrate da Eurostat (`gov_10a_main`), anno 2024, in milioni di euro (`*M`). Residenti ISTAT al 1° gennaio 2025.
- `C_OUT` (29 voci) e `C_IN` (17 voci): nomi e descrizioni delle voci dei Comuni. **L'ordine deve essere identico agli indici usati in `scripts/aggiorna_comuni.py`**: se aggiungi, togli o sposti una voce, cambia entrambi.
- `comuneData(row)`: trasforma una riga del JSON nello stesso formato di `ITALIA`.
- `render(D)`: disegna risultato, barra, elenchi "Dove vanno" e "Da dove arrivano". Le entrate con il campo `you` mostrano la riga "Come la paghi tu". `D.facts(c)` riempie il riquadro "Perché i conti non tornano" (Italia) o "Perché entrate e uscite non sono uguali" (Comune).
- `GLOSS` e `W(chiave, testo)`: parole spiegate. Nel testo `${W("irpef","IRPEF")}` o nel markup `<u data-w="irpef">IRPEF</u>`; toccandole si apre un cartoncino. Ogni parola tecnica nuova va spiegata così, in una o due frasi senza altre parole difficili. Le voci in comune devono restare identiche a quelle dello Scontrino delle tasse.
- Finestra di scelta: `openModal`, `search`, `loadComuni`. La media dei Comuni italiani (`AVG`) si calcola dal JSON.

Formato di una riga del JSON:
`[nome, provincia, regione, residenti, uscite[29], entrate[17], partite_giro_uscite, partite_giro_entrate, movimenti_finanziari_uscite, movimenti_finanziari_entrate]`, importi in euro.

## Regole sui dati

- **Nessuna stima.** Si usano solo dati pubblicati, il più recenti possibile. Se un dato non c'è, si spiega perché, non si inventa.
- **Italia: 2024.** È l'ultimo anno con la spesa divisa per voce: Eurostat pubblica la ripartizione per funzione più di un anno dopo. Quando esce il 2025 (inizio 2027) va aggiornato tutto `ITALIA` e il testo `why`.
- **Comuni: ultimi 12 mesi chiusi** di cassa SIOPE (pagamenti e incassi effettivi). SIOPE pubblica a metà mese, con il mese in corso incompleto.
- **Esclusi dallo scontrino**, e spiegati nelle note:
  - partite di giro (uscite titolo 7, entrate titolo 9): ritenute e IVA che il Comune incassa e gira allo Stato;
  - movimenti finanziari (uscite titoli 0, 3, 5; entrate titoli 0, 5, 7): anticipi di cassa della banca, depositi, titoli. Non sono spesa.
- Esclusi i Comuni con popolazione 0 o 1 nell'anagrafica SIOPE (dato errato, il conto per residente verrebbe assurdo).
- La spesa per residente non è "quanto paghi tu": va sempre detto.
- Debito pubblico (`ITALIA.debt`): Banca d'Italia, fine 2024 (2.966,9 mld, dato rivisto a febbraio 2026).
- **Stessi numeri dello Scontrino delle tasse**: l'array `SPESA` di `scontrino-stipendio/index.html` copia le 13 voci di spesa di `ITALIA` e i totali delle entrate. Se cambi `ITALIA`, aggiorna anche lì.

## Aggiornamento mensile dei Comuni

1. `python3 scripts/aggiorna_comuni.py` (oppure `--fine AAAA-MM` per scegliere l'ultimo mese).
   Se siope.it rifiuta il download, scaricare a mano gli zip da https://www.siope.it/documenti/siope2/open/last/ (`SIOPE_ANAGRAFICHE.zip`, `SIOPE_USCITE.<anno>.zip`, `SIOPE_ENTRATE.<anno>.zip`) dentro `data/raw/` e rilanciare.
2. Aggiornare in `index.html` i testi del periodo (cercare "ottobre 2025 – settembre 2026"):
   il campo `where` e le note in `comuneData`, il commento sopra `C_OUT`, e nel testo `why` il mese "non ancora finito".
3. Controllare un Comune noto (es. Firenze) prima e dopo: totali per residente che cambiano di molto vanno capiti.

## Stile

- Tema scuro fisso: sfondo nero, blu e arancio complementari (token in `:root`). Font: Bricolage Grotesque (titoli), Source Sans 3 (testo), IBM Plex Mono (cifre).
- Minimale. Cifre allineate come uno scontrino, voci a fisarmonica, barra "Ogni euro" con le prime sei voci e "Tutto il resto (…)" che elenca le voci incluse.
- Testi in italiano semplice, frasi brevi, senza gergo contabile. Le voci si chiamano con parole che una persona riconosce ("Rifiuti", non "Contratti di servizio 1.03.02.15.004").
- Deve funzionare a larghezza telefono (circa 400px) senza scroll orizzontale.

## Come lavorare con Marvin

- Scrivere in italiano, risposte dirette e brevi.
- Spiegare i concetti tecnici con un'analogia e un esempio pratico.
- Le richieste sono spesso brevi ("togli questo", "cambia colore"): fare esattamente quella modifica, senza riscrivere il resto.
- Se chiede solo una spiegazione, non modificare i file.
