from tkinter import * 
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw
import json
import os
import keyboard
import time


with open('data.json', 'r') as fichier:
    data = json.load(fichier)


def suppp():
    for compte in data:
        if compte["pseudo"] == identifiant_connecter:
            os.remove(compte["pp"])
            compte["pp"] = ""

            with open('data.json', 'w') as fichier:
                json.dump(data, fichier, indent=4)

            profil()


def modifpp():
    newpp = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.gif")])

    if newpp:
        image = Image.open(newpp)

        # Enregistrez l'image dans le répertoire de votre choix
        chemin_de_sauvegarde = os.path.join("pp", f"pp_{identifiant_connecter}.png")

        if chemin_de_sauvegarde:
            image.save(chemin_de_sauvegarde)
            print(f"L'image a été enregistrée sous {chemin_de_sauvegarde}")

            for compte in data:
                if compte["pseudo"] == identifiant_connecter:
                    compte["pp"] = f"pp/pp_{identifiant_connecter}.png"
            
                    print(f"La valeur 'pp' du compte '{identifiant_connecter}' a été modifiée.")

                    with open('data.json', 'w') as fichier:
                        json.dump(data, fichier, indent=4)
                    
                    while os.path.exists(chemin_de_sauvegarde) != True:
                        print()
                        
                    profil()


def supcompte():
    index_a_supprimer = None
    for i, personne in enumerate(data):
        if personne["pseudo"] == identifiant_connecter:
            if personne["pp"] != "":
                os.remove(personne["pp"])
            index_a_supprimer = i
            data.pop(index_a_supprimer)

            with open('data.json', 'w') as fichier:
                json.dump(data, fichier, indent=4)

            page_connection()


def newcompte():
    identifiant_incription = identifiant.get()
    mdp_incription = mdp.get()
    deja_utiliser = False

    if identifiant_incription != "" and mdp_incription != "":
        for compte in data:
            if compte["pseudo"] == identifiant_incription:
                label = Label(fenetre, text="Identifiant déjà utiliser", fg="red")
                label.pack()
                deja_utiliser = True

        if deja_utiliser == False:
            new_compte = {
                "pseudo": identifiant_incription,
                "mdp": mdp_incription,
                "pp": "",
                "followers": [],
                "suivis" : []
            }   

            data.append(new_compte)
            with open('data.json', 'w') as fichier:
                json.dump(data, fichier, indent=4)

            page_connection()
                    
    else:
        label = Label(fenetre, text="Veuiller remplir tout les champs", fg="red")
        label.pack()


def page_inscription():
    fenetre.title('Inscription')

    global identifiant, mdp, var_afficher

    for widget in fenetre.winfo_children():
        widget.destroy()

    label = Label(fenetre, text="Identifiant :")
    label.pack()
    identifiant = Entry(fenetre, width=30)
    identifiant.pack()


    label = Label(fenetre, text="Mot de passe :")
    label.pack()
    mdp = Entry(fenetre, show="*", width=30)
    mdp.pack()

    var_afficher = BooleanVar()
    case_a_cocher = Checkbutton(fenetre, text="Afficher le mot de passe", variable=var_afficher, command=voir_mdp)
    case_a_cocher.pack()

    Button(text="S'inscrire", command=newcompte).pack(pady=5)
    Button(text="Annuler", command=page_connection).pack(pady=5)


def add_suivi():
    compte["suivis"].append(compte["pseudo"])

    with open('data.json', 'w') as fichier:
        json.dump(data, fichier, indent=4)


