import json
from checker import Checker
import os
path = os.path.dirname(os.path.abspath(__file__))
#gets current path

def menu():

    header()

    print("Webcomic Checker. Check slow webcomics quickly. By Chichri\n")

    command_list()
    #Prints out initial command list
    while True:

        dec = input('What would you like to do?\n')

        dec = dec.rstrip()

        if dec == '1':
            create_set()
        elif dec == '2':
            check_set()
        elif dec == '3':
            see_sets()
        elif dec == '4':
            edit_sets()
        elif dec == '5':
            delete_set()
        elif dec == '6':
            info()
        elif dec == '7':
            command_list()
        elif dec == 'quit':
            break
        else:
            print("I'm sorry, I didn't recognize that command.")
#menu. Creates the elseif main command loop

def create_set():
    dec = input('You are about to create a new set of comics. '
    'You will need all the information neccissary to procced. Y/N\n')
    dec = dec.rstrip()
    if dec.upper() == 'N':
        pass
    if dec.upper() == 'Y':
        new_set = []
        flag = True
        while flag:
            name = input('Name\n')
            #Name of the comic
            url = input('Url\n')
            #homepage url
            txt = input('Text file\n')
            #name of the text file
            pos = 0
            #Position of the newlink
            lks = 0
            #flag for if links fail
            f = 0
            #flag for if the main url fails
            comic = {'name': name, 'url': url, 'txt': txt, 'pos': pos, 'lks': lks, 'f' : f}
            #the assembled set
            new_set.append(comic)

            dec = input('Next comic? Y/N\n')
            dec = dec.rstrip()
            if dec.upper() == 'Y':
                continue
            if dec.upper() == 'N':
                handle(txt_check(new_set))
                #txt_check works, figure out why its not friggen passing off correctly
                break
#create_set. The main function for making a set. It calls many of the funtions-
#-below The main concept is that it takeas a couple arguments and sets up the-
#-sets, which are then processed by the functions below.

#FUNCTIONS CALLED BY CREATE_SET()------------------------------------------

def txt_check(new_set):
    names = []
    for dic in new_set:
        names.append(dic['txt'])
    if len(names) != len(set(names)):
    #Checks for duplicate txt names
        for dic in new_set:
            checkingtxt = dic['txt']
            discname = dic['name']
            for dic in new_set:
                if discname == dic['name']:
                    pass
                if dic['txt'] == checkingtxt:
                    newname = input(dic['name'] + "'s txt name was shared with another txt name in this set. Please give it a new name.\n")
                    dic['txt'] = newname
        return txt_check(new_set)
    else:
        return new_set
#txt_check. Checks for txt name duplicates in sets being created

def handle(new_set):
    print(new_set)
    dec = input('This will be the set you are about to create. Is this okay? Y/N\n')
    dec = dec.rstrip()
    if dec.upper() == 'Y':
        save_set(new_set)
    if dec.upper() == 'N':
        dec = input('Start over? Y/N\n')
        dec = dec.rstrip()
        if dec.upper() == 'Y':
            create_set()
        if dec.upper() == 'N':
            handle(new_set)
#handle. Shuffles the set to either be saved or to go back to make a new one

def save_set(new_set):
    name = input('What will the name of this new set be?\n')
    with open(path + '/sets/' + name + '.json', 'w') as f_obj:
        json.dump(new_set, f_obj)
    prime_set(name)
    set_pos(name)
    fst_check(name)
#save_set. Begins the process of saving a set through 3 main functions

def set_pos(name):
        with open(path + '/sets/' + name + '.json') as f_obj:
            set = json.load(f_obj)
            for dic in set:
                comic = Checker(dic['url'], dic['txt'], dic['pos'])
                if comic.links == 'Something has gone wrong':
                    dic['f'] = 1
                #A little cheeky flag. If the main url failed, it creates a-
                #flag that deletes the comic all the way down the pipeline.
                #Also excuses the condemmed comic from a lot of work
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
                        #lks, a flag which triggers when the secondary link-
                        #-fails. Triggers manual_links later on.
                with open(path + '/sets/' + name + '.json', 'w') as f_obj:
                     json.dump(set, f_obj)
                     f_obj.close()
                f_obj.close()
                if dic['f'] == 1:
                    pass
            manual_links(name)
#set_pos. Certifies the 'position', the index in the list of links pulled by-
#-the requests module. Checks to see if there was an error with the links

def manual_links(name):
    with open(path + '/sets/' + name + '.json') as f_obj:
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
        with open(path + '/sets/' + name + '.json', 'w') as f_obj:
            json.dump(set, f_obj)
        if dic['f'] is 1:
            pass
#manual_links. If there was an error setting up the links, this function is-
#-called which prints out the entirety of the links and lets the user select-
#-them manunal

