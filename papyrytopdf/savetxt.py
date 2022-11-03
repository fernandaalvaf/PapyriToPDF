with open(f'Txts/{pdfname}.txt', "w") as text_file:
    text_file.write( f"{t1.id}\n\n {t1.ddbdp_data['Text']}")