# code for computing StormWISE benefit slopes and upper bounds
# plus code for converting benefit units based on file "convert_benefits.yaml"
# Copyright Arthur E. McGarity, 2016

from tools import format_dict_as_strings
from tools import multiply_dict_by_constant

def convert_benefit_units(benDict,benefitConvertUnits):
    dct = deepcopy(benDict)
    for t in sorted(dct):   # the first level is the benefit type
        dct[t] *= benefitConvertUnits[t]
    return dct

def format_and_convert_benefit_dict(dct,formatStr,benefitConvertUnits,benefitUnits):
    oneDimDict = False
    for t in sorted(dct):
        if type(dct[t]) is dict:
            multiply_dict_by_constant(dct[t],benefitConvertUnits[t])
            #formatWithUnits = formatStr + benefitUnits[t]
            format_dict_as_strings(dct[t],formatStr)
        else:
            oneDimDict = True
            dct[t] *= benefitConvertUnits[t]
    if oneDimDict:
        format_dict_as_strings(dct,formatStr)
    displayDict = {}
    for t in sorted(dct):
        key = t+' ('+benefitUnits[t]+')'
        displayDict[key] = dct[t]
    return(displayDict)

def benefit_slopes(inYamlDoc,kjdict,kdict):
        I = inYamlDoc['I']  # subwatershed index
        J = inYamlDoc['J']  # landuse index
        K = kdict # Gi type index
        KONJ = kjdict # GI types [k] on Landuse [j]
        T = inYamlDoc['T']  # GI benefit index
        cost = inYamlDoc['cost']  # cost of GI type [k] on landuse [j]
        export = inYamlDoc['export']  # the export coefficient of GI benefit [t] on land use [j]
        eta = inYamlDoc['eta']  # benefit generation efficiency [t] of GI [k] in watershed [i]
        s = {}  # will be a dictionary of dictionaries
        for i in I:  # generate decision variable dictionary
            jDict = {}
            for j in J: 
                kDict = {}
                if KONJ[j] != None:
                    for k in K:                   
                        tDict = {}
                        if k in KONJ[j]:
                            for t in T:
                                tDict[t] = eta[t][k][i]*export[t][j]/float(cost[k][j])
                        else:
                            for t in T:
                                tDict[t] = 0.0
                        kDict[k] = tDict
                else:
                    for k in K:
                        tDict = {}
                        for t in T:
                            tDict[t] = 0.0
                        kDict[k] = tDict                 
                jDict[j] = kDict
            s[i] = jDict
        return s

def upper_bounds(inYamlDoc,kjdict,kdict,Kgdict,Krdict):
        I = inYamlDoc['I']
        J = inYamlDoc['J']
        K = kdict
        Kg= Kgdict
        Kr=Krdict
        KONJ = kjdict
        cost = inYamlDoc['cost']
        fr = inYamlDoc['fr'] #change to fg and fr
        fg = inYamlDoc['fg']
        area = inYamlDoc['area']
        u = {}  # will be a dictionary of dictionaries
        for i in I:  # generate decision variable dictionary
            jDict = {}
            for j in J: 
                kDict = {}
                if KONJ[j] != None:
                    for k in K:                   
                        if k in Kg:
                            kDict[k] = cost[k][j]*fg[j][i]*area[j][i]	
                        elif k in Kr:
                            kDict[k] = cost[k][j]*fr[j][i]*area[j][i]
                        else: 
                            kDict[k] = 0.0
                else:
                    for k in K:
                        kDict[k] = 0.0
                jDict[j] = kDict
            u[i] = jDict    
        return u
