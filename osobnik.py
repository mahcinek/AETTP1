import copy
import random
from operator import itemgetter
from collections import Counter


class Osobnik:
    item_list = []
    location_list = []
    dist_arr = []
    mod_item_arr = []

    def __init__(self, size, items_count, plecak_size, plecak_koszt, max_speed, min_speed, item_list,
                 location_list, dist_arr, mod_item_arr, pop_chance, m_prawd, tabu_size):
        self.trasa = self.random_trasa(size)
        self.plecak = self.init_plecak(items_count)
        self.item_count = items_count
        self.wartosc_funkcji = 0
        self.size = size
        self.m_prawd = m_prawd
        self.pop_chance = pop_chance
        self.plecak_size = int(plecak_size)
        self.plecak_koszt = float(plecak_koszt)
        self.min_speed = float(min_speed)
        self.tabu_size = tabu_size
        self.max_speed = float(max_speed)
        self.k_trasy = 0
        self.s = 0
        self.tabu_list = []
        self.const_wsp = (self.max_speed - self.min_speed)/self.plecak_size
        if len(Osobnik.item_list) == 0:
            Osobnik.item_list = item_list
        if len(Osobnik.location_list) == 0:
            Osobnik.location_list = location_list
        if len(Osobnik.dist_arr) == 0:
            Osobnik.dist_arr = dist_arr
        if len(Osobnik.mod_item_arr) == 0:
            Osobnik.mod_item_arr = mod_item_arr
        self.ocen2()

    def random_trasa(self, size):
        lista = list(range(0, size))
        random.shuffle(lista)
        return copy.deepcopy(lista)

    def to_tabu_syntax(self):
        return ''.join(map(str, self.trasa))

    def sasiad(self):
        new_osobnik = copy.deepcopy(self)
        dlugosc = len(self.trasa)
        ind = random.sample(list(range(0,dlugosc-1)),2)
        swapper = new_osobnik.trasa[ind[0]]
        new_osobnik.trasa[ind[0]]=new_osobnik.trasa[ind[1]]
        new_osobnik.trasa[ind[1]] = swapper
        return copy.deepcopy(new_osobnik)



    def generuj_sąsiadow(self,liczba):
        ret_arr = []
        new_arr = []
        for i in range(liczba):
            ret_arr.append(self.sasiad())
        for elem in ret_arr:
            if elem.to_tabu_syntax() in self.tabu_list:
                continue
            else:
                new_arr.append(elem)
        if len(new_arr) < 1:
            new_arr.append(copy.deepcopy(self.mutuj_osobnika()))
        return new_arr

    def f_oceny(self):
        w = self.wart_plec()
        k = self.plecak_koszt
        # waga = self.waga_plecaka()
        t = self.koszt_trasy()
        # size = self.plecak_size
        r = w-k*t
        a= 0
        return r

    def waga_plecaka(self):
        plecak = self.plecak
        suma = 0
        index = 0
        for item in plecak:
            if item is not -1:
                suma = suma + Osobnik.item_list[index][2]
            index = index +1
        return suma

    def koszt_trasy(self):
        index = 0
        suma = 0
        w_kon = 0
        last_elem = []
        for elem in self.trasa:
            index = index + 1
            if index -1 == 0:
                last_elem = elem
                continue
            else:
                dist = self.get_distnace_from_arr(last_elem, elem)

                w, w2 = self.waga_trasy(last_elem,elem)
                w_kon = w
                w_k = w2
                speed = self.calc_speed(w2)
                ad = dist / speed
                suma = suma + ad
                last_elem = elem
            index = index + 1
        dist = self.get_distnace_from_arr(self.trasa[0], self.trasa[-1])
        speed = self.calc_speed(self.waga_plecaka())
        suma = suma + dist / speed
        self.k_trasy = suma
        return suma


    def ocen2(self):
        self.fill_backpack()
        self.wartosc_funkcji = self.f_oceny()

    def fill_backpack2(self,arr):
        self.plecak = self.init_plecak(self.item_count)
        new_item_arr = arr
        new_item_arr = sorted(new_item_arr, key=itemgetter(2))
        end = self.s
        i =0
        waga = 0
        s = self.plecak_size
        self.s = end + 1
        while waga <= s and i <= s:
            item = new_item_arr.pop(0)
            if waga + item[2] > self.plecak_size:
                break
            self.plecak[item[0] - 1] = item[3]
            waga = waga + item[2]
            a = 0
            i = i + 1
        return 0

    def fill_backpack(self):
        self.plecak = self.init_plecak(self.item_count)
        new_items_arr = self.mod_item_arr
        trasa = self.trasa
        index = 1
        exchange_list = []
        ret = []
        for miejsce in trasa:
            exchange_list.append((index,miejsce))
            index = index + 1
        for item in new_items_arr:
            ret.append([item[0],item[1],item[2],exchange_list[item[3]-2][1],item[4]])
        ret = sorted(ret, key=itemgetter(4,3))
        waga = 0
        while waga <= self.plecak_size and len(ret) > 0:
            wa = waga
            se = self.plecak_size
            if random.random() < self.pop_chance:
                break
            else:
                item = ret.pop(-1)
                watch = waga + item[2]
                if watch > self.plecak_size :
                    break
                self.plecak[item[0]-1] = copy.deepcopy(self.trasa[item[3]])
                waga = waga + item[2]

    def waga_trasy(self,first_city,sec_city):
        items = []
        index = 0
        for item in self.plecak:
            if item is not -1:
                items.append((index, item))
            index = index + 1
        if len(items) == 0:
            return 0
        else:
            tr = self.trasa
            city = min(tr.index(first_city), tr.index(sec_city))
            trasa_zrobiona = tr [:city+1]
            itemy = list(map(lambda elem: elem[1],filter(lambda elem: elem[1] in trasa_zrobiona, items)))
            il = self.item_list
            suma = 0
            ind = 0
            suma2 = 0
            for miejsce in trasa_zrobiona:
                if miejsce in self.plecak:
                    nr_przedmiotu = self.plecak.index(miejsce)
                    suma2 = suma2 + il[nr_przedmiotu][2]
            for item in itemy:
                suma = suma + il[ind][2]
                ind = ind + 1
            # waga_c = self.waga_plecaka()
            return suma,suma2


    def init_plecak(self, items_count):
        return [-1] * items_count

    def __str__(self):
        return str([self.trasa, self.plecak, self.wartosc_funkcji])

    def __repr__(self):
        return str(([self.trasa, self.plecak], self.wartosc_funkcji))

    def napraw_trase(self,trasa):
        tr = trasa
        pelna_lista = list(range(0,len(trasa)))
        wiecej_niz_raz= set([i for i in trasa if trasa.count(i) > 1])
        pelny_set = set(pelna_lista)
        brak = pelny_set - set(tr)
        while len(brak) > 0:
            a = list(wiecej_niz_raz)[0]
            tr[tr.index(a)] = list(brak)[0]
            wiecej_niz_raz = set([i for i in tr if tr.count(i) > 1])
            brak = pelny_set - set(tr)
        return copy.deepcopy(tr)

    def napraw_plecak(self):
        return 0

    def mutuj_osobnika(self):
        trasa = self.trasa
        for elem in trasa:
            if self.m_prawd >= random.random():
                indexes = random.sample(range(0, len(trasa) - 1), 1)
                ind = trasa.index(elem)
                swap = trasa[ind]
                trasa[ind] = trasa[indexes[0]]
                trasa[indexes[0]] = swap
                self.trasa = trasa
        return copy.deepcopy(self)

    def krosuj_osobnika(self, osobnik2):
        trasa1 = self.trasa
        dl_trasy = len(trasa1)
        r_start = round(dl_trasy/2-float(random.randint(0,1)))
        r_end = round(dl_trasy/2+float(random.randint(1,2)))
        if r_start == r_end:
            r_end = r_end+1
        choice = range(r_start,r_end)
        cut_index = random.sample(choice,1)
        cut_index = cut_index[0]
        if cut_index > dl_trasy:
            cut_index = dl_trasy - 2
        if cut_index < 0:
            cut_index = 1
        trasa2 = osobnik2.trasa
        t1cz1 = trasa1[:cut_index]
        t1cz2 = trasa1[cut_index:]
        t2cz1 = trasa2[:cut_index]
        t2cz2 = trasa2[cut_index:]
        t1 = t1cz1 + t2cz2
        t2 = t2cz1 + t1cz2
        t1 = self.napraw_trase(t1)
        t2 = self.napraw_trase(t2)
        self.trasa = copy.deepcopy(t1)
        osobnik2.trasa = copy.deepcopy(t2)
        return copy.deepcopy(self), copy.deepcopy(osobnik2)

    def wart_plec(self):
        # return 0 # disable this
        suma = 0
        index = 0
        for item in self.plecak:
            if item is not -1:
                dod = Osobnik.item_list[index][1]
                suma = suma + dod
            index = index + 1
        return suma

    def gen_sasiadow_sa(self, liczba):
        ret_arr = []
        new_arr = []
        for i in range(liczba):
            ret_arr.append(self.sasiad())
        return ret_arr

    def calc_speed(self, w_c):
        r = self.max_speed - w_c * self.const_wsp
        a = 0
        return r

    def get_distnace_from_arr(self, place1, place2):
        return Osobnik.dist_arr[place1][place2]