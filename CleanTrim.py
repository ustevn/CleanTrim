import os
import sys
import re
import datetime
import random

def briefing(path,prefisso,postfisso):
    """
    Fornisce un rapido briefing degli imput dell'utente
    
    Args:
        path (str): percorso della cartella da analizzare
        prefisso (str): Testo da aggiungere pre numerazione
        postfisso (str): Testo da aggiungere dopo la numerazione
    """
    print('\n--------Briefing--------\n\n'\
           f'I tuoi dati inseriti sono:'\
           f'\nPercorso: {path}'\
           f'\nPrefisso: {prefisso}'\
          )
    if postfisso!='':
        print(f'Postfisso:{postfisso}')
    print(f'\nScelta: {scelta}')
    risposta=input('Vuoi continuare? [y]/[n]')
    if risposta =='n':
        input('Uscita in corso...')
        sys.exit()
def aggiungi_prefisso(lista_titoli,prefisso):
    """
    Aggiunge un unico prefisso alla lista dei files nella cartella
    
    Args:
        lista_titoli (list): lista nomi degli elementi nella cartella
        prefisso (str): Prefisso da aggiungere ai titoli 
    
    Returns:
        list: la lista dei titoli modificata
    """
    print('\nEcco l\'anteprima titoli:')
    for i in range(len(lista_titoli)):
        if lista_titoli[i].find(prefisso)==-1: #Vede se questo prefisso non sia già presente
            lista_titoli[i]=prefisso + lista_titoli[i]
        print(lista_titoli[i],sep='\n')   
    return lista_titoli 
def numera(lista_titoli):
    """
    La funzione numera automaticamente gli elementi della cartella in ordine progressivo
    
    Args:
        lista_titoli (list): lista nomi degli elementi nella cartella
    
    Returns:
        list: la lista dei titoli modificata
    """
    print('\nEcco l\'anteprima titoli:')
    for i in range(len(lista_titoli)):
        if re.findall(r"^\d",str(lista_titoli[i]))==[]: #Controllo che non ci siano altre numerazioni in testa
            if i<9:
                lista_titoli[i]='0'+str(i+1) + ' '+ lista_titoli[i]
            else:
                lista_titoli[i]=str(i+1) + ' '+ lista_titoli[i]
        print(lista_titoli[i],sep='\n')
    return lista_titoli
