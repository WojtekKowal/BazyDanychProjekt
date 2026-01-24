import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

con = mysql.connector.connect(
    host='giniewicz.it',
    user='team03',
    password='te@mzoe',
    database='team03',
    port=3306
)

cursor = con.cursor()

# PYATANIE 1
print("PYTANIE 1: Znajdź najpopularniejsze atrakcje, porównaj koszta i zyski, czy są opłacalne? Jak ich czasowa niedostępność wpływała na przychody parku?")

# a) Najpopularniejsze atrakcje
print("a) Najpopularniejsze atrakcje")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji, COUNT(oa.id_atrakcji) AS liczba_odwiedzin 
FROM Atrakcje a
JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
GROUP BY a.id_atrakcji, a.nazwa_atrakcji
ORDER BY liczba_odwiedzin DESC;""")

popularne_atrakcje = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'liczba_odwiedzin'])
print(popularne_atrakcje)

# wykres słupkowy
top_atrakcje = popularne_atrakcje.head(10)
plt.figure(figsize=(12,6))
plt.bar(top_atrakcje['nazwa_atrakcji'], top_atrakcje['liczba_odwiedzin'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Atrakcja')
plt.ylabel('Liczba odwiedzin')
plt.title('Top 10 najpopularniejszych atrakcji')
plt.tight_layout() 
plt.show()



# b) Przychody generowane przez atrakcje
print("b) Przychody generowane przez atrakcje")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji, SUM(t.kwota) AS przychod
FROM Atrakcje a
JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
JOIN Wizyty w ON oa.id_wizyty = w.id_wizyty
JOIN Transakcje t ON w.id_transakcji = t.id_transakcji
GROUP BY a.id_atrakcji, a.nazwa_atrakcji;""")

przychody_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'przychod'])
print(przychody_atrakcji)

# Wykres kołowy
top_przychody = przychody_atrakcji.sort_values(by='przychod', ascending=False).head(10)
plt.figure(figsize=(8,8))
plt.pie(top_przychody['przychod'], labels=top_przychody['nazwa_atrakcji'], 
        autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
plt.title('Udział top 10 atrakcji w przychodach')
plt.axis('equal') # Równe proporcje
plt.show()


# c) Koszty obsługi atrakcji
print("c) Koszty obsługi atrakcji")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji, SUM(wy.wynagrodzenie) AS koszt_wynagrodzen
FROM Atrakcje a
JOIN Obsluga_atrakcji oa ON a.id_atrakcji = oa.id_atrakcji
JOIN Pracownicy p ON oa.id_stanowiska = p.id_stanowiska
JOIN Wynagrodzenia wy ON p.id_stanowiska = wy.id_stanowiska
GROUP BY a.id_atrakcji, a.nazwa_atrakcji;""")

koszty_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'koszt_wynagrodzen'])
print(koszty_atrakcji)

# Wykres poziomy
koszty_top = koszty_atrakcji.sort_values(by='koszt_wynagrodzen', ascending=False)
plt.figure(figsize=(10,6))
plt.barh(koszty_top['nazwa_atrakcji'], koszty_top['koszt_wynagrodzen'], color='lightgreen')
plt.xlabel('Koszt wynagrodzeń')
plt.ylabel('Atrakcja')
plt.title('Koszty obsługi atrakcji')
plt.gca().invert_yaxis()  # Największe koszty na górze
plt.tight_layout()
plt.show()


# d) Opłacalność atrakcji
print("d) Opłacalność atrakcji")

cursor.execute("""SELECT p.id_atrakcji, p.nazwa_atrakcji, p.przychod, k.koszt, (p.przychod - k.koszt) AS zysk
FROM (
    SELECT a.id_atrakcji, a.nazwa_atrakcji, SUM(t.kwota) AS przychod
    FROM Atrakcje a
    JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
    JOIN Wizyty w ON oa.id_wizyty = w.id_wizyty
    JOIN Transakcje t ON w.id_transakcji = t.id_transakcji
    GROUP BY a.id_atrakcji, a.nazwa_atrakcji
) p
JOIN (
    SELECT a.id_atrakcji, SUM(wy.wynagrodzenie) AS koszt
    FROM Atrakcje a
    JOIN Obsluga_atrakcji oa ON a.id_atrakcji = oa.id_atrakcji
    JOIN Wynagrodzenia wy ON oa.id_stanowiska = wy.id_stanowiska
    GROUP BY a.id_atrakcji
) k ON p.id_atrakcji = k.id_atrakcji;""")

oplacalnosc_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'przychod', 'koszt', 'zysk'])
print(oplacalnosc_atrakcji)


# Wykres poziomy
oplacalnosc_top = oplacalnosc_atrakcji.sort_values(by='zysk', ascending=False)

# Kolory: niebieski dla zysku >= 60000, czerwony dla < 60000
colors = ['blue' if x >= 60000 else 'red' for x in oplacalnosc_top['zysk']]

plt.figure(figsize=(12,6))
plt.barh(oplacalnosc_top['nazwa_atrakcji'], oplacalnosc_top['zysk'], color=colors)
plt.xlabel('Zysk (przychód - koszt)')
plt.ylabel('Atrakcja')
plt.title('Opłacalność atrakcji')
plt.gca().invert_yaxis()  # Najwyższy zysk na górze
plt.tight_layout()
plt.show()


# e) Czasowa niedostępność atrakcji
print("e) Czasowa niedostępność atrakcji")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji, COALESCE(SUM(DATEDIFF(IFNULL(aw.data_zakonczenia_naprawy, CURDATE()), aw.data_zgloszenia)), 0) AS dni_niedostepnosci
FROM Atrakcje a
LEFT JOIN Awarie aw ON a.id_atrakcji = aw.id_atrakcji
GROUP BY a.id_atrakcji, a.nazwa_atrakcji;""")

