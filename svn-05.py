
#------------------------------------------------------------------------------
#lecture du zip en coroutine
#renvoie une liste dont le remierelement est une liste aaa mm jj hh min + numero d'ordre de la minute
#ensuite on a open close high low
#debut : yyyy mm jj 
#------------------------------------------------------------------------------
def scanfile(debut,longueur):
    import zipfile    
    fh = open(nomfich, 'rb')
    z = zipfile.ZipFile(fh) # classe lisant le zipdanzs le fichier ouvert
    lstjour=0
    
    minute =0
    mindebut=0
    encore =0
    
    quadvalues=[]
    
    with z.open(nomfichshort) as zz:
        for eachLine in zz:
            encore = 1
            minute = minute+1
            
            splitLine = eachLine.split(";")
            annee = int(splitLine[0][0:4])
            mois=int(splitLine[0][4:6])
            jour=int(splitLine[0][6:8])
            heure=int(splitLine[0][9:11])
            minutes=int(splitLine[0][11:13])
            
            #test si on est dans les bonnes dates
            if debut[0] > annee : 
                continue   
            
            gooddate =False
            if debut[0] < annee :
                gooddate = True
            
            
            if debut[0] == annee and  debut[1] < mois :
                gooddate =True
            
            if debut[0] == annee and   debut[1] == mois and debut[2] <= jour:
                gooddate =True
                
            if gooddate:
                mindebut = mindebut+1
            else:
                continue
            
            dateheure=[annee,mois,jour,heure,minutes,minute]
            
            if jour !=  lstjour:
                print mindebut, dateheure
                lstjour = jour
            
            #lu open =1 high =2 low=3 close=4
            quadvalues = [dateheure,float(splitLine[1]),\
                          float(splitLine[2]),\
                          float(splitLine[3]),\
                          float(splitLine[4])]  
            
            #print quadvalues
            
            if mindebut == longueur : #on a lu assez de nombres
                encore =0
                z.close()
                fh.close()
        
            yield encore,quadvalues
    
    #fin de la boucle car plus rien a lire
    encore =0
    z.close()
    fh.close()
    yield encore,[] #liste vide
    
print 'scanfile ok' #juste pour avoirr un petit message

#-----------------------------------------------------------------------------


from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection

from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np


paire="EURUSD"
annee=2014
#mois=4

#nomfich=".\\data\\HISTDATA_COM_ASCII_{0}_M1{1:4d}{2:02d}.zip".format(paire,annee,mois)
#nomfich2="c:\\data\\{0}_M1_{1:4d}{2:02d}.csv".format(paire,annee,mois)
#nomfichshort="DAT_ASCII_{0}_M1_{1:4d}{2:02d}.csv".format(paire,annee,mois)
#lecture d'une annee
nomfich=".\\HISTDATA_COM_ASCII_{0}_M1{1:4d}.zip".format(paire,annee)
nomfichshort="DAT_ASCII_{0}_M1_{1:4d}.csv".format(paire,annee)

print nomfich,nomfichshort

lstdata=[-1,0,0,0,0]
       

#--------------------------------------------
## dessine des courbes des signaux a et b
#--------------------------------------------
def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

#--------------------------------------------
#dessine le waterfall des yes et des no
#--------------------------------------------
def multidraw(courbesA,courbesB):

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    verts = []
    facecolor=[]
    for lacourbe in courbesA:
        xs=[]
        closepoly=[]
        for idx,X in enumerate(lacourbe):
            xs.append(idx)
            closepoly.append(0)
            xs.append(idx)
            closepoly.append(X)
            xs.append(idx+.3)
            closepoly.append(X)
            xs.append(idx+.3)
            closepoly.append(0)
        xs.append(0)
        closepoly.append(0)
            
        verts.append(list(zip(xs, closepoly)))
        facecolor.append(cc('b'))

    for lacourbe in courbesB:
        xs=[]
        closepoly=[]
        for idx,X in enumerate(lacourbe):
            xs.append(idx)
            closepoly.append(0)
            xs.append(idx)
            closepoly.append(X)
            xs.append(idx+.3)
            closepoly.append(X)
            xs.append(idx+.3)
            closepoly.append(0)
        xs.append(0)
        closepoly.append(0)
        
        verts.append(list(zip(xs, closepoly)))
        facecolor.append(cc('y'))
    
    print len(facecolor) ,len(verts)
     
    poly = PolyCollection(verts, facecolors=facecolor)
    zs = range(0,len(facecolor))
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')
    
    ax.set_xlabel('X')
    ax.set_xlim3d(0,5)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-1, len(verts))
    ax.set_zlabel('Z')
    ax.set_zlim3d(-3, 3)

    plt.show()


        