def pulisci_prefisso(lista_titoli): #Aggiungere iterazioni multiple
    """
    Permette l'eliminazione delle parti comuni nei nomi dei files della cartella, elimina le numerazioni progressive in testa.
    
    Args:
        lista_titoli (list): lista nomi degli elementi nella cartella
    
    Returns:
        list: la lista dei titoli modificata
    """
    scelta=0
    while scelta not in [1,2,3]:
        scelta=input('Cosa vuoi rimuovere?\n'
                    '  1 Numeri\n'
                    '  2 Segni e spazi\n'
                    '  3 Testo\n')
        if scelta=='1':
            print('\nEcco l\'anteprima titoli:')
            for i in range(len(lista_titoli)):
                if re.findall(r"^\s*(\d+)",str(lista_titoli[i]))!=[]:#Elimino solo numerazione in testa
                    lista=re.sub(r"^\s*(\d+)",'',lista_titoli[i],count=2).strip()
                    lista_titoli[i]=lista
                print(lista_titoli[i])
        elif scelta=='2':
            print('\nEcco l\'anteprima titoli:')
            for i in range(len(lista_titoli)):
                if re.findall(r"^[^a-zA-Z0-9]+",str(lista_titoli[i]))!=[]:#Elimino solo simboli espazi in testa
                    lista=re.sub(r"^[^a-zA-Z0-9]+",'',lista_titoli[i],count=2).strip()
                    lista_titoli[i]=lista
                print(lista_titoli[i])
        elif scelta=='3':
            #trovo l'estensione; mi conflitta con omnisplit
            if lista_titoli[0].count('.')==1:
                ext=lista_titoli[0][lista_titoli[0].index('.'):]
                try:
                   lista_titoli=[titolo[:titolo.index('.')] for titolo in lista_titoli]
                except ValueError:
                    input('Trovato nome file vuoto! Premi un tasto per uscire')      
            else:
                raise Exception('La lista nomi non deve contenere punti, contattare lo sviluppatore')
            print('\nTrovata estensione:',ext)

            #cerco i vari pattern con un cronfronto tra due stringe successive scorrendo la lista
            init=0  #inidice del primo elemento in lista del i-esimo pattern
            finit=1 #inidice del ultimo elemento in lista del i-esimo pattern
            cycle_index=1    #indice di ciclo
            while init<len(lista_titoli):
                pattern=[]
                confronto1= omnisplit(lista_titoli[init])
                try:
                    confronto2= omnisplit(lista_titoli[init+1])
                except IndexError:
                    return lista_titoli
                # print('\nElementi confrontati:',confronto1,confronto2,'fine contronti\n',sep='\n\t')
                'questo mi serve per capire come confronta la roba e quindi fare debug'
                #Procedo in ordine sequenziale
                i=0
                try:
                    while confronto1[i]==confronto2[i]:
                        pattern.append(confronto1[i])
                        i+=1
                except:
                    pass

                if pattern!=[]:
                    print(f'Trovato il {cycle_index}° pattern:\n',pattern, end='\n')
                else:
                    lista_titoli[init]+=ext
                    init+=1
                    continue
                    
                #trovo quanti sono gli elementi con l'iesimo pattern e lo rimuovo
                print('\nEcco l\'anteprima titoli:')
                i=0
                try:
                    while set(pattern).issubset(omnisplit(lista_titoli[init+i]))==True:
                        indexs=[lista_titoli[i+init].index(pattern[0]),
                                lista_titoli[i+init].index(pattern[-1])+len(pattern[-1])-1]
                        lista_titoli[i+init]=lista_titoli[i+init][indexs[1]+1:] #sovrascrivo a partire dalla fine del pattern
                        lista_titoli[i+init]+=ext
                        
                        print(lista_titoli[i+init])
                        i+=1
                except IndexError:
                    return lista_titoli
                init+=i

                cycle_index+=1
        else:
            print('Scelta non valida. Riprova')
            continue
        return lista_titoli 
def omnisplit(text): #questo è quello di prima che separa anche spazi e dash. NON SEPARA SOLO IL "-""
    """
    é un metodo split() che funziona con ogni tipo di separazione, Camelcase, spazio, dash:_, non funziona con il "-"    

    Args:
        text (str): testo da separare
    
    Returns:
        list: lista delle parole splittate
    """
    pattern=r'.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])|(?<=\S)(?=\s)|(?<=\s)(?=\S)|(?<=\S)(?=_)|(?<=_)(?=\S)|$)'
    matches = re.findall(pattern, text)
    for i in range(len(matches)):
            try:
                matches.remove(' ')
            except ValueError:
                pass
            try:
                matches.remove('_')
            except ValueError:
                pass
    return matches
def riscrivi_titoli(lista_nuova,lista_vecchia,path):
    """
    Modifica i nomi dei files da vecchi a nuovi
    
    Args:
        lista_nuova (list): lista nomi modificati
        lista_vecchia (list): lista nomi originali
        path (str): percorso cartella
    
    """
    scelta=input('Procedere con la scrittura?[y][n]')
    if scelta=='y':   
        for i in range(len(lista_vecchia)):
            old_file = os.path.join(path, lista_vecchia[i])
            new_file = os.path.join(path, lista_nuova[i])
            try:
                os.rename(old_file, new_file)
            except FileExistsError:
                pass
    else:
        input('Addio') 
        sys.exit()  
