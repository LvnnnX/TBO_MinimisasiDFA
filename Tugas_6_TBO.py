from math import floor,sqrt
from numpy import arange
from os import system
class Bahasa():
    def __init__(self,name,state,table,final,simbols): #Memasukkan item-item dari bahasa
        self.name = name
        self.state = state
        self.table = table
        self.final = final
        self.simbols = simbols
    
    def change_stable(self,state,table,final): #mengubah state,table,dan final state
        self.state = state
        self.table = table
        self.final = final

def find_ab(counter): #Mencari baris,kolom
    kp = counter-1
    p = floor((sqrt(1 + 8 * kp) - 1) / 2)
    i = p + 2
    j = kp - p * (p+1)/2 + 1
    return int(i-1),int(j-1)

#detailed desc = Q, Sigma, Start state, final state, delta
def print_table(state,table,list_removed,final,simbol): #print tabel transisi
    print(f"{'state':^10}|",end='')
    for x in range(len(simbol)):
        print(f"{simbol[x]:^10}|",end='')
    print()
    for a,b in enumerate(state):
        if(b not in list_removed):
            if(b in final):
                print(f"{'*'+b:^10}|",end='')
            else:
                print(f"{b:^10}|",end='')
            for x in range(len(simbol)):
                print(f"{table[a*len(simbol)+x]:^10}|",end='')
            print()
    print('\nQuintuple:\nQ = {ε,',end='')
    state_temp = list(state)
    for a,b in enumerate(list_removed):
        if(b in state_temp):
            state_temp.remove(b)
    print(*state_temp,sep=',',end='}\n')
    print(f'Σ = {set(simbol)}')
    print(f'Start state = {state[0]}')
    print(f'Final state = {set(final)}')
    print(f'Delta : ')
    for a,b in enumerate(state):
        if(b not in list_removed):
            for c,d in enumerate(simbol):
                print(f"δ({b:<10},{d}) {'=':^5} {table[a*len(simbol)+c]:>10}")
    # print('Final state : ',end='')
    # print(*list(set(final)),sep=',',end='\n')

def find_counter(a,b): #mencari letak index segitiga bawah menggunakan baris,kolom
        return sum(arange(1,a)) + b

def cek_simbol(state1,state2,simbols,table,state,sectable): #cek simbol untuk state
    simbol = simbols     
    for b in simbol:
        #Karna make metode find_counter, perlu diketahui bahwa index state2 tidak boleh melebihi state1 karna di tabel segitiga kebawah, state1 pasti memiliki kotak sebanyak state1 itu sendiri.
        if(state.index(table[state.index(state1)*2+simbol.index(b)])<state.index(table[state.index(state2)*len(simbol)+simbol.index(b)])):
            x,y = state1,state2
            state2,state1=x,y
        #Ketika state1 == state2, kondisi tidak valid karna tidak bisa mengecek diri sendiri.
        if((table[state.index(state1)*len(simbol)+simbol.index(b)]==table[state.index(state2)*len(simbol)+simbol.index(b)])):
            continue
        if(sectable[find_counter(state.index(table[state.index(state1)*len(simbol)+simbol.index(b)]),state.index(table[state.index(state2)*len(simbol)+simbol.index(b)]))]!=-1):
            return b
    return -1

def iteration(state,final,table,simbol): #iterasi
    panjang = sum(arange(1,len(state)))
    sectable = [-1 for x in range(panjang)]
    ada_ubah = True
    counter = 0
    for a in range(1,len(state)): #iterasi pertama untuk mencari epsilon
        for b in range(a):
            if((state[a] in final and state[b] not in final) or (state[a] not in final and state[b] in final)):
                sectable[counter] = 'ε'
            counter+=1

    while(ada_ubah): #iterasi selanjutnya untuk mencari simbol-simbol pada segitiga bawah
        ada_ubah = False
        counter = 0
        for a in range(1,len(state)):
            for b in range(a):
                if(sectable[counter]==-1 and (cek_simbol(state[a],state[b],simbol,table,state,sectable)!=-1)):
                    sectable[counter]=cek_simbol(state[a],state[b],simbol,table,state,sectable)
                    ada_ubah = True
                counter+=1
    return remove_duplicate(state,table,sectable,final,simbol)

