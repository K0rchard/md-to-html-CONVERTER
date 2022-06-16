import re

from numpy import insert

def main():

    file = input("What file do you want to convert?\n")
    # file = input("Jaki plik chcesz przekonwertować?\n")
    # file = 'test_1.md'

    if file.endswith('.md'):

        markdown_to_html(file)

    else: 
        file = input("Incorrect extension, write the name of a markdown file you wish to convert:\n")
        # file = input("Nieprawidłowe rozszerzenie. Podaj nazwę pliku w języku markdown do konwersji:\n")

        
def markdown_to_html(file):

    md_f = open(file, 'r')
    htmlf_name = file.replace('.md', '.html')
    html_f = open(htmlf_name, 'w')
    
    # global mdt
    mdt = [['<!DOCTYPE html>'],['<html>'],['<body>'],[]]    

    for line in md_f:                                       #     rewriting markdown file into a table    #
        mdt.append(line.split())     

    mdt.append([])
    mdt.append(['</body>'])
    mdt.append(['</html>'])       


    for row in range(3, (len(mdt)-2)):                       #     fill empty rows with newline    #
        if len(mdt[row]) == 0:
            mdt[row] = ['\n']

    for row in range(3, (len(mdt)-1)):                       #     converting the table to html syntax #

        if re.match('#+', mdt[row][0]):                                     # header converter  #
            mdt[row] = convert_header(mdt, row, 0)

        elif re.match('^[\*-]+', mdt[row][0]):
            if len(mdt[row]) == 1 or re.match('[\*-]+', mdt[row][1]):       # hr converter  #
                convert_horizontal_rules(mdt, row)  

        if re.match('^[-\+\*]$', mdt[row][0]):                              # ul converter  #
            
            convert_ulist(mdt, row, 0)
        
        elif re.match('^[0-9]{1,}\.$', mdt[row][0]):                        # ol converter  #
            
            convert_olist(mdt, row, 0)             
          
    convert_table(mdt)

    convert_blockquotes(mdt)

    convert_italics(mdt)

    convert_bolds(mdt)

    convert_paragraphs(mdt)

    convert_boldits(mdt)

    convert_links(mdt)

    convert_images(mdt)

    write_to_html(mdt, html_f, htmlf_name)                                  #4     writing the converted table to .html file    #

def convert_header(mdt, row, word):
        n = mdt[row][word].count('#')
        mdt[row][word] = mdt[row][word].replace('#'*n, f'<h{n}>')
        mdt[row] += [f"</h{n}>"]
        return mdt[row] 

def convert_ulist(mdt, row, word):

    if not re.search('^[-\+\*(<ul>)(\t<li>)]', mdt[row-1][word]):
        
        mdt.insert(row, ['<ul>'])
    
    if mdt[row][0] != '<ul>':
        mdt[row][0] = mdt[row][0].replace('-','\t<li>')
        mdt[row][0] = mdt[row][0].replace('+','\t<li>')
        mdt[row][0] = mdt[row][0].replace('*','\t<li>')
        mdt[row].append('</li>')

    if len(mdt[row+1]) > 1 and re.search('#+', mdt[row+1][word+1]):       # headers in ul
        mdt[row+1][word+1] = convert_header(mdt, row+1, word+1)[1]

    if not re.search('^[-\+\*(</ul>)]', mdt[row+1][word]):
        mdt.insert(row+1, ['</ul>'])

    return mdt

def convert_olist(mdt, row, word):

    if not re.search('^[0-9]', mdt[row-1][word]) and not re.search('^[(<ol>)(\t<li>)]', mdt[row-1][word]):
        
        mdt.insert(row, ['<ol>'])
    
    # convert_ol(mdt[row])
    if mdt[row][0] != '<ol>':
        mdt[row][0] = mdt[row][0].replace(mdt[row][0], '\t<li>')
        mdt[row].append('</li>')

    if len(mdt[row+1]) > 1 and re.search('#+', mdt[row+1][word+1]):       # headers in ol #
        mdt[row+1][word+1] = convert_header(mdt, row+1, word+1)[1]

    if not re.search('^[(\d{1,}\.)(</ol>)]', mdt[row+1][word]):
        mdt.insert(row+1, ['</ol>'])

    return mdt

