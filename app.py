from flask import Flask, render_template, request, redirect, url_for,session,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nenoyam/@98'
app.config['MYSQL_DB'] = 'gsrdv'

app.secret_key="my secret key"
mysql = MySQL(app)
@app.route("/")
def home():
    flash('Bienvenue sur notre site web !')
    return render_template('accueil.html')
# Page d'inscription pour les utilisateurs
@app.route('/inscription_patient', methods=['GET', 'POST'])
def inscription_patient():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        adresse=request.form['adresse']
        passw = request.form['passw']
        confirm_pass1=request.form['confrm_pass1']
        sexe = request.form['sexe']
        tel = request.form['tel']
        
        if passw !=confirm_pass1:
            return render_template('inscription_patient.html',erreur="les deux mots de passe sont differentes")
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM patient WHERE adresse_email=%s",(email,))
        patients=cur1.fetchone()
        if patients:
            error = 'Cette adresse email est deja utilise'
            return render_template('inscription_medecin.html',error=error)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patient(nom, prenom, adresse,num_tel,adresse_email, mot_de_passe,sexe) VALUES (%s, %s, %s, %s,%s,%s,%s)", (nom, prenom,adresse,tel,email,passw,sexe))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login_patient'))
    return render_template('inscription_patient.html')
@app.route('/login_patient', methods=['GET', 'POST'])
def login_patient():
    if request.method == 'POST':
        nom_pa = request.form['nom_pa']
        mot_de_passe = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM patient WHERE adresse_email=%s AND mot_de_passe=%s", (nom_pa, mot_de_passe))
        patient = cur.fetchone()
        cur.close()
        if patient:
            session['nom_patient']=nom_pa
            return redirect(url_for('chercher'))
        else:
            print("Mot de passe incorrect")
            return render_template('login_patient.html', erreur='Adresse e-mail ou mot de passe incorrect')
    return render_template('login_patient.html')

# Page d'inscription pour les médecins
@app.route('/inscription_medecin', methods=['GET', 'POST'])
def inscription_medecin():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        specialite = request.form['specialite']
        tel=request.form['telephone']
        sexe=request.form['sexe']
        adresse=request.form['adresse']
        passwd = request.form['passw']
        confirm_pass2=request.form['confrm_pass2']
        if passwd !=confirm_pass2:
            return render_template('inscription_medecin.html',erreur="les deux mots de passe sont differentes")
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM medecin WHERE adresse_email=%s",(email,))
        medecin=cur1.fetchone()
        if medecin:
            error = 'Cette adresse email est deja utilise'
            return render_template('inscription_medecin.html',error=error)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medecin(nom,specialite,adresse,num_tel,adresse_email,mot_de_passe,sexe,prenom) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)", (nom, specialite,adresse,tel,email,passwd,sexe,prenom))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login_medecin'))
    return render_template('inscription_medecin.html')

# Page de connexion pour les médecins
@app.route('/login_medecin', methods=['GET', 'POST'])
def login_medecin():
    if request.method == 'POST':
        nom_med = request.form['nom_med']
        mot_de_passe = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM medecin WHERE adresse_email=%s AND mot_de_passe=%s", (nom_med, mot_de_passe))
        medecin = cur.fetchone()
        cur.close()
        if medecin:
            session['nom_medecin']=nom_med
            return redirect(url_for('profil_medecin'))
        else:
            return render_template('login_medecin.html', erreur='Adresse e-mail ou mot de passe incorrect')
    return render_template("login_medecin.html")

@app.route('/profil_medecin')
def profil_medecin():
    nom_m=session.get('nom_medecin',None)
    if nom_m is not None:
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM medecin WHERE adresse_email=%s", (nom_m,))
        result1 = cur1.fetchone()
        id_medecin=result1[0]
        cur1.close()
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM disponibilite WHERE id_medecin=%s", (id_medecin,))
        disponibilites = cur2.fetchall()
        cur2.close()
        if result1 :
            if disponibilites:
                return render_template('profil_medecin.html', name=result1[1], specialite=result1[2],adresse=result1[3],tel=result1[4],email=result1[5],prenom=result1[8], disponibilites=disponibilites,d="dispo")
            else:
                return render_template('profil_medecin.html', name=result1[1], specialite=result1[2],adresse=result1[3],tel=result1[4],email=result1[5],prenom=result1[8],d="")
    else:
       return redirect(url_for('home'))
