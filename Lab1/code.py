import pulp

problem = pulp.LpProblem("LP_Problem", pulp.LpMinimize)

Pv=50
Ch=0.8
ARP=1.3
MRP=2
StandardP=1800
OverP=2.5
UnderP=4
D=[2100, 1900, 1600, 1500, 1550, 1400, 1250, 1700, 2200, 2300, 2100, 1950]

P = [pulp.LpVariable(f"P{i}", lowBound=0) for i in range(0, 13)]
A = [pulp.LpVariable(f"A{i}", lowBound=0) for i in range(0, 13)]
MAX_P1 = [pulp.LpVariable(f"MAX_P1_{i}", lowBound=0) for i in range(0, 13)]
MAX_P2 = [pulp.LpVariable(f"MAX_P2_{i}", lowBound=0) for i in range(0, 13)]
MAX_SP1 = [pulp.LpVariable(f"MAX_SP1_{i}", lowBound=0) for i in range(0, 13)]
MAX_SP2 = [pulp.LpVariable(f"MAX_SP2_{i}", lowBound=0) for i in range(0, 13)]

def custom_function(A,P,MAX_P1,MAX_P2,MAX_SP1,MAX_SP2):
    _return=A[0]-A[0]
    for i in range(1,13):
        _return+= Pv*P[i]+Ch*A[i]+ARP*MAX_P1[i]+MRP*MAX_P2[i]+OverP*MAX_SP1[i]+UnderP*MAX_SP2[i]
    return _return

objective = custom_function(A,P,MAX_P1,MAX_P2,MAX_SP1,MAX_SP2) 

problem += objective, "Objective"

constraints=[
    A[0]==700,
    P[0]==1600
]
for i in range(1,13):
    constraints.append(A[i-1]+P[i] >= D[i-1])
    constraints.append(A[i] == A[i-1] + P[i] - D[i-1])
    constraints.append(MAX_P1[i]>=0)
    constraints.append(MAX_P2[i]>=0)
    constraints.append(MAX_SP1[i]>=0)
    constraints.append(MAX_SP2[i]>=0)
    constraints.append(MAX_P1[i]>= P[i]-P[i-1])
    constraints.append(MAX_P2[i]>= -P[i]+P[i-1])
    constraints.append(MAX_SP1[i]>= P[i]-StandardP)
    constraints.append(MAX_SP2[i]>= -P[i]+StandardP)

for i, constraint in enumerate(constraints):
    problem += constraint, f"Constraint{i+1}"
problem.solve()
for var in problem.variables():
    print(f"{var.name}: {var.varValue}")
print(f"Optimal Objective Value: {pulp.value(problem.objective)}")