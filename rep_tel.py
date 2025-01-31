from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def menu():
    """renvoie la page html du menu"""
    return render_template("menu.html")


@app.route('/ajout_num', methods=["get","post"])
def ajout_num():
    """renvoie la page html d'ajout du contact"""
    if request.method== "POST": #lorsque le nom a été entré par l'utilisateur
        x= request.form["nom"]
        y= request.form["numtel"]
        if len(recherchenum())>0: #le numéro existe déja
            return render_template("ajout_num_non.html", numtel=y) #renvoi à la page pour la présence du numero
        else:
            ajout() #ajout du contact dans la table
            return render_template("ajout_num_fait.html", numtel=y, nom=x)  #renvoie à la nouvelle page html de confirmation de l'ajout avec les 2 variables numtel et nom

    else:
        return render_template("ajout_num.html") #reste sur la page si aucun nom n'est entré


@app.route('/recherche_num', methods=['GET', 'POST'])
def recherche_num():
    """renvoie la page html pour effectuer une recherche"""
    if request.method== "POST": #lorsque le nom a été entré par l'utilisateur
        z= request.form["nomrecherche"]
        numtrouve =recherche()
        print("le numéro trouvé est :",numtrouve)
        #print(type(numtrouve))
        #print("long",len(numtrouve))
        if len(numtrouve)>0: #le contact se trouve dans la table
            return render_template("recherche_num_oui.html", nomrecherche=z,numtrouve=numtrouve) #renvoie à la nouvelle page html de confirmation de l'ajout avec les 2 variables nomrecherche et numtrouve

        else: #aucun contact ne correspoond au nom cherché
            return render_template("recherche_num_non.html", nomrecherche=z)
    else:
        return render_template("recherche_num.html") #reste sur la page si aucun nom n'est entré

@app.route('/recherche_num/supp_num/<nom>/<num>')
def supp_num(nom,num):
    """renvoie la page html de suppression de contact
    nom de type str : nom du contact à supprimer
    num de type int : numéro du dernier contact ayant le nom 'nom' """
    print("nom à supp",nom)
    print("numero à supp",num)
    if request.method== "GET":
        #print(nom)
        #print(num)
        supp(nom,num)
        return render_template("supp_num_fait.html") #renvoie à la nouvelle page html de confirmation de la suppression

    else:
        return render_template("recherche_num_oui.html")


######ne fonctionne pas ...#######
@app.route('/recherche_num/modif_num/<nom1>', methods=["get","post"])
def modif_num(nom1):
    """renvoie la page html pour modifier un contact de la table Contact
    nom1 de type str : nom du contact à modifier"""
    #print("avant",nom1)
    #nomrecherche=nom1
    #print(nomrecherche)
    #print(request.method)

    if request.method== "POST":#lorsque le nouveau numéro a été entré par l'utilisateur
        print("mm")
        print(nom1)
        m= request.form["nouvnum"]
        print(m)
        modif(nom1)
        #modification du contact dans la table

        return render_template("modif_num_conf.html", nouvnum=m, nom1=nomrecherche)  #renvoie à la nouvelle page html de confirmation du changement

    else:
        #return render_template("modif_num.html", nom=nom1) #reste sur la page si aucun nom n'est entré
        print("get retour")
        #if len(nom1)==0:
        #    print("rien")
        #else :
        #    print("oui")
        #modif_num(nom1)
        return render_template("modif_num.html", nom1=nom1) #reste sur la page si aucun nom n'est entré
        #return render_template("/recherche_num/modif_num/<nom1>", nom1=nom1) #reste sur la page si aucun nom n'est entré


@app.route('/tous_contacts')
def tous_contacts():
    """renvoie la page html affichant les 10 premiers contacts de l'annuaire"""
    contenu=tous() #liste contenant les tuples d'identifiant, de nom et numero de chaque contact
    #print(type)
    print("contenu en liste",contenu)
    #for i in range(len(contenu)):
    #    return render_template("tous_contacts.html",contenu=(contenu[i][0], contenu[i][1], contenu[i][2]))

    #id =[]
    #nom=[]
    #num=[]
    #for i in range(len(contenu)):
    #    id.append(contenu[i][0])
    #    nom.append(contenu[i][1])
    #    num.append(contenu[i][2])

    return render_template("tous_contacts.html",contenu=contenu)

