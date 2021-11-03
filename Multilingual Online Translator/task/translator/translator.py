import requests
from bs4 import BeautifulSoup
import sys


def extract_translations(from_which_language, to_which_language, sample, amount):
    url = f'https://context.reverso.net/translation/{from_which_language.lower()}-{to_which_language.lower()}/{sample}'
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if page.status_code == 200:
        pass
    elif page.status_code == 404:
        print(f'Sorry, unable to find {sample}')
        sys.exit()
    else:
        print('Something wrong with your internet connection')
        sys.exit()

    page_soup = BeautifulSoup(page.content, 'html.parser')
    translations_block = page_soup.find('div', {'id': 'translations-content'})

    print(f'{to_which_language.capitalize()} Translations:')
    f.write(f'{to_which_language.capitalize()} Translations:\n')

    translations_block = translations_block.find_all('a', {'class': 'translation'})

    for translation in translations_block[0:amount]:
        translation = translation.text
        translation = translation.strip()
        f.write(translation + '\n')
        print(translation)

    f.write('\n')
    print()

    f.write(f'{to_which_language.capitalize()} Examples:\n')
    print(f'{to_which_language.capitalize()} Examples:')

    examples_block = page_soup.find('section', {'id': 'examples-content'})
    examples_block = examples_block.find_all('div', {'class': 'example'})
    examples_src_block = []
    examples_trg_block = []
    for result in examples_block[0:amount]:
        examples_src_block.append(result.find('div', {'class': 'src'}))
        examples_trg_block.append(result.find('div', {'class': 'trg'}))

    for src, trg in zip(examples_src_block, examples_trg_block):
        src = src.text
        src = src.strip()
        trg = trg.text
        trg = trg.strip()
        print(src)
        print(trg)
        print()
        f.write(src + '\n')
        f.write(trg + '\n\n')
    return


args = sys.argv

lang_list = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
             'Portuguese', 'Romanian', 'Russian', 'Turkish']

chosen_lang_src, chosen_lang_trg, word = args[1:]

check_lang = (chosen_lang_trg, chosen_lang_src)
for lang in check_lang:
    if lang.capitalize() in lang_list or lang == 'all':
        pass
    else:
        print(f"Sorry, the program doesn't support {lang}")
        sys.exit()

number = 5

f = open(f'{word}.txt', 'w', encoding='utf-8')

if chosen_lang_trg == 'all':
    number = 1
    for lang in lang_list:
        if lang.lower() == chosen_lang_src.lower():
            continue
        else:
            extract_translations(chosen_lang_src, lang, word, number)
else:
    extract_translations(chosen_lang_src, chosen_lang_trg, word, number)

f.close()
