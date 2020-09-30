import json
from checker import Checker
import os


def menu():
    print("Webcomic Checker. Enter 'help' to for a list of comands\n")

    while True:

        commands = """
        'create set' :   make a new set of comics\n
        'check set'  :   check the comics within a specified set\n
        'info'       :   information on how to use this program. You should run this first \n
        'see_sets'   :   view your sets\n
        'edit_sets'  :   edit your sets\n
        'delete_set' :   delete a set\n
        'quit'       :   close the program \n

        """

        dec = input('What would you like to do?\n')

        if dec == 'help':
            print(commands)
        elif dec == 'create_set':
            create_set()
        elif dec == 'check_set':
            check_set()
        elif dec == 'see_sets':
            see_sets()
        elif dec == 'edit_sets':
            edit_sets()
        elif dec == 'delete_set':
            delete_set()
        elif dec == 'quit':
            break
        else:
            print("I'm sorry, I didn't recognize that command.")

def create_set():
    dec = input('You are about to create a new set of comics. '
    'You will need all the information neccissary to procced. Y/N\n')
    if dec.upper() == 'N':
        pass
    if dec.upper() == 'Y':
        new_set = []
        flag = True
        while flag:
            name = input('Name\n')
            url = input('Url\n')
            txt = input('Text file\n')
            pos = 0
            lks = 0
            f = 0
            comic = {'name': name, 'url': url, 'txt': txt, 'pos': pos, 'lks': lks, 'f' : f}
            new_set.append(comic)

            dec = input('Next comic? Y/N\n')
            if dec.upper() == 'Y':
                continue
            if dec.upper() == 'N':
                handle(new_set)
                break

#FUNCTIONS CALLED BY CREATE_SET()------------------------------------------

def handle(new_set):
    print(new_set)
    dec = input('This will be the set you are about to create. Is this okay? Y/N\n')
    if dec.upper() == 'Y':
        save_set(new_set)
    if dec.upper() == 'N':
        dec = input('Start over? Y/N\n')
        if dec.upper() == 'Y':
            create_set()
        if dec.upper() == 'N':
            handle(new_set)

def save_set(new_set):
    name = input('What will the name of this new set be?\n')
    with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json', 'w') as f_obj:
        json.dump(new_set, f_obj)
    prime_set(name)
    set_pos(name)
    fst_check(name)

def set_pos(name):
        with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
            set = json.load(f_obj)
            for dic in set:
                comic = Checker(dic['url'], dic['txt'], dic['pos'])
                if comic.links == 'Something has gone wrong':
                    dic['f'] = 1
                if dic['f'] == 0:
                    pos_link = input('What is the newest link for ' + dic['name'] + '?\n')
                    try:
                        pos = comic.links.index(pos_link)
                        dic['pos'] = pos
                        print(dic['name'] + ' processed succesfully')
                    except ValueError:
                        print('Error with ' + dic['name'] + '. The position was not found.' )
                        dic['lks'] = 1
                        dic['pos'] = 0
                with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json', 'w') as f_obj:
                     json.dump(set, f_obj)
                     f_obj.close()
                f_obj.close()
                if dic['f'] == 1:
                    pass
            manual_links(name)

def manual_links(name):
    with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
    for dic in set:
        if dic['lks'] is 1 and dic['f'] is 0:
            comic = Checker(dic['url'], dic['txt'], dic['pos'])
            print(dic['name'] + ':')
            for link in comic.links:
                print(link)
            print('Current posistion: ' + str(dic['pos']))
            pos = input('Please check if the link specified is correct. If not, replace the postion\n')
            dic['pos'] = int(pos)
        with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json', 'w') as f_obj:
            json.dump(set, f_obj)
        if dic['f'] is 1:
            pass

def prime_set(name):
    with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
        for dic in set:
            filename = dic['txt']
            f = open('Desktop/Coding_Projects/Webcomic_Checker/comics/' + filename + '.txt', 'w+')
            f.write('Primer')
            f.close()

def fst_check(name):
    with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
        for dic in set:
            if dic['f'] is 0:
                comic = Checker(dic['url'], dic['txt'], dic['pos'])
                comic.check()
            else:
                faliure_mode(name, dic['name'], dic['txt'])

def faliure_mode(name, dicname, dictxt):
    with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
    for dic in set:
        if dicname == dic.get('name'):
            print("One or more of the urls you provided for the homepages didn't work. The comic(s) has been removed from the set")
            os.remove('Desktop/Coding_Projects/Webcomic_Checker/comics/' + dictxt + '.txt')
            del set[set.index(dic)]
            if bool(set) is False:
                print('After removing the comics, the set was found to be empty and therefore delete.')
                os.remove('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json')
                return
            with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json', 'w') as f_obj:
                json.dump(set, f_obj)

    return
#CHECK_SET AND OTHERS---------------------------------------------------------

def check_set():
    file = input('Which set are you checking?\n')
    try:
        with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + file + '.json') as f_obj:
            set = json.load(f_obj)
    except FileNotFoundError:
        print('That set does not exist')
        return
    for dic in set:
        comic = Checker(dic['url'], dic['txt'], dic['pos'])
        print(dic['name'] + ': ' + comic.check())

def see_sets():
    sets = os.listdir('Desktop/Coding_Projects/Webcomic_Checker/sets/')
    for set in sets:
        print(set)
    print('\n')
    name = input('Which set would you like to view?\n')
    try:
        with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
            print('The comics within this set are:')
            set = json.load(f_obj)
            for dic in set:
                print(dic['name'])
    except FileNotFoundError:
        print('That set does not exist')
        return