def page_decouvrir():
    fenetre.title('Découvrir')

    global img

    for widget in fenetre.winfo_children():
        widget.destroy()
    
    label = Label(fenetre, text="Connecter a " + identifiant_connecter)
    label.pack()

    Button(text='Profil', command=profil).pack(pady=5)

    image_list = []

    for compte in data:
        if compte["pseudo"] != identifiant_connecter:

            if compte["pp"] == "":
                pp = "pp/compte.png"
            else:
                pp = compte["pp"]

            image_pillow = Image.open(pp)
            largeur, hauteur = image_pillow.size
            taille_max = min(largeur, hauteur)
            image_carree = Image.new("RGBA", (taille_max, taille_max), (255, 255, 255, 0))
            image_carree.paste(image_pillow, ((taille_max - largeur) // 2, (taille_max - hauteur) // 2))
            masque = Image.new("L", (taille_max, taille_max), 0)
            draw = ImageDraw.Draw(masque)
            draw.ellipse((0, 0, taille_max, taille_max), fill=255)
            image_circulaire = Image.new("RGBA", (taille_max, taille_max))
            image_circulaire.paste(image_carree, (0, 0), masque)
            img = ImageTk.PhotoImage(image_circulaire.resize((50, 50), Image.ANTIALIAS))
            
            # Ajoutez l'objet ImageTk.PhotoImage à la liste
            image_list.append(img)

            label_image = Label(fenetre, image=img)
            label_image.image = img  # Maintenir une référence à l'objet PhotoImage
            label_image.pack()

            Label(fenetre, text=compte["pseudo"] + " " + str(len(compte["followers"])) + " followers").pack()

            Button(text='Suivre', command=add_suivi).pack(pady=5)


def profil():
    fenetre.title('Profil')

    global img

    followers = len(compte["followers"])
    suivis = len(compte["suivis"])

    for widget in fenetre.winfo_children():
        widget.destroy()

    if compte["pp"] == "":
        pp = "pp/compte.png"
    else:
        pp = compte["pp"]

    image_pillow = Image.open(pp)
    largeur, hauteur = image_pillow.size
    taille_max = min(largeur, hauteur)
    image_carree = Image.new("RGBA", (taille_max, taille_max), (255, 255, 255, 0))
    image_carree.paste(image_pillow, ((taille_max - largeur) // 2, (taille_max - hauteur) // 2))
    masque = Image.new("L", (taille_max, taille_max), 0)
    draw = ImageDraw.Draw(masque)
    draw.ellipse((0, 0, taille_max, taille_max), fill=255)
    image_circulaire = Image.new("RGBA", (taille_max, taille_max))
    image_circulaire.paste(image_carree, (0, 0), masque)
    img = ImageTk.PhotoImage(image_circulaire.resize((50, 50), Image.ANTIALIAS))
    Label(fenetre, image=img).pack()

    Button(text='Modifier la photo de profil', command=modifpp).pack(pady=5)
    Button(text='Suprimer la photo de profil', command=suppp).pack(pady=5)

    label = Label(fenetre, text=str(followers) + " followers")
    label.pack()

    label = Label(fenetre, text=str(suivis) + " suivi(e)s")
    label.pack()

    Button(text='Découvrir', command=page_decouvrir).pack(pady=5)

    label = Label(fenetre, text="Identifiant : " + identifiant_connecter)
    label.pack()

    label = Label(fenetre, text="Mots de passe : " + mdp_connecter)
    label.pack()

    Button(text='Se déconnecter', command=page_connection).pack(pady=5)
    Button(text='Suprimer mon compte', command=supcompte).pack(pady=5)


def connecter():
    global identifiant_connecter, mdp_connecter, compte

    identifiant_connecter = identifiant.get()
    mdp_connecter = mdp.get()

    for compte in data:
        if compte["pseudo"] == identifiant_connecter and compte["mdp"] == mdp_connecter:
            for widget in fenetre.winfo_children():
                widget.destroy()
            profil()
            fenetre.unbind("<KeyPress>", on_key_press)
            return

    label = Label(fenetre, text="Identifiant ou Mot de passe incorrect", fg="red")
    label.pack()


def voir_mdp():
    global var_afficher

    if var_afficher.get():
        mdp.config(show="")
    else:
        mdp.config(show="*")


def on_key_press(event):
    if event.keysym == "Return":  # Vérifie si la touche pressée est "Entrée"
        connecter()


def page_connection():
    fenetre.title('Connection')

    global identifiant, mdp, var_afficher

    for widget in fenetre.winfo_children():
        widget.destroy()

    label = Label(fenetre, text="Identifiant :")
    label.pack()
    identifiant = Entry(fenetre, width=30)
    identifiant.pack()


    label = Label(fenetre, text="Mot de passe :")
    label.pack()
    mdp = Entry(fenetre, show="*", width=30)
    mdp.pack()

    var_afficher = BooleanVar()
    case_a_cocher = Checkbutton(fenetre, text="Afficher le mot de passe", variable=var_afficher, command=voir_mdp)
    case_a_cocher.pack()

    Button(text='Se connecter', command=connecter).pack(pady=5)
    Button(text="Crée un compte", command=page_inscription).pack(pady=5)
    
    fenetre.bind("<KeyPress>", on_key_press)


fenetre = Tk()
fenetre.geometry('300x300')
page_connection()
fenetre.iconbitmap('icon.ico')
fenetre.mainloop()