def convert_table(mdt):

    row = 4

    while row < len(mdt) - 4:

        if re.search('\|', mdt[row][0]):

            header = ' '.join(str(word) for word in mdt[row])
            header = re.sub(r'^\|(\s[\w\d]+\s*[\w\d]*\s)\|' , r' \n\t\t\t<th> \1 </th>', header)
            header = re.sub (r'(\s[\w\d]+\s*[\w\d]*\s)\|$' , r' \n\t\t\t<th> \1 </th>\n', header)
            header = re.sub (r'(\s[\w\d]+\s*[\w\d]*\s)\|' , r' \n\t\t\t<th> \1 </th>', header)

            mdt[row] = ['<table>\n\t<head>\n\t\t<tr>' + header + '\t\t</tr>\n\t</head>']

            row += 1
            mdt[row] = ['\t<tbody>']
            row += 1

            while re.search('\|', mdt[row][0]):

                wiersz = ' '.join(str(word) for word in mdt[row])
                wiersz = re.sub(r'^\|(\s[\w\d]+\s*[\w\d]*\s)\|' , r' \n\t\t\t<td> \1 </td>', wiersz)
                wiersz = re.sub (r'(\s[\w\d]+\s*[\w\d]*\s)\|$' , r' \n\t\t\t<td> \1 </td>\n', wiersz)
                wiersz = re.sub (r'(\s[\w\d]+\s*[\w\d]*\s)\|' , r' \n\t\t\t<td> \1 </td>', wiersz)

                mdt[row] = ['\t\t<tr>' + wiersz + '\t\t</tr>']

                row += 1

            mdt.insert(row, ['\t</tbody>\n</table>'])

        row += 1

    return mdt

def convert_blockquotes(mdt):

    row = 4

    while row < len(mdt)-2:
        
        if re.match('^>', mdt[row][0]):                                  #   blockquotes converter   #
            mdt.insert(row, ['<blockquote>'])
            row+=1

            while re.match('^>', mdt[row][0]) or re.match('^[(<\w+>)(\t<li>)]', mdt[row][0]) and row < len(mdt)-2: # ??? <\w+> fixed it??
                line = ' '.join(str(word) for word in mdt[row])
                if line != '>':
                    line = re.sub(r'^>', r'', line)

                    mdt[row] = line.split()

                    if re.search('#+', mdt[row][0]):                    # headers in blockquote #
                        mdt[row][0] = convert_header(mdt, row, 0)[0]

                    elif re.match('^[-\+\*]$', mdt[row][0]):                            # ul converter  #

                        convert_ulist(mdt, row, 0)

                    elif re.match('^[0-9]{1,}\.$', mdt[row][0]):                        #   ol converter    #

                        convert_olist(mdt, row, 0)  

                else:
                    mdt[row] = ['\n']

                row += 1

            mdt.insert(row, ['</blockquote>'])
            row+=1

        row += 1
    return mdt

def convert_paragraphs(mdt):
    row = 4

    while row < len(mdt) - 4:
        paragraf = '^[^(\n)(\t)<>]'
        if re.match(paragraf, mdt[row][0]):
            mdt[row][0] = '<p>' + mdt[row][0] 

            if not re.match(paragraf, mdt[row+1][0]):
                mdt[row][-1] += '</p>'
            else:
                row += 1
                while re.match(paragraf, mdt[row][0]) and row < len(mdt) - 2:
                    row += 1
                mdt[row-1][-1] += '</p>'  

        row += 1

    return mdt

def convert_boldits(mdt):

    for row in range(len(mdt)):
        line = ' '.join(str(word) for word in mdt[row])
        
        if re.search('^\*{1}[^\*]+\*{1}$', line) or re.search('^\*{1}[^\*]+\*{1}[^\*]', line) or re.search('[^\*]\*{1}[^\*]+\*{1}[\^*]', line) or re.search('[^\*]\*{1}[^\*]+\*{1}', line):
            # line = re.sub(r'', r'', line)
            # print("     IT")
            # print(line)
            pass

        if re.search('^\*{2}[^\*]+\*{2}$', line) or re.search('^\*{2}[^\*]+\*{2}[^\*]', line) or re.search('[^\*]\*{2}[^\*]+\*{2}[\^*]', line) or re.search('[^\*]\*{2}[^\*]+\*{2}', line):
            # line = re.sub(r'', r'', line)
            # print("     BOLD")
            # print(line)
            pass

        if re.search('^\*{3}[^\*]+\*{3}$', line) or re.search('^\*{3}[^\*]+\*{3}[^\*]', line) or re.search('[^\*]\*{3}[^\*]+\*{3}[\^*]', line) or re.search('[^\*]\*{3}[^\*]+\*{3}', line):
            # line = re.sub(r'', r'', line)
            # print("     BOLDIT")
            # print(line)
            pass


            mdt[row] = line.split()

    return mdt

