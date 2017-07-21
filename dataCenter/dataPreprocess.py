import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def main():
    total = {'skillBoat' : 0, 'superCase' : 0, 'superBoat' : 0, 'skill' : 0, 'legendary' : 0,  'vouchers' : 0, 'draws' : 0, 'super' : 0}
    dctItems = ('skillBoat', 'superCase', 'superBoat', 'skill', 'legendary', 'vouchers', 'draws', 'super')
    fileName = 'chrome-'
    fileNames = []
    for x in range(1, 9):
        fileNames.append('C:/Users/email/Desktop/wheel/' + fileName + str(x) + '/statistics/wheel' + str(x))
    for file in fileNames:
        dct = load_obj(file)
        print(file)
        for item in dctItems:
            total[item] += dct[item]
    print(total)
    save_obj(total, 'stats')
main()
