file = open('config/iframe.txt','w')
print('Only run this file to set or change name and iframe of bot')
name = input("enter account name: ")
iframe = input("enter account iframe: ")
file.write(name + '\n')
file.write(iframe + '\n')
file.close() 
print('Done.')