def convert_italics(mdt):
    row = 4
    while row < len(mdt)-2:

        word = 0
        while word < len(mdt[row]):
            if re.search('^\*[^\*]', mdt[row][word]): #and re.search('^\*\S', mdt[row][word]):
                if re.search('[^\*]\*$', mdt[row][word]): #and re.search('\S\*$', mdt[row][word]):
                    mdt[row][word] = '<i>' + mdt[row][word][1:-1] + '</i>'
                    # print(mdt[row][word] + '   one word it')

                else:
                    mdt[row][word] = '<i>' + mdt[row][word][1:]
                    # print(mdt[row][word] + '   it starts here')

                    while not re.search('[^\*]\*$', mdt[row][word]) and word < len(mdt[row])-1:

                        word += 1
                    
                    if re.search('[^\*]\*$', mdt[row][word]): #and re.search('\S\*$', mdt[row][word]):
                        mdt[row][word] = mdt[row][word][0:-1] + '</i>'
                        # print(mdt[row][word] + '  it ends here')
                
                    else:
                        # print('multiline it')
                        word = 0

                        while not re.search('[^\*]\*$', mdt[row][word]) and row < len(mdt)-1: #and not re.search('\S\*$', mdt[row][word]) 
                            row += 1

                            while not re.search('[^\*]\*$', mdt[row][word]) and word < len(mdt[row])-2: #and not re.search('\S\*$', mdt[row][word]) 
                                word+=1
                        
                        mdt[row][word] = mdt[row][word][0:-1] + '</i>'
                        # print(mdt[row][word] + '       end of multiline it')
                            
                    word+=1
            word+=1
        row+=1

    return mdt

def convert_bolds(mdt):
    row = 3
    while row < len(mdt)-2:

        word = 0
        while word < len(mdt[row]):
            if re.search('^\*{2}[^\*]', mdt[row][word]): #and re.search('^\*{2}\S', mdt[row][word]):
                if re.search('[^\*]\*{2}$', mdt[row][word]): #and re.search('\S\*{2}$', mdt[row][word]):
                    mdt[row][word] = '<b>' + mdt[row][word][2:-2] + '</b>'
                    # print(mdt[row][word] + '   one word bold')

                else:
                    mdt[row][word] = '<b>' + mdt[row][word][2:]
                    # print(mdt[row][word] + '   bold starts here')

                    while not re.search('[^\*]\*{2}$', mdt[row][word]) and word < len(mdt[row])-1:

                        word += 1
                    
                    if re.search('[^\*]\*{2}$', mdt[row][word]): # and re.search('\S\*{2}$', mdt[row][word]):
                        mdt[row][word] = mdt[row][word][0:-2] + '</b>'
                        # print(mdt[row][word] + '  bold ends here')
                
                    else:
                        # print('multiline bold')
                        word = 0

                        while not re.search('[^\*]\*{2}$', mdt[row][word]) and row < len(mdt)-1: #and not re.search('\S\*{2}$', mdt[row][word]) 
                            row += 1

                            while not re.search('[^\*]\*{2}$', mdt[row][word]) and word < len(mdt[row])-1: #and not re.search('\S\*{2}$', mdt[row][word]) 
                                word+=1
                        
                        mdt[row][word] = mdt[row][word][0:-2] + '</b>'
                        # print(mdt[row][word] + '       end of multiline bold')
                            
                    word+=1
            word+=1
        row+=1

    return mdt

def convert_links(mdt):
    for row in range(len(mdt)):
        line = ' '.join(str(word) for word in mdt[row])
        
        if re.search('[^!]\[[\w\s\d]+\]\(.+\)', line):
            line = re.sub(r'[^!]\[([\w\s\d]+)\]\((.+)\)', r' <a href="\2">\1</a>', line)

            mdt[row] = line.split()

    return mdt

def convert_images(mdt):
    for row in range(len(mdt)):
        line = ' '.join(str(word) for word in mdt[row])
        
        if re.search('!\[[\w\s\d]+\]\(.+\)', line):
            line = re.sub(r'!\[([\w\s\d]+)\]\((.+)\)', r'<img src="\2" alt="\1">', line)

            mdt[row] = line.split()

    return mdt

def convert_horizontal_rules(mdt, row):
    
    line = ' '.join(str(word) for word in mdt[row])
    if re.match('^\*{3}|-{3}' ,line) or re.match('^[\*|\s]{4,}|[-|\s]{4,}' ,line):

        mdt[row] = ['<hr />']

def write_to_html(mdt, html_f, htmlf_name):

    for row in range(len(mdt)):                             

        converted_line = ' '.join(str(word) for word in mdt[row])
        
        if mdt[row] == '\n':
            html_f.write('\n')
        
        elif mdt[row] != mdt[-1]:                     
            html_f.write(converted_line + '\n')
        
        else:
            html_f.write(converted_line)

    print(f'\nConverted file has been saved to: {htmlf_name}')

main()