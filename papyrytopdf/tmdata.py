# -*- coding: UTF-8 -*-


"""

TM Data extracts the following information from Trismegistos:
    - papyri.info URL
    - publications
    - mentioned people
        - TM Per id
        - name
    - TM id *
* this should be given by the user.

"""


# OPENING THE WEBSITE AND PARSING THE HTML
tmurl_base = 'https://www.trismegistos.org/text/' # Defines the root of the url for the texts in Trismegistos
tmurl = tmurl_base + str(tmid) # Creates the url of the text by adding the TM number at the end
tmhtml = urlopen(tmurl).read() # extracts the html code of the website
tmsoup = bs(tmhtml, features='html.parser') # parses the html with the Beautiful Soup library
# LOOKING FOR THE INFORMATION IN THE HTML CODE
div_publications = tmsoup.find_all('div', attrs={'id':'text-publs'}) # locates the section in the html code where the publs are stored
publs = div_publications[0].find_all('p') # breaks the section into pagragraphs (each contains a publ)
p_textrelations = tmsoup.find_all('p', attrs={'id':'texrelations'}) # locates the section in the html where the links are

if len(p_textrelations) >0:
    links = p_textrelations[0].find_all('a') # breaks the section into individual links
    papinfo = None # gives a value None if there is no link to papyri.info
    for l in links: # finds the one that directs to papyri.info
        if 'DDbDP' in l.text:
            papinfo= l['href'] # stores the url in a variable
else:
    papinfo = None

# CLEANING THE DATA
publications = []  # creates a list to store the post-processed publications

for pub in publs: # iterates through the list of publications we saved
    pub = pub.text # grabs only the text
    if '∙' in pub: # looks for ∙
        pub = pub.replace('∙', '') # removes it if it is present
    if 'link' in pub:
        pub = re.sub('(link.*?\[)', '[', pub) # looks for info about the link provider and removes it if it is present
    publications.append(pub) # adds to the list we created before

'''When there is additional bibliography it is duplicated
    because the paragraph is nested within the last publication.
    For example:
    when there is something like this: Other bibliography: BL 4, 1964, p. 24; P. L. Bat. 21, 1981, p. 99
    it is nested into the last paragraph <p> publication <p> other bib</p></p>
    Since we look for paragraphs we end up with: 'publication other bib' and 'other bib'. '''
if len(publications) >2:
    if publications[-1] in publications[-2]: # checks if the text of the last item of the list is repeated in the previous item
        publications[-2] = publications[-2].replace(publications[-1],'') # if so, it removes it

publications = set(list(publications))  # just confirming that there are no duplicates

t1.addtmdata(publications,papinfo) #adds to the object
