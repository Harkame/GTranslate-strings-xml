import os
import xml.etree.ElementTree as ET
import shutil
from pathlib import Path
from googletrans import Translator

# ask user for paramters, apply defaults
INFILE = input("Enter input filename: [default: strings.xml]\n")
INPUTLANGUAGE = input("\nEnter source language: [default: en]\n")
OUTPUTlangs = input(
    "\nEnter output language(s): (space separated) \n\n").split()

if not OUTPUTlangs:
    OUTPUTlangs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "rw", "ko", "ku",
                   "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
    OUTPUTlangs.remove(INPUTLANGUAGE)
if not INFILE:
    INFILE = "strings.xml"
if not INPUTLANGUAGE:
    INPUTLANGUAGE = "en"

print("=================================================\n\n")

OUTDIRECTORY = Path('out')
if OUTDIRECTORY.exists():
    shutil.rmtree("out")
os.makedirs("out")


def perform_translate(OUTPUTLANGUAGE):
    translator = Translator()

    OUTFILE = "out/strings-{OUTPUTLANGUAGE}.xml".format(
        OUTPUTLANGUAGE=OUTPUTLANGUAGE)

    tree = ET.parse(INFILE)
    root = tree.getroot()

    print(OUTPUTLANGUAGE + "...\n")

    for i in range(len(root)):
        isTranslatable = root[i].get('translatable')
        if(root[i].tag == 'string') & (isTranslatable != 'false'):

            totranslate = root[i].text
            if(totranslate is not None):
                root[i].text = translator.translate(
                    totranslate, src=INPUTLANGUAGE, dest=OUTPUTLANGUAGE).text

        if(root[i].tag == 'string-array'):
            for j in range(len(root[i])):
                isTranslatable = root[i][j].get('translatable')
                if(root[i][j].tag == 'item') & (isTranslatable != 'false'):

                    totranslate = root[i][j].text
                    if(totranslate != None):
                        root[i][j].text = translator.translate(
                            totranslate, src=INPUTLANGUAGE, dest=OUTPUTLANGUAGE).text
                    if len(root[i][j]) != 0:
                        for element in range(len(root[i][j])):
                            root[i][j][element].text = " " + translator.translate(
                                root[i][j][element].text, src=INPUTLANGUAGE, dest=OUTPUTLANGUAGE).text
                            root[i][j][element].tail = " " + translator.translate(
                                root[i][j][element].tail, src=INPUTLANGUAGE, dest=OUTPUTLANGUAGE).text

    tree.write(OUTFILE, encoding='utf-8')


if __name__ == '__main__':
    for OUTPUTLANGUAGE in OUTPUTlangs:
        perform_translate(OUTPUTLANGUAGE)
    print("done")
