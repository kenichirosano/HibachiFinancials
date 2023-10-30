import hi_Concept_Class as Concept
import hi__EXT_ETtree as hi_EXT_ET
import hi_TaxonomySchema_Class as TaxonomySchema

def getConcept_OnPython(listOfDTS, listOfConcept):
    '''
    Get all the concepts from listOfDTS and put them in to listOfConcept
    '''
    uniquePathList = [] # List to hold links that is already read
    for taxonomy_schema in listOfDTS:
        # Read only if the path is taxonomy schema
        if taxonomy_schema.__class__.__name__ == 'TaxonomySchema':
            if (taxonomy_schema.isFragmentID_only != True): # If the path is not fragment ID only
                if taxonomy_schema.tag in ('schemaRef','import','include'):
                    file_path = taxonomy_schema.searchablePath # Get the file path
                    # To read the files only one time, store the path already read into uniquePathList
                    if file_path in uniquePathList:
                        continue
                    else:
                        root = hi_EXT_ET.etree_parse_remove_NS(file_path) # Parse the file
                        uniquePathList.append(file_path) # Add to the already read file list
                        if root != None: # If there's no tree from the path, end the process
                            # Get defining elements part with substitutionGroup attribute item or tuple
                            for concept_element in root.iter('element'):
                                substitutionGroup = concept_element.get('substitutionGroup') # Specification 4.6
                                if substitutionGroup: # If the element has substitutionGroup attritube
                                    if (('item' in substitutionGroup) or ('tuple' in substitutionGroup)): # If the element has item or tuple as head
                                        listOfConcept.append(Concept.Concept(file_path, concept_element)) #Add to the xlink list
