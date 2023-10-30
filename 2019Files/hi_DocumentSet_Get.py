# -*- coding: utf-8 -*-

def getDocumentSet(root_ElementTree, fileName):
    '''
    Return a dictionay containing edinet code and filing date.
    '''

    list_of_EdinetCode = []
    dict_of_DocumentSet = {
        'edinetCode':None
        ,'filingDate':None
        ,'documentType':'Yuho'
        ,'repFileName': fileName
    }

    # Get edinet code only if the file has only 1 edinet code
    # Edinet code is stored in <identifier> element in the form of [Edinet code]-[追番]
    for identifier_ElementTree in root_ElementTree.iter('identifier'):
        list_of_EdinetCode.append(identifier_ElementTree.text.split("-")[0])

    if len(set(list_of_EdinetCode)) == 1:
        dict_of_DocumentSet['edinetCode'] = list_of_EdinetCode[0]

    else:
        print ('Error: Multiple Edinet Codes.')
        return None

    # Get filingDate
    for context_ElementTree in root_ElementTree.findall('context'):

        if context_ElementTree.get('id') == 'FilingDateInstant':

            for period_ElementTree in context_ElementTree.findall('period'):

                for instant_ElementTree in period_ElementTree.findall('instant'):
                    dict_of_DocumentSet['filingDate'] = instant_ElementTree.text

    return dict_of_DocumentSet
