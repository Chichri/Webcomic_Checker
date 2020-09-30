import requests
from bs4 import BeautifulSoup, SoupStrainer

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

    def links(self):
        try:
            links = []
            soup = BeautifulSoup(self.text, 'html.parser', parse_only=SoupStrainer('a'))
            for link in soup.find_all('a'):
                links.append(link.get('href'))
            return links
        except:
            return 'Something has gone wrong' 

    def last_recent(self):
        with open('Desktop/Coding_Projects/Webcomic_Checker/comics/'+ self.file + '.txt') as f_obj:
            last_recent = f_obj.read()
        return last_recent.rstrip()

    def most_recent(self):
        return self.links[self.position]

    def check(self):
        if str(self.most_recent) != self.last_recent:
            with open('Desktop/Coding_Projects/Webcomic_Checker/comics/'+ self.file + '.txt', 'w') as f_obj:
                f_obj.write(str(self.most_recent))
            return 'This comic has updated'
        if str(self.most_recent) == self.last_recent:
            return 'This comic has not been updated'

    def print_links(self):
        print(self.links)

#Ok it was figured out: just rstrip last_recent, reading it appends an extra '\n'
#Now, implement the BeutifualSoup link finder from d20m.py to the class in a couple of methods
