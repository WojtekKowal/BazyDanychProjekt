import random
import datetime
from decimal import Decimal
import mysql.connector

con = mysql.connector.connect(
    host = "giniewicz.it",
    user = "team03",
    password = "te@mzoe",
    database = "team03"
)

mycursor = con.cursor()

# Usuwanie istniejących danych

mycursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
mycursor.execute("TRUNCATE TABLE Odwiedzone_atrakcje;")
mycursor.execute("TRUNCATE TABLE Wypadki;")
mycursor.execute("TRUNCATE TABLE Transakcje;")
mycursor.execute("TRUNCATE TABLE Wizyty;")
mycursor.execute("TRUNCATE TABLE Bilety;")
mycursor.execute("TRUNCATE TABLE zakres_ubezpieczenia;")
mycursor.execute("TRUNCATE TABLE Ubezpieczenia;")
mycursor.execute("TRUNCATE TABLE Zdarzenia;")
mycursor.execute("TRUNCATE TABLE Awarie;")
mycursor.execute("TRUNCATE TABLE Obsluga_atrakcji;")
mycursor.execute("TRUNCATE TABLE Atrakcje;")
mycursor.execute("TRUNCATE TABLE Goscie;")
mycursor.execute("TRUNCATE TABLE Pracownicy;")
mycursor.execute("TRUNCATE TABLE Wynagrodzenia;")
mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")



# Zmienne globalne

start_parku = datetime.date(2018, 6, 23)

liczba_pracownikow = 6 # ma być 15

liczba_gosci = 750

liczba_wizyt = 1000 

otwarcie = datetime.time(7, 30, 0)

zamkniecie = datetime.time(21, 30, 0)

# Nazwy

imiona_m = [
    "Jan", "Stanisław", "Piotr", "Andrzej", "Krzysztof", "Józef", "Tomasz", "Paweł", 
    "Michał", "Tadeusz", "Marcin", "Adam", "Marek", "Jerzy", "Grzegorz", "Henryk", 
    "Zbigniew", "Łukasz", "Jakub", "Kazimierz", "Mateusz", "Ryszard", "Wojciech", 
    "Marian", "Dariusz", "Władysław", "Mariusz", "Robert", "Maciej", "Rafał", 
    "Jacek", "Janusz", "Franciszek", "Antoni", "Kamil", "Mirosław", "Dawid", 
    "Roman", "Edward", "Mieczysław", "Sławomir", "Jarosław", "Wiesław", "Czesław", 
    "Szymon", "Zdzisław", "Stefan", "Kacper", "Artur", "Bartosz", "Sebastian",
]

imiona_z = ["Anna", "Maria", "Katarzyna", "Zofia", "Małgorzata", "Krystyna", "Agnieszka", 
    "Barbara", "Janina", "Ewa", "Elżbieta", "Helena", "Teresa", "Jadwiga", 
    "Magdalena", "Joanna", "Marianna", "Aleksandra", "Irena", "Monika", "Danuta", 
    "Stanisława", "Halina", "Marta", "Karolina", "Natalia", "Beata", "Dorota", 
    "Julia", "Grażyna", "Jolanta", "Alicja", "Iwona", "Paulina", "Bożena", 
    "Urszula", "Justyna", "Wiktoria", "Renata", "Wanda", "Sylwia", "Józefa", 
    "Agata", "Zuzanna", "Stefania", "Weronika", "Genowefa", "Emilia", "Patrycja", 
    "Izabela", "Hanna"
]

nazwiska_m = [
    "Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński", 
    "Lewandowski", "Zieliński", "Szymański", "Dąbrowski", "Kozłowski", 
    "Mazur", "Jankowski", "Kwiatkowski", "Wojciechowski", "Krawczyk", 
    "Kaczmarek", "Piotrowski", "Grabowski", "Zając", "Pawłowski", 
    "Król", "Michalski", "Wróbel", "Wieczorek", "Jabłoński", 
    "Nowakowski", "Majewski", "Olszewski", "Dudek", "Stępień", 
    "Jaworski", "Adamczyk", "Malinowski", "Górski", "Pawlak", 
    "Nowicki", "Sikora", "Witkowski", "Rutkowski", "Walczak", 
    "Baran", "Michalak", "Szewczyk", "Ostrowski", "Tomaszewski", 
    "Zaleśki", "Pietrzak", "Wróblewski", "Jasiński"
]

