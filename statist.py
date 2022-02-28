def media(list):
    if len(list)==0:
        return(0.0)
    media=0.0
    for x in list:
        media+=float(x)
    media/=float(len(list))
    return(media)

def varianza(list):
    if len(list)==0:
        return(0.0)
    med=media(list)
    var=0.0
    for x in list:
        var+=pow((float(x)-med),2.0)
    var/=float(len(list))
    return(var)

def varianza_stima(list):
    if len(list)==0:
        return(0.0)
    med=media(list)
    var=0.0
    for x in list:
        var+=pow((float(x)-med),2.0)
    var/=float((len(list))-1)#- 1 per stima
    return(var)

def media_var(list):
    #ottimizza il procedimento di calcolo integrando il calcolo
    #della media e della varianza
    if len(list)==0:
        return(0.0,0.0)
    media=0.0
    for x in list:
        media+=float(x)
    med=media/float(len(list))
    var=0.0
    for x in list:
        var+=pow((float(x)-med),2.0)
    var/=float(len(list))
    return(med,var)

def media_var_stima(list):
    #come sopra ma usa la stima della varianza
    #ottimizza il procedimento di calcolo integrando il calcolo
    #della media e della varianza
    if len(list)==0:
        return(0.0,0.0)
    media=0.0
    for x in list:
        media+=float(x)
    med=media/float(len(list))
    var=0.0
    for x in list:
        var+=pow((float(x)-med),2.0)
    var/=(float(len(list))-1)#- 1 per stima
    return(med,var)

def coov(list1,list2):
    med1=media(list1)
    med2=media(list2)
    coov=0.0
    for x in range(0,len(list1)):
        coov+=(float(list1[x])-med1)*(float(list2[x])-med2)
    coov/=float(len(list1))
    return(coov)

def r(vettx,vetty):
    """" r - Bravais Pearson (x,y)"""
    med1,var1=media_var(vettx)
    med2,var2=media_var(vetty)
    coov=0.0
    for x in range(0,len(vettx)):
        coov+=(float(vettx[x])-med1)*(float(vetty[x])-med2)
    coov/=float(len(vettx))
    if var1*var2<>0:
        r=coov/(pow(var1,0.5)*pow(var2,0.5))
    else:
        r=1
    return(r)

def a_b(vettx,vetty):
    """ritorna a e b coefficenti della retta di reg: Y=a+bX"""
    b=coov(vettx,vetty)/varianza(vettx)
    a=media(vetty)-b*media(vettx)
    return(a,b)

def a_b_var_stima(vettx,vetty):
    #come sopra ma usa la stima della varianza
    """ritorna a e b coefficenti della retta di reg: Y=a+bX"""
    b=coov(vettx,vetty)/varianza_stima(vettx)
    a=media(vetty)-b*media(vettx)
    return(a,b)
