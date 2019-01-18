import random

from osobnik import Osobnik
import copy


class Populacja:

    tour_size = 0

    def __init__(self, pop_size, trasa_size, item_count, plecak_size, plecak_koszt, min_speed, max_speed, m_prawd,
                 x_prawd, tour_size, item_list, location_list, dist_arr, mod_item_arr, pop_chance):
        self.m_prawd = m_prawd
        self.x_prawd = x_prawd
        self.tour_size = tour_size
        self.pop = self.generuj_pop(pop_size, trasa_size, item_count, plecak_size, plecak_koszt, min_speed, max_speed,
                                    item_list, location_list, dist_arr, mod_item_arr, pop_chance, m_prawd)


    @staticmethod
    def generuj_pop(size, trasa_size, item_count, plecak_size, plecak_koszt, min_speed, max_speed, item_list,
                    location_list, dist_arr, mod_item_arr, pop_chance, m_prawd):
        ret = []
        for i in range(size):
            ret.append(Osobnik(trasa_size, item_count, plecak_size, plecak_koszt, min_speed, max_speed, item_list,
                               location_list, dist_arr, mod_item_arr, pop_chance, m_prawd, 0)) #tabu size 0
        return copy.deepcopy(ret)

    def get_best(self):
        index = 0
        best_index = 0
        max = self.pop[0].wartosc_funkcji
        for osobnik in self.pop:
            wart = osobnik.wartosc_funkcji
            if wart > max:
                best_index = index
                max = wart
            index = index + 1
        return copy.deepcopy(self.pop[best_index])

    def get_best_worst_average(self):
        index = 0
        best_index = 0
        worst_index = 0
        suma = 0
        max = self.pop[0].wartosc_funkcji
        min = self.pop[0].wartosc_funkcji
        for osobnik in self.pop:
            wart = osobnik.wartosc_funkcji
            if wart > max:
                best_index = index
                max = wart
            if wart < min:
                worst_index = index
                min = wart
            suma = suma +wart
            index = index + 1
        avg = round(suma,5)/index
        return max,min, avg, copy.deepcopy(self.pop[best_index])

    def get_besT_from_list(self,lista):
        index = 0
        best_index = 0
        max = lista[0].wartosc_funkcji
        for osobnik in lista:
            wart = osobnik.wartosc_funkcji
            if wart > max:
                best_index = index
                max = wart
            index = index + 1
        return copy.deepcopy(lista[best_index])

    def mutuj_pop(self):
        for osobnik in self.pop:
            osobnik.mutuj_osobnika()

    def krosuj_pop(self):
        ind = 0
        for osobnik in self.pop:
            if self.x_prawd >= random.random():
                os2= random.sample(self.pop,1)
                os2 = os2[0]
                i = self.pop.index(os2)
                t1 = osobnik.trasa
                t2 = os2.trasa
                osobnik, osobnik2 = osobnik.krosuj_osobnika(os2)
                self.pop[i] = osobnik2
                self.pop[ind] = osobnik
                a = 0
                ind= ind + 1
        a=0


    def ocen_pop(self):
        for elem in self.pop:
            elem.ocen2()

    def turniej(self):
        sample = random.sample(self.pop, self.tour_size)
        b = self.get_besT_from_list(sample)
        return copy.deepcopy(b)

    def get_distnace_from_arr(self, place1, place2):
        return Osobnik.dist_arr[place1][place2]