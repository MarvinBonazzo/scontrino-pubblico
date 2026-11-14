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
- Monetine e scontrino finale sono generati in JS dall'array `V` (emoji, nome della voce, spesa in milioni di €, colore). I nomi sono gli stessi del Wrapped dello stipendio.

## Dati (non inventare numeri)
Stessi dati di `scontrino-pubblico/index.html` (oggetto `ITALIA`):
- Spesa ed entrate pubbliche 2024: Eurostat COFOG (`gov_10a_exp`, `gov_10a_main`).
- Residenti: 58.934.177 (ISTAT, 1° gennaio 2025).
- Formula per gli euro al giorno: `spesa in € / 58.934.177 / 365`.

Le cifre scritte a mano nelle slide (es. 2,80 € ospedali, 6,75 € IVA, 12,93 € contributi) sono calcolate con questa formula dalle sotto-voci di `ITALIA`. Se aggiorni i dati, ricalcola anche quelle.
Anche le entrate al giorno della slide "E i soldi da dove arrivano?" (12,93 contributi, 12,72 IRPEF, 6,75 IVA, 4,60 accise, 3,04 IRAP e IMU, 2,73 IRES, 2,41 servizi, 2,98 il resto: somma 48,16) e il debito a testa (2.966,9 mld di Banca d'Italia ÷ residenti = 50.343 €). "Il resto" è arrotondato a 2,98 invece di 2,99 perché la somma torni con il totale.

## Parole spiegate (glossario)
Come nel Wrapped dello stipendio: ogni parola tecnica si scrive `<u data-w="chiave">parola</u>` e toccandola si apre un cartoncino in basso. Le spiegazioni sono nell'oggetto `GLOSS`, una o due frasi senza altre parole difficili. Se aggiungi una parola tecnica nuova, aggiungi anche la sua voce.

## Fine della storia
Sotto lo scontrino finale: "Ricomincia", poi i link alle due pagine complete ("Scontrino dello stipendio", "Scontrino dello Stato") e il bottone "Fonti, calcoli e numeri interi". Il bottone apre il pannello `#info`: spesa ed entrate 2024 in euro interi (array `V` ed `ENTRATE`), deficit, debito (`DEBITO`), residenti, le formule delle storie e i link alle fonti. Se cambi un dato, il pannello si aggiorna da solo tranne i testi delle fonti.

## Regole di testo
- Si dà sempre del tu, con rispetto: anche quando si sceglie un lavoro di esempio, chi legge è "tu" ("il tuo netto", "paghi").
- Diretto, senza addolcire: "Pensioni" e "anziani", non "nonni"; "Sussidi e assistenza", non "aiuti a chi ha bisogno". I nomi delle 13 voci sono gli stessi del Wrapped dello Stato.
- Linguaggio per un ragazzo di 12-14 anni: frasi brevi, niente sigle senza spiegazione.
- Solo informazioni utili a capire come vengono usati i soldi, niente curiosità fini a sé stesse.
- Tono neutro: fatti e confronti, nessun giudizio politico.
- Ricordare sempre che è una media divisa per tutti i residenti, non quanto paga una persona.

## Idee per i prossimi passi
- Versione Comune: stesse storie usando `comuni-12mesi.json`.
- Pulsante per esportare lo scontrino finale come immagine da condividere.
