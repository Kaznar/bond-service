# Bond Service Interview Assignment

## Cíl
Vaším úkolem je vytvořit backendovou službu pro investování do korporátních dluhopisů pomocí Pythnu, Djanga a Django Rest Frameworku. Tato služba umožní uživatelům spravovat své investice do korporátních dluhopisů a sledovat výkonnost svého portfolia v čase.

## Fíčury
### 1. Autentizace uživatele
Jednoduchá autentizace pomocí API tokenu je dostatečná.

### 2. Správa dluhopisů
Uživatelé by měli být schopni:
- Přidat nové dluhopisy do svého portfolia, včetně názvu emise, ISIN emise, hodnoty dluhopisu, úrokové sazby, data nákupu, data splatnosti a frekvence úrokových plateb (výnosů).
- Aktualizovat údaje o vlastněných dluhopisech.
- Smazat dluhopis ze svého portfolia.
- Zobrazit seznam všech dluhopisů, které vlastní.

### 3. Analýza investic
Implementujte endpoint, který vrátí analýzu portfolia uživatele, včetně:
- Průměrná úroková sazba všech dluhopisů.
- Dluhopis, který bude nejbližší k splatnosti.
- Celková hodnota portfolia.
- Budoucí hodnota portfolia.

### 4. Dokumentace API
Zahrňte API dokumentaci pomocí built-in knihoven Django Rest Frameworku nebo 3rd party knihoven.

### 5. Validace
ISIN by měl být validován pomocí veřejného API Centrálního depozitáře cenných papírů. Zde je příklad volání API s platným ISIN identifikátorem:
```
GET https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin=CZ0003551251

{
   "vydaneisiny":[
      {
         "cval":"CZ0003551251",
         "ison":"Rentico Invest/11.23 DEB 20260531",
         "tval":"100",
         "pdcp":"list",
         "regdt":"2023-05-24",
         "eico":"0019319703",
         "ename":"Rentico Invest s.r.o.",
         "elei":"315700PZ559GOUR26559"
      }
   ]
}
```
### 6. Tests
Pokryjte backend rozumným množstvím testů.

### 7. NTH: Dockerizace Django backendu

## Co budeme hodnotit
- Dobře strukturovaný a čistý kód
- Použití RESTful API principů
- Zpracování chyb
- Přístup k testování

## Odevzdání
Prosím, umístěte kód do GitHub repozitáře. Vložte soubor README s instrukcemi, jak nastavit a spustit projekt.