@app.route('/deconnecter_medecin')
def deconnexion_medecin():
    session.pop("nom_medecin",None)
    return redirect(url_for('home'))
@app.route('/deconnecter_admin')
def deconnexion_admin():
    session.pop("email",None)
    return redirect(url_for('home'))
@app.route('/deconnecter_patient')
def deconnexion_patient():
    session.pop("nom_patient",None)
    session.pop('name_med',None)
    return redirect(url_for('home'))

@app.route('/chercher' ,methods=['POST','GET'] )
def chercher():
    nom_p=session.get('nom_patient',None)
    if nom_p is not None:
        if request.method=='POST':
            nom=request.form['nom']
            prenom=request.form['prenom']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM medecin WHERE nom=%s and prenom=%s", (nom,prenom))
            medecin = cur.fetchone()
            
            cur.close()
            if medecin:
                session['nom_med']=nom
                id_medecin=medecin[0]
                cur3 = mysql.connection.cursor()
                cur3.execute("SELECT * FROM disponibilite WHERE id_medecin=%s", (id_medecin,))
                result3 = cur3.fetchall()
                cur3.close()
                if result3:
                    return render_template('detail_medecin.html',medecin=medecin,dispo=result3,d="dispo")
                else:
                    return render_template('detail_medecin.html',medecin=medecin,d="") 
            else:
                return render_template('chercher_medecin.html', erreur='Aucun medecin avec ces informations')
        else:
            return render_template('chercher_medecin.html')
    else:
         return redirect(url_for('home'))
@app.route('/ajouter_dispo')
def ajouter_dispo():
    nom_m=session.get('nom_medecin',None)
    if nom_m is not None:
        return render_template('ajouter_disponibilite.html')
    else:
       return redirect(url_for('home'))
    
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nom_m=session.get('nom_medecin',None)
        if nom_m is not None:
            date = request.form['date']
            heure_d = request.form['hd']
            heure_f= request.form['hf']
            cur = mysql.connection.cursor()
            print("1")
            cur.execute("SELECT * FROM medecin WHERE adresse_email=%s", (nom_m,))
            result = cur.fetchone()
            id_medecin=result[0]
            cur.close()
            print("2")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO disponibilite(jour,heure_debut,heure_fin,id_medecin) VALUES (%s, %s, %s, %s)", (date, heure_d,heure_f,id_medecin))
            print("3")
            mysql.connection.commit()
            cur.close()
            print("4")
            return redirect(url_for('profil_medecin'))
        else:
            return redirect(url_for('home'))

@app.route('/prendreRDV', methods=['GET', 'POST'])
def prendreRDV():
    if request.method == 'POST':
        nom_p=session.get('nom_patient',None)
        if nom_p is not None:
            date=request.form['date']
            heure=request.form['heur']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM patient WHERE adresse_email=%s", (nom_p,))
            result = cur.fetchone()
            id_patient=result[0]
            print("1")
            cur.close()
            cur2 = mysql.connection.cursor()
            nom_med=session.get('nom_med')
            cur2.execute("SELECT * FROM medecin WHERE nom=%s", (nom_med,))
            result2 = cur2.fetchone()
            id_medecin=result2[0]
            cur2.close()
            cur3 = mysql.connection.cursor()
            cur3.execute("SELECT * FROM disponibilite WHERE id_medecin=%s", (id_medecin,))
            result3 = cur3.fetchone()
            id_dispo=result3[0]
            cur3.close()
            cur4 = mysql.connection.cursor()
            cur4.execute("INSERT INTO rendezvous(jour,heure,id_patient,id_medecin,id_dispo) VALUES (%s, %s, %s, %s,%s)", (date, heure,id_patient,id_medecin,id_dispo))
            mysql.connection.commit()
            cur4.close()
            return redirect(url_for('rdv'))
        else:
            return redirect(url_for('home'))
    else:
        return render_template('prendreRDV.html')

