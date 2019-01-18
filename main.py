import random

from populacja import Populacja
from scipy.spatial.distance import squareform, pdist
import numpy as np
from operator import itemgetter
import csv

def generate_disntance_matrix(coordinates_array):
    dist_array = pdist(coordinates_array)
    dist_matrix = squareform(dist_array)
    return dist_matrix

file_name = 'medium_1.ttp'
file = open(file_name, 'r')
# print(file.read())
problem_name = file.readline()
print(problem_name)
knapsack_data_type = file.readline()
print(knapsack_data_type)
dimension = file.readline()
print(dimension)
nr_of_items_line = file.readline()
print(nr_of_items_line)
capacity_of_k_line = file.readline()
print(capacity_of_k_line)
min_speed_line = file.readline()
print(min_speed_line)
max_speed_line = file.readline()
print(max_speed_line)
renting_ratio_line = file.readline()
print(renting_ratio_line)
edge_weight_type = file.readline()
print(edge_weight_type)
sht = file.readline()
print(sht)
location_list = []
loc = file.readline()
while (loc[0].isdigit()):
    loc = list(map(float, loc.split()))
    location_list.append(loc)
    loc = file.readline()
items = file.readline()
items_list = [list(map(float, items.split()))]
item = file.readline()
while bool(item) and item[0].isdigit():
    item = list(map(float, item.split()))
    items_list.append(item)
    item = file.readline()
print(location_list)
print()
print(items_list)
print()
l_os = 0
ww = []
tour_sizea = 75 #trivial 8
item_eff_meter = 0.0
x_chance = 0.25  # trivial 0.3
m_chance = 0.05 # trivial 0.18
krokm = 0.00005
krokt =2
co_ile = 12
co_ile_var = 11
best_r = -11111111110
l_os = 160
for tr in range(1):
    run_times = 600

    dist_arr = np.array(location_list)[:,[1,2]]
    dist_arr = generate_disntance_matrix(dist_arr)
    sec_item_list =list(map(lambda x: [int(x[0]), x[1],x[2],int(x[3]), round(x[1]/x[2],5)],items_list))
    sec_item_list = sorted(sec_item_list, key=itemgetter(4))
    current_run = 0
    best_arr = []
    licznik = 0
    d = []
    for i in range(6):
        best_a = -10000000
        d= []
        co_ile = 15
        co_ile_vara =29
        current_run = 0
        tour_size = tour_sizea
        best_array_one = []
        pop = Populacja(l_os,
                        len(location_list),
                        len(items_list),
                        capacity_of_k_line.split()[-1],
                        renting_ratio_line.split()[-1],
                        max_speed_line.split()[-1],
                        min_speed_line.split()[-1], m_chance, x_chance, tour_size, items_list, location_list, dist_arr,
                        sec_item_list, item_eff_meter)
        current_run = current_run + 1
        print(dist_arr)
        while current_run < run_times:

            print('start')
            licznik = licznik+1
            new_pop_list = []
            index = 0
            co_ile_vara = co_ile_vara - 1
            if co_ile_vara == 0:
                co_ile_vara = co_ile
                tour_size = tour_size + 1
                pop.tour_size = tour_size #t size change
            pop.ocen_pop()
            # print('a')
            best, worst, aver, najl_osobnik = pop.get_best_worst_average()
            if best > best_a:
                best_a = best
            if best > best_r:
                best_r = best
            a = (best, aver, worst, najl_osobnik, best_a, best_r)
            print(str(i) + ' ' + str(current_run) + ' ' + str(pop.tour_size) + ' ' + str(pop.m_prawd) + ' ' + str(best))
            d = a
            current_run = current_run + 1
            while index < l_os:
                new_pop_list.append(pop.turniej())
                index = index + 1
            pop.pop = new_pop_list
            pop.m_prawd = pop.m_prawd - krokm
            pop.mutuj_pop()
            pop.krosuj_pop()
            best_array_one.append(d)
        print('appending')
        ww.append(best_array_one[-1])
    with open('allnile '+ str(krokt) +'co ile '+ str(co_ile) +'krokm '+ str(krokm) +'dd' +file_name+' 3item_eff_meter '+ str(item_eff_meter)+' los ' + str(l_os)+' x_chance ' + str(x_chance)+' m_chance ' + str(m_chance)+ ' tour_size '+ str(tour_sizea)+ ' run_times ' +str(run_times)+ ' '+ str(random.randint(1,99999899))+'.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerows(ww)
    best_arr.append(best_array_one)

    size = len(best_arr)
    ind = 0
    ret_arr = []
    for row in best_arr[0]:
        suma_najl = 0
        suma_najg = 0
        suma_avg = 0
        suma_best = 0
        s_best_best = 0
        for lists in range(0,size-1):
            suma_najl = suma_najl + best_arr[lists][ind][0]
            val = best_arr[lists][ind][0]
            check = [lists, ind,0]
            print(suma_najg)
            val2 = best_arr[lists][ind][2]
            suma_najg = suma_najg + val2
            check2 = [lists, ind, 2]
            suma_avg = suma_avg + best_arr[lists][ind][1]
            suma_best = suma_best + best_arr[lists][ind][4]
            s_best_best = s_best_best + best_arr[lists][ind][5]
        wyn = [suma_najl/size, suma_avg/size, suma_najg/size, suma_best/size, s_best_best/size]
        ret_arr.append(wyn)
        ind = ind + 1

    b_a = [item for sublist in best_arr for item in sublist]
    with open( str(krokt) +'allfbbco ile '+ str(co_ile) +'krokm '+ str(krokm) +'dd' +file_name+' 3item_eff_meter '+ str(item_eff_meter)+' los ' + str(l_os)+' x_chance ' + str(x_chance)+' m_chance ' + str(m_chance)+ ' tour_size '+ str(tour_size)+ ' run_times ' +str(run_times)+ ' '+ str(random.randint(1,99998999))+'.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerows(b_a)


    with open( str(krokt) +'allfssco ile '+ str(co_ile) +'krokm '+ str(krokm) +'dd' +file_name+' 3avg item_eff_meter '+ str(item_eff_meter)+' los '+ str(l_os)+' x_chance ' + str(x_chance)+' m_chance ' + str(m_chance)+ ' tour_size '+ str(tour_size)+ ' run_times ' +str(run_times)+ ' '+ str(random.randint(1,999988999))+'.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerows(ret_arr)