niedostepnosc_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'dni_niedostepnosci'])
print(niedostepnosc_atrakcji)

# dni niedostępności malejąco
niedostepnosc_top = niedostepnosc_atrakcji.sort_values(by='dni_niedostepnosci', ascending=False)
# Wykres słupkowy
plt.figure(figsize=(12,6))
plt.bar(niedostepnosc_top['nazwa_atrakcji'], niedostepnosc_top['dni_niedostepnosci'], color='skyblue')
plt.xticks(rotation=45, ha='right') 
plt.ylabel('Dni niedostępności')
plt.xlabel('Atrakcja')
plt.title('Czasowa niedostępność atrakcji')
plt.tight_layout()
plt.show()

# f) Wpływ awarii na przychody
print("f) Wpływ awarii na przychody")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji,
    SUM(CASE 
            WHEN EXISTS (
                SELECT 1
                FROM Awarie aw
                WHERE aw.id_atrakcji = a.id_atrakcji
                  AND w.data_wizyty BETWEEN aw.data_zgloszenia 
                                       AND IFNULL(aw.data_zakonczenia_naprawy, CURDATE())
            )
            THEN t.kwota
            ELSE 0
        END) AS przychod_stracony,
    SUM(t.kwota) AS przychod_calkowity
FROM Atrakcje a
LEFT JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
LEFT JOIN Wizyty w ON oa.id_wizyty = w.id_wizyty
LEFT JOIN Transakcje t ON w.id_transakcji = t.id_transakcji
GROUP BY a.id_atrakcji, a.nazwa_atrakcji;""")

awaria_a_przychody = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'przychod_stracony', 'przychod_calkowity'])
print(awaria_a_przychody)

# Wykres liniowy
awaria_a_przychody_sorted = awaria_a_przychody.sort_values(by='przychod_calkowity', ascending=False)
plt.figure(figsize=(14,6))

# Linia dla przychodów całkowitych
plt.plot(awaria_a_przychody_sorted['nazwa_atrakcji'], awaria_a_przychody_sorted['przychod_calkowity'], 
         marker='o', color='green', label='Przychód całkowity')

# Linia dla przychodów straconych
plt.plot(awaria_a_przychody_sorted['nazwa_atrakcji'], awaria_a_przychody_sorted['przychod_stracony'], 
         marker='o', color='red', label='Przychód stracony (awarie)')

plt.xticks(rotation=45, ha='right')
plt.ylabel('Kwota przychodu')
plt.xlabel('Atrakcja')
plt.title('Wpływ awarii na przychody atrakcji')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# PYATANIE 2: Sporządź wykres liczby obsłużonych klientów w każdym miesiącu działalności firmy, czy firma rośnie, czy podupada?
print("PYTANIE 2: Sporządź wykres liczby obsłużonych klientów w każdym miesiącu działalności firmy, czy firma rośnie, czy podupada?")

cursor.execute("""SELECT DATE_FORMAT(data_wizyty, '%Y-%m') AS miesiac, COUNT(*) AS liczba_wizyt
FROM Wizyty
GROUP BY miesiac
ORDER BY miesiac;""")

wizyty_miesiac = pd.DataFrame(cursor.fetchall(), columns=['miesiac', 'liczba_wizyt'])
print(wizyty_miesiac)

plt.figure(figsize=(12,6))
plt.plot(wizyty_miesiac['miesiac'], wizyty_miesiac['liczba_wizyt'], marker='o', color='blue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Miesiąc')
plt.ylabel('Liczba obsłużonych klientów')
plt.title('Liczba obsłużonych klientów w każdym miesiącu')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# PYTANIE 3: Sprawdź, czy któreś atrakcje są zbyt niebezpieczne? Czy trzeba poprawić ich bezpieczeństwo, a może zwiększyć koszt ubezpieczenia?
print("PYTANIE 3: Sprawdź, czy któreś atrakcje są zbyt niebezpieczne? Czy trzeba poprawić ich bezpieczeństwo, a może zwiększyć koszt ubezpieczenia?")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji, COUNT(wp.id_wypadku) AS liczba_wypadkow, AVG(IFNULL(wp.wyplacona_kwota, 0)) AS srednia_wyplata, COUNT(wp.id_wypadku) / COUNT(DISTINCT v.id_wizyty) AS wypadki_na_wizyte
FROM Atrakcje a
LEFT JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
LEFT JOIN Wizyty v ON oa.id_wizyty = v.id_wizyty
LEFT JOIN Wypadki wp ON v.id_wizyty = wp.id_wizyty
GROUP BY a.id_atrakcji, a.nazwa_atrakcji
ORDER BY liczba_wypadkow DESC;""")

