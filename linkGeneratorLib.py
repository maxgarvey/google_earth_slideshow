#this script is a library that I made to handle the various functions involved in making the kml
#and getting all of the links, as well as getting the user's input and processing it, to a degree.
import WeoGeoAPI
import BeautifulSoup
import random
import getpass #trying this for password input
baseUrlString = 'http://market.weogeo.com/'     #baseUrlString is a string we will need later on, for the api calls
username = ''
password = ''
http = WeoGeoAPI.httpController( )              #an httpController object to handle the requests and such
                                                #get params asks the user for their input on a few relevant questions
def getParams( ):
    paramsEntered = False                       #this boo will be turned true if the parameters entered are valid
    validSubDomain = False
    while not paramsEntered:                    #this part will take some params
        try:
            print "enter your parameters:"
            while not validSubDomain:
                subdomain = raw_input("enter your desired subdomain ('http://market.weogeo.com' is default):\n")
                if subdomain == '':
                    subdomain = 'market.weogeo.com'
                thisUsername = raw_input("enter your username:\n")
                thisPassword = getpass.getpass("enter your password:\n") #haven't tested this yet
                urlExt = 'datasets.json?page=1&east=0&north=0&south=0&west=0'
                resultCode, resultString = http.Get( subdomain, urlExt, thisUsername, thisPassword )
                if( resultCode == 200 ):
                    baseUrlString = subdomain
                    username = thisUsername
                    password = thisPassword
                    validSubDomain = True
            num_links = int( raw_input( "Number Of Maps: " ))   #for most of the params, we take raw input and cast to int
            while isNumeric( num_links ) == False:
                print "Please enter a numerical value"
                num_links = raw_input( "Number Of Maps: " )
            north_coor = raw_input( "North Coordinate: " )
            while isNumeric( north_coor ) == False:
                print "Please enter a numerical value"
                north_coor = raw_input( "North Coordinate: " )
            south_coor = raw_input( "South Coordinate: " )
            while isNumeric( south_coor ) == False:
                print "Please enter a numerical value"
                south_coor = raw_input( "South Coordinate: " )
                    
            #this block makes sure that the north coordinate is greater than the south coordinate
            while south_coor >= north_coor:
                print "you entered a southern coordinate that was greater than the northern coordinate, please try again."
                north_coor = raw_input( "North Coordinate: " )
                while isNumeric( north_coor ) == False:
                    print "Please enter a numerical value"
                    north_coor = raw_input( "North Coordinate: " )
                south_coor = raw_input( "South Coordinate: " )
                while isNumeric( south_coor ) == False:
                    print "Please enter a numerical value"
                    south_coor = raw_input( "South Coordinate: " )
            
            east_coor = raw_input( "East Coordinate: " )
            while isNumeric( east_coor ) == False:
                print "Please enter a numerical value"
                south_coor = raw_input( "East Coordinate: " )
            west_coor = raw_input( "West Coordinate: " )
            while isNumeric( west_coor ) == False:
                print "Please enter a numerical value"
                west_coor = raw_input( "West Coordinate: " )
            paramsEntered = True
        except:
            print "invalid input, please try again."
    #we return a list with the params
    return [num_links, north_coor, south_coor, east_coor, west_coor, subdomain, username, password]