nazwiska_z = [
    "Nowak", "Kowalska", "Wiśniewska", "Wójcik", "Kowalczyk", "Kamińska", 
    "Lewandowska", "Zielińska", "Szymańska", "Dąbrowska", "Kozłowska", 
    "Jankowska", "Mazur", "Kwiatkowska", "Wojciechowska", "Krawczyk", 
    "Kaczmarek", "Piotrowska", "Grabowska", "Pawłowska", "Michalska", 
    "Zając", "Król", "Wieczorek", "Jabłońska", "Wróbel", "Nowakowska", 
    "Majewska", "Olszewska", "Adamczyk", "Jaworska", "Malinowska", 
    "Stępień", "Dudek", "Górska", "Nowicka", "Pawlak", "Witkowska", 
    "Sikora", "Rutkowska", "Walczak", "Michalak", "Szewczyk", 
    "Ostrowska", "Baran", "Tomaszewska", "Pietrzak", "Zalewska", 
    "Wróblewska", "Jasińska"
]

atrakcje = [
    ["rollercoaster", "diabelski młyn", "młot"],
    ["zjeżdżalnia", "leniwa rzeka", "laser tag"],
    ["escape room", "brodzik", "gokarty", "nawiedzony dom", "karuzela", "wyścigi chomików"]
] # podzielone na 3 drogie, tańsze i tanie i ma być ich 20

zdarzenia = [
    ["stracenie wzroku przez atrakcję", "atak terrorystyczny", "śmierć"], 
    ["zatrucie pokarmowe", "spuszczenie telefonu w toalecie", "zgubienie dziecka w tłumie", "zadławienie się", "uszczerbek na zdrowiu"], 
    ["atak gołębi", "naruszenie strefy osobistej przez maskotkę parku", "wkurzający dzieciak", "utknięcie w atrakcji", "awaria atrakcji"]
] # też podzielone na 3 i ma być ich 20

# Pomocnicze funkcje

def losowa_data(p, k, i):
    roznica_dni = k - p
    roznica = roznica_dni.days
    losowy_dzien = random.randint(0, roznica)
    data = p + datetime.timedelta(days = losowy_dzien)
    if i == 0:
        return data.strftime("%Y-%m-%d")
    else: return data

def cena(a, b, t = 0):
    a1, b1 = int(a * 100), int(b * 100)
    if t == 0:
        return float(Decimal(random.randint(a1, b1)) / Decimal(100))
    else: return Decimal(random.randint(a1, b1)) / Decimal(100)
    
def losowa_godzina(p, k, i):
    p_sek = p.hour * 3600 + p.minute * 60 + p.second
    k_sek = k.hour * 3600 + k.minute * 60 + k.second
    sek = random.randint(p_sek, k_sek)

    h = sek // 3600
    m = (sek % 3600) // 60
    s = sek % 60
    godzina = datetime.time(h, m, s)
    if i == 0:
        return godzina.strftime("%H:%M:%S")
    else: return godzina



# Generowanie danych: 

# Wynagrodzenia

Wynagrodzenia = [
    ("sprzątacz", cena(4806.02, 5000)), ("obsługa rollercoasteru", cena(4806.52, 5050)), ("obsługa VR", cena(5500.83, 6750)),
    ("ubezpieczyciel", cena(6500.95, 8000)), ("konserwator", cena(4806.01, 5000)), ("technik", cena(7489.99, 8500))
] # ma być ich 10



# Pracownicy

def nazwiska(imie):
    if imie in imiona_m:
        return random.choice(nazwiska_m)
    else: return random.choice(nazwiska_z) 

def pracownicy(S, M, k, s = start_parku):
    L = []
    R = list(range(1, len(S) + 1))
    for i in range(k):
        imie_f = random.choice(M)
        nazwisko_f = nazwiska(imie_f)
        email_f = imie_f.lower() + "." + nazwisko_f.lower() + "@gmail.com"
        tele = random.randint(111111111, 999999999)
        id_stan = random.choice(R)
        R.remove(id_stan)
        data_zat = losowa_data(s, datetime.date.today(), 0)
        L.append((imie_f, nazwisko_f, email_f, tele, id_stan, data_zat))
    return L

Pracownicy = pracownicy(Wynagrodzenia, M = (imiona_m + imiona_z), k = liczba_pracownikow)



# Goscie