bezpieczenstwo_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'liczba_wypadkow', 'srednia_wyplata', 'wypadki_na_wizyte'])
print(bezpieczenstwo_atrakcji)

print("""Atrakcje z dużą liczbą wypadków i dużą średnią wypłatą --> niebezpieczne, mogą wymagać poprawy bezpieczeństwa lub dodatkowego szkolenia obsługi.
Atrakcje z wysokim wskaźnikiem wypadków na wizytę --> ryzyko wysokie w stosunku do liczby klientów, warto rozważyć podwyższenie kosztu ubezpieczenia.
Jeśli wypadki są nieliczne i kwoty małe --> zwykle wystarczy monitoring i drobne poprawki bezpieczeństwa.""")


plt.figure(figsize=(12,6))
plt.scatter(bezpieczenstwo_atrakcji['liczba_wypadkow'], bezpieczenstwo_atrakcji['srednia_wyplata'], 
            s=100, color='red', alpha=0.6)
for i, row in bezpieczenstwo_atrakcji.iterrows():
    if row['liczba_wypadkow'] > 0:
        plt.text(row['liczba_wypadkow']+0.1, row['srednia_wyplata'], row['nazwa_atrakcji'], fontsize=9)
plt.xlabel('Liczba wypadków')
plt.ylabel('Średnia wypłata z ubezpieczenia')
plt.title('Niebezpieczeństwo atrakcji – liczba wypadków vs średnia wypłata')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

print("""Atrakcje w prawym górnym rogu --> dużo wypadków i wysokie koszty → priorytet do poprawy bezpieczeństwa lub ubezpieczenia
Atrakcje w lewym dolnym rogu --> mało ryzykowne""")



# PYTANIE 4: Które atrakcje generują dużo przychodu przy niskich kosztach obsługi?
print("PYTANIE 4: Które atrakcje generują dużo przychodu przy niskich kosztach obsługi?")

