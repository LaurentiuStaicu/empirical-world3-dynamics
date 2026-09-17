# R1 — Închiderea fundației empirice

Data: 17 septembrie 2026

## Decizie

R1 este considerat închis după ce această ramură trece CI-ul complet și este
integrată în `main`. Închiderea R1 nu promovează nicio extensie nouă în rularea
centrală. Aplicația rămâne 0.10.2, iar modelul central rămâne BAU Hibrid 2026
v0.10.0, o singură rulare World3-03 derivată din scenariul 2 (BAU2).

Scopul R1 a fost să construiască o fundație empirică auditabilă pentru energia
fizică, EROI, industrie și resurse/minerale, plus un contract temporal pentru
prognoze externe. O sursă sau un mecanism poate fi păstrat ca observație,
diagnostic sau sensibilitate chiar dacă nu trece pragul pentru cuplare în
modelul central.

## Contractul de acceptare

| Componentă | Evidență acceptată în R1 | Decizie pentru modelul central |
|---|---|---|
| Energie primară și mix | Energy Institute Statistical Review 2026, serie globală 1965–2025, cu proveniență | observat pentru inițializare/diagnostic; nu este stocul World3 și nu produce singur feedback nou |
| EROI fosil | Aramendia et al. 2024, 1971–2020, frontiere primară/finală/utilă și variante cu/fără energie indirectă păstrate separat | relația resurse World3 → EROI este respinsă prospectiv; extensia rămâne sensibilitate structurală |
| Energie și emisii la nivel de centrală | EIA/eGRID, bilanțuri și cohorte 2021–2023 cu proveniență, surse și limite contabile explicite | diagnostic fizic; hindcast publicat cu întârziere, nu forecast și nu recalibrare a curbei centrale |
| Industrie | World Bank + UNIDO MVA + UNIDO IIP public reconstruit | triangulare acceptată; proxy-urile UNIDO nu schimbă selectorul, deci nu promovează recalibrare |
| Minerale tehnologice | USGS/BGS/OWID, separat pentru cupru, nichel, litiu, cobalt, pământuri rare și grafit natural | registru observat de risc; fluxurile miniere nu calibrează direct stocul latent World3 |
| Prognoze externe | registru versionat cu `release_date`, `captured_on`, `available_from`, geografie, unitate și scenariu | benchmark prospectiv numai după apariția observațiilor comparabile; interzis ca țintă de calibrare |

## Energie și EROI

Datele Energy Institute și Aramendia sunt deja ingerate și testate. Pentru EROI,
frontiera contabilă este parte din definiția variabilei: EROI primar, final și
util nu sunt interschimbabile. Seria Aramendia păstrează explicit toate cele
șase combinații de frontieră și includere/excludere a energiei indirecte.

Auditul din 30 august a testat relația propusă dintre fracția de resurse World3
și EROI fosil la mai multe origini temporale. Relația pierde față de persistență
la toate cele trei frontiere agregate și este respinsă. Valoarea final-stage din
2020 poate fi folosită ca reper de persistență într-o sensibilitate, dar nu este
transformată într-o observație pentru 2025.

PR-ul R0/R1 adaugă un strat fizic separat pentru energie și emisii. Modulele
separă energia combustibilului, electricitatea brută/netă, emisiile directe și
stocul atmosferic; eficiența derivată din heat rate nu este etichetată EROI.
Auditul eGRID folosește ediții publicate după anii datelor și cunoaște producția
anului țintă, de aceea este denumit explicit hindcast/stability audit, nu
backtest prospectiv. Reconcilierea centrală–unitate–generator păstrează
vizibile discontinuitățile de acoperire în loc să le interpreteze ca schimbări
fizice de eficiență.

## Industrie

World Bank rămâne proxy-ul industrial folosit de modelul central. UNIDO MVA și
IIP sunt diagnostice independente. IIP este conceptual mai apropiat de volumul
manufacturier real, dar în originile compatibile selectează aceiași candidați
ca World Bank; câștigul prospectiv al schimbării proxy-ului este 0%, sub pragul
de promovare. Diferența de nivel din 2025 nu este tratată ca dinamică nouă.

## Minerale și resurse

R1 separă explicit fluxurile observate de stocurile latente. Producția minieră,
rezervele raportate și concentrarea geografică sunt păstrate pe material și nu
sunt însumate într-un pseudo-stoc global. Rezervele nu sunt interpretate drept
„ani până la epuizare”. Conflictul de versiune identificat pentru pământurile
rare rămâne vizibil și blochează calculul care ar amesteca surse incompatibile.

În R2, orice modul dinamic de minerale trebuie să distingă cel puțin stocul pe
material, capacitatea minieră, rafinarea, reciclarea, concentrarea geografică și
întârzierile de dezvoltare. R1 nu furnizează încă o asemenea ecuație.

## Proveniență, vintage și prevenirea informației din viitor

Observațiile procesate au proveniență și amprente; snapshotul central rămâne
reproductibil. Prognozele externe sunt stocate într-un registru separat și
funcția de acces ca observații de calibrare refuză orice înregistrare. Pentru
o pagină live fără arhivă a ediției originale, disponibilitatea este data
conservatoare a capturii, nu data nominală de publicare.

Testele temporale deja reutilizate în dezvoltare sunt descrise ca atare și nu
sunt redenumite ulterior „holdout neatins”. R2 trebuie să predeclare noi
ferestre confirmatorii când datele viitoare devin disponibile.

## Ce este respins sau amânat la sfârșitul R1

- cuplarea centrală EROI bazată pe fracția de resurse World3;
- persistența brută a intensității fiecărei centrale eGRID ca regulă de model;
- calibrarea stocului neregenerabil World3 direct pe fluxurile miniere;
- înlocuirea țintei industriale doar pentru că IIP este conceptual mai apropiat;
- folosirea prognozelor EIA sau a altor instituții drept observații de calibrare;
- interpretarea auditurilor eGRID 2021–2023 drept forecast real-time;
- orice schimbare a curbelor BAU Hibrid 2026 care nu trece un prag prospectiv
  predeclarat.

## Poarta de ieșire R1

R1 este finalizat numai dacă, pe head-ul care va fi integrat:

1. reproducerea rezultatelor științifice centrale nu produce schimbări
   neautorizate;
2. toate testele științifice și contractele de release trec;
3. Flatpak-ul se construiește în CI;
4. PR-ul este integrat în `main` fără schimbarea versiunii modelului central;
5. CI-ul post-merge pe `main` este verde.

După îndeplinirea acestor condiții, următorul pas este R2: definirea contractului
structural al Modelului Real. R2 poate utiliza componentele R1 ca observații,
priors, diagnostice sau benchmarkuri numai în rolurile documentate aici; nu le
promovează automat în feedbackuri cauzale.

## Documente de audit asociate

- `energy-coupling-audit-2026-08-30.md`
- `unido-industry-proxy-audit-2026-09-07.md`
- `unido-iip-volume-audit-2026-09-08.md`
- `technology-minerals-audit-2026-09-08.md`
- `forecast-vintages-2026-09-11.md`
- `eia-energy-boundary-audit.md`
- `energy-emissions-experiment.md`
- `egrid-plant-audit.md`
- `egrid-temporal-stability-audit-2026-09-12.md`
- `egrid-influence-audit-2026-09-12.md`
- `egrid-boundary-reconciliation-2026-09-13.md`