def goscie(M, k):
    L = []
    for i in range(k):
        imie_f = random.choice(M)
        nazwisko_f = nazwiska(imie_f)
        data_ur = losowa_data(datetime.date(1970, 1, 1), datetime.date(2018, 1, 1), 0) # według rozkładu normalnego
        email_f = imie_f.lower() + "." + nazwisko_f.lower() + "@gmail.com"
        tele = random.randint(111111111, 999999999)
        L.append((imie_f, nazwisko_f, data_ur, email_f, tele))
    return L

Goscie = goscie(M = (imiona_m + imiona_z), k = liczba_gosci)



# Atrakcje

atrakcje_all = atrakcje[0] + atrakcje[1] + atrakcje[2]

def nastepny_przeglad(t):
    data = t + datetime.timedelta(days = random.randint(9 * 31, 15 * 31))
    return data.strftime("%Y-%m-%d")

def roczny_koszt(a, A):
    if a in A[0]:
        return cena(2000000, 4000000) / 12
    elif a in A[1]:
        return cena(500000, 1000000) / 12
    else:
        return cena(50000, 80000) / 12

data_przeglądu = losowa_data(datetime.date(2025, 5, 1), datetime.date.today(), 1)


Atrakcje = [(a, losowa_data(datetime.date(2025, 5, 1), datetime.date.today(), 0), nastepny_przeglad(data_przeglądu), 
            random.randrange(10, 25), random.randrange(20, 35), roczny_koszt(a, atrakcje)) for a in atrakcje_all]


# Obsługa atrakcji

def obsluga(j):
    L = []
    for i in range(len(j)):
        L.append((i + 1, random.randrange(1, len(Wynagrodzenia))))
    return L

Obsluga_atrakcji = obsluga(atrakcje_all)



# Awarie

def awarie_if(a, dn):
    # atr_all = [[], [], []]
    # i = 1
    # for j in range(len(atrakcje)):
    #     for a in atrakcje[j]:
    #         atr_all[j].append(i)
    #         i = i + 1

    if a[0] in atrakcje[0]:
        data_zgl = dn - datetime.timedelta(days = random.randrange(6 * 31, 9 * 31))
        napr = round(cena(2000000, 4000000) / 5, 2)
        return (a[1], data_zgl, dn, napr)

    elif a[0] in atrakcje[1]:
        data_zgl = dn - datetime.timedelta(days = random.randrange(2 * 31, 3 * 31))
        napr = round(cena(500000, 1000000) / 5, 2)
        return (a[1], data_zgl, dn, napr)
        
    elif a[0] in atrakcje[2]:
        data_zgl = dn - datetime.timedelta(days = random.randrange(15, 25))
        napr = round(cena(50000, 80000) / 5, 2)
        return (a[1], data_zgl, dn, napr)

def awarie(a, i, d, L):
    if i == 0:
        return None
    else:
            data_nap = d - datetime.timedelta(days = random.randrange(12 * 31, 18 * 31))
            data_nap_f = data_nap.strftime("%Y-%m-%d")
            data_zgl = awarie_if(a, data_nap)[1]
            data_zgl_f = data_zgl.strftime("%Y-%m-%d")
            napr = awarie_if(a, data_nap)[3]
            L.append((atrakcje_all.index(a[0]) + 1, data_zgl_f, data_nap_f, napr))
            i = i - 1
            awarie(a, i, data_zgl, L)

def Awarie_f(A, n):
    aa = [(A[i], A.index(A[i]), random.randrange(0, 3), A[A.index(A[i])][1]) for i in random.sample(list(range(len(atrakcje_all))), k = n)] # do naprawy bo za malo tych awarii
    L = []
    for a in aa:
        awarie(a[0], a[2], datetime.date.fromisoformat(a[3]), L)
    return L

Awarie = Awarie_f(Atrakcje, 10)



# Zdarzenia

zdarzenia_all = zdarzenia[0] + zdarzenia[1] + zdarzenia[2]

def prawdop(Z, i): 
    if Z[i] in zdarzenia[0]:
        return round(random.uniform(0.001, 0.0005), 4)

    elif Z[i] in zdarzenia[1]:
        return round(random.uniform(0.05, 0.001), 4)
        
    elif Z[i] in zdarzenia[2]:
        return round(random.uniform(0.1, 0.05), 4)

Zdarzenia = [(zdarzenia_all[n], prawdop(zdarzenia_all, n)) for n in range(len(zdarzenia_all))]



# Ubezpieczenia