@app.route('/rdv')
def rdv():
        nom_p=session.get('nom_patient',None)
        if nom_p is not None:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM patient WHERE adresse_email=%s", (nom_p,))
            result = cur.fetchone()
            id_patient=result[0]
            cur2 = mysql.connection.cursor()
            query = "SELECT r.jour, r.heure, m.nom,m.prenom FROM rendezvous r JOIN medecin m ON r.id_medecin = m.id_medecin WHERE r.id_patient = %s"
            cur2.execute(query, (id_patient,))
            rdv = cur2.fetchall()
            if rdv:
                return render_template('mesRDV.html',rdv=rdv)
            else:
                return render_template('mesRDV.html')

        else:
            return redirect(url_for('home'))
@app.route('/listes_rdv')
def listes_rdv():
        nom_m=session.get('nom_medecin',None)
        if nom_m is not None:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM medecin WHERE adresse_email=%s", (nom_m,))
            result = cur.fetchone()
            id_medecin=result[0]
            cur2 = mysql.connection.cursor()
            query = "SELECT r.jour, r.heure, p.nom, p.prenom,p.num_tel,p.adresse_email FROM rendezvous r JOIN patient p ON r.id_patient = p.id_patient WHERE r.id_medecin = %s"
            cur2.execute(query, (id_medecin,))
            rdv = cur2.fetchall()
            if rdv:
                return render_template('listesRDV.html',rdv=rdv)
            else:
                    return render_template('listesRDV.html')

        else:
            return redirect(url_for('home'))

@app.route('/inscription_admin',methods=['post','get'])
def inscription_admin():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        passw = request.form['passw']
        confirm_pass= request.form['confrm_pass1']
        if passw !=confirm_pass:
            return render_template('inscription_admin.html',erreur="les deux mots de passe sont differentes")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admin(nom, prenom,email, mot_de_passe) VALUES (%s, %s, %s, %s)", (nom, prenom,email,passw))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login_admin'))
    else:
        return render_template('inscription_admin.html')


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        passw = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE email=%s AND mot_de_passe=%s", (email,passw))
        admin=cur.fetchone()
        if admin:
            session['email']=email
            return render_template('accueil_admin.html')
         
        else:
            return render_template('login_admin.html', erreur='Adresse e-mail ou mot de passe incorrect')
    else:
        return render_template('login_admin.html')
    

@app.route('/gerer_medecins')
def gerer_medecins():
        email_ad=session.get('email',None)
        if email_ad is not None:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM medecin")
            medecins=cur.fetchall()
            cur.close()
            if medecins:
                return render_template("gerer_medecins.html",medecins=medecins)
            else:
                return render_template("accueil_admin.html")
        else:
            return redirect(url_for('home'))

@app.route('/gerer_patients')
def gerer_patients():
        email_ad=session.get('email',None)
        if email_ad is not None:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM patient")
            patients=cur.fetchall()
            if patients:
                return render_template("gerer_patients.html",patients=patients)
            else:
                return render_template("accueil_admin.html")
        else:
            return redirect(url_for('home'))

@app.route('/supprimer/<string:id>')
def supprimer(id):
    email_ad=session.get('email',None)
    if email_ad is not None:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM medecin WHERE id_medecin=%s",id)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('gerer_medecins'))
    else:
        return redirect(url_for('home'))
    
@app.route('/supprimer_patient/<string:id>')
def supprimer_patient(id):
    email_ad=session.get('email',None)
    if email_ad is not None:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM patient WHERE id_patient=%s",id)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('gerer_patients'))
    else:
        return redirect(url_for('home'))