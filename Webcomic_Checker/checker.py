import requests
from bs4 import BeautifulSoup, SoupStrainer
import os
path = os.path.dirname(os.path.abspath(__file__))

class Checker():
    def __init__(self, url, file, position):
        self.url = url
        self.file = file
        self.position = position
        self.text = self.text()
        self.links = self.links()
        self.last_recent = self.last_recent()
        self.most_recent = self.most_recent()

    def text(self):
        try:
            r = requests.get(self.url)
        except:
            return
        return r.text
    #text. Uses the requests module to return the text attribute of the request-
    #-object genreated by the homepage url.

    def links(self):
        try:
            links = []
            soup = BeautifulSoup(self.text, 'html.parser', parse_only=SoupStrainer('a'))
            for link in soup.find_all('a'):
                links.append(link.get('href'))
            return links
        except:
            return 'Something has gone wrong'
    #links. Returns a list of links from which the new link is picked out of. -
    #-If something goes wrong, it triggers a flag which triggers manual_links.

    def last_recent(self):
        with open(path + '/comics/'+ self.file + '.txt') as f_obj:
            last_recent = f_obj.read()
        return last_recent.rstrip()
    #last_recent. Returns the last most recent comic url stored in the text file.

    def most_recent(self):
        return self.links[self.position]
    #most_recent. returns the most recent comic url stored in the text file.

    def check(self):
        if str(self.most_recent) != self.last_recent:
            with open(path + '/comics/'+ self.file + '.txt', 'w') as f_obj:
                f_obj.write(str(self.most_recent))
            return 'This comic has updated'
        if str(self.most_recent) == self.last_recent:
            return 'This comic has not been updated'
        #check. The most used method, likely. Checks the last most recent comic-
        #-against the current most recent comic.

    def print_links(self):
        print(self.links)
    #print_links. Prints the links
