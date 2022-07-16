#!/usr/bin/env python
# ===
# Devanagari syllabizer

# 01-May-2021,  V1.0,  Chaitanya Lakkundi,  Initial devanagari syllabizer
# 04-May-2021,  V2.0,  Chaitanya Lakkundi,  Syllabizer Type 1 (cut at swaras) and Type 2 (laghu guru as we pronounce), get laghu guru with T2 input

# ===

import re

# ॠ is a special character not included within the unicode range of अ-औ
ach_re = r"([अ-औ]|ॠ)"
hal_re = r"[क-ह]"

aa_sign_re = "का"[-1]
au_sign_re = "कौ"[-1]
LLi_sign_re = "कॢ"[-1]

ach_sign_re = r"[{0}-{1}{2}{3}{4}{5}{6}{7}]".format(aa_sign_re, au_sign_re, LLi_sign_re, "कं"[-1], "कः"[-1], "कॅ"[-1], "कऀ"[-1], "कँ"[-1])

dirgha_ach_set = {"कं"[-1], "कः"[-1], 'आ', 'ा', 'ई', 'ी', 'ऊ', 'ू', 'ॠ', 'ॄ', 'ए', 'े', 'ऐ', 'ै', 'ओ', 'ो', 'औ', 'ौ'}
# hrasva_ach_set = {"अ", "इ", "उ", "ऋ", "ऌ", "ि", "ु", 'ृ'}

avagraha = "ऽ"
halanta = "क्"[-1]
om = "ॐ"
danda = "।"
double_danda = "॥"

digits_re = r"[०-९]"

# name = "मम नाम चैतन्यः । अहम् अस्मि । सः आगच्छति ।"
name = "एषोऽस्त्रान् विविधान् वेत्ति त्रैलोक्ये सचराचरे।"

ach_in_name = re.findall(ach_re, name)
hal_in_name = re.findall(hal_re, name)
sign_in_name = re.findall(ach_sign_re, name)

print(ach_in_name, hal_in_name, sign_in_name)

# a syllable always ends with an ach_sign or an अकार (implicit)
# a syllable can contain a hal or many hals separated by halanta

dev_syllable_re = ach_re + "|" + hal_re

def get_syllables_T12(sentence, pronounce=False):
    syll_in_name = re.findall(r"[क-हअ-औॠ]{0}*{1}?".format(ach_sign_re, halanta), sentence)
    vyanjanas = syll_in_name[:]
    
    # Syllabize type 1 (default), pronounce=False
    # Cut at swaras

    # Syllabize type 2, pronounce=True
    # Output for laghu guru syllables as we pronounce
    
    start_i = 0
    if pronounce:
        start_i = 1

    for i in range(len(syll_in_name)):
      try:

        while syll_in_name[i + start_i][-1] == halanta:
            syll_in_name[i] += syll_in_name[i+1]
            del syll_in_name[i+1]

      except:
        pass

    return syll_in_name, vyanjanas

def get_laghu_guru_T2(word):
    out = []
    start_i = 0

    # if the first ele does not contain swaras, it is invalid
    wch = word[0].count(halanta)
    if len(word[0])-wch == wch:
        out.append("-")
        start_i = 1

    for w in word[start_i:]:
        if w[-1] in dirgha_ach_set or w[-1] == halanta:
            out.append("G")
        else:
            out.append("L")
    return out, len(out)

words = ["सत्री", "स्त्री", "दृष्ट्वा", "उक्तवत्यः", "हिरण्यकशिपुर्नाम", "नरसिंहावतारं", "अखिलोपि", "आरब्धवान्", "राक्षससंहारम्", "इन्द्रप्रस्थनगरात्", "युधिष्ठिरः", "सङ्कल्पम्", "श्रीकृष्णं", "ज्ञानवृद्धः", "रुक्मिणीं", "बन्धुद्रोहो", "राजसूययागाय", "श्रीकृष्णस्यागमनवृत्तान्तः", "श्रीकृष्णस्य", "शत्रुः", "मूर्खः", "त्वं", "युद्धम्", "मतिः", "गुरुः", "गुरुं", "कार्त्स्न्यम्", "स गच्छति", "अत्र प्रविशति", "सम्प्राप्तिः"]

shlokas = [
"येनाक्षरसमाम्नायमधिगम्यमहेश्वरात्", 
"एषोऽस्त्रान् विविधान् वेत्ति त्रैलोक्ये सचराचरे।", 
"पश्य लक्ष्मण यक्षिण्या भैरवं दारुणं वपुः। भिद्येरन् दर्शनादस्या भीरूणां हृदयानि च॥ १०॥", 
"अश्मवर्षं विमुञ्चन्ती भैरवं विचचार सा। ततस्तावश्मवर्षेण कीर्यमाणौ समन्ततः॥२०॥ दृष्ट्वा गाधिसुतः श्रीमानिदं वचनमब्रवीत्। अलं ते घृणया राम पापैषा दुष्टचारिणी॥२१॥ यज्ञविघ्नकरी यक्षी पुरा वर्धेत मायया। वध्यतां तावदेवैषा पुरा संध्या प्रवर्तते॥२२॥ रक्षांसि संध्याकाले तु दुर्धर्षाणि भवन्ति हि।"
]

for w in words:
    wt1, vyanjanas = get_syllables_T12(w)
    wt2 = get_syllables_T12(w, pronounce=True)[0]

    print(w, "\n", vyanjanas, "\n", wt1, "\n", wt2, "\n", get_laghu_guru_T2(wt2), "\n", sep="")