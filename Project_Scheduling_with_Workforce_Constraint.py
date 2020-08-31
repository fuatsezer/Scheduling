import pandas as pd
import numpy as np
#%% Variable identification
Np=2
W1=4
W2=8
df=pd.DataFrame({"jobs":range(1,6),
                 "pesimistic_time":np.array([5,7,8,4,3]),
                 "most_likely_time":np.array([3,6,6,3,2]),
                 "optimistic_time":np.array([2,4,4,1,1]),
                 "W1j":np.array([2,1,3,1,2]),
                 "W2j":np.array([3,0,4,0,3]),
                 "predeccessor":np.array([[],[],[],[1],[2,3]]),
                 "basladi":False,
                 "bitti":False,
                 "starting_time":-5,
                 "finishing_time":10000})
#%% calculate mean and variance of processing time
df["mean_time"]=0
df["variance_time"]=0.0
for i in range(0,len(df)):
    df["mean_time"][i] =(df["optimistic_time"][i]+4*df["most_likely_time"][i]+df["pesimistic_time"][i])/6
    df["variance_time"][i] = (df["pesimistic_time"][i]-df["optimistic_time"][i])/6
#%% calculate makespawn
Cmax_list =[]
for i in range(0,len(df)):
    if df["predeccessor"][i] != []:
        for  z in range(0,len(df["predeccessor"][i])):
            sayi=df["predeccessor"][i][z]

            if df["predeccessor"][sayi-1] == []:
                
                Cmax_list.append(df["mean_time"][i] + df["mean_time"][sayi-1])
            else:
                for  d in range(0,len(df["predeccessor"][sayi-1])):
                    sayi2=df["predeccessor"][sayi-1][d]
                    if df["predeccessor"][sayi2-1] == []:
                        Cmax_list.append(df["mean_time"][i]+df["mean_time"][sayi-1] + df["mean_time"][sayi2-1])
Cmax = max(Cmax_list)
#%% calculate prob
from scipy import stats
gun = int(input("Gün sayısını giriniz"))
z_değeri = (gun-Cmax)/np.sqrt(df["variance_time"].sum())
p_values = 1- stats.norm.sf(z_değeri )
print("Projenin {} günden önce bitme olasılığı: % {:.2f}".format(gun,p_values*100))
#%%
for t in range(0,Cmax+1):
    # bittiyi etkinleştirme
    for i in range(0,len(df)):
        if df["finishing_time"][i] == t:
            df["bitti"][i] = True
            
            
        
    # t zamanında işlenebilecek işlerin bulunması
    islenebilecek_isler_index =[]
    for j in range(0,len(df)):
        if (df["predeccessor"][j] == []) & (df["basladi"][j] == False):
            islenebilecek_isler_index.append(j)
            
        elif (df["basladi"][j] == False):
            mylist=[]
            for i in range(0,len(df["predeccessor"][j])):
                mylist.append(df["bitti"][i])
            if (all(mylist) == True) :
                
                islenebilecek_isler_index.append(j)
    # w1 ve W2 kontrol etme
    w1_total=0
    w2_total=0
    for f in range(0,len(df)):
        if(df["basladi"][f] == True) & (df["bitti"][f]==False):
            w1_total += df["W1j"][f]
            w2_total += df["W2j"][f]
        for i in islenebilecek_isler_index:
            w1_total += df["W1j"][i]
            w2_total += df["W2j"][i]
        if (W1 >=w1_total) & (W2 >=w2_total):
            for j in islenebilecek_isler_index:
                print("a")
                df["basladi"][j] = True
                df["starting_time"][j] = t
                df["starting_time"][j] = t
                df["finishing_time"][j] = t+ df["mean_time"][j]
        else:
            w1_total=0
            w2_total=0
            for f in range(0,len(df)):
                if(df["basladi"][f] == True) & (df["bitti"][f]==False):
                    w1_total += df["W1j"][f]
                    w2_total += df["W2j"][f]
            if (W1 >=w1_total) & (W2 >=w2_total):
                index_list=[]
                print("İş indeksi {} olanlar kısıtları aşıyor".format(islenebilecek_isler_index))
                kac = int(input("Kaç iş seçeceksiniz: "))
                for _ in range(0,kac):
                    sayi = int(input("Sayıyı giriniz: "))
                    index_list.append(sayi)
        
                for s in index_list:
                    w1_total += df["W1j"][s]
                    w2_total += df["W2j"][s]
                if (W1 >=w1_total) & (W2 >=w2_total):
                    for d in index_list:
                        print("b")
                        df["basladi"][d] = True
                        df["starting_time"][d] = t
                        df["starting_time"][d] = t
                        df["finishing_time"][d] = t+ df["mean_time"][d]
                
            
        
        
            
            
            
            
        
    
 
    
       