############################################################################################################################################################################################################################################################################################
import sqlite3

def ajout():
    """ajoute un contact à la table Contact"""
    conn = sqlite3.connect('repertoire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, numero TEXT)")   #crée un table Contact avec 2 attributs : nom et numero

    y= request.form["numtel"]
    x= request.form["nom"]
    x=x.lower() #transforme le nom entré en minuscule pour éviter les problèmes liés aux majuscules
    data = (x,y)
    cur.execute("INSERT INTO Contact(nom, numero) VALUES(?, ?)", data)

    conn.commit()
    cur.close()
    conn.close()


def recherchenum():
    """vérifie si le numéro est déjà pris
    renvoie la liste de la recherche"""
    conn = sqlite3.connect('repertoire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, numero TEXT)")   #crée un table Contact avec 2 attributs : nom et numero

    y= request.form["numtel"]
    la=(y,)
    cur.execute('SELECT * FROM Contact WHERE numero = ?',la) #voir si le numero existe deja
    liste = cur.fetchall()
    #print(liste)
    return liste
    conn.commit()

    cur.close()
    conn.close()


def recherche():
    """recherche un contact dans la table Contact
    renvoie le numéro trouvé"""
    conn = sqlite3.connect('repertoire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, numero TEXT)")   #crée un table Contact avec 2 attributs : nom et numero

    z= request.form["nomrecherche"]
    z=z.lower() #si une majuscule est entrée elle est transformée en lettre minuscule
    #print("le nom à chercher est ", z)
    recherche = (z,)
    cur.execute('SELECT numero FROM Contact WHERE nom = ?', recherche)
    liste = cur.fetchall()
    print(liste)
    #print(type(liste))
    #print(liste[0][0])
    if len(liste)>0: #le contact existe
        liste = str(liste[-1][0]) #le numéro choisi est le denrier de la liste, le denrier entré dans la table
        #print(liste)
    return liste

    conn.commit()
    cur.close()
    conn.close()

def supp(nom,num):
    """supprime un contact de la table le nom recherché
    nom de type str : nom recherché à supprimer
    num de type int : numéro du dernier contact ayant comme nom 'nom' """
    conn = sqlite3.connect('repertoire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, numero TEXT)")   #crée un table Contact avec 2 attributs : nom et numero
    #print("maj",nom)
    nom=nom.lower() #le nom entré est mis en minuscule
    #print("minu",nom)
    #print(num)
    suppr = (nom,num)
    cur.execute('DELETE FROM Contact WHERE nom = ? AND numero = ?', suppr)

    conn.commit()
    cur.close()
    conn.close()

def modif(nom):
    """modifie un contact de la table Contact
    nom de type str : nom recherché à modifier"""
    conn = sqlite3.connect('repertoire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, numero TEXT)")   #crée un table Contact avec 2 attributs : nom et numero
    print("maj",nom)
    nom=nom.lower()
    print("min",nom)
    m= request.form["nouvnum"]
    print(m)
    data = (m,nom)
    cur.execute('UPDATE Contact SET numero = ? WHERE nom = ?', data)
    conn.commit()


    cur.close()
    conn.close()


def tous():
    """selectionne tous les contact de la table Contact
    renvoie le contenu de la table sous forme de liste"""
    conn = sqlite3.connect('repertoire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, numero TEXT)")   #crée un table Contact avec 2 attributs : nom et numero

    cur.execute('SELECT * FROM Contact')
    liste = cur.fetchall()
    #print(liste)
    #print(type(liste))
    #print(liste[0][0])
    for i in range(len(liste)):
        print(liste[i][0], liste[i][1], liste[i][2])
    print()
    cur.execute('SELECT count (*) FROM Contact') #permet de connaitre le nombre de contact que contient la table
    comb = cur.fetchall()
    comb=comb[0][0]
    print("il y a",comb,"contacts")
    #for i in range (comb):

    return liste

    conn.commit()
    cur.close()
    conn.close()


app.run(debug=False,port=5001)