cursor.execute("""SELECT p.id_atrakcji, p.nazwa_atrakcji, p.przychod, k.koszt, (p.przychod - k.koszt) AS zysk, (p.przychod - k.koszt) / k.koszt AS zysk_przez_koszt
FROM (
    SELECT a.id_atrakcji, a.nazwa_atrakcji, SUM(t.kwota) AS przychod
    FROM Atrakcje a
    JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
    JOIN Wizyty w ON oa.id_wizyty = w.id_wizyty
    JOIN Transakcje t ON w.id_transakcji = t.id_transakcji
    GROUP BY a.id_atrakcji, a.nazwa_atrakcji
) p
JOIN (
    SELECT a.id_atrakcji, SUM(wy.wynagrodzenie) AS koszt
    FROM Atrakcje a
    JOIN Obsluga_atrakcji oa ON a.id_atrakcji = oa.id_atrakcji
    JOIN Wynagrodzenia wy ON oa.id_stanowiska = wy.id_stanowiska
    GROUP BY a.id_atrakcji
) k ON p.id_atrakcji = k.id_atrakcji
ORDER BY zysk_przez_koszt DESC;""")

efektywnosc_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'przychod', 'koszt', 'zysk', 'zysk_przez_koszt'])
print(efektywnosc_atrakcji)

cursor.execute("""SELECT id_atrakcji, COUNT(*) AS liczba_odwiedzin
FROM Odwiedzone_atrakcje
GROUP BY id_atrakcji;""")
odwiedziny = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'liczba_odwiedzin'])
print(odwiedziny)
efektywnosc_atrakcji = efektywnosc_atrakcji.merge(odwiedziny, on='id_atrakcji')
efektywnosc_atrakcji['zysk_przez_koszt'] = efektywnosc_atrakcji['zysk_przez_koszt'].astype(float)
print(efektywnosc_atrakcji)

# Wykres rozrzutu
plt.figure(figsize=(12,6))
plt.scatter(
    efektywnosc_atrakcji['liczba_odwiedzin'], 
    efektywnosc_atrakcji['zysk'], 
    s=efektywnosc_atrakcji['zysk_przez_koszt']*50,
    c=efektywnosc_atrakcji['zysk_przez_koszt'],   
    cmap='viridis', 
    alpha=0.7,
    edgecolors='w'
)

for i, row in efektywnosc_atrakcji.iterrows():
    if row['zysk'] > 0:
        plt.text(row['liczba_odwiedzin']+0.5, row['zysk'], row['nazwa_atrakcji'], fontsize=9)

plt.xlabel('Liczba odwiedzin (popularność)')
plt.ylabel('Zysk atrakcji')
plt.title('Efektywność atrakcji: zysk vs liczba odwiedzin')
plt.colorbar(label='Zysk / Koszt')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()



# PYTANIE 5: Jak atrakcyjność atrakcji zmienia się w zależności od sezonu?
print("PYTANIE 5: Jak atrakcyjność atrakcji zmienia się w zależności od sezonu?")

cursor.execute("""SELECT a.id_atrakcji, a.nazwa_atrakcji, MONTH(w.data_wizyty) AS miesiac, COUNT(*) AS liczba_wizyt
FROM Atrakcje a
JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
JOIN Wizyty w ON oa.id_wizyty = w.id_wizyty
GROUP BY a.id_atrakcji, a.nazwa_atrakcji, MONTH(w.data_wizyty)
ORDER BY a.id_atrakcji, miesiac;""")

sezon_atrakcji = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'miesiac', 'liczba_wizyt'])
print(sezon_atrakcji)

# wiersze = atrakcje, kolumny = miesiące, wartości = liczba wizyt
pivot_sezon = sezon_atrakcji.pivot(index='nazwa_atrakcji', columns='miesiac', values='liczba_wizyt').fillna(0)
print(pivot_sezon)

plt.figure(figsize=(12,8))
sns.heatmap(pivot_sezon, annot=True, fmt=".0f", cmap='YlOrRd', cbar_kws={'label': 'Liczba wizyt'})
plt.xlabel('Miesiąc')
plt.ylabel('Atrakcja')
plt.title('Sezonowa popularność atrakcji (liczba wizyt w miesiącach)')
plt.yticks(rotation=0) 
plt.show()



# PYTANIE 6: Czy wiek gości ma wpływ na wybór atrakcji i korzystanie z VR?
print("PYTANIE 6: Czy wiek gości ma wpływ na wybór atrakcji i korzystanie z VR?")

