# Scontrino pubblico

Quanti soldi arrivano allo Stato, da dove, e come vengono spesi, divisi per ogni persona che vive in Italia. Mostrato come uno scontrino: ogni riga è una voce di spesa, in fondo c'è il totale.

### 👉 [Apri lo scontrino](https://marvinbonazzo.github.io/scontrino-pubblico/)

### 🎁 [Apri il Wrapped dello Stato](https://marvinbonazzo.github.io/scontrino-pubblico/wrapped/)

Gli stessi numeri dell'Italia raccontati a storie, come lo Spotify Wrapped, pensati per ragazzi delle medie e delle superiori: una schermata, un'idea, e alla fine uno scontrino di carta di un giorno qualunque. Si tocca a destra per andare avanti, a sinistra per tornare indietro.

Progetto gemello: **[Scontrino delle tasse](https://marvinbonazzo.github.io/scontrino-stipendio/)**. Questo scontrino mostra i soldi di tutti; quello parte dal tuo stipendio e ti mostra quanto ci metti tu, in contributi e IRPEF, e in quali voci finisce. Le due pagine usano gli stessi numeri 2024 e si linkano a vicenda ([codice](https://github.com/MarvinBonazzo/scontrino-stipendio)).

---

## Cosa fa

1. **Italia intera.** Prende tutta la spesa pubblica di un anno (Stato, Regioni, Comuni e INPS insieme) e la divide per i 58,9 milioni di residenti.
2. **Lo scontrino.** Mostra quanto va a ogni voce (pensioni, sanità, scuola, interessi sul debito…) per residente, all'anno e al mese.
3. **Da dove arrivano i soldi.** Sotto le uscite ci sono le entrate dello stesso anno (tasse, contributi, altre entrate). Per ogni entrata, una riga "Come la paghi tu" dice dove la incontri: in busta paga, nel prezzo di quello che compri, nelle bollette.
4. **Perché i conti non tornano.** Se le uscite sono più delle entrate, lo scontrino spiega come si copre la differenza (deficit e debito, con BTP e BOT), quanto costano gli interessi rispetto alla scuola, e perché i contributi non bastano per le pensioni. Per i Comuni spiega perché non possono fare debito per le spese di ogni giorno.
5. **Il tuo Comune.** In fondo un pulsante apre la ricerca tra circa 7.900 Comuni. Per ognuno si vede quanto ha speso per residente negli ultimi 12 mesi, voce per voce, e il confronto con la media dei Comuni italiani.

Un esempio: scegli Firenze, e lo scontrino ti dice quanto il Comune ha speso per ogni fiorentino in personale, rifiuti, strade, trasporti, scuole e mense e così via, e quanto è arrivato da IMU, TARI, multe, imposta di soggiorno o dallo Stato.

## Come funziona

La pagina ha tre schermate, come lo Scontrino delle tasse:

| Schermata | Cosa succede |
| --- | --- |
| 1. Inizio | Si parte dall'Italia: premi "Stampa lo scontrino". |
| 2. Stampa | Un'animazione mostra i passaggi del calcolo: leggo i dati, tolgo ciò che non è spesa, divido per i residenti. |
| 3. Scontrino | Il totale per residente, la barra "Ogni euro" con le voci più grandi, e gli elenchi "Dove vanno" e "Da dove arrivano". Ogni voce si apre e spiega da cosa è fatta. In fondo, "Scegli un Comune" apre la ricerca. |

Il conto è sempre lo stesso, per l'Italia e per i Comuni:

```
spesa di una voce ÷ numero di residenti = euro per residente
```

Ogni parola tecnica (IRPEF, accise, deficit, SIOPE…) è sottolineata a puntini: toccandola si apre una spiegazione di una o due frasi.

Tutto avviene nel tuo browser. La pagina non ha account, non salva niente e non ha statistiche o tracciamento: anche la ricerca del Comune si fa sul tuo dispositivo.

## Perché ti puoi fidare

**Solo dati ufficiali, nessuna stima.** Ogni cifra viene da un ente pubblico che raccoglie i conti dello Stato:

- **Eurostat** (l'ufficio statistico dell'Unione europea) pubblica i conti pubblici italiani che gli manda l'**ISTAT**, divisi per funzione con regole uguali per tutti i Paesi UE (classificazione COFOG).
- **ISTAT** conta i residenti.
- **SIOPE**, gestito dalla **Ragioneria Generale dello Stato** (Ministero dell'Economia) e dalla **Banca d'Italia**, registra ogni pagamento e ogni incasso dei Comuni, mese per mese. Non sono previsioni di bilancio: sono soldi davvero usciti ed entrati in banca.

Se un dato non c'è, la pagina spiega perché invece di inventarlo. Per esempio: l'Italia è ferma al 2024 perché Eurostat pubblica la spesa divisa per voce più di un anno dopo (il 2025 uscirà a inizio 2027).

**Il codice è aperto.** Tutto quello che la pagina fa è in questo repository: puoi leggere ogni formula in [`index.html`](index.html).

**Si può rifare da soli.** Lo script [`scripts/aggiorna_comuni.py`](scripts/aggiorna_comuni.py) scarica i file pubblici di SIOPE e ricostruisce da zero i dati dei Comuni. Chiunque può lanciarlo e controllare di ottenere gli stessi numeri.

**Quello che si toglie è dichiarato.** Alcuni movimenti di cassa non sono spesa vera, e contarli gonfierebbe lo scontrino. Vengono esclusi e la pagina dice quanto valgono:

- **Soldi di passaggio** (partite di giro): ritenute e IVA che il Comune incassa e gira subito allo Stato. È come il cassiere che ti dà il resto: i soldi passano dalle sue mani, ma non sono suoi.
- **Movimenti finanziari**: anticipi di cassa della banca, depositi, acquisto di titoli. Spostano soldi, non pagano servizi.
- **Comuni con 0 o 1 residente** nell'anagrafica SIOPE: è un dato sbagliato e il conto per residente verrebbe assurdo.

## Cosa lo scontrino non dice

- **Non è quanto paghi tu.** È la spesa totale divisa per tutti i residenti, neonati compresi. Quanto paga una persona dipende dal suo reddito: per quello c'è lo [Scontrino delle tasse](https://marvinbonazzo.github.io/scontrino-stipendio/).
- **I nomi delle voci sono semplificati.** I codici contabili (per esempio "Contratti di servizio 1.03.02.15.004") sono raggruppati in voci che una persona riconosce ("Rifiuti"). Il raggruppamento è di questo progetto; i numeri sotto sono quelli ufficiali, senza ritocchi.
- **Italia e Comuni non vanno sommati.** L'Italia comprende già la spesa dei Comuni, e i periodi sono diversi (anno 2024 contro ultimi 12 mesi).

## Fonti

| Dato | Fonte | Periodo |
| --- | --- | --- |
| Spesa pubblica per funzione | [Eurostat, `gov_10a_exp`](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_exp/default/table) (COFOG) | 2024 |
| Entrate pubbliche | [Eurostat, `gov_10a_main`](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_main/default/table) | 2024 |
| Residenti in Italia | [ISTAT](https://demo.istat.it/) | 1° gennaio 2025 |
| Pagamenti e incassi dei Comuni | [SIOPE, dati open](https://www.siope.it/documenti/siope2/open/last/) | ottobre 2025 – settembre 2026 |
| Residenti dei Comuni | Anagrafica SIOPE | come sopra |

## Vedere la pagina sul tuo computer

Il doppio clic su `index.html` non basta: il browser blocca la lettura del file dei Comuni da una pagina aperta come file. Serve un piccolo server locale:

```bash
python3 -m http.server 8000
```

poi apri http://localhost:8000

## Aggiornare i dati dei Comuni

SIOPE pubblica i nuovi dati a metà di ogni mese.

```bash
python3 scripts/aggiorna_comuni.py
```

Con `--fine AAAA-MM` scegli l'ultimo mese da includere. Se siope.it rifiuta il download, scarica a mano `SIOPE_ANAGRAFICHE.zip`, `SIOPE_USCITE.<anno>.zip` e `SIOPE_ENTRATE.<anno>.zip` da https://www.siope.it/documenti/siope2/open/last/ dentro `data/raw/` e rilancia lo script.

Poi in `index.html` aggiorna i testi del periodo (cerca "ottobre 2025 – settembre 2026").

## File

| File | A cosa serve |
| --- | --- |
| `index.html` | La pagina completa: stile, testi, calcoli e i dati dell'Italia. |
| `comuni-12mesi.json` | I dati di tutti i Comuni, caricati quando apri la ricerca. |
| `scripts/aggiorna_comuni.py` | Rifà `comuni-12mesi.json` dai file open di SIOPE. |
| `wrapped/index.html` | Il Wrapped dello Stato: la versione a storie, in un solo file. Usa i dati dell'Italia di `index.html` trasformati in euro al giorno per residente. |
