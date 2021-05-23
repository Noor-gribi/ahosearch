# ____________________________Prefixes ______________________________________

# function to calculate prefixes of a given array of strings
def pref(m):
    newString = []
    # we perform operations on first word of the array
    for s in m:
        n = ""
        # we iterate through word[s]
        for i in range(0, len(s)):
            # we construct our prefixes one by one through each iteration
            n += s[i]
            # we add the prefixe to the new array
            newString.append(n)
        # we cast the output list to a set in order to remove all doubles
        new = set(newString)
        # we recast the output of the set casting to a list in order to get an output type of an array
        renew = list(new)
        # we sort the output list so it would look appealing
        output = sorted(renew)
    return output


m = ['attac', 'ac', 'tacg', 'atatc']
print(pref(m))


# ____________________________TRIE ______________________________________
# this is the function that makes our trie( automaton )
def make_trie(*args):
    # we declare a set named trie
    trie = {}
    # we iterate through each word given as an argument in main
    for word in args:
        # if the word is not a string , raise an error
        if type(word) != str:
            raise TypeError('Try again with a string input')
        # we store our trie in another variable
        temporary_trie = trie
        # we iterate through each letter in the word given as an arg
        for letter in word:
            # we store our data in a dictionnary so we can access it easily
            temporary_trie = temporary_trie.setdefault(letter, {})
        # when each region is done being displayed we print an {end} like
        # pattern to organize things
        # Example : ('at','tatt','tt')
        #    __ t
        #   |
        #   a__ t __ a __ t __t
        #       |
        #       t
        # at / tatt / t ----> are the different patterns that are organized
        # by the _end_ key & value.
        temporary_trie = temporary_trie.setdefault('_end_', '_end_')
    return trie


# this is simple, we're just looking if each word of the list M exists
# in our trie
def in_trie(trie, word):
    exists = ''
    temporary_trie = trie
    for letter in str(word):
        if letter not in temporary_trie:
            return False, word
        else:
            return True, word
        temporary_trie = temporary_trie[letter]
    return True


trie = make_trie('at', 'tatt', 'tt')
print(trie)

# ____________________________AHO CORASICK ______________________________________

#STRUCTURE DE L'ALGORITHME  : on va construire le trie, puis definir
# les transitions d'echec. apres la construction du trie
# on traverse le trie au fur et à mesure que nous lisons\
# le texte d'entrée et sortons les positions auxquelles\
# nous trouvons les mots-clés.
#

from collections import deque
# le trie est represente comme une liste d'adjacence , sous forme : [{noeud:index}]
AdjList = []


def init_trie(keywords):
    """ creates a trie of keywords, then sets fail transitions """
    create_empty_trie()
    add_keywords(keywords)
    set_fail_transitions()


def create_empty_trie():
    """ initalize the root of the trie """
    # VALUE : Le char represented par le noeud
    # NEXT_STATES : une liste des identifiants des noeuds fils
    # FAIL_ STATE : l'id de l'état d'échec,
    # OUTPUT : une liste de tous les mots-clés complets que nous
    # avons rencontrés en parcourant le texte d'entree

    #On initialise le Trie qu'on a appelé AdjList et on ajoute le noeud principal
    AdjList.append({'value': '', 'next_states': [], 'fail_state': 0, 'output': []})

# les mots cle qu'on va ajouter au trie un par un
def add_keywords(keywords):
    """ add all keywords in list of keywords """

    for keyword in keywords:
        add_keyword(keyword)

# On defini une fonction "Helper" qui prends comme param un noeud et une valeur
# et qui retourne l'id du fils du meme noeud elli fiha value matches value
#Sinon on retourne None si on trouve rien.
def find_next_state(current_state, value):
    for node in AdjList[current_state]["next_states"]:
        if AdjList[node]["value"] == value:
            return node
    return None