cena_S = cena(15, 30, t = 1) # mało poważne

cena_M = cena(35, 55, t = 1) # mniej poważne

cena_L = cena(60, 85, t = 1) # najpoważniejsze

Ubezpieczenia = [
    ("pakiet S", float(cena_S)), ("pakiet M", float(cena_M)), ("pakiet L", float(cena_L)),
    ("pakiet S + M", float(cena_S + cena_M)), ("pakiet ALL", float(cena_S + cena_M + cena_L)), ("pakiet M + L", float(cena_M + cena_L))
]



# Zakres ubezpieczenia

ubez_hierar = [[("pakiet S", 1), ("pakiet S + M", 4), ("pakiet ALL", 5)], [("pakiet M", 2), ("pakiet S + M", 4), 
                ("pakiet ALL", 5), ("pakiet M + L", 6)], [("pakiet L", 3), ("pakiet ALL", 5), ("pakiet M + L", 6)]]

def zakres(Z, u):
    L = []
    z_all = Z[0] + Z[1] + Z[2]
    u_all = list(set(u[0] + u[1] + u[2]))

    u_sort = {}
    for i in u_all:
        u_sort[i[0]] = i[1]

    u_noid = [[], [], []]
    for j in range(3):
        for k in range(len(u[j])):
            u_noid[j].append(u_all[k][0])

    for i in z_all:
        if i in Z[2]:
            wyp = cena(50, 250)
            for a in u_noid[0]: # mało powazne
                L.append((z_all.index(i) + 1, u_sort[a], wyp))

        elif i in Z[1]:
            wyp = cena(500, 2000)
            for a in u_noid[1]: # srednio powazne
                L.append((z_all.index(i) + 1, u_sort[a], wyp)) 

        else:
            wyp = cena(5000, 10000)
            for a in u_noid[2]: # bardzo powazne
                L.append((z_all.index(i) + 1, u_sort[a], wyp))
    return L

Zakres = zakres(zdarzenia, ubez_hierar)



# Bilety

def bilet(c: int, t: int):
    L = [c]
    if t >= 0:
        for i in range(t):
            k = L[i] + 10
            L.append(k)
    else:
        for i in range(-t):
            k = L[i] - 10
            L.append(k)

    return random.choice(L)

ulg, nor = bilet(139, 3) + 0.99, bilet(169, 4) + 0.99

rodzaje = [
    ("ulgowy", ulg) , ("normalny", nor), ("VIP", bilet(249, 7) + 0.99), ("urodzinowy", bilet(119, 2) + 0.99),
    ("imieninowy", bilet(129, 2) + 0.99), ("dla niepełnosprawnych", bilet(149, 2) + 0.99), ("ulgowy z obiadem", ulg + 20), ("normalny z obiadem", nor + 20)
]

Bilety = [(rodzaje[i][0],  True, rodzaje[i][1]) for i in range(len(rodzaje))] + [(rodzaje[i][0] + " VR", False , rodzaje[i][1] - 100) for i in range(len(rodzaje))]



# Wizyty

def wizyty_f(U, B, K, k = liczba_gosci):
    id_ubezp = [random.randrange(1, len(U)) for _ in range(k)]
    id_gos = [random.randrange(1, liczba_gosci) for _ in range(k)]

    bez_ul = B.copy()
    tyl_ul = []
    for a in B:
        if a[0][0:2] == "ul":
            tyl_ul.append(a)
            bez_ul.remove(a)
    
    id_bil = []
    for i in range(k):
        ur = datetime.date.fromisoformat(K[id_gos[i]][2])
        roz = datetime.date.today() - ur
        lat = round(roz.days / 365.25, 0)
        if 18 < lat < 65:
            b = random.choice(bez_ul)
            id_bil.append(B.index(b))
        else:
            r = random.randint(1, 75)
            if r == 67:
                b = random.choice(bez_ul)
                id_bil.append(B.index(b))
            else:
                b = random.choice(tyl_ul)
                id_bil.append(B.index(b))
    
    data = [losowa_data(start_parku, datetime.date.today(), 0) for _ in range(k)]

    W = []
    for i in range(k):
        W.append((id_ubezp[i], id_bil[i] + 1, id_gos[i], i + 1, data[i]))
    return W

Wizyty = wizyty_f(Ubezpieczenia, Bilety, Goscie, k = liczba_wizyt)



# Transakcje

