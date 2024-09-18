#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3.7
 
import os
from glob import iglob
from shutil import copy2
 
##############################################################################
def modifini(fichier, entete="en-GB."):
    """modifie le nom du fichier en retirant l'en-tête indiqué
    """
    # sépare le chemin et le nom de fichier
    chemin, nom = os.path.split(fichier)
    # calcule le nouveau nom
    if nom.startswith(entete):
        # modifie le nom
        nom = nom[len(entete):] # supprime l'en-tête
        # recalcule le nouveau nom du fichier avec son chemin   
        fichier = os.path.join(chemin, nom)
    # et retourne le nom (modifié ou pas) du fichier avec son chemin
    return fichier
 
##############################################################################
def sauveselect(repsrce, repdest, motifs=['*'], modifie=None, affiche=False):
    """Trouve (recherche récursive) les fichiers du répertoire source repsrce 
       satisfaisant l'un des motifs 'wildcard' de la liste motifs,
       et les recopie dans le répertoire destination 'repdest' seulement si:
       - le fichier source n'existe pas dans la destination,
       - ou le fichier source est plus récent que le fichier destination
       Si modifie=unefonction, modifie le fichier en appelant unefonction(...)
       Si affiche=True: affiche les opérations faites en console
       Retourne le nombre de fichiers trouvés + copiés, ainsi que les erreurs
    """
    # normalisation des répertoires
    repsrce = os.path.abspath(os.path.expanduser(repsrce))
    lgrepsrce = len(repsrce) # longueur du chemin du répertoire source
    repdest = os.path.abspath(os.path.expanduser(repdest))
 
    # traitement des recopies
    erreurs = []
    nsrce, ndest = 0, 0
    for motif in motifs:
        for ficsrce in iglob(os.path.join(repsrce, "**", motif), recursive=True):
 
            if os.path.isfile(ficsrce): # on ne s'intéresse qu'aux fichiers
 
                nsrce += 1 # nouveau fichier source trouvé
                ficdest = repdest + ficsrce[lgrepsrce:] # => fichier destination
 
                # modifie le nom de fichier destination si c'est demandé
                if modifie is not None:
                    ficdest = modifie(ficdest)
 
                rep = os.path.dirname(ficdest) # répertoire du fichier destination
                if not os.path.exists(rep):
                    # crée le ou les répertoire(s) manquant(s) de la destination
                    os.makedirs(rep)
 
                if not os.path.exists(ficdest):
                    # fichier destination absent => recopie du fichier source
                    try:
                        copy2(ficsrce, ficdest)
                        ndest += 1
                        if affiche: print("Recopie fichier absent de la destination:", ficsrce)
                    except Exception as msgerr:
                        erreurs.append(str(msgerr))    
                else:
                    # ici, on sait que le fichier destination existe déjà
                    if os.path.getmtime(ficsrce) > os.path.getmtime(ficdest):         
                        # fichier source plus récent => recopie
                        try:
                            copy2(ficsrce, ficdest)
                            ndest += 1
                            if affiche: print("Recopie fichier plus récent que la destination:", ficsrce)
                        except Exception as msgerr:
                            erreurs.append(str(msgerr))    
 
    return nsrce, ndest, erreurs
# répertoire source
repsrce = r"C:\Users\yanni\Documents\GitHub\flexicontent-cck"
 
# répertoire destination
repdest = r"C:\Users\yanni\Documents\GitHub\flexicontent-translations"
 
# liste de motifs de type "wildcard"
motifs = ["*.ini"]
 
# appel de la sauvegarde sélective
nsrce, ndest, erreurs = sauveselect(repsrce, repdest, motifs, modifie=modifini, affiche=True)
 
print("nombre de fichiers trouvés:", nsrce)
print("nombre de fichiers mis à jour", ndest)
if len(erreurs)==0:
    print("Aucune erreur")
else:
    print("Erreurs:", len(erreurs))
    for erreur in erreurs:
        print(erreur)
 
