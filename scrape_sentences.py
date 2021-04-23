# Scrape gloss_sentences, tokens
# Scrape their vidoes
# https://dai.cs.rutgers.edu/dai/s/searchresult?signName=book&full_partial=0&hand=0%2C1&all_signs=all_signs_egcl&SignTag=1&SignTag=5&SignTag=3&SignTag=9&incl_comp=incl_non_comp&datasource=678922&datasource=798401&datasource=792081&datasource=678925&datasource=744398&datasource=678927&datasource=678928&datasource=798400&datasource=678930&datasource=678931&datasource=744399&datasource=678933&datasource=678934&datasource=678935&datasource=678936&datasource=678937&datasource=744400&datasource=678939&datasource=798404&datasource=798403&datasource=678942&datasource=678943&datasource=678944&datasource=678945&datasource=678946&datasource=678947&datasource=678948&datasource=678949&datasource=678950&datasource=678951&datasource=678952&datasource=678953&datasource=678954&datasource=678955&datasource=678956&datasource=678957&datasource=678958&datasource=678959&datasource=678960&datasource=678961&datasource=744401&datasource=678963&datasource=798402&dspdatasource=678989&dspdatasource=678990&dspdatasource=678991&dspdatasource=678992&dspdatasource=678993&dspdatasource=678994&dspdatasource=678995&dspdatasource=678996&dspdatasource=678997&dspdatasource=678998&dspdatasource=790834&dspdatasource=679000&dspdatasource=679001&dspdatasource=679002&dspdatasource=679003&dspdatasource=679004&dspdatasource=679005&dspdatasource=679006&participant=23&participant=24&participant=6&participant=5&participant=2&participant=25&participant=26&participant=7&participant=8&participant=4&participant=27&participant=9&participant=10&participant=11&participant=1&participant=3&participant=28&participant=12&participant=29&participant=13&video_views=noCare&color=noCare&sleeves=noCare&glasses=noCare&minOccur=-1&data_source=&color=noCare&sleeves=noCare&glasses=noCare&allBox=noCare&results_view=front&resultsPerPage=25&id_dh_start=&id_nd_start=&id_nd_end=&id_dh_end=&canonical_sign_id=152&signName=BOOK

import requests
from bs4 import BeautifulSoup
import urllib.request
import os

url = "https://dai.cs.rutgers.edu/dai/s/searchresult?page_num=2&page_num=1&page_num=2&signName=House&full_partial=0&hand=0%2C1&all_signs=all_signs_egcl&SignTag=1&SignTag=5&SignTag=3&SignTag=9&incl_comp=incl_non_comp&datasource=678922&datasource=798401&datasource=792081&datasource=678925&datasource=744398&datasource=678927&datasource=678928&datasource=798400&datasource=678930&datasource=678931&datasource=744399&datasource=678933&datasource=678934&datasource=678935&datasource=678936&datasource=678937&datasource=744400&datasource=678939&datasource=798404&datasource=798403&datasource=678942&datasource=678943&datasource=678944&datasource=678945&datasource=678946&datasource=678947&datasource=678948&datasource=678949&datasource=678950&datasource=678951&datasource=678952&datasource=678953&datasource=678954&datasource=678955&datasource=678956&datasource=678957&datasource=678958&datasource=678959&datasource=678960&datasource=678961&datasource=744401&datasource=678963&datasource=798402&dspdatasource=678989&dspdatasource=678990&dspdatasource=678991&dspdatasource=678992&dspdatasource=678993&dspdatasource=678994&dspdatasource=678995&dspdatasource=678996&dspdatasource=678997&dspdatasource=678998&dspdatasource=790834&dspdatasource=679000&dspdatasource=679001&dspdatasource=679002&dspdatasource=679003&dspdatasource=679004&dspdatasource=679005&dspdatasource=679006&participant=23&participant=24&participant=6&participant=5&participant=2&participant=25&participant=26&participant=7&participant=8&participant=4&participant=27&participant=9&participant=10&participant=11&participant=1&participant=3&participant=28&participant=12&participant=29&participant=13&video_views=noCare&color=noCare&sleeves=noCare&glasses=noCare&minOccur=-1&data_source=&color=noCare&sleeves=noCare&glasses=noCare&allBox=noCare&results_view=front&resultsPerPage=25&id_dh_start=&id_nd_start=&id_nd_end=&id_dh_end=&canonical_sign_id=63&signName=HOUSE"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
vid = soup.find_all(id="ds_26")

count = 1
roughgloss_boxes = soup.find_all("td", class_="helpBod roughgloss")
video_boxes = soup.find_all("video")

gloss_sentences = ""
eng_sentences = ""
video_links = ""

have_eng_sentence_index = []

for i in range(len(roughgloss_boxes)):
    # Skip boxes that don't have english sentences
    box_text = str(roughgloss_boxes[i])
    if(box_text.find("engl trans:") != -1):
        have_eng_sentence_index.append(i)
        #print(box_text)
        gloss_sentence_box = box_text[box_text.find("dh:")+1:box_text.find("dh shape:")]
        gloss_sentence = ""
        while(gloss_sentence_box.find("<u>") != -1):
            gloss = gloss_sentence_box[gloss_sentence_box.find("<u>")+3:gloss_sentence_box.find("</u>")]
            # The gloss in the query will be saved in a span style
            if("span style" in gloss):
                gloss_in_span = gloss[gloss.find(">")+1: gloss.rfind("<")]
                gloss_after_span = gloss[gloss.find("</span>")+7:]
                gloss = gloss_in_span + gloss_after_span
            if(gloss != "TABLE"):
                gloss_sentence += gloss + " "
            # Removes gloss that was just added from gloss_sentence_box 
            gloss_sentence_box = gloss_sentence_box[gloss_sentence_box.find("</u>")+4:]
        
        gloss_sentences += gloss_sentence + "\n"

        # Adds english translations
        eng_text = box_text[box_text.find("engl trans:")+12:box_text.find("</pre>")].strip()
        eng_sentences += eng_text + "\n"

# Adds youtube links
for k in range(len(video_boxes)):
    if(k in have_eng_sentence_index):
        #print(box) #  MM-sentences-062818_TC_hb U:DEER # sign_63320
        video_link = video_boxes[k].find('source').get('src')
        # Only saves front view video and removes src links to the icon images of the utterance vidoes 
        if('ss3front' in video_link and 'sign_' not in video_link):
            video_links += video_link + "\n"

with open("gloss_sentences.txt", "a") as myfile:
    myfile.write(gloss_sentences)

with open("eng_sentences.txt", "a") as myfile:
    myfile.write(eng_sentences)

with open("video_links.txt", "a") as myfile:
    myfile.write(video_links)
