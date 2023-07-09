f = open("catalog.txt", "r")
#print(f.read())

#list of gym items
fit_items=["treadmill","lifting","weights","cycle","rowing machine","exercise ball","dumbell","pushup bar","leg machine","skipping rope"]


lines=f.readlines()

d1={}
d2={}

for item in fit_items:
    for line in lines:
        gym_equip=line.strip().split(',')
        if item==gym_equip[0]:
            print("match found for item: ",item)
            category=gym_equip[1]
            quantity=gym_equip[2]
            d1.update({item:category})
            d2.update({item:quantity})
    

    
            
        
