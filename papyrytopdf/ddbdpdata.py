# -*- coding: UTF-8 -*-

'''
DDbDP Data extracts the following information from papyri.info:
    # HGV
        - Translations
        - Date
        - Subjects
    # APIS
        - Title
        - Summary
        - Origin
    # DDbDP
        - Text
        - Translation (?)
'''


pap_raw = 'https://papyri.info'

# OPENING THE WEBSITE AND PARSING THE HTML
if papinfo is None:
    subjects = 'No HGV data available'
    date = 'No HGV data available'
    translations = ['No HGV data available']
    title = 'No APIS data available'
    summary = 'No APIS data available'
    origin = 'No APIS data available'
    translationpap = 'No translation  available'
    text = 'No Transcription  available'

else:

    pap_html = urlopen(papinfo).read() # extracts the html code of the website
    pap_soup = bs(pap_html, 'html.parser') # parses the html with the Beautiful Soup library
    # HGV
    div_hgv = pap_soup.find_all('div', attrs={'hgv data'}) # look for the HGV contents
    if len(div_hgv) > 0:
        xml_hgv = div_hgv[0].find_all('a', attrs={'class':'xml'})[0]['href'] # grab the link for the xml
        hgv_data = urlopen(pap_raw+xml_hgv).read() # grab the xml
        hgv_soup = bs(hgv_data, 'xml') # parse the xml
                # Translations
        bib_trans = hgv_soup.find('div',attrs={'subtype':'translations'})
        translations = [] # open list to store our translations
        if bib_trans is not None:
            bibs = bib_trans.find_all('bibl')
            for bib in bibs:
                translations.append(bib.text)
        else:
            translation = 'no translation recorded'
            translations.append(translation)
                # Date
        date = hgv_soup.find('origDate').text
                # Subjects
        keywords = hgv_soup.find_all('keywords', attrs={'scheme':'hgv'})
        terms = keywords[0].find_all('term')
        subjects = ''
        for term in terms:
            subjects = subjects + term.text + ', '
        subjects = subjects[:-2]
    else:
        subjects = 'No HGV data available'
        date = 'No HGV data available'
        translations = ['No HGV data available']



    # APIS
    div_apis = pap_soup.find_all('div', attrs={'apis data'}) # look for the APIS contents
    if len(div_apis) > 0:
        xml_apis = div_apis[0].find_all('a')[0]['href'] # grab the link for the xml
        apis_data = urlopen(pap_raw+xml_apis).read() # grab the xml
        apis_soup = bs(apis_data, 'xml') # parse the xml
                # Title
        title = apis_soup.find('title').text
                # Summary
        summary = apis_soup.find('summary')
        if summary is not None:
            summary = summary.text
        else:
            summary = 'No summary available'
                # Subjects
        try:
            origin = apis_soup.find('origPlace').text
        except AttributeError:
            origin = hgv_soup.find('origPlace').text + '(from HGV)'

    else:
        title = 'No APIS data available'
        summary = 'No APIS data available'
        origin = 'No APIS data available'



    # DDbDP 1 - Text
    div_ddbdp = pap_soup.find_all('div', attrs={'transcription data'}) # look for the DDbDP contents
    """Type A - XML"""
    # if len(div_ddbdp) > 0:
    #     xml_ddbdp = div_ddbdp[0].find_all('a')[0]['href'] # grab the link for the xml
    #     ddbdp_data = urlopen(pap_raw+xml_ddbdp).read() # grab the xml
    #     ddbdp_soup = bs(ddbdp_data, 'xml') # parse the xml
    #             # Title
    #     text = ddbdp_soup.find('div', attrs={'type':'edition'}).get_text()
    #     text = text.replace("\n\n",'\n')[1:]
    #
    # else:
    #     text = 'No Transcription  available'
    """Type B - HTML"""

    try:

        # get text
        textsoup = bs(str(pap_soup.find_all('div', attrs={'id': 'edition'})[0]).replace('<br', '\n<br'),
                      'html.parser')  # look for the DDbDP contents
        text = textsoup.getText()
        text = text.split('\n')
        newstring = []
        for i in text:
            if re.match('^\d', i):
                linenumber = re.findall('^\d+', i)[0]
                linetxt = re.split('^\d+', i, maxsplit=1)[1]
                if len(linenumber)>1:
                    line = linenumber + '  ' + linetxt + '\n'
                else:
                    line = linenumber + '    ' + linetxt + '\n'
                newstring.append(line)
            else:
                line = '      ' + i + '\n'
                newstring.append(line)

        text = ''.join(newstring)

        text = text.replace('v','\n\nv\n').replace('Apparatus','\nApparatus').replace('      r\n','r\n')

    except IndexError:
        text = 'No Transcription  available'

    # DDbDP 2 - Translation
    div_ddbdpt = pap_soup.find_all('div', attrs={'translation data'}) # look for the DDbDP contents
    if len(div_ddbdpt) > 0:
        try:
            xml_ddbdpt = div_ddbdpt[0].find_all('a')[0]['href'] # grab the link for the xml
            ddbdp_datat = urlopen(pap_raw+xml_ddbdpt).read() # grab the xml
            ddbdp_soupt = bs(ddbdp_datat, 'xml') # parse the xml
                    # Title
            translationpap = ddbdp_soupt.find('div', attrs={'type':'translation'}).text
            translationpap = translationpap.replace("\n",'')
        except IndexError:
            translationpap = div_ddbdpt[0].find_all('p')[0].getText()
            translationpap = translationpap.replace("\n", '')


    else:
        translationpap = 'No translation  available'


t1.addhgvdata(translations,date,subjects)
t1.addapisdata(summary,title,origin) #adds to the object
t1.addpapsdata(text,translationpap)