cursor.execute("""SELECT CASE
    WHEN TIMESTAMPDIFF(YEAR, g.data_urodzenia, CURDATE()) < 12 THEN 'Dzieci'
    WHEN TIMESTAMPDIFF(YEAR, g.data_urodzenia, CURDATE()) BETWEEN 12 AND 17 THEN 'Młodzież'
    WHEN TIMESTAMPDIFF(YEAR, g.data_urodzenia, CURDATE()) BETWEEN 18 AND 60 THEN 'Dorośli'
    ELSE 'Seniorzy'
END AS grupa_wiekowa,
COUNT(*) AS liczba_wizyt,
SUM(CASE WHEN oa.czy_vr = 1 THEN 1 ELSE 0 END) AS wizyty_vr
FROM Goscie g
JOIN Wizyty w ON g.id_goscia = w.id_goscia
JOIN Odwiedzone_atrakcje oa ON w.id_wizyty = oa.id_wizyty
GROUP BY grupa_wiekowa
ORDER BY liczba_wizyt DESC;""")

wiek_vr = pd.DataFrame(
    cursor.fetchall(),
    columns=['grupa_wiekowa', 'liczba_wizyt', 'wizyty_vr']
)

# Procent wizyt VR
wiek_vr['procent_vr'] = (wiek_vr['wizyty_vr'] / wiek_vr['liczba_wizyt']) * 100
print(wiek_vr)

x = np.arange(len(wiek_vr))
width = 0.35

plt.figure(figsize=(10,6))
plt.bar(x - width/2, wiek_vr['liczba_wizyt'], width, label='Wszystkie wizyty')
plt.bar(x + width/2, wiek_vr['wizyty_vr'], width, label='Wizyty VR')

plt.xticks(x, wiek_vr['grupa_wiekowa'])
plt.xlabel('Grupa wiekowa')
plt.ylabel('Liczba wizyt')
plt.title('Korzystanie z atrakcji VR według grup wiekowych')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()



# PYTANIE 7: Czy koszty utrzymania atrakcji są proporcjonalne do ich popularności wśród odwiedzających?
print("PYTANIE 7: Czy koszty utrzymania atrakcji są proporcjonalne do ich popularności wśród odwiedzających?")

cursor.execute("""SELECT p.id_atrakcji, p.nazwa_atrakcji, p.liczba_odwiedzin, k.koszt_utrzymania, k.koszt_utrzymania / p.liczba_odwiedzin AS koszt_na_wizyte
FROM (
    SELECT 
        a.id_atrakcji,
        a.nazwa_atrakcji,
        COUNT(*) AS liczba_odwiedzin
    FROM Atrakcje a
    JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
    GROUP BY a.id_atrakcji, a.nazwa_atrakcji
) p
JOIN (
    SELECT 
        a.id_atrakcji,
        SUM(wy.wynagrodzenie) AS koszt_utrzymania
    FROM Atrakcje a
    JOIN Obsluga_atrakcji oa ON a.id_atrakcji = oa.id_atrakcji
    JOIN Wynagrodzenia wy ON oa.id_stanowiska = wy.id_stanowiska
    GROUP BY a.id_atrakcji
) k ON p.id_atrakcji = k.id_atrakcji;""")

koszt_popularnosc = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'liczba_odwiedzin', 'koszt_utrzymania', 'koszt_na_wizyte'])
print(koszt_popularnosc)

plt.figure(figsize=(12,6))
plt.scatter(
    koszt_popularnosc['liczba_odwiedzin'],
    koszt_popularnosc['koszt_utrzymania'],
    s=80,
    alpha=0.7
)

for _, row in koszt_popularnosc.iterrows():
    plt.text(
        row['liczba_odwiedzin'] + 0.5,
        row['koszt_utrzymania'],
        row['nazwa_atrakcji'],
        fontsize=9
    )

plt.xlabel('Liczba odwiedzin (popularność)')
plt.ylabel('Koszt utrzymania')
plt.title('Koszt utrzymania atrakcji a ich popularność')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()



# PYTANIE 8: Czy goście, którzy korzystają z atrakcji VR, generują wyższe przychody niż pozostali?
print("PYTANIE 8: Czy goście, którzy korzystają z atrakcji VR, generują wyższe przychody niż pozostali?")

print("Przychód gości korzystających z VR vs zwykłe atrakcje")

cursor.execute("""SELECT 
    CASE WHEN oa.czy_vr = 1 THEN 'VR' ELSE 'Non-VR' END AS typ_atrakcji,
    COUNT(*) AS liczba_wizyt,
    SUM(t.kwota) AS laczny_przychod,
    AVG(t.kwota) AS sredni_przychod_na_wizyte
FROM Odwiedzone_atrakcje oa
JOIN Wizyty w ON oa.id_wizyty = w.id_wizyty
JOIN Transakcje t ON w.id_transakcji = t.id_transakcji
GROUP BY typ_atrakcji;""")

