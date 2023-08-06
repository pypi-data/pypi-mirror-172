``br_gender`` - Gender by name Python Lib (IBGE Info)
#######################################################


Description
***********

br_gender predicts gender from Brazilian first names using data from the Instituto Brasileiro de Geografia e Estatistica’s 2010 Census.


Requirements
************

::

    Python 3


Install:
########

::

    pip install br_gender


Usage
#####

>>> from br_gender.base import br_gender_info

get_gender (method)
*******************
Returns gender of name. Possible results: Male, Famele, Unisex and Unk (for unknown cases).

|

Syntax:

- br_gender_info.get_gender('name')


|

*Exemple:*

>>> print(br_gender_info.get_gender('Arthur'))
Male

>>> print(br_gender_info.get_gender('Carla'))
Female

>>> print(br_gender_info.get_gender('Ariel'))
Unisex

>>> print(br_gender_info.get_gender('Atwesbwwhiel'))
Unk

------

get_gender_by_majority (method)
*******************
Returns gender of name. Possible results: Male, Famele and Unk (for unknown cases). **In this case, the function does not return 'unisex' and chooses to return the gender based on the number of examples per name.**

|

Syntax:

- br_gender_info.get_gender('name')


|

*Exemple:*

>>> print(br_gender_info.get_gender('Arthur'))
Male

>>> print(br_gender_info.get_gender('Carla'))
Female

>>> print(br_gender_info.get_gender('Ariel'))
Unisex

>>> print(br_gender_info.get_gender('Atwesbwwhiel'))
Unk

------

Lib Dev Information
#####

:Authors:
    Arthur Fortes

:Version: 0.1.0 of 10/2022
