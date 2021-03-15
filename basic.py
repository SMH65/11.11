import matplotlib.pyplot as plt
import numpy as np
import csv

x=[]
y=[]
f = open('dir\data.csv')
rdr = csv.reader(f)

for line in rdr:
    if len(line)==2: # line에서 각각의 리스트가 있는데 공백이 포함되어 있다. 이를 없애기 위해 리스트의 길이를 잰다.
        x.append(line[0])
        y.append(line[1])
        # print(type(x[0])) = > str 이다. 그래프로 잘 그리기 위해서는 실수로 변환해주어야 한다.

del x[0]
del y[0] #맨 앞의 문자를 빼주었다.

# 실수로 변환하는 과정

# enumerate(x) => (0, x[0]), (1, x[1]), ... 이렇게 indexing 따라서 i에는 0, 1, 2, ...이 들어가고, x에는 x[0], x[1], x[2], ...가 들어간다.
for i, val in enumerate(x):
   x[i] = float(x[i])

   #print(z) # 처음에는 float (x) 로 썼는데 x안에 있는 어떤 값은 리스트면 안된다고 한다. 그래서 val를 사용하였다.

for i, val in enumerate(y):
    y[i] = float(y[i])

f.close()

# 변수를 선언하고 초기값을 0으로 한다.
avg1 = 0
avg2 = 0

# 기울기를 구하기 위해 샘플링할 구간의 길이를 선언해준다.
sam_len = 10

# 구간의 길이에 해당하는 데이터 값을 모두 더해준다.
for i in range(sam_len):
    avg1 = avg1 + y[i]
for i in range(int((len(y)-sam_len)/2), int((len(y))/2)):
    avg2 = avg2 + y[i]

# 더한 데이터 값을 구간의 길이로 나누어 평균을 구해준다.
avg1 = avg1/sam_len
avg2 = avg2/sam_len

# 평균의 차를 구간의 길이로 나누어 기울기를 구한다.
slope = (avg2-avg1)/((len(y)/2)-sam_len)

data = []

# y = a*x + c => y = c로 만들어야 하므로 모든 y 성분에 -a*x에 해당하는 값을 빼준다.
# zip(x, y) => (x[0], y[0]), (x[1], y[1]), (x[2], y[2]), ... i => x[0], x[1], x[2], ... j => y[0], y[1], y[2]
for i, j in zip(x, y):
    data.append(j - slope*i)


plt.plot(x, data, color='orange')
plt.plot(x, y)
plt.show()