def versioning(lista_nuova):
    """
    Crea un file log con le modifiche o permette la lettura del file log
    
    Args:
        lista_nuova (list): lista nomi modificati
        parametro2 (tipo): descrizione del parametro
    
    """
    scelta=input('Procedere con salvataggio su file?[y][n]')
    if scelta=='y':
        try:
            posizione= f"{path}\\log_folder\\log_file.txt"
            os.makedirs(f"{path}\\log_folder",exist_ok=True)
            file=open(posizione,"+a")
            file.write('Log:'+str(datetime.datetime.now())+'\n')
            [file.write(titolo+'\n') for titolo in lista_nuova]
            file.close()
            print('log_file.txt salvato in: \n',posizione)
        except OSError:
            print('Errore apertura file')
    # else:
    #     print('Addio') 
    #     sys.exit()
def nuova_numerazione(lista_titoli,prefisso,postfisso):
    """
    La funzione crea una nuova numerazione con un nuovo prefisso, una numerazione progressiva ed un postfisso
    
    Args:
        lista_titoli (list): lista nomi degli elementi nella cartella
        prefisso (str): Testo da aggiungere pre numerazione
        postfisso (str): Testo da aggiungere dopo la numerazione
    
    Returns:
        list: la lista dei titoli modificata
    """
    #trovo l'estensione, la salvo e la elimino dalla stringa dei titoli; mi conflitta con omnisplit
    if lista_titoli[0].count('.')==1:
        ext=lista_titoli[0][lista_titoli[0].index('.'):]
        try:
            lista_titoli=[titolo[:titolo.index('.')] for titolo in lista_titoli] #riscrivo la lista titoli senza estenzione
        except ValueError:
            input('Trovato nome file vuoto! Premi un tasto per uscire')      
    else:
        raise Exception('La lista nomi non deve contenere punti, contattare lo sviluppatore')
    
    print('\nEcco l\'anteprima titoli:')
    for i in range(len(lista_titoli)):
        if i<9:
            lista_titoli[i]=prefisso + '0'+str(i+1) + postfisso + ext
        else:
            lista_titoli[i]=prefisso + str(i+1) + postfisso + ext
        print(lista_titoli[i],sep='\n')
    return lista_titoli
"--------------------------------Inizio programma-------------------------------"

print('Benvenuto in CleanTrim Alpha:\n'\
'      ...............................           Ti aiuterò nel mettere ordine nei tuoi files:\n'
'   ~YPGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG5?.        In questo programma, potrai revisionare i \n'
'  !BBBBB##########################BBBB#Y        titoli dei tuoi files rimuovendo o aggiungendo \n'
'  ?BBBBY777777777777777777777777777BBBB5        parti in modo da renderli più facilemente\n'
'  7BBBB7                          .GBBB5        navigabili\n'
'  ?BBBBGPPPPPPPPPPPPPPPPPPPPPPPPPPPBBBB5        Prima di iniziare fai un backup dei files,\n'
'  ?BBBBB###########################BBBB5        oppure puoiusare la funzione "versioning" \n'
'  ?BBBBY!!!!!!!!!!!!!!!!!!!!!!!!!!!GBBB5        per creare un files logcon l\'attuale \n'
'  ?BBBB7                          .GBBB5        situazione prima di iniziare.\n'
'  ?BBBBGPPPPPPPPPPPPPPPGGGGGPPPPPPPBBB#P     \n'
'  ?BBBBBBBBBBBBBBBBBBBBPJ??YG#BBBBBBBGP?     \n'
'  ?BBBBJ~~~~~~~~~~~~!!^  :  :5BBBBBP7: ..    \n'
'  ?BBBB7 ..........    !Y5J:  ?BBP7. :7YYJ^  \n'
'  ?BBBBGGGGGGGGGGGGP:  J555Y^  !?. .75555J:  \n'
'  ?BBBBBBBBBBBBBBBBBJ  :J5555!    ~Y555Y7.   \n'
'  7BBBBBBBBBBBBBBBBBBY. .75555?.^J5555?:     \n'
'  7BBBBBBBBBBBBBBBBBB#P^  ~Y555Y5555J^       \n'
'  ?#BBBBBBBBBBBBBBBGY?!^   :J55555J~         \n'
'  ~BBBBBBBBBBBBBB5!. .:^^:.!Y55555J^.:^^:.   \n'
'   ^?555555555557  ^?YYJYY5555J7Y555YYYY5Y7. \n'
'                  ^557.  .?55!. :?557:..:J5J.\n'
'                  ^557.  .?5Y:   ~55~   .?5Y:\n'
'                   ~J5YJJY5J~     !Y5YJJY5J^ \n'
'                     :^~~^:        .:~~~^:      creator Francesco.Stefanelli aka Steven \n')
ok='notok'
while ok!='ok':
    path=input('Inserisci il percorso della cartella\n')
    lista_nuova=[]
    try:
        with os.scandir(path) as dir: 
            for file in dir:
                if file.is_file(): #Questo controllo mi permette di ignorare le sottocartelle
                    lista_nuova.append(file.name)   #inizializzo le variabili duplicandole
                    lista_vecchia=list(lista_nuova) #sono due liste di stringhe
    except FileNotFoundError:
        print('Percorso inserito non valido, inserisci nuovo percorso\n')
        input("Schiaccia invio per riprovare...")
        ok='notok'
        continue
    except OSError:
        print('Devi togliere le virgolettte dal percorso\nCià\n')
        input("Schiaccia invio per riprovare...")
        ok='notok'
        continue
    ok='ok'
