from qiskit import QuantumCircuit,transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

n=4
stocks=[]
returns=[]
risks=[]
for i in range(n):
    l=input("enter name of stock")
    stocks.append(l)
    k=int(input("enter return of stock "))
    returns.append(k)
    p=int(input("enter risk of stock"))
    risks.append(p)
#Checking type of investor 
print("Investor types:")
print("1: Aggressive investor")
print("2: Balanced investor")
print("3: Conservative investor")

o=int(input("Choose the type of investor you are and select it's index number"))
if o==1:
    return_weight=0.8
    risk_weight=0.2
elif o==2:
    return_weight=0.5
    risk_weight=0.5
else:
    return_weight=0.3
    risk_weight=0.7
scores=[]
for i,j in zip(returns,risks):
    score=return_weight*i-risk_weight*j
    scores.append(score)
qc=QuantumCircuit(4,4)
for i in range(4):
    qc.h(i)
gamma=0.3
beta=0.5
for i in range(4):
    qc.rz(-2*gamma*scores[i],i)
for i in range(4):
    qc.rx(2*beta,i)
qc.measure(range(4),range(4))
print("Quantum Circuit:\n")
print(qc.draw())

simulator=AerSimulator()
results=simulator.run(qc,shots=1024).result()
count=results.get_counts()
print("Portfolio possiblities:")
print(count)
plot_histogram(count)
plt.title("Results")
plt.show()

# Best possible solution

best=max(count,key=count.get)
print("best portfolio state found:")
print(best)

total_return=0
total_risk=0
for i in range(4):
    if best[3-1]=="1":
        print("Buy stock",stocks[i])
        total_return+=returns[i]
        total_risk+=risks[i]
print("Portfolio summary:\n")
print("Total returns:",total_return)
print("Total risk :",total_risk)

final_score=(total_return*return_weight-total_risk*risk_weight)
print("Weighted final score =\n")
print(round(final_score,2))