#------------------------------------------------------------------------------
#dit si une cande monte ou descend
#------------------------------------------------------------------------------
def senscandle(data):
    
    if data[1]<data[2]:
        return 1   #deb < fin : ca monte
    if data[1]>data[2] :
        return 2  #deb > fin  ; ca descend
    return 0  #deb = fin


stackpast=[[-1,0,0,0,0]]




#------------------------------------------------------------------------------
#detecte les retournements montee descente
#la detection se fait sur les 2 eme a xieme items de la stack
# car le dernier item est celui qui correspond a l'achat/vente
#------------------------------------------------------------------------------
def testrevertupdown(stackdata):
    stackdata.insert(0,['date','op','hi','lo','cl'])
    rdata = map(list,zip(*stackdata))
    stack = {d[0]:d[1:] for d in rdata}  #on en fait un dict
    del stackdata[0]  #stackpast ne doit plus s'allonger   
      

    #test une descente apres deux montees nettes : signal de depart
    
    #le dernier commence plus bas que finit le prec
    cond1 = (stack['cl'][-1] > stack['op'][-1]) 
    val1a = stack['cl'][-1]
    val1b = stack['op'][-1]
    
    # le precedent etait parti plus bas que la fin de celui d'avant et etait descendu
    #cond2 = (stack['fin'][-3] > stack['deb'][-2])  \
    #        and (stack['deb'][-2] > stack['fin'][-2])  
    cond2 = (stack['op'][-2] >= stack['cl'][-2])  
    val2a = stack['cl'][-2]
    val2b = stack['op'][-2]
    
    #celui d'avant etait une montee : commence + haut que son prec et est une montee
    #celui encore avant : idem
    #cond3 = (stack['fin'][-4] < stack['deb'][-3]) \
    #         and (stack['deb'][-3] < stack['fin'][-3])
    cond3 = (stack['op'][-3] <= stack['cl'][-3])
    val3a = stack['cl'][-3]
    val3b = stack['op'][-3]
    
    #cond4 = (stack['fin'][-5] < stack['deb'][-4]) \
    #        and (stack['deb'][-4] < stack['fin'][-4]) # ca monte
    
    cond4 = (stack['op'][-4] <= stack['cl'][-4]) # ca monte
    val4a = stack['cl'][-4]
    val4b = stack['op'][-4]
    
    return cond1 , cond2 and cond3 and cond4 

#---------------------------------
#normlise les dnnees du pattern
#---------------------------------
def normalisedata(stackdata):
    valmin = float(stackdata[-5][2])
    valmax = float(stackdata[-2][3])
    scale = 0.001 #(valmax - valmin) #/(valmax+valmin)*2
    #scale = (valmax - valmin) #/(valmax+valmin)*2
    output=[]
    for i in [-5,-4,-3,-2,-1]:
            output.append((stackdata[i][2]-valmin)/scale)
    return output

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def extractfeatures(stackdata):
    stackdata.insert(0,['date','op','hi','lo','cl'])
    rdata = map(list,zip(*stackdata))
    #[list(i) for i in zip(*stackdata)] ferait aussi la transposee
    rdict = {d[0]:d[1:] for d in rdata}  #on en fait un dict
    del stackdata[0]  #stackpast ne doit plus s'allonger   
  
    featureline=[]
    #sort les features d'avan le retournement
    featureline.append(rdict['lo'][-2] - rdict['hi'][-2]) #delta minmax
    featureline.append(rdict['op'][-2] - rdict['cl'][-2]) #delta deb fin
    featureline.append(rdict['lo'][-3] - rdict['hi'][-3]) #delta minmax
    featureline.append(rdict['op'][-3] - rdict['cl'][-3]) #delta deb fin
    featureline.append(rdict['lo'][-4] - rdict['hi'][-4]) #delta minmax
    featureline.append(rdict['op'][-4] - rdict['cl'][-4]) #delta deb fin
    featureline.append(rdict['lo'][-5] - rdict['hi'][-5]) #delta minmax
    featureline.append(rdict['op'][-5] - rdict['cl'][-5]) #delta deb fin
    
