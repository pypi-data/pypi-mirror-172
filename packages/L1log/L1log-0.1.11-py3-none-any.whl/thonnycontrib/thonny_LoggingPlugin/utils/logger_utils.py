import re 
import hashlib
import getpass

def sans_commentaire_entete(s : str) -> str:
    '''Renvoie une chaîne identique à `s` mais sans les premiers
    commentaires et autres lignes blanches.

    Au cas où l'éditeur soit vide
    >>> sans_commentaire_entete('')
    ''
    
    Uniquement un en-tête
    >>> s = "\\n#sdf\\n#qsdfgt\\n#sdfghjk\\n\\t#qsdfgh\\n"
    >>> sans_commentaire_entete(s)
    ''

    Pas d'en-tête
    >>> s = "def toto():\\n\\treturn"
    >>> sans_commentaire_entete(s)
    'def toto():\\n\\treturn'
    

    Des commentaires et espacement avant un début de programme
    >>> s = "# nom prenom\\n\\n  # nom prenom\\n\\t  \\n# pouet pouet\\ndef toto():\\n\\treturn"
    >>> sans_commentaire_entete(s)
    'def toto():\\n\\treturn'
    '''
    liste_lignes = re.split('\n', s)
    i = 0
    while i < len(liste_lignes) and (liste_lignes[i].strip() == '' or liste_lignes[i].strip()[0] == '#'):
        i = i + 1
    return '\n'.join(liste_lignes[i:])    

def cut_topfile_comments(s : str) -> str:
    """
    cut the header of the file where the program begins
    """
    if not isinstance(s,str):
        return s
    return sans_commentaire_entete(s)

def cut_filename(s : str) -> str:
        """
        Cut the filename to keep only the last part, that is the name
        without the access path.

        Args : 
            s (str) the filename

        Return :
            (str) the filename cutted

        """
        try :
            return re.search("\/[^\/]*$",s).group()
        except Exception as e :
            return s

def hash_identifiant() -> str:
    '''
    Renvoie une version hachée de l'identifiant de la 
        personne connectée.
    '''
    return _hash_224_15_premiers(_get_identifiant())

def _hash_224_15_premiers(s : str) -> str:
    '''
    Code `s` avec sha224 qui renvoie une chaîne de taille 56, dont
    on ne garde que les 15 premiers caractères.

    >>> x = _hash_224_15_premiers("fg:ggvjhvkkm,: àpmiyg")
    >>> len(x)
    15
    '''
    return hashlib.sha224(bytes(s,"utf-8")).hexdigest()[:15]

def _get_identifiant() -> str:
    '''
    Renvoie l'identifiant de la personne connectée. 
    '''
    return getpass.getuser()
    
def hash_filename(s : str) -> str:
    """
    Returns a hashed name for s : its hash value.
    """
    return "file_" + _hash_224_15_premiers(s)

def remplace_nom_repertoire_ds_commande_cd(s : str) -> str:
    '''
    Remplace le nom du répertoire par une valeur hachée.

    Args :
    - s (str) : de la forme "%cd <chemin_acces_dir_travail>"

    Return : 
        (str) la même chaîne commençant par "%cd" sauf que 
    <chemin_acces_dir_travail> est remplacé par une valeur hachée.
    
    '''
    nom_repertoire = s[4:].strip()
    return "%cd " + hash_filename(nom_repertoire) + "\n"

def remplace_nom_fichier_ds_commande_Run_program(s : str) -> str:
    '''Pour une commande %Run <nom_fichier>, remplace le nom du fichier
    par une valeur hachée.

    Args :
    - s (str) : de la forme "%Run <nom_fichier>"

    Return : 
        (str) la même chaîne commençant par "%Run" sauf que 
    <nom_fichier> est remplacé par une valeur hachée.

    '''
    nom_fichier = s[5:].strip()
    return "%Run " + hash_filename(nom_fichier) + "\n"

def remplace_nom_fichier_ds_commande_Debug(s : str) -> str:
    '''Pour une commande %Debug <nom_fichier>, remplace le nom du fichier
    par une valeur hachée.

    Args :
    - s (str) : de la forme "%Debug <nom_fichier>"

    Return : 
        (str) la même chaîne commençant par "%Debug" sauf que 
    <nom_fichier> est remplacé par une valeur hachée.

    '''
    nom_fichier = s[7:].strip()
    return "%Debug " + hash_filename(nom_fichier) + "\n"


