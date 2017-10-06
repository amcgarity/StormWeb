# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 18:53:23 2016

@author: arthur,fengwei
"""

from stormwise_grnacr_benefits_and_bounds import upper_bounds
from stormwise_grnacr_benefits_and_bounds import benefit_slopes

def generate_ampl_dat_file(inYamlDoc,fDict,kjdict,kdict,Kgdict,Krdict):
    ampl = ""   # string containing ampl code to be returned when filled
    upperBounds = upper_bounds(inYamlDoc,kjdict,kdict,Kgdict,Krdict)
    benefitSlopes = benefit_slopes(inYamlDoc,kjdict,kdict)
    I = inYamlDoc['I']
    J = inYamlDoc['J']
    K = kdict
    T = inYamlDoc['T']
    Ta = inYamlDoc['Ta']
    Ts = inYamlDoc['Ts']
    Kg = Kgdict
    Kr = Krdict
    fg = inYamlDoc['fg']
    fr = inYamlDoc['fr']
    weighting = inYamlDoc['weighting']
    KONJ = kjdict

    sets = ['I','J','K','T','Ta','Ts','Kg','Kr','weighting'] 
    # I = zone, J = landuse, K = GItype, T = benefit
    # Ta = co-benefits, Ts = SW benefits, Kg = ground installation, Kr = roof installation
    # weighting = weightings retrieved from VoAH stakeholder meeting

    for s in sets:  
        ampl = ampl + "set %s := " % s 
        if s != 'K' and s != 'Kg' and s != 'Kr':
            x = inYamlDoc[s]
        elif s == 'K':
            x = kdict
        elif s == 'Kg':
            x = Kgdict
        elif s == 'Kr':
            x = Krdict
        for h in sorted(x):
            ampl += "%s " % h
        ampl += ";\n"        
    setsonset = {'KONJ': ('K','J')}
    for s in sorted(setsonset):
        s1 = setsonset[s][1]
        x = inYamlDoc[s1]
        for h in sorted(x):
            ampl = ampl + "set %s[%s] := " % (s,h)
            elements = kdict
            if elements == None:
                value = "" 
                ampl = ampl + "%s;\n" % value 
            else:
                for g in sorted(elements):
                    value = g
                    ampl += "%s " % value
                ampl += " ;\n"

    # process parameters: w1, w, 1_min, 2_range, scale... :
    

    ampl += "param w1: "
    w1= inYamlDoc['w1']
    for t in sorted(Ta):
        ampl += "%s " % t
    ampl += " :=\n"
    for w in sorted(weighting):
        ampl += "  %s " % (w)
        for t in sorted(Ta):
                ampl += "  %10.2f" % w1[w][t]
        ampl += "\n"
    ampl += ";\n"   
    
    # process parameters: w
#    ampl += "param w:= "
#    h= inYamlDoc['w']
#    for t in sorted(Ta):
#        ampl += " %s " % t 
#        ampl += " %4.2f " % h[t] 
#    ampl += ";\n"
    
    # process parameters: area
    ampl += "param area: "
    area= inYamlDoc['area']
    for j in sorted(J):
        ampl += "%s " % j
    ampl += " :=\n"
    for i in sorted(I):
        ampl += "  %s " % (i)
        for j in sorted(J):
                ampl += "  %6.2f " % area[j][i]
        ampl += "\n"
    ampl += ";\n"   
    
    ampl += "param fg: "
    fg = inYamlDoc['fg']
    for j in sorted(J):
        ampl += "%s " % j
    ampl += " :=\n"
    for i in sorted(I):
        ampl += "  %s " % (i)
        for j in sorted(J):
            ampl += "  %6.2f" % fg[j][i]
        ampl += "\n"
    ampl += ";\n"

    ampl += "param fr: "
    fr = inYamlDoc['fr']
    for j in sorted(J):
        ampl += "%s " % j
    ampl += " :=\n"
    for i in sorted(I):
        ampl += "  %s " % (i)
        for j in sorted(J):
            ampl += "  %6.2f" % fr[j][i]
        ampl += "\n"
    ampl += ";\n"

    # process parameters: w, 1_min, 2_range, scale... :
    ampl += "param 1_min:= "
    h= inYamlDoc['1_min']
    for t in sorted(T):
        ampl += " %s " % t 
        ampl += " %4.2f " % h[t] 
    ampl += ";\n"
    
    ampl += "param 2_range:= "
    h= inYamlDoc['2_range']
    for t in sorted(T):
        ampl += " %s " % t 
        ampl += " %4.2f " % h[t] 
    ampl += ";\n"       

    # process parameters:  scale... :
    ampl += "param scale:= "
    h= inYamlDoc['scale']
    for t in sorted(T):
        ampl += " %s " % t 
        ampl += " %6.3f " % h[t] 
    ampl += ";\n"         
 
    # process parameters:  f
    
    ampl += "param f:"
    f= fDict
    for k in sorted(K):
        ampl += "%s " % k
    ampl += " :=\n"
    for i in sorted(I):
        for j in sorted(J):
            ampl += "  %s %s" % (i,j)
            if KONJ[j] != None:
                for k in sorted(K):
                    if k in KONJ[j]:
                        if '1_headwaters' in f:
                            ampl += "  %10.2f" % f[i][k][j]
                        else:    
                            ampl += "  %10.2f" % f[k][j][i]
                    else:
                        ampl += "  %10.2f" % 0.0
            else:
                for k in sorted(K):
                    ampl += "  %10s" % '.'
            ampl += "\n"
    ampl += ";\n"
    
    # process parameters:  cost
    ampl += "param cost:"
    cost= inYamlDoc['cost']
    for k in sorted(K):
        ampl += "%s " % k
    ampl += " :=\n"
    for j in sorted(J):
        ampl += "  %s " % (j)
        for k in sorted(K):
                ampl += "  %10.2f" % cost[k][j]
        ampl += "\n"
    ampl += ";\n"   

    # process upper bound data:
    ampl += "param u:"
    for k in sorted(K):
        ampl += "%s " % k
    ampl += " :=\n"
    for i in sorted(I):
        for j in sorted(J):
            ampl += "  %s %s" % (i,j)
            if KONJ[j] != None:
                for k in sorted(K):
                    if k in KONJ[j]:
                        ampl += "  %10.2f" % upperBounds[i][j][k]
                    else:
                        ampl += "  %10.2f" % 0.0
            else:
                for k in sorted(K):
                    ampl += "  %10s" % '.'
            ampl += "\n"
    ampl += ";\n"
        
    # process benefit slope data:
    ampl += "param s: "
    for t in sorted(T):
        ampl += "%s " % t
    ampl += " :=\n"
    for i in sorted(I):
        for j in sorted(J):
          
            if KONJ[j] != None:
                for k in sorted(K):
                    if k in KONJ[j]:
                        ampl += "  %s %s %s" % (i,j,k)
                        for t in sorted(T):
                            ampl += "  %15.14f" % benefitSlopes[i][j][k][t]
                        ampl += "\n"

    ampl += ";\n"      
    return ampl

def generate_ampl_benefit_file(inYamlBenefitDoc,budget):
    ampl = ''
    benefitLowerBounds = inYamlBenefitDoc['benefitLowerBounds']  #['benefitLowerBounds']
    benefitWeight = inYamlBenefitDoc['weights']  #['benefitLowerBounds']

    ampl += "data;\n"
    ampl += "param bud := %20.10f\n" % budget
    ampl += ";\n"
    ampl += "param Bmin :=\n"
    for t in sorted(benefitLowerBounds):
        ampl += "    %s    %20.10f\n" % (t,benefitLowerBounds[t])
    ampl += ";\n"
    ampl += "\nparam w :=\n"
    for t in sorted(benefitWeight):
        ampl += "    %s    %20.10f\n" % (t,benefitWeight[t])
    ampl += ";\n"
    ampl += "model;\n"
    return ampl

'''

'''