def edit_sets():
    name = input('Which set would you like to edit?\n')
    name = name
    try:
        with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
            set = json.load(f_obj)
    except FileNotFoundError:
        print('That set does not exist')
        return
    dec = input('Would you like to add or remove?\n')
    if dec == 'add':
        add_set(set, name)
    if dec == 'remove':
        remove_set(set, name)
    if dec == 'back':
        pass

def add_set(set, name):
    name = name
    cname = input('Name\n')
    url = input('Url\n')
    txt = input('Text file\n')
    pos = 0
    comic = {'name': cname, 'url': url, 'txt': txt, 'pos': pos}
    prime_comic(comic)
    comic = set_pos_com(comic)

    set.append(comic)

    m_handle(set, name)

def m_handle(set, name):
    name = name
    dec = input('Another comic? Y/N\n')
    if dec.upper() == 'Y':
        add_set(set)
    if dec.upper() == 'N':
        print(set)
        dec = input('Are you okay with the new set Y/N:')
        if dec.upper() == 'Y':
            with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json', 'w') as f_obj:
                json.dump(set, f_obj)
            fst_check(name)
        if dec.upper() == 'N':
            m_handle(set, name)
        if dec == 'back':
            pass

def prime_comic(comic):
    filename = comic['txt']
    f = open('Desktop/Coding_Projects/Webcomic_Checker/comics/' + filename + '.txt', 'w+')
    f.write('Primer')
    f.close()

def set_pos_com(comic):
    temp = comic
    temp = Checker(temp['url'], temp['txt'], temp['pos'])
    pos_link = input('What is the newest link for ' + comic['name'] + '?\n')
    pos = temp.links.index(pos_link)
    comic['pos'] = pos
    return comic


def remove_set(set, name):
    names = []
    dec = input('Which comic would you like to remove?\n')
    for dic in set:
        cname = dic.get('name')
        names.append(cname)
    if dec in names:
        for dic in set:
            if dic['name'] == dec:
                cho = input('You want to remove ' + dic['name'] + '? Y/N: ')
                if cho.upper() == 'Y':
                    os.remove('Desktop/Coding_Projects/Webcomic_Checker/comics/' + dic['txt'] + '.txt')
                    del set[set.index(dic)]
                    newset = set
                    print(newset)
                    with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json', 'w') as f_obj:
                        json.dump(newset, f_obj)
                    dec = input('Would you like to remove another? Y/N')
                    if dec.upper() == 'Y':
                        remove_set(newset, name)
                    if dec.upper() == 'N':
                        pass
    elif dec == 'back':
        pass
    else:
        print('That comic is not in this set')
        remove_set(set, name)

def delete_set():
    dec = input('You want to delete a set? Y/N \n')
    if dec.upper() == 'Y':
        name = input('What set would you like to delete?\n')
        try:
            with open('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json') as f_obj:
                set = json.load(f_obj)
        except FileNotFoundError:
            print('Could not find the set. Please try again')
            return
        for dic in set:
            os.remove('Desktop/Coding_Projects/Webcomic_Checker/comics/' + dic['txt'] + '.txt')
            os.remove('Desktop/Coding_Projects/Webcomic_Checker/sets/' + name + '.json')
        print('Set removed')
        pass
    if dec.upper() == 'N':
        pass


#Possible refactor needed with prime_set and save_set

def info():
    print("""
    Hi, and welcome to Webcomic Checker. This program is a webscraping script
    designed to check webcomics with inconsistent updating schedules en masse
    so that you don't have to. \n

    Now first and formost, you'll want to create a set of comics. Within this program,
    a set is a collection of comics that can all be checked at the same time. You
    can create multiple sets and group them however you like, wheter it be by
    genre, frequency of updatings, or simply whichever ones you like more.

    When creating a set, you will be asked to supply two things: the url of the comic
    and a text file. \n

    Firstly, lets talk about the url. You can find the url of your comic by visiting
    the site and copying the contents of the search bar. This should be the homepage
    of the comic, which is to say that you shouldn't see any 'archive', 'comic#' or
    other identifiers appended to the end of the url. For most comics, this will
    display the most recent comic, but for some it won't.Just make sure you are
    entering the homepage url. \n

    Next, the text file. When making a set of comics to check, you will be asked
    to enter a 'txt'. This is short for text file, and don't worry, you don't need
    to make one. A text file for this comic will be generated automatically in the
    'comics' folder. This is neccsiary for some of the internal workings of
    the program. All you need to do is provide a sutible name which can be anything,
    but I would advise making it the same as the name of the comic or an abriviaton
    to keep everything organized.\n

    Next, the program will ask you to name the set. Again, this is up to you.
    After providing a name, you will see the names of the comics you entered
    into that set along with a prompt asking you to provide the most recent
    link. This is the last step of setting up your set. You will need to provide
    the link to the most recent comic so internally, it knows where to look
    when checking the comic in the future. \n

    If everything goes to plan, that should be it. However, there is a chance that
    the most recent link wont exaclty match up what it actually is behind the scences.
    If this happens, it will trigger a manual input where it list each link returned
    and ask you to just find it. It's unfortunate, but to make it easier, comics
    that were proccesed properly before the manual set kicked in have their proper
    link highlighted in green and the position already listed, so you can just re-enter it.
    For the offending comic however, (and all comics after it, I'm working on this),
    you will need to manually enter the proper posistion. Remember to start counting
    from zero, because thats where computers start at. \n

    Now you are all done! I hope you make use of this program.

    """
    )