#    print "feature",stackdata,featureline
    return [i * 10000 for i in featureline] #muliply par 10000

#------------------------------------------------------------------------------
#un petit essai d'analyse triviale pour prenre une decision triviale
# on met 1 si on sort rentre plus bas qu'on est sorti avant
# retourne ladifff qui vaut 1,0 ou 1 suivant que detection a ete faite ou non
# ok qui vaut 0 tant qu'on n'a âs eu assez de donnees
# learning qui contient une ligne de learnig matrice (feature  groupe)
#------------------------------------------------------------------------------

def analyse(data):
    global lstdata,stackpast
    ladiff =0
    ok=False
    learning=[] #init bidon
    
    stackpast.append(data[:]) #ajout de la derniere valeur ds stackpast
    
    if len(stackpast)==7 :
        ok=True
        del stackpast[0]  #stackpast ne doit plus s'allonger   
        yess,detected = testrevertupdown(stackpast)
        if detected:
            if yess:
                ladiff =1
            else:
                ladiff = -1
                    
            learning=extractfeatures(stackpast)  #extraction des features du detected
            learning.extend([ladiff]) # categorie en fin de feature
        
    return ok,ladiff, learning    


#------------------------------------------------------------------------------
#plot le graph des candle de candlegraf
# et met les points de analysegraf qui contient des doublets (index,valeur) des marques a rajouter a candlegraf
#------------------------------------------------------------------------------

def plotresu(candlegraf,analysetab):
    #print entrybar
    import matplotlib.pyplot as ml

#   from matplotlib.finance import candlestick
    from matplotlib.finance import candlestick_ohlc
    import matplotlib.pyplot as plt
    
    lafig = plt.figure()
    ax1 = plt.subplot(1,1,1)
    #ax2 = plt.subplot(2,1,2)


    tabplot=[]
    X=[]
    Y=[]


    #print tabplot
    #candlestick open high low close
    candlestick_ohlc(ax1,candlegraf, width=.75, colorup='r', colordown='g')
    #yscale = ax1.get_ybound()  #renvoie le min et max de l'afficahge
    #print yscale

    for i in range(len(analysetab)):
        if analysetab[i][0]==1 :
            indx = analysetab[i][1]
            X.append(candlegraf[indx][0]) #-1 = dennier indice de la liste dateheure : minute
            #on ajoute a y le doublet yscale multiplie par 1 (=lui meme) ou 0 (vide) 
            #c'est pas ce que je voulais faire , je voulais multipler chaque point de y (des 1) par une valeur
            #mais bon ca marche un peu. il va falloir passer tout ca en traiteent listes/matrices sinon c'est moche
            Y.append([candlegraf[indx][1],candlegraf[indx][2],candlegraf[indx][3],candlegraf[indx][4]])  

    print len(X), len(Y)

    ax1.plot(X,Y,'bo')

    X=[]
    Y=[]
    for i in range(len(analysetab)):
        if analysetab[i][0]==-1 :
            indx = analysetab[i][1]
            X.append(candlegraf[indx][0])#on ajoute a y le doublet yscale multiplie par 1 (=lui meme) ou 0 (vide) 
            #c'est pas ce que je voulais faire , je voulais multipler chaque point de y (des 1) par une valeur
            #mais bon ca marche un peu. il va falloir passer tout ca en traiteent listes/matrices sinon c'est moche
            Y.append([candlegraf[indx][1],candlegraf[indx][2],candlegraf[indx][3],candlegraf[indx][4]])  

    ax1.plot(X,Y,'yo')

    plt.show()


#------------------------------------------------------------------------------
# analyse des resultats en comparant les resultats de la matrice des resultats
# learnresu contient en 0 reel 1 estimé
#------------------------------------------------------------------------------

