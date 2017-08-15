import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pickle
with open('firefox-bot/config/iframe.txt', 'r') as loginInfo:
    newName = loginInfo.readline()
    newName = newName.rstrip()
    
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
stats = load_obj('firefox-bot/statistics/' + newName)
print(stats)
v = stats['vouchers']
spins = v/5
wheelItems = ('skillBoat', 'superCase', 'superBoat', 'legendary')
y_pos = np.arange(len(wheelItems))
width=(1/2.5)

for index, item in enumerate(wheelItems):
    plt.bar(index, stats[item], width, label=item + ' ' + str(round((stats[item]/spins)*100, 3)) + '%')
    if stats[item] and item != 'skill':
        print(item, '1 out of ', round(spins/stats[item]), ' spins')
        
plt.legend(loc='best')
plt.xticks(y_pos, wheelItems)
plt.ylabel('total collected')
plt.xlabel('items')
plt.title('totalSpins: ' + str(int(spins)))
plt.show()