scelta=99
while scelta!=0:
    scelta=input('Cosa vuoi fare?:\n'
                '   1:Aggiungi prefisso\n' \
                '   2:Numera\n' \
                '   3:Pulisci prefisso\n'\
                '   4:Versioning\n'
                '   5:Riscrivi tutto\n'
                '   0:Esci\n')

    if scelta =='1':
        prefisso=input('Inserisci il prefisso(gli spazi alla fine contano)\n')
        briefing(path,prefisso,postfisso='null')
        lista_nuova=aggiungi_prefisso(lista_nuova,prefisso)#questo passaggio modifica la lista_nuova con i titoli nuovi
        riscrivi_titoli(lista_nuova,lista_vecchia,path) #questo passaggio scrive i titoli nuovi su file
        versioning(lista_nuova)
    elif scelta =='2':
        briefing(path,prefisso='null',postfisso='null')
        lista_nuova=numera(lista_nuova)#questo passaggio modifica la lista_nuova con i titoli nuovi
        riscrivi_titoli(lista_nuova,lista_vecchia,path) #questo passaggio scrive i titoli nuovi su file
        versioning(lista_nuova)
    elif scelta =='3':
        briefing(path,prefisso='null',postfisso='null')
        lista_nuova=pulisci_prefisso(lista_nuova)
        riscrivi_titoli(lista_nuova,lista_vecchia,path) #questo passaggio scrive i titoli nuovi su file
        versioning(lista_nuova)
    elif scelta =='4':
        scelta=input('Vuoi salvare o leggere lo stato attuale dei titoli?\n' \
                    '[1]:Leggere\n' \
                    '[2]:Salvare\n')
        if scelta=='1':
            try:
                file=open(f"{path}\\log_folder\\log_file.txt","r")
                lista_attuale=file.readlines()
                righe=int(len(lista_nuova))
                for line in lista_attuale[-righe:]:
                    print(line.strip())
                file.close()
            except OSError:
                print('Errore apertura file')
            pass
        elif scelta=='2':
            versioning(lista_nuova)
        else:
            print('Scelta non valida. Riprova')
            continue
    elif scelta =='5':
        prefisso=input('Inserisci il prefisso(gli spazi alla fine contano)\n')
        postfisso=input('Inserisci il postfisso(gli spazi all\'inizio contano)\n')
        briefing(path,prefisso,postfisso)
        lista_nuova=nuova_numerazione(lista_nuova,prefisso,postfisso)
        riscrivi_titoli(lista_nuova,lista_vecchia,path) #questo passaggio scrive i titoli nuovi su file
        versioning(lista_nuova)


    elif scelta =='0':
        sys.exit()
    else:
        print('Riprova')
        continue