def trans(W, B, U, i):
    u = U[W[i][0] - 1][1]
    b = B[W[i][1] - 1][2]
    g = W[i][2]
    z = datetime.datetime.combine(datetime.date.today(), zamkniecie) - datetime.timedelta(minutes = 30) # 30 min przed zamknieciem

    d_14 = datetime.date.fromisoformat(W[i][4]) - datetime.timedelta(days = 14) # 14 dni kupiony bilet przed wizytą
    d_w = datetime.date.fromisoformat(W[i][4])
    data = losowa_data(d_14, d_w, 0)
    d = data + " " + losowa_godzina(otwarcie, z, 0)
    return (g, d, u + b)

Transakcje = [trans(Wizyty, Bilety, Ubezpieczenia, i) for i in range(liczba_wizyt)]



# Wypadki

def prawdop_zd(Zd):
    p = round(random.random(), 4)
    Zd_shuf = list(Zd)
    random.shuffle(Zd_shuf)
    Zd_all = []
    for k in Zd:
        Zd_all.append(k[0])

    for i in range(len(Zd_all)):
        if p < Zd[i][1]:
            return Zd_all.index(Zd[i][0]) + 1

def wyp(Wi, Za, Zd, Tr, i): # to do naprawy bo dziwnie często są id zdarzenia od 4 do 8
    if Bilety[Wi[i][1] - 1][1] == True:
        Zd_all = [] # ryzyko maleje z wiekszym indeksem listy
        for k in Zd:
            Zd_all.append(k[0])
        Zd_pr = [] # prawdop rosnie z wiekszym indeksem listy
        for j in Zd:
            Zd_pr.append(j[1])

        id_zd = prawdop_zd(Zd) 
        if id_zd == None:
            return

        Zd_Ub = []
        for l in Za:
            Zd_Ub.append((l[0], l[1]))

        if (id_zd, Wi[i][0]) in Zd_Ub:
            for b in Za:
                if (id_zd, Wi[i][0]) == (b[0], b[1]):
                    wyp = b[2]
        else: wyp = 0

        if Tr[i][1][-8:] == Wi[i][4]:
            cz_tr = datetime.time.fromisoformat(Tr[i][1][-8:])
            cz_tr_off = (datetime.datetime.combine(datetime.date.today(), cz_tr) + datetime.timedelta(minutes = 30)).time()
            cz_zm_off = (datetime.datetime.combine(datetime.date.today(), zamkniecie) - datetime.timedelta(minutes = 30)).time()
            cz = losowa_godzina(cz_tr_off, cz_zm_off, 0)
        else:
            cz_tr_off = (datetime.datetime.combine(datetime.date.today(), otwarcie) + datetime.timedelta(minutes = 30)).time()
            cz_zm_off = (datetime.datetime.combine(datetime.date.today(), zamkniecie) - datetime.timedelta(minutes = 30)).time()
            cz = losowa_godzina(cz_tr_off, cz_zm_off, 0)

        return (i + 1, id_zd, wyp, Wi[i][4] + " " + cz)

Wypadki = list(filter(None, [wyp(Wizyty, Zakres, Zdarzenia, Transakcje, i) for i in range(liczba_wizyt)]))



# Odwiedzone atrakcje

def czy_aw(id_at, i):
    for aw in Awarie:
        if id_at == aw[0]:
            if datetime.date.fromisoformat(aw[1]) <= datetime.date.fromisoformat(Wizyty[i][4]) <= datetime.date.fromisoformat(aw[2]):
                p = round(random.random(), 4)
                if p < 0.005: # to jest po to że jak będzie awaria ale ktoś i tak odwiedzi tą atrakcje w vr
                    return True

def odw(Wi, At, Bi, k, i): # k to ile może być maksymalnie odwiedzonych atrakcji w jednejk wizycie
    At_all = []
    for a in At:
        At_all.append(a[0])
    At_od = []
    Id_at = [i for i in range(len(At_all))]
    for j in range(random.randint(1, k)):
        id_at = random.choice(Id_at) # to sa id z listy At_all
        At_od.append(id_at)
        Id_at.remove(id_at)

    L = []                  
    if Bi[Wi[i][1] - 1][1] == False:
        for a in At_od:
            L.append((a + 1, i + 1, True))
        return L
    else: 
        for a in At_od:
            czy_vr = czy_aw(a, i)
            if czy_vr == True:
                L.append((a + 1, i + 1, czy_vr))
            else:
                p = round(random.random(), 4)
                if p < 0.0005:
                    L.append((a + 1, i + 1, True))
                else: L.append((a + 1, i + 1, False))
    return L