# Pour ajouter un mot-clé dans le trie, nous parcourons le préfixe le plus long
# du mot-clé qui existe dans le trie à partir de la racine, puis nous ajoutons
# les caractères du reste du mot-clé en tant que noeuds dans le trie sous forme de chaine.
def add_keyword(keyword):
    """ add a keyword to the trie and mark output at the last node """
    current_state = 0
    j = 0
    child = find_next_state(current_state, keyword[j])
    #La boucle while trouve le préfixe le plus long du
    # mot-clé qui existe jusqu'à présent dans le trie,
    # et se terminera lorsque nous ne pouvons plus faire
    # correspondre plus de caractères à l'index j.
    while child != None:
        current_state = child
        j = j + 1
        if j < len(keyword):
            child = find_next_state(current_state, keyword[j])
        else:
            break
    #La boucle for parcourt le reste du mot-clé, créant
    # un nouveau nœud pour chaque caractère et l'ajoutant à AdjList.
    for i in range(j, len(keyword)):
        node = {'value': keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}
        AdjList.append(node)
        #len (AdjList) - 1 donne l'identifiant du noeud que nous ajoutons
        # puisque nous ajoutons à la fin de AdjList
        AdjList[current_state]["next_states"].append(len(AdjList) - 1)
        current_state = len(AdjList) - 1
    #Lorsque nous avons terminé d'ajouter le mot-clé dans le trie
    # AdjList [current_state] ["output"].append (keyword) ajoutera
    # le mot-clé à la sortie du dernier noeud, pour marquer la fin du mot-clé à ce noeud.
    AdjList[current_state]["output"].append(keyword)

# Nous ferons une première recherche approfondie sur le trie et définirons l'état d'échec de chaque noeud.

def set_fail_transitions():
    # list-like container with fast appends and pops on either end
    # |REMINDER|: l'état d'échec indique la fin du suffixe approprié le plus
    # long suivant de la chaîne que nous avons actuellement mis en correspondance.
    q = deque()
    child = 0
    # Tout d'abord, nous définissons tous les fils de la racine pour qu'ils aient l'état d'échec de la racine
    # car le suffixe strict le plus long d'un caractère serait la chaîne vide, représentée par la racine.
    for node in AdjList[0]["next_states"]:
        q.append(node)
        AdjList[node]["fail_state"] = 0

    # Initialement, le parent potentiel de l'état d'échec de child,


    while q:
        r = q.popleft()
        # Nous définissons l'état d'échec pour le noeud fils de r.
        for child in AdjList[r]["next_states"]:
            q.append(child)
            # state sera le prochain suffixe approprié le plus long,
            # qui est marqué par l'état d'échec de r.
            state = AdjList[r]["fail_state"]
            # S'il n'y a pas de transition de l'état d'échec de r vers un noeud
            # avec la même valeur que child, alors nous passons au suffixe
            # approprié le plus long suivant, qui est l'état d'échec de l'état d'échec de r et ainsi de suite,
            # jusqu'à ce que nous trouvions celui qui fonctionne, ou nous sommes à la racine.
            while find_next_state(state, AdjList[child]["value"]) == None \
                    and state != 0:
                state = AdjList[state]["fail_state"]
            AdjList[child]["fail_state"] = find_next_state(state, AdjList[child]["value"])
            if AdjList[child]["fail_state"] is None:
                AdjList[child]["fail_state"] = 0
            # Nous ajoutons la sortie de l'état d'échec à la sortie du child car,
            # puisque l'état d'échec est un suffixe de la chaîne qui se termine par child,
            # les mots correspondants trouvés à l'état d'échec se produiront également chez child.
            AdjList[child]["output"] = AdjList[child]["output"] + AdjList[AdjList[child]["fail_state"]]["output"]

# notre trie est construit.

# allant jusqu'à l'état d'échec lorsque nous ne correspondons plus au caractère
# suivant de la ligne.
def get_keywords_found(line):
    """ returns true if line contains any keywords in trie """
    line = line.lower()
    current_state = 0
    keywords_found = []
    # Étant donné une entrée, ligne, nous parcourons chaque caractère de la ligne
    for i in range(len(line)):
        # allant jusqu'à l'état d'échec lorsque nous ne correspondons plus au caractère
        # suivant de la ligne.
        while find_next_state(current_state, line[i]) is None and current_state != 0:
            current_state = AdjList[current_state]["fail_state"]
        current_state = find_next_state(current_state, line[i])
        # À chaque nœud, nous vérifions s'il y a une sortie,
        if current_state is None:
            current_state = 0
        # et nous capturerons tous les mots sortis et leurs indices respectifs.
        else:
            for j in AdjList[current_state]["output"]:
                keywords_found.append({"index": i - len(j) + 1, "word": j.upper()})
    return keywords_found


init_trie(['GTA','AGT','AAC'])
print(get_keywords_found("CAGTAACCGTA"))