def remplace_email_par_masque(texte, char):
    '''
    Renvoie une version de `texte` dans laquelle toutes les adresses mail
    sont remplacées par des suites de `char`

    Dans un texte ne contenant qu'une adresse mail, celle-ci est remplacée. 
    >>> texte = "me@univ-lille.fr"
    >>> len(texte)
    16
    >>> nouv = remplace_email_par_masque(texte, 'X')
    >>> nouv
    'XXXXXXXXXXXXXXXX'
    >>> len(nouv)
    16

    Dans un texte contenant 2 adresses mail noyées dans le reste, celles-ci
    sont remplacées.
    >>> texte = "$$ $$ ZQEDS  mi.nebut.etu@univ-lille.fr$$$$machin@gmail.com**"
    >>> len(texte)
    61
    >>> nouv = remplace_email_par_masque(texte, '@')
    >>> len(nouv)
    61
    >>> nouv
    '$$ $$ ZQEDS  @@@@@@@@@@@@@@@@@@@@@@@@@@$$$$@@@@@@@@@@@@@@@@**'

    Pas de changement si le texte ne contient aucune adresse mail.
    >>> remplace_email_par_masque('', '@')
    ''
    >>> texte = '*%µ%$'
    >>> nouv = remplace_email_par_masque(texte, '@')
    >>> nouv == texte
    True
    '''
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.finditer(pattern, texte)
    res = ''
    i = 0
    for m in matches:
        deb = m.start() # inclus
        fin = m.end() # exclus
        res += texte[i:deb] + char*(fin-deb)
        i = fin
    if i != len(texte):
        res += texte[i:]
    return res


def remplace_commentaire_par_masque(texte, char):
    '''
    Renvoie une version de `texte` dans laquelle tous les commentaires
    sont remplacés par des suites de `char`

    Dans un texte ne contenant qu'un commentaire, celui-ci est remplacé. 
    >>> texte = "# truc"
    >>> len(texte)
    6
    >>> nouv = remplace_commentaire_par_masque(texte, 'X')
    >>> nouv
    '#XXXXX'
    >>> len(nouv)
    6

    Dans un texte contenant 2 commentaires noyés dans le reste, ceux-ci
    sont remplacés.
    >>> texte = "$$ $$# ZQEDS\\nazerty#mi.nebut.etu@univ-lille.fr\\n**"
    >>> len(texte)
    49
    >>> nouv = remplace_commentaire_par_masque(texte, '@')
    >>> len(nouv)
    49
    >>> nouv
    '$$ $$#@@@@@@\\nazerty#@@@@@@@@@@@@@@@@@@@@@@@@@@\\n**'

    Pas de changement si le texte ne contient aucune adresse mail.
    >>> remplace_commentaire_par_masque('', '@')
    ''
    >>> texte = '*%µ%$'
    >>> nouv = remplace_commentaire_par_masque(texte, '@')
    >>> nouv == texte
    True
    '''
    pattern = r'[#].*'
    matches = re.finditer(pattern, texte)
    res = ''
    i = 0
    for m in matches:
        deb = m.start() # inclus
        fin = m.end() # exclus
        res += texte[i:deb+1] + char*(fin-deb-1) # on garde le #
        i = fin
    if i != len(texte):
        res += texte[i:]
    return res

def remplace_suite_chiffres_par_masque(texte, char):
    '''
    Renvoie une version de `texte` dans laquelle toutes les suites
    de plus de 8 chiffres sont remplacées par `char`.

    Permet de capter les numéros de carte bancaire (13 à 16 chiffres) et 
    les NIP étudiants (8 chiffres).

    Dans un texte ne contenant qu'une suite de chiffres, celle-ci est remplacée. 
    >>> texte = "1234567890"
    >>> len(texte)
    10
    >>> nouv = remplace_suite_chiffres_par_masque(texte, 'X')
    >>> nouv
    'XXXXXXXXXX'
    >>> len(nouv)
    10

    Dans un texte contenant 2 suites noyées dans le reste, celles-ci
    sont remplacées.
    >>> texte = "azed3456 zaesdfg12 123456432123R4 23456543567ezdfSDF34E"
    >>> len(texte)
    55
    >>> nouv = remplace_suite_chiffres_par_masque(texte, 'X')
    >>> len(nouv)
    55
    >>> nouv
    'azed3456 zaesdfg12 XXXXXXXXXXXXR4 XXXXXXXXXXXezdfSDF34E'

    Pas de changement si le texte ne contient aucune suite.
    >>> remplace_suite_chiffres_par_masque('', '@')
    ''
    >>> texte = '*%µ%$12'
    >>> nouv = remplace_suite_chiffres_par_masque(texte, '@')
    >>> nouv == texte
    True
    '''
    pattern = r'\d{8,}'
    matches = re.finditer(pattern, texte)
    res = ''
    i = 0
    for m in matches:
        deb = m.start() # inclus
        fin = m.end() # exclus
        res += texte[i:deb] + char*(fin-deb)
        i = fin
    if i != len(texte):
        res += texte[i:]
    return res