przychod_vr = pd.DataFrame(cursor.fetchall(), columns=['typ_atrakcji', 'liczba_wizyt', 'laczny_przychod', 'sredni_przychod_na_wizyte'])
print(przychod_vr)

plt.figure(figsize=(8,6))
plt.bar(
    przychod_vr['typ_atrakcji'],
    przychod_vr['sredni_przychod_na_wizyte'],
    color=['skyblue', 'salmon']
)
plt.ylabel('Średni przychód na wizytę')
plt.xlabel('Typ atrakcji')
plt.title('Porównanie średniego przychodu: VR vs Non-VR')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()



# PYTANIE 9: Jaki rodzaj biletów jest najczęściej sprzedawany?
print("PYTANIE 9: Jaki rodzaj biletów jest najczęściej sprzedawany?")

cursor.execute("""SELECT b.rodzaj_biletu, COUNT(*) AS liczba_sprzedanych
FROM Bilety b
JOIN Wizyty w ON b.id_biletu = w.id_biletu
GROUP BY b.rodzaj_biletu
ORDER BY liczba_sprzedanych DESC;""")

bilety_rodzaje = pd.DataFrame(cursor.fetchall(), columns=['rodzaj_biletu', 'liczba_sprzedanych'])
print(bilety_rodzaje)

plt.figure(figsize=(8,6))
plt.bar(
    bilety_rodzaje['rodzaj_biletu'],
    bilety_rodzaje['liczba_sprzedanych'],
    color='skyblue'
)
plt.xlabel('Rodzaj biletu')
plt.ylabel('Liczba sprzedanych biletów')
plt.title('Najczęściej sprzedawane rodzaje biletów')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



# PYTANIE 10: Które atrakcje przyciągają najwięcej gości i mają najmniejszą liczbę awarii – czyli które są najbardziej „pewne i popularne”?
print("PYTANIE 10: Które atrakcje przyciągają najwięcej gości i mają najmniejszą liczbę awarii – czyli które są najbardziej „pewne i popularne”?")

cursor.execute("""SELECT p.id_atrakcji, p.nazwa_atrakcji, p.liczba_odwiedzin, k.dni_niedostepnosci
FROM (
    SELECT 
        a.id_atrakcji,
        a.nazwa_atrakcji,
        COUNT(oa.id_wizyty) AS liczba_odwiedzin
    FROM Atrakcje a
    LEFT JOIN Odwiedzone_atrakcje oa ON a.id_atrakcji = oa.id_atrakcji
    GROUP BY a.id_atrakcji, a.nazwa_atrakcji
) p
JOIN (
    SELECT 
        a.id_atrakcji,
        COALESCE(SUM(DATEDIFF(IFNULL(aw.data_zakonczenia_naprawy, CURDATE()), aw.data_zgloszenia)), 0) AS dni_niedostepnosci
    FROM Atrakcje a
    LEFT JOIN Awarie aw ON a.id_atrakcji = aw.id_atrakcji
    GROUP BY a.id_atrakcji
) k ON p.id_atrakcji = k.id_atrakcji;""")

atrakcje_bezpieczne = pd.DataFrame(cursor.fetchall(), columns=['id_atrakcji', 'nazwa_atrakcji', 'liczba_odwiedzin', 'dni_niedostepnosci'])
print(atrakcje_bezpieczne)

plt.figure(figsize=(12,6))
plt.scatter(
    atrakcje_bezpieczne['liczba_odwiedzin'],
    atrakcje_bezpieczne['dni_niedostepnosci'],
    s=100,
    alpha=0.7,
    color='green'
)

for _, row in atrakcje_bezpieczne.iterrows():
    plt.text(
        row['liczba_odwiedzin'] + 0.5,
        row['dni_niedostepnosci'],
        row['nazwa_atrakcji'],
        fontsize=9
    )

plt.xlabel('Liczba odwiedzin (popularność)')
plt.ylabel('Dni niedostępności (awarie)')
plt.title('Popularność atrakcji vs niezawodność (dni niedostępności) – poprawione')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


cursor.close()
con.close()