``br_locations`` - Cities and States of Brazil Python Lib (IBGE Info)
#######################################################


Description
***********

Cities and States of Brazil Python Lib  based on IBGE Info.


Requirements
************

::

    Python 3


Install:
########

::

    pip install br_locations


Usage
#####

>>> from br_locations.base import br_locale_info

list_states (@property)
*********************
Returns a list of all states in alphabetical order (abbreviations)

|

Syntax:

- br_locale_info.list_states

|

*Exemple:*

>>> print (br_locale_info.list_states)
['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

----

list_all_cities (@property)
*********************
Returns a list of all cities in all states

|

Syntax:

- br_locale_info.list_all_cities

|

*Exemple:*

>>> print (br_locale_info.list_all_cities)
[['Acrelândia', 'Assis Brasil', 'Brasiléia', 'Bujari', 'Capixaba', ...]


----

dict_states (@property)
*********************
Returns a dict of all states with IBGE code and full name

|

Syntax:

- br_locale_info.dict_states

|

*Exemple:*

>>> print (br_locale_info.dict_states)
{'AC': {'code': 12, 'name': 'Acre'}, 'AL': {'code': 27, 'name': 'Alagoas'}, 'AP': {'code': 16, 'name': 'Amapá'}, 'AM': {'code': 13, 'name': 'Amazonas'}, 'BA': {'code': 29, 'name': 'Bahia'}, 'CE': {'code': 23, 'name': 'Ceará'}, 'DF': {'code': 53, 'name': 'Distrito Federal'}, 'ES': {'code': 32, 'name': 'Espírito Santo'}, 'GO': {'code': 52, 'name': 'Goiás'}, 'MA': {'code': 21, 'name': 'Maranhão'}, 'MT': {'code': 51, 'name': 'Mato Grosso'}, 'MS': {'code': 50, 'name': 'Mato Grosso do Sul'}, 'MG': {'code': 31, 'name': 'Minas Gerais'}, 'PR': {'code': 41, 'name': 'Paraná'}, 'PB': {'code': 25, 'name': 'Paraíba'}, 'PA': {'code': 15, 'name': 'Pará'}, 'PE': {'code': 26, 'name': 'Pernambuco'}, 'PI': {'code': 22, 'name': 'Piauí'}, 'RN': {'code': 24, 'name': 'Rio Grande do Norte'}, 'RS': {'code': 43, 'name': 'Rio Grande do Sul'}, 'RJ': {'code': 33, 'name': 'Rio de Janeiro'}, 'RO': {'code': 11, 'name': 'Rondônia'}, 'RR': {'code': 14, 'name': 'Roraima'}, 'SC': {'code': 42, 'name': 'Santa Catarina'}, 'SE': {'code': 28, 'name': 'Sergipe'}, 'SP': {'code': 35, 'name': 'São Paulo'}, 'TO': {'code': 17, 'name': 'Tocantins'}}


------

list_cities (method)
*******************
Returns a list of all cities in a state.

|

Syntax:

- br_locale_info.list_cities('XX'),
- br_locale_info.list_cities(abbr='XX'),
- br_locale_info.list_cities(code='NN')

|

where:


abbr = State abbreviation, e.g.: São Paulo = SP, Rio de Janeiro = RJ

code = State code at IBGE, e.g.: Amapá = 12,  Acre = 16

|

*Exemple:*

>>> print(br_locale_info.list_cities('AC'))
['ACRELÂNDIA', 'ASSIS BRASIL', 'BRASILÉIA', 'BUJARI', 'CAPIXABA', ...]

------


Lib Dev Information
#####

:Authors:
    Arthur Fortes

:Version: 0.1.0 of 10/2022
