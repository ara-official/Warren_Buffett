########################################
# reference page
# https://wikidocs.net/4761
# https://nittaku.tistory.com/117

########################################


import matplotlib.pyplot as plt

########################################
# graph
fig = plt.figure()

행 = 2
열 = 2

sub_1 = fig.add_subplot(행, 열, 1) # 행, 열, 번째
sub_2 = fig.add_subplot(행, 열, 2)
sub_3 = fig.add_subplot(행, 열, 3)
sub_4 = fig.add_subplot(행, 열, 4)

sub_1.title.set_text('price')
sub_2.title.set_text('shares')

########################################

########################################
# data
stocks = [
    {'name':'samsung', 'price':50000, 'cur_price':45000, 'shares':10,},
    {'name':'hynix', 'price':90000, 'cur_price':100000, 'shares':1,},
]

list_name = []
list_price = []
list_shares = []

for i in range(len(stocks)):
    dic = stocks[i]
    list_name.append(dic['name'])
    list_price.append(dic['price'])
    list_shares.append(dic['shares'])
########################################

########################################
# view graph

# sub_1.plot(list_name, list_price)
sub_1.bar(list_name, list_price)
# sub_1.xlabel('name')
# sub_1.ylabel('price')
sub_2.bar(list_name, list_shares)
# plt.xlabel('name')
# plt.ylabel('price')
# # plt.plot(x_axis_name, y_axis)
# plt.plot(x_axis, y_axis, z_axis)
plt.show()
########################################
