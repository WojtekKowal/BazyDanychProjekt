
CREATE TABLE Atrakcje
(
  id_atrakcji                INT           NOT NULL,
  nazwa_atrakcji             VARCHAR(50)   NULL    ,
  data_przegladu             DATE          NULL     COMMENT 'ostatni wykonany',
  data_nastepnego_przegladu  DATE          NULL     COMMENT 'nastepna, nie musi być w stałym odstępie',
  liczba_miejsc              INT           NULL    ,
  liczba_miejsc_vr           INT           NULL    ,
  miesieczny_koszt_dzialania DECIMAL(15,2) NULL    ,
  PRIMARY KEY (id_atrakcji)
);

CREATE TABLE Awarie
(
  id_zgloszenia            INT           NOT NULL,
  id_atrakcji              INT           NOT NULL,
  data_zgloszenia          DATE          NULL    ,
  data_zakonczenia_naprawy DATE          NULL    ,
  koszt_naprawy            DECIMAL(20,2) NULL    ,
  PRIMARY KEY (id_zgloszenia)
);

CREATE TABLE Bilety
(
  id_biletu     INT          NOT NULL,
  rodzaj_biletu VARCHAR(40)  NOT NULL,
  na_miejscu    BOOL         NULL    ,
  cena          DECIMAL(7,2) NOT NULL,
  PRIMARY KEY (id_biletu)
);

CREATE TABLE Goscie
(
  id_goscia      INT         NOT NULL,
  imie           VARCHAR(20) NOT NULL,
  nazwisko       VARCHAR(30) NOT NULL,
  data_urodzenia DATE        NULL    ,
  email          VARCHAR(75) NULL    ,
  nr_telefonu    VARCHAR(17) NULL    ,
  PRIMARY KEY (id_goscia)
);

CREATE TABLE Obsluga_atrakcji
(
  id_atrakcji   INT NOT NULL,
  id_stanowiska INT NOT NULL,
  PRIMARY KEY (id_atrakcji, id_stanowiska)
) COMMENT 'nie wszystkie stanowiska musza sie tu znalezc, mozna obslugiwac wiecej niz jedna atrak';

CREATE TABLE Odwiedzone_atrakcje
(
  id_atrakcji INT  NOT NULL,
  id_wizyty   INT  NOT NULL,
  czy_vr      BOOL NULL    ,
  PRIMARY KEY (id_atrakcji, id_wizyty)
);

CREATE TABLE Pracownicy
(
  id_pracownika     INT         NOT NULL,
  imie              VARCHAR(20) NOT NULL,
  nazwisko          VARCHAR(30) NOT NULL,
  email             VARCHAR(75) NULL    ,
  nr_telefonu       VARCHAR(17) NULL    ,
  id_stanowiska     INT         NOT NULL,
  data_zatrudnienia DATE        NOT NULL,
  PRIMARY KEY (id_pracownika)
);

CREATE TABLE Transakcje
(
  id_transakcji   INT           NOT NULL,
  id_goscia       INT           NOT NULL,
  data_transakcji TIMESTAMP     NOT NULL,
  kwota           DECIMAL(10,2) NULL     COMMENT 'cena biletow i ubezpieczen w chwilii zakupu biletu',
  PRIMARY KEY (id_transakcji)
);

CREATE TABLE Ubezpieczenia
(
  id_ubezpieczenia INT          NOT NULL,
  nazwa            VARCHAR(50)  NULL    ,
  cena             DECIMAL(7,2) NULL    ,
  PRIMARY KEY (id_ubezpieczenia)
);

CREATE TABLE Wizyty
(
  id_wizyty        INT  NOT NULL,
  id_ubezpieczenia INT  NOT NULL,
  id_biletu        INT  NOT NULL,
  id_goscia        INT  NOT NULL,
  id_transakcji    INT  NOT NULL,
  data_wizyty      DATE NULL    ,
  PRIMARY KEY (id_wizyty)
) COMMENT 'unikalne dla kazdej osoby';

CREATE TABLE Wynagrodzenia
(
  id_stanowiska INT           NOT NULL,
  stanowisko    VARCHAR(50)   NOT NULL,
  wynagrodzenie DECIMAL(12,2) NOT NULL COMMENT 'na miesiac',
  PRIMARY KEY (id_stanowiska)
) COMMENT 'na kazdym stanowisku takie samo wynagrodzenie';