#diagnosticRequest makes the first query to the web
def diagnosticRequest( params ):
    num_links  = params[0]   #these are all of the params
    north_coor = params[1]   #that we've gathered so far,
    south_coor = params[2]   #they are given names that are more easily read
    east_coor  = params[3]
    west_coor  = params[4]
    subdomain  = params[5]
    username   = params[6]
    password   = params[7]
    availablePages = []                     #a new list is created for the availablePages
    keepGoingIfNotEnoughDatasets = True     #keepGoingIfNotEnoughDatasets holds whether or not to continue if the num of datasets < desired
    retrieved = False                       #retrieved records whether or not we have retrieved a dataset from the net
    #urlExt is the extension for the url of the query.
    urlExt = 'datasets.weo?page=1&east=' + east_coor + '&north=' + north_coor + '&south=' + south_coor + '&west=' + west_coor
    print "URL: " + baseUrlString + urlExt # debug
    while not retrieved:    #when we receive a response, retrieved is set to true so we can exit the while loop
        try:
            resultCode, resultString = http.Get( subdomain, urlExt, username, password )    #here, we make the http request
            retrieved = True
        except:
            resultString = ''
            retrieved = False
    if resultString != '':  #if we have a string of results
        weoSoup = BeautifulSoup.BeautifulSoup( resultString )
        totalPages = int( weoSoup.datasets['total_pages'] )
        print "totalPages: " + str( totalPages ) # debug
        for i in range( 0, totalPages ):
            availablePages.append( i + 1 )                                  #each page number is appended to the availablePages list
        totalEntries = int( weoSoup.datasets['total_entries'] )
        print "totalEntries: " + str( totalEntries ) # debug
        if totalEntries < num_links:                                       #if there arent enough links to meet the users desired threshhold
            print "there are only " + str( totalEntries ) + " datasets that match the geographic criteria."
            keep_going = raw_input( "Do you want to proceed?(y/n)" )       #if the person doesn't want to proceed, keepGoing is set to false
            if (keep_going == 'n') | (keep_going == 'no'):
                keepGoingIfNotEnoughDatasets = False
    return[availablePages, totalEntries, totalPages, keepGoingIfNotEnoughDatasets]  #the array of page numbers, total # of entries, total # of pages
                                                                                #and keepGoing boo are returned
def getTokens( params ):
    num_links                    = params[0]        #these are all of the params
    north_coor                   = params[1]        #that we've gathered so far,
    south_coor                   = params[2]        #they are given names that are more easily read
    east_coor                    = params[3]
    west_coor                    = params[4]
    subdomain                    = params[5]
    username                     = params[6]
    password                     = params[7]
    availablePages               = params[8]
    totalPages                   = params[9]
    keepGoingIfNotEnoughDatasets = params[10]
    tokenList = []                                  #also, a list is made for the tokens
    pageIndex = 0                                   #and an index for pages
    # this is the main loop of the program
    while len( tokenList ) < int( num_links ):   # as long as we don't have more than the requested number of tokens
        # the following lines put together the URL we need, and make the request
        urlExt = 'datasets.weo?page=' + str( availablePages[pageIndex] ) + '&east=' + east_coor + '&north=' + north_coor + \
            '&south=' + south_coor + '&west=' + west_coor + '&per_page=15'
        print "URL: " + baseUrlString + urlExt # debug
        try:
            resultCode, resultString = http.Get( subdomain, urlExt, username, password )    #this is where the http request is made
        except:
            resultString = ''
        print "resultString: " + resultString # debug
        if resultString != '':                          #if we get results
            if pageIndex == ( totalPages - 1 ):         #if we're at the last page, then the user is told there aren't enough datasets
                print "There aren't " + str( num_links ) + " datasets that match the geographic criteria."  #meeting the criteria
                break
            pageIndex += 1                              #pageIndex is incremented to prepare for the next call
            weoSoup = BeautifulSoup.BeautifulSoup( resultString )
            datasetsList = weoSoup.datasets.findAll('dataset')
            print 'datasetsList: ' + str( datasetsList ) #debug
            for dataset in datasetsList:
                token = dataset.token.string
                if not token in tokenList:
                    tokenList.append( token )
                    #print "tokenList: " + str( self.tokenList ) #debug
                    # print "token: " + token # debug
    return tokenList                                                            #token list is returned
#getTokenUrls takes a list of tokens, and returns a list of the request urls; so this method is really just formatting and adding to the string
def getTokenUrls( tokens ):
    tokenRequestList = []
    for token in tokens:
        tokenKmlRequest = 'http://market.weogeo.com/datasets/' + token + '.kml'
        tokenRequestList.append( tokenKmlRequest )
    return tokenRequestList
#isNumeric method returns a boolean based on whether or not what is input can be cast to an integer
def isNumeric( input ):
    try:
        temp = int( input )
        return True
    except:
        return False