def checkquality(learnresu):
    nbyesifyes=0
    nbyesifno=0
    nbnoifyes=0
    nbnoifno=0
    
    print "learnresu size",len(learnresu)
    for i in learnresu:
        valestim = i[1]
        valreelle = i[0]
        #print valreelle,valestim
    
        if valestim == 1 and valreelle==1:
            nbyesifyes = nbyesifyes+1
            #print "yesIFyes=",nbyesifyes
    
        if valestim == 1 and valreelle==-1:
            nbyesifno = nbyesifno+1
            #print "yesIFno=",nbyesifno
  
        if valestim == -1 and valreelle==1:
            nbnoifyes = nbnoifyes+1
            #print "noIFyes=",nbnoifyes

        if valestim == -1 and valreelle==-1:
            nbnoifno = nbnoifno+1
                #print "noIFyes=",nbnoifyes
    
    print "detect false no",nbnoifyes
    print "detect true yes",nbyesifyes
    print "detect false yes",nbyesifno
    print "detect true no ",nbnoifno
    
    print '%correct (nb yes justes sur les yes trouves) ',float(nbyesifyes)/float(nbyesifyes+nbyesifno) *100.0
    print '%detected (nb yes trouves sur les yes reels) ' , float(nbyesifyes)/float(nbyesifyes+nbnoifyes) *100.0 

    print '%correct du yes trivial (nb yes justes si on trouve que des yes) ',float(nbyesifyes)/float(nbyesifyes+nbyesifno+nbnoifno+nbnoifyes) *100.0
    
#------------------------  MAIN  ---------------------------------
datebar=[]
candlegraf=[]
analysetab=[]
learnmat=[]

minute =0
index=0

lescanfile = scanfile([annee,2,2],1000)
graphyes = []
graphno = []


while True:
#    minute = minute+1
    encore,quadvalues = lescanfile.next()
    if encore ==0:
        break
            
    ok,resu,features = analyse(quadvalues)    
    if  resu<>0 :  #pile assez grosse pour faire les features : on genere les matrices
        learnmat.append(features) #matrice des features learning
        analysetab.append([resu, index]) #liste des events detectes pour la viualisation des detections 
        if (resu ==1):
            graphyes.append(normalisedata(stackpast))
        else:
            graphno.append(normalisedata(stackpast))
 
    if ok: #on est dans l'intervalle a scanner
        #ordre ohlc 
        #on reconstruit une ligne avec 1 X et 4 valeurs
        ladate = quadvalues[0]
        #print ladate
        quadline=ladate[-1:]  #-1 : numero d'ordre de la manute 
        quadline.extend(quadvalues[1:5])
        #print quadline
        candlegraf.append(quadline) #matrice des valeurs brutes pour le graph cndles
        index= index+1

#icci on a la matrice de learning qui a son ensemble d'apprentissage et ses evenements en sortie
print "learning size = ",len(candlegraf)
print "positve size =",len([x for x in analysetab if x[0]==1])
print "negative size =",len([x for x in analysetab if x[0]==-1])

#on dessine les resultats calcules
plotresu(candlegraf,analysetab)

#on fait la waterfall des patterns trouves
multidraw(graphyes,graphno)

#on va faire les estimations

#on a la matrice de features
#print learnmat
features = [x[0:-2] for x in learnmat]
categories = [x[-1] for x in learnmat]

from sklearn import svm

#clf = svm.SVC(gamma=0.001, C=100.)
clf = svm.SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, degree=2,
              gamma='auto', kernel='rbf', max_iter=-1, probability=False, random_state=None,
              shrinking=True, tol=0.001, verbose=False)
clf.fit(features, categories)

#learnresu =[]
valtest=[]
valresu=[]

#on verifie l'efficacite du learning en recalculant les resultats estimes sur les vleurs de check
nbyesifyes = 0
nbnoifyes = 0
nbyesifno = 0

#on rescane l'ensemble de check
lescanfile = scanfile([annee,2,2],1400)

while True:
    encore,quadvalues = lescanfile.next()
    if encore ==0:
        break

    ok,resu,features = analyse(quadvalues)     #calcul des features
    if  resu<>0 :  #on a un resultat
        valtest.append(features[:-2]) #on cree une liste d'echantillons a estimer
        valresu.append(resu)
    
    if ok:
        index= index+1


valout = clf.predict(valtest) #on fait le predict sur tous les echantillons 
learnresu=zip(valresu,valout) #matrice valeur reelle, valeur estimee
print learnresu
checkquality(learnresu)

#ici il faudrait visualiser les bons et les mauvais pour voir comment ameliorer les positifs / faux positifs