def remplace_numero_tel_par_masque(texte, char):
    '''
    Renvoie une version de `texte` dans laquelle tous les numéros
    de tel à la française sont remplacés par une suite de `char`.

    Un numéro de tel est pour cette fonction:
    - 10 chiffres
    - possiblement découpés en 5 groupes de 2
    - possiblement par groupes de 2 séparés par des '-'
    - possiblement au format x xxx xx xx xx 
    - possiblement au format +xxx xxx xx xx xx

    Dans un texte ne contenant qu'un numero, celui-ci est remplacé. 
    >>> texte = "1234567890"
    >>> len(texte)
    10
    >>> nouv = remplace_numero_tel_par_masque(texte, 'X')
    >>> nouv
    'XXXXXXXXXX'
    >>> len(nouv)
    10

    Dans un texte contenant des numéros noyés dans le reste, celles-ci
    sont remplacées.
    >>> texte = "0000000000zerd04 50 34 03 04sdfgdsfg+123 456 33 33 33zesrgtfh0 623 23 34 45zedgfh34ze0000zesfg00000000  12-34-56-78-944"
    >>> len(texte)
    119
    >>> nouv = remplace_numero_tel_par_masque(texte, 'X')
    >>> len(nouv)
    119
    >>> nouv
    'XXXXXXXXXXzerdXXXXXXXXXXXXXXsdfgdsfgXXXXXXXXXXXXXXXXXzesrgtfhXXXXXXXXXXXXXXzedgfh34ze0000zesfg00000000  XXXXXXXXXXXXXX4'

    Pas de changement si le texte ne contient aucune suite.
    >>> remplace_numero_tel_par_masque('', '@')
    ''
    >>> texte = '*%µ%$12'
    >>> nouv = remplace_numero_tel_par_masque(texte, '@')
    >>> nouv == texte
    True
    '''
    pattern = (r'\d{10}|'
               r'(\d\d[ ]){4}\d\d|'
               r'(\d\d-){4}\d\d|'
               r'([+]\d{3}[ ]\d{3}[ ](\d\d[ ]){2}\d\d)|'
               r'\d[ ]\d{3}[ ](\d\d[ ]){2}\d\d'
               )
    matches = re.finditer(pattern, texte)
    res = ''
    i = 0
    for m in matches:
        deb = m.start() # inclus
        fin = m.end() # exclus
        res += texte[i:deb] + char*(fin-deb)
        i = fin
    if i != len(texte):
        res += texte[i:]
    return res

def remplace_identifiant_par_masque(texte, char):
    '''Renvoie une version de `texte` dans laquelle tous les 
    identifiants étudiants type prenom.nom.etu sont remplacés 
    par une suite de `char`.

    >>> texte = '  a.b.etu45mi.nebut.etu***.etu%=)..etu56'
    >>> nouv = remplace_identifiant_par_masque(texte, '@')
    >>> nouv
    '  @@@@@@@45@@@@@@@@@@@@***.etu%=)..etu56'
    '''
    pattern = r'[a-z]+[.][a-z]+[.]etu'
    matches = re.finditer(pattern, texte)
    res = ''
    i = 0
    for m in matches:
        deb = m.start() # inclus
        fin = m.end() # exclus
        res += texte[i:deb] + char*(fin-deb)
        i = fin
    if i != len(texte):
        res += texte[i:]
    return res

    
def appose_masque(texte : str) -> str:
    '''Renvoie texte ds lequel les commentaires, les emails, les suites
    de plus de 8 chiffres et les num de tel sont masqués par des X.

    >>> texte = '1234543245zadsefgmirabelle.nebut.etu$^ù$^ù0255771945#zadefgh\\n$$mi.nebut.etu@univ-lille.fr'
    >>> nouv = appose_masque(texte)
    >>> nouv
    '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@$^ù$^ù@@@@@@@@@@#@@@@@@@\\n$$@@@@@@@@@@@@@@@@@@@@@@@@@@'
    '''
    tmp = remplace_commentaire_par_masque(texte, '@')
    tmp = remplace_email_par_masque(tmp, '@')
    tmp = remplace_suite_chiffres_par_masque(tmp, '@')
    tmp = remplace_numero_tel_par_masque(tmp, '@')
    return remplace_identifiant_par_masque(tmp, '@')
    
import doctest
if __name__ == '__main__':
    doctest.testmod()
