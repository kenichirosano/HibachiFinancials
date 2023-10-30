# -*- coding: utf-8 -*-
import hi__EXT_XLink as hi_EXT_XL

def returnElementAsDict(currentElement, dictOfAttributes):
    '''
    Function to return dictionary containing attributes for
    <labelLink> <presentationLink> <definitionLink> <calculationLink> <referenceLink>
    '''
    dictInside = dictOfAttributes.copy()
    # Get the attributes of the child element handling the exceptions
    for key in dictInside.keys():
        if key == 'tag':
            dictInside[key] = currentElement.tag
        elif key == 'childList':
            pass
        elif key == 'originalPath':
            dictInside[key] = hi_EXT_XL.getOriginalPath(currentElement)
        else:
            dictInside[key] = currentElement.get(key)

    return dictInside

# Function to return dictionary containing attributes for <loc> <arc> <label>
def returnChildElementListOfDict(fileName, parentElement, childElementTagList, dictOfAttributes):
    listOfDict = []

    for empty_Var, temp_tagName in enumerate(childElementTagList):  # get the tag one by one
        for childElement in parentElement.findall(temp_tagName):    # search for the element with the tag
            dictInside = dictOfAttributes.copy()
            for key in dictInside.keys():
                if key == 'tag':
                    dictInside[key] = childElement.tag
                elif key == 'content':
                    dictInside[key] = childElement.text
                elif key == 'originalPath': # get the value in @href attibute
                    dictInside[key] = hi_EXT_XL.getOriginalPath(childElement)
                    dictInside['searchablePath'] = hi_EXT_XL.createSearchablePath(fileName, dictInside[key])[1]
                    dictInside['fragment_ID'] = hi_EXT_XL.split_Fragment_ID(dictInside[key])[1]
                elif key == 'fragment_ID' or key == 'searchablePath':
                    pass
                else: #Get the values in other attributes one by one
                    dictInside[key] = childElement.get(key)

            listOfDict.append(dictInside) # Add to the list             

    return listOfDict
