import linkGeneratorLib
#this line will make sure that we ask again if the number of links is less than the user wants
#and the number is important to the user.
enoughLinks = False
while not enoughLinks:                          
    params = linkGeneratorLib.getParams( )      #we get the appropriate params from library methods
    more_params = linkGeneratorLib.diagnosticRequest( params )
    params.append( more_params[0] )             #then, we add the number of available pages
    total_entries = more_params[1]              #the total number of entries for the given criteria
    params.append( more_params[2] )             #and the total number of pages
    params.append( more_params[3] )             #and wether or not the person wants to proceed if there aren't enough datasets
    if( not params[10] ):                       #if the user cares if there aren't the specified number of entries
        if( params[1] < total_entries ):    #and the number of entries is less than the specified number
            pass
    else:
        enoughLinks = True
tokens = linkGeneratorLib.getTokens( params )               #this line gets the token names and returns a list named tokens
tokenRequestUrls = linkGeneratorLib.getTokenUrls( tokens )  #tokens is passed into the getTokenUrls method which translates them into addresses for 
                                                            #curl the file that will hold the tokenUrls is opened
file = open( 'tokenRequestUrls.txt', 'w' )                  #and all of the urls are added here
for url in tokenRequestUrls:
    file.write( url + '\n')
file.close()                                                #file is closed, we're done.