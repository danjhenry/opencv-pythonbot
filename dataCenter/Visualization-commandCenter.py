import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pickle

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
stats = load_obj('stats')
print(stats)
d = stats['draws']
comItems = ('skill', 'super')
y_pos = np.arange(len(comItems))
width=(1/5)
for index, item in enumerate(comItems):
    plt.bar(index, stats[item], width, label=item + ' ' + str(round((stats[item]/d)*100, 3)) + '%')
            #' frequency: 1 / ' + str(round(spins/stats[item])))
    if(stats[item]):
        print(item, '1 out of ', round(d/stats[item]), ' draws')
plt.legend(loc='best')
plt.xticks(y_pos, comItems)
plt.ylabel('total collected')
plt.xlabel('items')
plt.title('totalDraws: ' + str(int(d)))
plt.show()
