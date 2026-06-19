import pulp
def resolver_red(puertos_necesarios=494, ancho_necesario=3800, energia_max=700):  
  prob = pulp.LpProblem("Universidad_Min_Costo", pulp.LpMinimize)

    x1 = pulp.LpVariable("Switches", lowBound=0, cat='Integer')   
 x2 = pulp.LpVariable("Routers", lowBound=0, cat='Integer')    
x3 = pulp.LpVariable("Servidores", lowBound=0, cat='Integer')

    prob += 65*x1 + 150*x2 + 1200*x3, "Costo_Total"

    prob += 24*x1 + 4*x2 >= puertos_necesarios, "Puertos"   
 prob += 500*x2 + 1000*x3 >= ancho_necesario, "AnchoBanda"   
 prob += 15*x1 + 20*x2 + 180*x3 <= energia_max, "Energia"   
 prob += x2 <= 3, "MaxRouters"    prob += x3 >= 1, "MinServidores"
    prob.solve(pulp.PULP_CBC_CMD(msg=1))

    if pulp.LpStatus[prob.status] == 'Optimal':   

     print(f"\nCosto mínimo: USD ${pulp.value(prob.objective):.2f}")      
  print(f"Switches 24p: {int(x1.varValue)}")      
  print(f"Routers ONT: {int(x2.varValue)}")      
  print(f"Servidores 1U: {int(x3.varValue)}")       
 return int(x1.varValue), int(x2.varValue), int(x3.varValue)  
  
else:       
 print(f"\nNo hay solución factible. Estado: {pulp.LpStatus[prob.status]}")     
   print("Probá aumentar energia_max o reducir requerimientos")     
   return None
if __name__ == "__main__":    
print("=== OPTIMIZADOR RED UNIVERSIDAD ===")   
 resolver_red()