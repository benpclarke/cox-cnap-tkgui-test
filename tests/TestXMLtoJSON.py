# From StackOverflow
# https://stackoverflow.com/questions/191536/converting-xml-to-json-using-python

from xml.dom import minidom
import json
import os
from tkinter.filedialog import askopenfilename
import tkinter as tk


def parse_element(element):
    dict_data = dict()
    if element.nodeType == element.TEXT_NODE:
        dict_data['data'] = element.data
    if element.nodeType not in [element.TEXT_NODE, element.DOCUMENT_NODE,
                                element.DOCUMENT_TYPE_NODE]:
        for item in element.attributes.items():
            dict_data[item[0]] = item[1]
    if element.nodeType not in [element.TEXT_NODE, element.DOCUMENT_TYPE_NODE]:
        for child in element.childNodes:
            child_name, child_dict = parse_element(child)
            if child_name in dict_data:
                try:
                    dict_data[child_name].append(child_dict)
                except AttributeError:
                    dict_data[child_name] = [dict_data[child_name], child_dict]
            else:
                dict_data[child_name] = child_dict
    return element.nodeName, dict_data


def openFile(fileXt, prompt='Select file'):
    # Use tkinter library to select file
    lenFileXt = len(fileXt) - 1
    rootfilechooser = tk.Tk()
    fileWLEN = askopenfilename(title=prompt,
                               filetypes=(('text files', fileXt), ('all files', '*.*')))
    dirWLEN = os.path.split(fileWLEN)[0]
    fileName = os.path.split(fileWLEN)[1][:-lenFileXt]
    rootfilechooser.destroy()

    # handle cancellation by user
    if fileWLEN == '':
        print('No file selected by user. Terminating process')
        return ['', '', '']
    else:
        print('Selected file: ' + fileWLEN)
        return [fileName, fileWLEN, dirWLEN]


def openRawFile(fileXt='*.txt', prompt='Select file'):
    fileName, fileWLEN, dirWLEN = openFile(fileXt, prompt)
    return [fileName, fileWLEN, dirWLEN]


if __name__ == '__main__':
    fileName, fileXML, dirXML = openRawFile('.xml')
    dom = minidom.parse(fileXML)
    fileJSON = dirXML + '/' + fileName + 'json'
    with open(fileJSON, 'w') as fileWrite:
        json.dump(parse_element(dom), sort_keys=True, indent=4, fp=fileWrite)
        fileWrite.close()
    print('File saved as: ' + fileJSON)
