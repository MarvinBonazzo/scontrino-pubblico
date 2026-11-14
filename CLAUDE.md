# Scontrino dello Stato

Un anno di soldi pubblici raccontato a storie, una schermata alla volta, per ragazzi delle medie e delle superiori: quanto spende lo Stato per ognuno di noi, per cosa, da dove arrivano i soldi e perché non bastano. Finisce con uno scontrino di carta di un giorno qualunque.

Progetto gemello dello **Scontrino dello Stipendio** (repo `scontrino-stipendio`): stesso stile, stessi colori, stessa navigazione, stessi dati. Questo mostra i soldi di tutti; quello cosa paghi tu partendo dal tuo stipendio. Si linkano a vicenda.

La parola "Wrapped" non si usa: i due progetti si chiamano Scontrino dello Stato e Scontrino dello Stipendio. Il repo si chiama ancora `scontrino-pubblico` per non rompere i link.

## File
- `index.html`: pagina unica e autosufficiente (HTML + CSS + JS inline). Unica risorsa esterna: Google Fonts (Archivo, Space Mono). Si apre anche con un doppio clic.
- La vecchia pagina con la scelta dei Comuni (con `comuni-12mesi.json` e `scripts/aggiorna_comuni.py`) è stata tolta il 14 novembre 2026. È recuperabile dalla cronologia di git, commit `c51d039`.

## Struttura
- Ogni schermata è un `<section class="slide COLORE">` dentro `<main class="phone">`.
- Colori di sfondo: `.y` giallo, `.p` rosa, `.b` blu, `.o` arancio, `.l` lilla, `.k` nero (solo scontrino finale).
- Navigazione: tocco a destra = avanti, tocco nel 30% sinistro = indietro, frecce da tastiera. Le barre in alto si generano da sole contando le slide.
- Numeri animati: `<span data-n="16.72" data-d="2">`, dove `data-n` è il valore e `data-d` i decimali.
- Barre di confronto: `<div class="cmp">` con righe `<div><span>Nome</span><em>valore</em><i><b style="--w:PERCENTUALE%"></b></i></div>`. `--w` è relativo alla barra più lunga della stessa slide.
- Monetine, scontrino finale e pannello fonti sono generati in JS dall'array `V` (emoji, nome della voce, spesa in milioni di €, colore) e da `ENTRATE`.

## Dati (non inventare numeri)
- Spesa ed entrate pubbliche 2024: Eurostat (`gov_10a_exp` per funzione COFOG, `gov_10a_main`), in milioni di euro. È l'ultimo anno con la spesa divisa per voce: il 2025 esce a inizio 2027.
- Debito pubblico a fine 2024: 2.966,9 miliardi (Banca d'Italia, dato rivisto a febbraio 2026), costante `DEBITO`.
- Residenti: 58.934.177 (ISTAT, 1° gennaio 2025).
- Formula per gli euro al giorno: `spesa in € / 58.934.177 / 365`.

Le cifre scritte a mano nelle slide (es. 2,80 € ospedali, 6,75 € IVA, 12,93 € contributi, le entrate al giorno che sommano 48,16 €, il debito a testa 50.343 €) sono calcolate con questa formula. Se aggiorni i dati, ricalcola anche quelle. "Il resto" delle entrate è arrotondato a 2,98 invece di 2,99 perché la somma torni con il totale.

**Stessi numeri dello Scontrino dello Stipendio**: le 13 voci di `V` (nomi e milioni), le entrate totali, IVA, accise e residenti devono restare uguali a quelli di `scontrino-stipendio/index.html`. Se cambi un dato, cambialo in tutti e due.

## Fine della storia
Sotto lo scontrino finale: "Ricomincia", poi il link "Scontrino dello Stipendio" e il bottone "Fonti, calcoli e numeri interi". Il bottone apre il pannello `#info`: spesa ed entrate 2024 in euro interi, deficit, debito, residenti, le formule delle storie e i link alle fonti. Se cambi un dato, il pannello si aggiorna da solo tranne i testi delle fonti.

## Parole spiegate (glossario)
Ogni parola tecnica si scrive `<u data-w="chiave">parola</u>` e toccandola si apre un cartoncino in basso. Le spiegazioni sono nell'oggetto `GLOSS`, una o due frasi senza altre parole difficili. Se aggiungi una parola tecnica nuova, aggiungi anche la sua voce.

## Regole di testo
- Si dà sempre del tu, con rispetto.
- Diretto, senza addolcire: "Pensioni" e "anziani", non "nonni"; "Sussidi e assistenza", non "aiuti a chi ha bisogno".
- Linguaggio per un ragazzo di 12-14 anni: frasi brevi, niente sigle senza spiegazione.
- Solo informazioni utili a capire come vengono usati i soldi, niente curiosità fini a sé stesse.
- Tono neutro: fatti e confronti, nessun giudizio politico.
- Ricordare sempre che è una media divisa per tutti i residenti, non quanto paga una persona.

## Come lavorare con Marvin
- Scrivere in italiano, risposte dirette e brevi.
- Spiegare i concetti tecnici con un'analogia e un esempio pratico.
- Le richieste sono spesso brevi: fare esattamente quella modifica, senza riscrivere il resto.
- Se chiede solo una spiegazione, non modificare i file.

## Idee per i prossimi passi
- Versione per il proprio Comune, con i dati SIOPE (vedi la vecchia pagina nella cronologia di git).
- Pulsante per esportare lo scontrino finale come immagine da condividere.