odwiedzane = [odw(Wizyty, Atrakcje, Bilety, 7, i) for i in range(liczba_wizyt)] # zwieksz do 7

Odwiedzane_atrakcje = [od[i] for od in odwiedzane for i in range(len(od))]      



# Testy

# print(Wynagrodzenia)
# print(Pracownicy)
# print(Goscie)
# print(Atrakcje)
# print(Obsluga_atrakcji)
# print(Awarie)
# print(Zdarzenia)
# print(Ubezpieczenia)
# print(Zakres)
# print(Bilety)
# print(Wizyty)
# print(Transakcje)
# print(Wypadki)
# print(Odwiedzane_atrakcje)



# Populowanie bazy:

sql_wynagrodzenia = "INSERT INTO Wynagrodzenia (stanowisko, wynagrodzenie) VALUES (%s, %s)"
mycursor.executemany(sql_wynagrodzenia, Wynagrodzenia)
con.commit()

sql_pracownicy = "INSERT INTO Pracownicy (imie, nazwisko, email, nr_telefonu, id_stanowiska, data_zatrudnienia) VALUES (%s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql_pracownicy, Pracownicy)
con.commit()

sql_goscie = "INSERT INTO Goscie (imie, nazwisko, data_urodzenia, email, nr_telefonu) VALUES (%s, %s, %s, %s, %s)"
mycursor.executemany(sql_goscie, Goscie)
con.commit()

sql_atrakcje = "INSERT INTO Atrakcje (nazwa_atrakcji, data_przegladu, data_nastepnego_przegladu, liczba_miejsc, liczba_miejsc_vr, miesieczny_koszt_dzialania) VALUES (%s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql_atrakcje, Atrakcje)
con.commit()

sql_obsluga = "INSERT INTO Obsluga_atrakcji (id_atrakcji, id_stanowiska) VALUES (%s, %s)"
mycursor.executemany(sql_obsluga, Obsluga_atrakcji)
con.commit()

sql_awarie = "INSERT INTO Awarie (id_atrakcji, data_zgloszenia, data_zakonczenia_naprawy, koszt_naprawy) VALUES (%s, %s, %s, %s)"
mycursor.executemany(sql_awarie, Awarie)
con.commit()

sql_zdarzenia = "INSERT INTO Zdarzenia (nazwa, prawdopodobienstwo) VALUES (%s, %s)"
mycursor.executemany(sql_zdarzenia, Zdarzenia)
con.commit()

sql_ubezpieczenia = "INSERT INTO Ubezpieczenia (nazwa, cena) VALUES (%s, %s)"
mycursor.executemany(sql_ubezpieczenia, Ubezpieczenia)
con.commit()

sql_zakres = "INSERT INTO zakres_ubezpieczenia (id_zdarzenia, id_ubezpieczenia, wyplata) VALUES (%s, %s, %s)"
mycursor.executemany(sql_zakres, Zakres)
con.commit()

sql_bilety = "INSERT INTO Bilety (rodzaj_biletu, na_miejscu, cena) VALUES (%s, %s, %s)"
mycursor.executemany(sql_bilety, Bilety)
con.commit()

sql_transakcje = "INSERT INTO Transakcje (id_goscia, data_transakcji, kwota) VALUES (%s, %s, %s)"
mycursor.executemany(sql_transakcje, Transakcje)
con.commit()

sql_wizyty = "INSERT INTO Wizyty (id_ubezpieczenia, id_biletu, id_goscia, id_transakcji, data_wizyty) VALUES (%s, %s, %s, %s, %s)"
mycursor.executemany(sql_wizyty, Wizyty)
con.commit()

sql_wypadki = "INSERT INTO Wypadki (id_wizyty, id_zdarzenia, wyplacona_kwota, czas_wypadku) VALUES (%s, %s, %s, %s)"
mycursor.executemany(sql_wypadki, Wypadki)
con.commit()

sql_odwiedzone = "INSERT INTO Odwiedzone_atrakcje (id_atrakcji, id_wizyty, czy_vr) VALUES (%s, %s, %s)"
mycursor.executemany(sql_odwiedzone, Odwiedzane_atrakcje)
con.commit()

mycursor.close()
con.close() 