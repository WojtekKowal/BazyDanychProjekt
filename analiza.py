import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
'''
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


'''
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


















cursor.close()
con.close()