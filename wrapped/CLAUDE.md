# Wrapped dello Stato: istruzioni per Claude Code

Prototipo di una versione "a storie" (stile Spotify Wrapped) dello Scontrino pubblico.
Pensata per ragazzi delle medie e superiori: una schermata, un'idea.

## File
- `index.html`: pagina unica e autosufficiente (HTML + CSS + JS inline). Unica risorsa esterna: Google Fonts (Archivo, Space Mono).

## Struttura
- Ogni schermata è un `<section class="slide COLORE">` dentro `<main class="phone">`.
- Colori di sfondo: `.y` giallo, `.p` rosa, `.b` blu, `.o` arancio, `.l` lilla, `.k` nero (solo scontrino finale).
- Navigazione: tocco a destra = avanti, tocco nel 30% sinistro = indietro, frecce da tastiera. Le barre in alto si generano da sole contando le slide.
- Numeri animati: `<span data-n="16.72" data-d="2">`, dove `data-n` è il valore e `data-d` i decimali.
- Barre di confronto: `<div class="cmp">` con righe `<div><span>Nome</span><em>valore</em><i><b style="--w:PERCENTUALE%"></b></i></div>`. `--w` è relativo alla barra più lunga della stessa slide.
- Monetine e scontrino finale sono generati in JS dall'array `V` (emoji, nome semplice, spesa in milioni di €, colore).

## Dati (non inventare numeri)
Stessi dati di `scontrino-pubblico/index.html` (oggetto `ITALIA`):
- Spesa ed entrate pubbliche 2024: Eurostat COFOG (`gov_10a_exp`, `gov_10a_main`).
- Residenti: 58.934.177 (ISTAT, 1° gennaio 2025).
- Formula per gli euro al giorno: `spesa in € / 58.934.177 / 365`.

Le cifre scritte a mano nelle slide (es. 2,80 € ospedali, 6,75 € IVA, 12,93 € contributi) sono calcolate con questa formula dalle sotto-voci di `ITALIA`. Se aggiorni i dati, ricalcola anche quelle.

## Regole di testo
- Linguaggio per un ragazzo di 12-14 anni: frasi brevi, niente sigle senza spiegazione.
- Solo informazioni utili a capire come vengono usati i soldi, niente curiosità fini a sé stesse.
- Tono neutro: fatti e confronti, nessun giudizio politico.
- Ricordare sempre che è una media divisa per tutti i residenti, non quanto paga una persona.

## Idee per i prossimi passi
- Versione Comune: stesse storie usando `comuni-12mesi.json`.
- Versione Scontrino delle tasse con personaggi (pizzaiolo, infermiera, programmatrice) al posto del campo stipendio.
- Pulsante per esportare lo scontrino finale come immagine da condividere.