CREATE TABLE Wypadki
(
  id_wypadku      INT           NOT NULL,
  id_wizyty       INT           NOT NULL,
  id_zdarzenia    INT           NOT NULL,
  wyplacona_kwota DECIMAL(10,2) NULL     COMMENT 'faktycznie wypłacona kwota',
  czas_wypadku    TIMESTAMP     NULL     COMMENT 'w dniu daty wizyty',
  PRIMARY KEY (id_wypadku)
);

CREATE TABLE zakres_ubezpieczenia
(
  id_zdarzenia     INT           NOT NULL,
  id_ubezpieczenia INT           NOT NULL,
  wyplata          DECIMAL(10,2) NULL    ,
  PRIMARY KEY (id_zdarzenia, id_ubezpieczenia)
);

CREATE TABLE Zdarzenia
(
  id_zdarzenia       INT          NOT NULL,
  nazwa              VARCHAR(40)  NULL    ,
  prawdopodobienstwo DECIMAL(5,4) NULL    ,
  PRIMARY KEY (id_zdarzenia)
);

ALTER TABLE Pracownicy
  ADD CONSTRAINT FK_Wynagrodzenia_TO_Pracownicy
    FOREIGN KEY (id_stanowiska)
    REFERENCES Wynagrodzenia (id_stanowiska);

ALTER TABLE Awarie
  ADD CONSTRAINT FK_Atrakcje_TO_Awarie
    FOREIGN KEY (id_atrakcji)
    REFERENCES Atrakcje (id_atrakcji);

ALTER TABLE Odwiedzone_atrakcje
  ADD CONSTRAINT FK_Atrakcje_TO_Odwiedzone_atrakcje
    FOREIGN KEY (id_atrakcji)
    REFERENCES Atrakcje (id_atrakcji);

ALTER TABLE Odwiedzone_atrakcje
  ADD CONSTRAINT FK_Wizyty_TO_Odwiedzone_atrakcje
    FOREIGN KEY (id_wizyty)
    REFERENCES Wizyty (id_wizyty);

ALTER TABLE Obsluga_atrakcji
  ADD CONSTRAINT FK_Atrakcje_TO_Obsluga_atrakcji
    FOREIGN KEY (id_atrakcji)
    REFERENCES Atrakcje (id_atrakcji);

ALTER TABLE Obsluga_atrakcji
  ADD CONSTRAINT FK_Wynagrodzenia_TO_Obsluga_atrakcji
    FOREIGN KEY (id_stanowiska)
    REFERENCES Wynagrodzenia (id_stanowiska);

ALTER TABLE Wizyty
  ADD CONSTRAINT FK_Ubezpieczenia_TO_Wizyty
    FOREIGN KEY (id_ubezpieczenia)
    REFERENCES Ubezpieczenia (id_ubezpieczenia);

ALTER TABLE Wizyty
  ADD CONSTRAINT FK_Bilety_TO_Wizyty
    FOREIGN KEY (id_biletu)
    REFERENCES Bilety (id_biletu);

ALTER TABLE zakres_ubezpieczenia
  ADD CONSTRAINT FK_Zdarzenia_TO_zakres_ubezpieczenia
    FOREIGN KEY (id_zdarzenia)
    REFERENCES Zdarzenia (id_zdarzenia);

ALTER TABLE zakres_ubezpieczenia
  ADD CONSTRAINT FK_Ubezpieczenia_TO_zakres_ubezpieczenia
    FOREIGN KEY (id_ubezpieczenia)
    REFERENCES Ubezpieczenia (id_ubezpieczenia);

ALTER TABLE Wizyty
  ADD CONSTRAINT FK_Goscie_TO_Wizyty
    FOREIGN KEY (id_goscia)
    REFERENCES Goscie (id_goscia);

ALTER TABLE Wizyty
  ADD CONSTRAINT FK_Transakcje_TO_Wizyty
    FOREIGN KEY (id_transakcji)
    REFERENCES Transakcje (id_transakcji);

ALTER TABLE Wypadki
  ADD CONSTRAINT FK_Wizyty_TO_Wypadki
    FOREIGN KEY (id_wizyty)
    REFERENCES Wizyty (id_wizyty);

ALTER TABLE Wypadki
  ADD CONSTRAINT FK_Zdarzenia_TO_Wypadki
    FOREIGN KEY (id_zdarzenia)
    REFERENCES Zdarzenia (id_zdarzenia);

ALTER TABLE Transakcje
  ADD CONSTRAINT FK_Goscie_TO_Transakcje
    FOREIGN KEY (id_goscia)
    REFERENCES Goscie (id_goscia);