def remove_duplicate(state,table,sectable,final,simbol): #menghapus state duplikat
    list_removed = []
    for x in range(len(sectable)): #meminimisasi state
        if(sectable[x]==-1):
            a,b = find_ab(x+1)
            if(b<a):
                b,a = a,b
            temp = state[a]
            state[a] = str(state[a] + '/' + state[b])
            for x,y in enumerate(table): #minimisasi state pada table
                if(y==state[b] or y==temp):
                    table[x] = state[a]
            list_removed.append(state[b])
            for x,y in enumerate(final): #minimisasi state pada final
                if(y==state[b] or y==temp):
                    final[x] = state[a]

    for x in range(len(state)): #menghapus state duplikat
        for y in range(len(state)):
            if(x==y):
                continue
            if(state[x].find(state[y])!=-1):
                if(state[y] not in list_removed):
                    if((table[x*len(simbol)]==table[y*len(simbol)]) and (table[x*len(simbol)+1]==table[y*len(simbol)+1])):
                        list_removed.append(state[y])
    return print_table(state,table,list_removed,final,simbol),print_segitigabawah(state,sectable)

def print_segitigabawah(state,sectable): #print segitiga bawah
    counter=0         
    for a in range(1,len(state)):
        for _ in range(a):
            print(sectable[counter], end = ' ')
            counter+=1
        print()

#List untuk menyimpan bahasa yang ada
list_bahasa = []
list_bahasa.append(Bahasa('L1',['q0','q1','q2','q3','q4'],['q1','q2','q2','q3','q2','q4','q3','q3','q4','q4'],['q3','q4'],[0,1]))
list_bahasa.append(Bahasa('L2',['q0','q1','q2','q3','q4','q5'],['q1','q2','q2','q3','q2','q4','q3','q3','q4','q4','q5','q4'],['q3','q4'],[0,1]))
list_bahasa.append(Bahasa('L3',['q0','q1','q2','q3','q4','q5'],['q1','q2','q3','q4','q4','q3','q5','q5','q5','q5','q5','q5'],['q2','q1','q5'],[0,1]))

def pilmenu(): #Pilihan menu
    system('cls')
    print("Menu Program DFA\n")
    for a in range(len(list_bahasa)):
        if(a<3):
            print(f'{a+1}. {list_bahasa[a].name} pada OASE')
        else:
            print(f'{a+1}. {list_bahasa[a].name} inputan user')
    print(f'{len(list_bahasa)+1}. Masukkan diagram baru')
    cek_func = int(input("Pilihan : "))
    if(cek_func<len(list_bahasa)+1):
        system('cls')
        print('Sebelum minimisasi :')
        simpan_state,simpan_table,simpan_final = list(list_bahasa[cek_func-1].state),list(list_bahasa[cek_func-1].table),list(list_bahasa[cek_func-1].final) #Simpan state,table dan final karna saat iterasi, mereka diubah dan setelah print quintuple, harus dikembalikan seperti semula agar tidak terjadi bug
        print_table(simpan_state,simpan_table,[],simpan_final,list_bahasa[cek_func-1].simbols)
        print('\nSetelah minimisasi :')
        iteration(list_bahasa[cek_func-1].state,list_bahasa[cek_func-1].final,list_bahasa[cek_func-1].table,list_bahasa[cek_func-1].simbols)
        list_bahasa[cek_func-1].change_stable(simpan_state,simpan_table,simpan_final) #mengembalikan state,table dan final ke kondisi semula
    elif(cek_func==len(list_bahasa)+1):
        print('\nPenambahan minimisasi DFA baru')
        nama_bahasa = str(input('Masukkan nama bahasa : ')) #User input nama bahasa
        berapa_state = int(input('Masukkan jumlah state yang ada : ')) #User input jumlah state
        lstate = []
        for x in range(berapa_state):
            print(f'State ke {x+1}: ',end='') #User input state state
            lstate.append(str(input()))
        lsimbol = [x for x in input('Masukkan list simbol (dipisah dengan koma) : ').split(',')] #User input simbol yang dipisahkan dengan koma
        ltable = []
        for y in range(len(lstate)):
            for z in range(len(lsimbol)):
                print(f'Hubungan {lstate[y]} simbol {lsimbol[z]} : ',end='') #User input hubungan state dengan simbol simbolnya
                ltable.append(str(input()))
        banyak_finalstate = int(input('Masukkan jumlah final state : ')) #User input jumlah final state
        lfinal = []
        for x in range(banyak_finalstate):
            lfinal.append(str(input(f'Masukkan final state ke-{x+1}: '))) #User memasukkan final final state yang ada
        list_bahasa.append(Bahasa(nama_bahasa,lstate,ltable,lfinal,lsimbol)) #Buat class sesuai dengan deskripsi user
        print('\n Bahasa Telah Terbuat!\n Ulangi untuk menggunakan!\n')
  
    print("\nApakah ingin mengulang?\n1. Yes\n2. No\n")
    x = int(input("Pilihan : "))
    if(x==1):
        pilmenu()

pilmenu()