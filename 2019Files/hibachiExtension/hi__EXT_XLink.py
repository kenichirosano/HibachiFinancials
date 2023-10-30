import os
import re

def createSearchablePath(fileName, hrefPath):
    '''Identify the link path types
    If the path has fragment ID, this returns only before FID as newpath.'''
    jfsaPath = 'http://disclosure.edinet-fsa.go.jp/'
    xbrlorgPath = 'http://www.xbrl.org/'
    if hrefPath != None:
        if jfsaPath in hrefPath:# If the path contains JFSA path
            newPath = split_Fragment_ID(remove_JFSA_path(hrefPath))[0]
            return 'JFSA', newPath
        elif xbrlorgPath in hrefPath: # If the path contains XBRL ORG path
            newPath = split_Fragment_ID(remove_XBRLORG_path(hrefPath))[0]
            return 'XBRLORG', newPath
        elif (hrefPath[0] == '#'): # If the path is fragment ID only
            return 'FIDONLY', fileName
        else:
            if '/' in fileName:# If the file being read is in a different path than the starting point file
                newPath = removeOnlyFilenameFromPath(fileName, hrefPath) + remove_relative_parent_path(split_Fragment_ID(hrefPath)[0])
                return 'FILES', newPath
            else:
                return 'OTHERS', hrefPath
    else: return 'No href', None

def remove_JFSA_path(path):
    '''Remove JFSA link path'''
    jfsaPath = 'http://disclosure.edinet-fsa.go.jp/'
    if jfsaPath in path:# If the path contains JFSA path
        path = re.split(jfsaPath, path)[1] #Get the latter part of the xpath
    return path

def remove_XBRLORG_path(path):
    '''Remove JFSA link path'''
    xbrlorgPath = 'http://www.xbrl.org/'
    if xbrlorgPath in path:# If the path contains JFSA path
        path = re.split(xbrlorgPath,path)[1] #Get the latter part of the xpath
    return path

def removeOnlyFilenameFromPath(filePath, hrefPath):
    '''Remove the filename from the fileName and return the fileName before the filename
        (ladderCount argument is the number of ''../' the href has in the fileName.)
    '''
    hrefPath_ladderCount = hrefPath.count('../')
    filePath_list = filePath.rsplit('/')
    if len(filePath_list) > 1: # If the fileName contains slash
        listWithoutFilePath = ''
        for i in range(0, len(filePath_list) - 1 - hrefPath_ladderCount) : # Remove the filename only
            listWithoutFilePath += filePath_list[i]
            listWithoutFilePath += '/'
        pathBeforeFilename = ''.join(map(str, listWithoutFilePath)) # Convert list to string
        return pathBeforeFilename
    else: # When only file name
        return None
    return

def remove_relative_parent_path(path): # Remove ../ from link path

    matchPosition = re.search('\.\./',path)
    if matchPosition:
        newPath = path.replace('../','') # delete palent pathes
    else: newPath = path
    return newPath

def split_Fragment_ID(path):
    '''Split fragment id in the path if it has a fragment id'''
    if path != None:
        path_list = path.split('#')
        if len(path_list) > 1: # If the path contains hash
            return path_list[0], path_list[1]
        else:
            return path_list[0], None
    else: return None, None

def getOriginalPath(element):
    '''Get simple link path'''
    if (element.tag == 'import') or (element.tag == 'include'):
        return element.get('schemaLocation')
    else:
        return element.get('href')

def add_relative_parent_path(path):
    # Add relative path to link path
    newPath = '../' + path # add the relative parent path at the start
    return newPath # Return new path

def isUniquePath(listOfDTS, new_path):
    '''Return True if the path is new and False if it is already in listOfDTS.'''
    for taxonomySchema in listOfDTS:
        if taxonomySchema.__class__.__name__ == 'TaxonomySchema':
            if (str(taxonomySchema.searchablePath) == str(new_path)): return False
    return True