def prime_set(name):
    disc_names = []
    with open(path + '/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
        for comic in set:
            disc_names.append(comic['name'])
        f_obj.close()
    #Gets the names of the comics in the set being checked
    sets = os.listdir(path + '/sets/')
    text_files = []
    txt_names = []
    for set in sets:
        with open(path + '/sets/' + set) as f_obj:
            text_set = json.load(f_obj)
            text_files.append(text_set)
            f_obj.close()
    for tlist in text_files:
        for tdic in tlist:
            if tdic['name'] in disc_names:
                pass
            else:
                txt_names.append(tdic['txt'])
    #Gets the name of all current txt names without the ones belonging to set-
    #-being checked using the sets names

    with open(path + '/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
        f_obj.close()
    for dic in set:
        filename = dic['txt']
        if filename in txt_names:
            for comic in set:
                if comic['txt'] in txt_names:
                    print("You've given " + comic['name'] +  "'s' text file a name another text file has. Please give it a new one.")
                    tname = input('Name\n')
                    comic['txt'] = tname
            with open(path + '/sets/' + name + '.json', 'w') as f_obj:
                json.dump(set, f_obj)
                f_obj.close()
            return prime_set(name)
        else:
            f = open(path + '/comics/' + filename + '.txt', 'w+')
            f.write('Primer')
            f.close()
#prime_set. Creates a text file and writes to it so it can be manipulated later.
#Also checks for duplicate text file names in sets being created with outside-
#-sest so that no duplicates appear

def fst_check(name):
    with open(path + '/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
        for dic in set:
            if dic['f'] is 0:
                comic = Checker(dic['url'], dic['txt'], dic['pos'])
                comic.check()
            else:
                faliure_mode(name, dic['name'], dic['txt'])
#fst_check. Checks the comic once internally so that you don't get a false-
#-positive when you check it for the first time. Also the check point for the-
#-failiure parameter, which if triggered intiates faliure_mode.

def faliure_mode(name, dicname, dictxt):
    with open(path + '/sets/' + name + '.json') as f_obj:
        set = json.load(f_obj)
    for dic in set:
        if dicname == dic.get('name'):
            print("One or more of the urls you provided for the homepages didn't work. The comic(s) has been removed from the set")
            os.remove('Desktop/Coding_Projects/Webcomic_Checker/comics/' + dictxt + '.txt')
            del set[set.index(dic)]
            if bool(set) is False:
                print('After removing the comics, the set was found to be empty and therefore deleted.')
                os.remove(path + '/sets/' + name + '.json')
                return
            with open(path + '/sets/' + name + '.json', 'w') as f_obj:
                json.dump(set, f_obj)
#faliure_mode. Called if the basic url for the comic was miss-entered. Wipes-
#-the comic from the set, and the set if it ends up empty the set is wiped too.

    return

#CHECK_SET AND OTHERS---------------------------------------------------------

def check_set():
    file = input('Which set are you checking?\n')
    try:
        with open(path + '/sets/' + file + '.json') as f_obj:
            set = json.load(f_obj)
    except FileNotFoundError:
        print('That set does not exist')
        return
    for dic in set:
        comic = Checker(dic['url'], dic['txt'], dic['pos'])
        if comic.check() == 'This comic has updated':
            print(dic['name'] + ': ' + comic.check() + ' ' + '\033[32m' + comic.most_recent + '\033[0m')
        elif comic.check() == 'This comic has not been updated':
            print(dic['name'] + ': ' + comic.check())
#check_set. Calls check set in the Checker class. Checks the set. Can't get-
#-much similar then that.

def see_sets():
    print('\n')
    sets = os.listdir(path + '/sets/')
    for set in sets:
        print(set)
    print('\n')
    dec = input('Would you like to view the comics of a set? Y/N\n')
    if dec.upper() == 'N':
        return
    elif dec.upper() == 'Y':
        name = input('Which set would you like to view?\n')
        try:
            with open(path + '/sets/' + name + '.json') as f_obj:
                print('The comics within this set are:')
                set = json.load(f_obj)
                for dic in set:
                    print(dic['name'])
        except FileNotFoundError:
            print('That set does not exist')
            return
#see_sets. Prints out all the sets to the console.

def edit_sets():
    name = input('Which set would you like to edit?\n')
    name = name
    try:
        with open(path + '/sets/' + name + '.json') as f_obj:
            set = json.load(f_obj)
    except FileNotFoundError:
        print('That set does not exist')
        return
    dec = input('Would you like to add or remove?\n')
    dec = dec.rstrip()
    if dec == 'add':
        add_set(set, name)
    if dec == 'remove':
        remove_set(set, name)
    if dec == 'back':
        pass
#edit_sets. The first step to editing sets. Shuffles the user around for-
#-confirmation of what they exactly want to do.

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
#add_set. Adds another comic to a set.

def m_handle(set, name):
    name = name
    dec = input('Another comic? Y/N\n')
    dec = dec.rstrip()
    if dec.upper() == 'Y':
        add_set(set)
    if dec.upper() == 'N':
        print(set)
        dec = input('Are you okay with the new set Y/N:')
        dec = dec.rstrip()
        if dec.upper() == 'Y':
            with open(path + '/sets/' + name + '.json', 'w') as f_obj:
                json.dump(set, f_obj)
            fst_check(name)
        if dec.upper() == 'N':
            m_handle(set, name)
        if dec == 'back':
            pass
#m_handle. Confirms adding another comic to a set, after some more shuffling.

def prime_comic(comic):
    filename = comic['txt']
    f = open(path + '/comics/' + filename + '.txt', 'w+')
    f.write('Primer')
    f.close()
#prime_comic. Primes a comic that hasn't been added in the creation of a set.

def set_pos_com(comic):
    temp = comic
    temp = Checker(temp['url'], temp['txt'], temp['pos'])
    pos_link = input('What is the newest link for ' + comic['name'] + '?\n')
    pos = temp.links.index(pos_link)
    comic['pos'] = pos
    return comic
#set_pos_com. Sets the positon of a comic not added in the creation of a set.

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
                    os.remove(path + '/comics/' + dic['txt'] + '.txt')
                    del set[set.index(dic)]
                    newset = set
                    print(newset)
                    with open(path + '/sets/' + name + '.json', 'w') as f_obj:
                        json.dump(newset, f_obj)
                    dec = input('Would you like to remove another? Y/N')
                    dec = dec.rstrip()
                    if dec.upper() == 'Y':
                        remove_set(newset, name)
                    if dec.upper() == 'N':
                        pass
    elif dec == 'back':
        pass
    else:
        print('That comic is not in this set')
        remove_set(set, name)
#remove_set. Removes comics from sets. Bit of a misnomer on this one.

def delete_set():
    dec = input('You want to delete a set? Y/N \n')
    dec = dec.rstrip()
    if dec.upper() == 'Y':
        name = input('What set would you like to delete?\n')
        try:
            with open(path + '/sets/' + name + '.json') as f_obj:
                set = json.load(f_obj)
        except FileNotFoundError:
            print('Could not find the set. Please try again')
            return
        for dic in set:
            os.remove(path + '/comics/' + dic['txt'] + '.txt')
        os.remove(path + '/sets/' + name + '.json')
        print('Set removed')
        pass
    if dec.upper() == 'N':
        pass
#delete_set. Deletes a set and it is related files in its enterity.

def command_list():
    print("""

[\033[32m1\033[0m] :   make a new set of comics
[\033[32m2\033[0m] :   check the comics within a specified set
[\033[32m3\033[0m] :   view your sets
[\033[32m4\033[0m] :   edit your sets
[\033[32m5\033[0m] :   delete a set
[\033[32m6\033[0m] :   information on how to use this program. You should run this first
[\033[32m7\033[0m] :   list of commands
quit:   close the program

     """)
#command_list. Prints the list of primary commands availble to the user

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

    ---------------------------------------------------------------------------

    Prompts and Particularities

    At times, you will be given a Y/N prompt. This a simple yes or no question
    and you only have to input a singular 'y' or 'n' to denote your response

    For the most part, inputing the wrong command or string will cause whatever
    action you're performing to default back to the main prompt.

    Don't give text files the same name; you'll be routed if you do

    When using this program, you should maximize your window. Text can be affected
    by the edge of the border.

    If a comic updates but the link leads to something other then the new comic,
    it means the postion has broken because the comics website has moved things
    around. Remove the comic from the set and re-add it to fix the problem



    Now you are all done! I hope you make use of this program.

    """
    )
#info. Prints information on the program

def header():

    print(' __      __      ___.                        .__         _________ .__                   __ ')
    print('/  \    /  \ ____\_ |__   ____  ____   _____ |__| ____   \_   ___ \|  |__   ____   ____ |  | __ ___________')
    print('\   \/\/   // __ \| __ \_/ ___\/  _ \ /     \|  |/ ___\  /    \  \/|  |  \_/ __ \_/ ___\|  |/ // __ \_  __ \ ')
    print(' \        /\  ___/| \_\ \  \__(  <_> )  Y Y  \  \  \___  \     \___|   Y  \  ___/\  \___|    <\  ___/|  | \/')
    print('  \__/\  /  \___  >___  /\___  >____/|__|_|  /__|\___  >  \______  /___|  /\___  >\___  >__|_ \ \___  >__|')
    print('       \/       \/    \/     \/            \/        \/          \/     \/     \/     \/     \/    \/    ')
    print('\n\n')
#header. Prints this snazzy ASCII art header. Props to patorjk.
