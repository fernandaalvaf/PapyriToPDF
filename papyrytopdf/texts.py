# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import lxml
import pandas as pd
from fpdf import FPDF

os.chdir('..') # sets the root directory of the project

def unpack(s):
    return "\n".join(map(str, s))

newline = "\n"

class PDF(FPDF):

    def header(self):
        # helvetica bold 14
        self.set_font("helvetica", "B", 14)
        # Calculate width of title and position
        width = self.get_string_width(self.title) + 6
        # Colors of frame, background and text
        self.set_fill_color(255,255,255)
        self.set_text_color(0, 0, 0)
        # Title
        self.cell(
            width,
            9,
            self.title,
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
            fill=True,
        )
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, f"{self.page_no()}", align="R")

    def text_title(self, id, title):
        # helvetica 12
        self.set_font("DejaVu", "", 12) #font change
        # Background color
        self.set_fill_color(218,218,218)
        # Title
        self.cell(
            0,
            6,
            f"TM {id} : {title}",
            new_x="LMARGIN",
            new_y="NEXT",
            align="L",
            fill=True,
        )
        # Line break
        self.ln(4)


    def text_body(self, text):
        # Read text file
        txt = text
        # Times 12
        pdf.set_font('DejaVu', '', 12) # font change
        # Output text
        self.multi_cell(
            0,
            5,
            f'Text:\n\n{txt}',
            align='L')
        # Line break
        self.ln(2)


    def translation_body(self, translation):
        # Read text file
        txt = translation
        # helvetica 12
        pdf.set_font('helvetica', '', 12) #fontchange
        # Output text
        self.multi_cell(
            0,
            5,
            f'Translation:\n\n{txt}',
            align='L')
        # Line break
        self.ln()


    def metadata_body(self):
        # helvetica 12
        pdf.set_font('DejaVu', '', 12) # font change
        # Output text
        self.multi_cell(
            0,
            5,
            f'{t1.outputinfo()}',
            align='L')
        # Line break
        self.ln(4)


    def print_text(self, id, title, name, translation):
        self.add_page()
        self.text_title(id, title)
        self.metadata_body()
        self.text_body(name)
        self.translation_body(translation)



class Text():
    """Stores the information about the texts"""

    def __init__(self, tmid):
        self.id = tmid
        self.publications = []
        self.papyriinfo_URL = ''
        self.hgv_data = {'Translations': [],
                         'Date':'',
                         'Subjects': ''}
        self.apis_data = {'Title': '',
                         'Summary': '',
                         'Origin': ''}
        self.ddbdp_data = {'Text': '',
                         'Translation': ''}


    def tm_id(self):
        return self.id


    def showinfo(self):
        print(f'TM id: {self.id}\n#\tPapyriinfo: {self.papyriinfo_URL}'
              f'\n#\tPublications: \n{unpack(self.publications)}'
              f'\n#\tHGV Data: \n{newline.join(f"{key}: {value}" for key, value in self.hgv_data.items())}'
              f'\n#\tAPIS Data: \n{newline.join(f"{key}: {value}" for key, value in self.apis_data.items())}'
              f'\n#\tDDbDP Data: \n{newline.join(f"{key}: {value}" for key, value in self.ddbdp_data.items())}')

    def outputinfo(self):
        content = (f'#  Publications: \n{unpack(self.publications)}\n'
                   f'\n#  HGV Data: \n'
                   f'Translations: \n{unpack(self.hgv_data["Translations"])}\n'
                   f'Date: {self.hgv_data["Date"]}\n'
                   f'Subjects: {self.hgv_data["Subjects"]}\n'
                   f'\n#  APIS Data: \n'
                   f'Summary: \n {self.apis_data["Summary"]}\n')
        return content

    def get_tmdata(self):
        tmid = str(self.tm_id())
        exec(open('papyrytopdf/tmdata.py').read())


    def get_ddbdpdata(self):
        papinfo = self.papyriinfo_URL
        exec(open('papyrytopdf/ddbdpdata.py').read())


    def addtmdata(self, publications, papyriinfo_URL):
        self.publications = publications
        self.papyriinfo_URL = papyriinfo_URL


    def addhgvdata(self, translations, date, subjects):
        self.hgv_data['Translations'] = translations
        self.hgv_data['Date'] = date
        self.hgv_data['Subjects'] = subjects


    def addapisdata(self, summary, title, origin):
        self.apis_data['Title'] = title
        self.apis_data['Summary'] = summary
        self.apis_data['Origin'] = origin


    def addpapsdata(self, text, translation):
        self.ddbdp_data['Text'] = text
        self.ddbdp_data['Translation'] = translation


if len(targets) > 1:
    print('Input the title of the .pdf. \nEx: A group of accounts from the Zenon archive')
    doctitle = input('Title of the document:')
else:
    doctitle = 'TM ' + str(targets[0])

ts = []
pdf = PDF()
pdf.set_title(doctitle)
pdf.add_font('DejaVu', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed.ttf')

pdf.set_font('DejaVu', '', 14)


count = 0
for target in targets:
    count += 1
    print(f'Progress: {count/len(targets)*100}%\nTM {target}')
    t1 = Text(target)
    t1.get_tmdata()
    t1.get_ddbdpdata()
    ts.append(t1)
    if len(targets) == 1:
        doctitle = t1.apis_data['Title']

    #with open(f'Txts/{t1.id}.txt', "w", encoding="utf-8") as text_file:
    #    text_file.write(f"{t1.id}\n\n {t1.ddbdp_data['Text']}")
    pdf.print_text(t1.id, t1.apis_data['Title'], t1.ddbdp_data['Text'],t1.ddbdp_data['Translation'])


pdfname = input('Name your pdf:')

pdf.output(f'Saved PDFs/{pdfname}.pdf')

