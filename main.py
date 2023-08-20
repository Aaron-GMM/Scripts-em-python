from datetime import datetime
#ultilizando variaveis globais em escopo local
x = 10;
def global_sum(y):
 global x
 x=15
 return x+y

print(x)

print(global_sum(20))

print(x)

#pegando horario
print(datetime.now());



