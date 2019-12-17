'''
We are using spacy module for Named Entity Recognition.
pip install spacy

For en_core_web_sm, we need to install spacy and then run:
python -m spacy download en
'''
import en_core_web_sm

nlp = en_core_web_sm.load()

SYMBOL_TO_NAME = [
    {'symbol': 'C', 'name': 'CITIGROUP INC'},
    {'symbol': 'C', 'name': 'CITI BANK'},
    {'symbol': 'GOOGL', 'name': 'ALPHABET INC CLASS A'},
    {'symbol': 'GOOG', 'name': 'ALPHABET INC CLASS C'},
    {'symbol': 'GOOG', 'name': 'GOOGLE'},
    {'symbol': 'DB', 'name': 'DEUTSCHE BANK AG'},
    {'symbol': 'WFC', 'name': 'WELLS FARGO & CO'},
    {'symbol': 'GS', 'name': 'GOLDMAN SACHS GROUP INC'},
    {'symbol': 'JPM', 'name': 'JPMORGAN CHASE & CO'},
    {'symbol': 'JPM', 'name': 'J. P. MORGAN CHASE'},
    {'symbol': 'BAC', 'name': 'BANK OF AMERICA CORP'},
    {'symbol': 'BCS', 'name': 'BARCLAYS PLC'},
    {'symbol': 'MS', 'name': 'MORGAN STANLEY'},
    {'symbol': 'USB', 'name': 'U.S. BANCORP'},
    {'symbol': 'USB', 'name': 'US BANCORP'},
    {'symbol': 'GSK', 'name': 'GLAXOSMITHKLINE PLC'},
    {'symbol': 'UBS', 'name': 'UBS GROUP AG'},
]

NAME_TO_SYMBOL = {}
for sym in SYMBOL_TO_NAME:
    NAME_TO_SYMBOL[sym['name']] = sym['symbol']

def get_symbol(company_name):
    '''
    It returns stock symbol of the company, given in parameter.
    :param company_name: company name as str
    :return: stock symbol if company is found, otherwise an empty string
    '''
    company_name = company_name.upper()
    print('company_name:', company_name)
    sym = NAME_TO_SYMBOL.get(company_name, '')
    if not sym:
        for k in SYMBOL_TO_NAME:
            if company_name in k['name']:
                return k['symbol']
    return sym


def get_stock_symbol_for_entity(text):
    '''
    Pass a text to this and it will perform Named Entity Recognition on the text, try to figure
    out the Organizations in the text.
    :param text:
    :return:
    '''
    doc = nlp(text)
    sym = ''
    for X in doc.ents:
        if X.label_ == 'ORG':
            sym = get_symbol(X.text)
            if sym:
                break
    return sym


if __name__ == '__main__':
    print(get_stock_symbol_for_entity('European authorities fined Google a record $5.1 billion on Wednesday '
               'for abusing its power in the mobile phone market and ordered the company to alter its practices'))
    print('-' * 5)
    print(get_stock_symbol_for_entity('Citigroup hit hardest as EU Fines Banks $1.2 Billion Over FX'))
    print('-' * 5)
    print(get_stock_symbol_for_entity('Wells Fargo in hot water again, may refund customers for account service fees Business'))
    print('-' * 5)
    print(get_stock_symbol_for_entity("Wells Fargo’s $110 Million Settlement"))
    print('-' * 5)
