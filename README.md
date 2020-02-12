# Projektna-naloga
Analiza podatkov pri programiranju 1

Najbolj popularne restavracije v Ljubljani in okolici
==============================================

Analizirala bom vse ljubljanske restavracije, ki se nahajajo v seznamu na strani
TripAdvisor : https://www.tripadvisor.com/Restaurants-g274873-Ljubljana_Upper_Carniola_Region.html#EATERY_OVERVIEW_BOX


Za vsako restavracijo bom zajela:
* ime restavracije
* oceno
* število glasov
* tip hrane, ki jo stežejo (npr. mediteranska, italijanska ...)
* povprečno ceno jedilnika


Pod zavihkom restavracije se nahajata dve csv datoteki;
- prva zajema ime, rating, število glasov ter ceno
- druga zajema ime ter tip restavracije

Dokument Analiza.ipynb vsebuje obravnavo zgornjih datotek.

Dokument restavracije_zajem_podatkov.py vsebuje postopek zajema podatkov iz spletne strani.


### Delovne hipoteze:
* Vprašanje 1a : Kateri tip hrane se najpogosteje pojavlja pri najbolje ocenjenih restavracijah?
  HIPOTEZA : Predvidevam, da bodo to restavracije tipa Steakhouse, Seafood in Japanese.

* Vprašanje 1b : Kateri tip hrane se najpogosteje pojavlja pri najslabše ocenjenih restavracijah?
  HIPOTEZA : Predvidevam, da bodo to restavracije tipa Fast Food, Pizza, Cafe.

* Vprašanje 2 : Kakšna je povezava med številom glasov in oceno restavracije?
  HIPOTEZA : Predvidevam, da najmanj ljudi oceni posamezno restavracijo z oceno 1.0, največ pa z 4.0.

* Vprašanje 3 : Kateri tipi restavracij so največkrat ocenjeni?
  HIPOTEZA : Predvidevam, da so to restavracije tipa Pizza, Slovenian in Italian.

* Vprašanje 4 : Najbolj pogost tip restavracij v Ljubljani?
  HIPOTEZA : Predvidevam, da bodo to restavracije tipa Slovenian, Pizza, Bar in Barbecue.


### ODGOVORI NA ZASTAVLJENA ZPRAŠANJA : 

* Odgovor 1a : Najbolje ocenjene restavracije so največkrat tipa: European, Mediterranean, Healthy, Slovenian, International.

* Odgovor 1b : Najslabše ocenjene restavracije so največkrat tipa: Pizza, Slovenian, Italian, European.

* Odgovor 2 : Največ ljudi bo restavracijo ocenilo z oceno 4.5, najmanj pa z oceno 1.0.

* Odgovor 3 : Največkrat ocenjene so v povprečju restavracije sledečih tipov : Contemporary, Eastern European, American.

* Odgovor 4 : V Ljubljani bomo najpogosteje naleteli na restavracije tipa : European, Slovenian, Italian, Pizza, Bar.


### ANALIZA PRIDOBLJENIH REZULTATOV :

* 1a : Hipoteza se ne ujema z rezultatom. Upoštevati moramo pa, da tip "European"  lahko predstavlja zelo različne restavracije in je tudi najbolj pogost tip.

* 1b : Hipoteza se delno ujema z rezultatom. Upoštevati moramo pa, da tip "European"  lahko predstavlja zelo različne restavracije in je tudi najbolj pogost tip, prav tako kot je Slovenian tudi med najbolj pogostimi tipi.

* 2 : Hipoteza se skoraj ujema z rezultatom. Sklepamo, da je zelo slabih restavracij malo oziroma jih ljudje raje ne ocenjujejo.

* 3 : Hipoteza se ne ujema z rezultatom. Restavracije, ki jih ljudje največkrat ocenjujejo (lahko predvidevamo, da so med bolj obiskanimi) niso v skladu s pričakovanji.

* 4 : Hipoteza se skoraj ujema z rezultatom.