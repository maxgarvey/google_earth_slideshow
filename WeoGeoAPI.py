"""
Copyright (C) 2011 by WeoGeo, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

REPORTING BUGS
    Report bugs to <support@weogeo.com>.

PURPOSE:
A simple python wrapper around the WeoGeo API.

API docs at: http://wiki.weogeo.com/index.php/WeoGeo_API_Wrappers_(Python)
"""
import httplib
import base64
try:
    import json
except ImportError:
    import simplejson as json

try:
    import weoXML
    _DEFINE_USING_WEOXML = True
except ImportError:
    _DEFINE_USING_WEOXML = False

#formats_object###################################################################################################################
class formats( object ):
    JSON = 0
    XML  = 1
    WEO  = 2
    KML  = 3

    def __init__( self, newFormat ):
        if isinstance( newFormat, formats ) == True:
            self.type = newFormat.type
        elif isinstance( newFormat, int ) == True:
            if newFormat < self.JSON or newFormat > self.KML:
                raise Exception( 'Format error: format "' + str(newFormat) + '" is not supported.' )
            self.type = newFormat
        elif isinstance( newFormat, str ) == True:
            newFormat_lower = newFormat.lower()
            if newFormat_lower == 'json':
                self.type = self.JSON
            elif newFormat_lower == 'xml':
                self.type = self.XML
            elif newFormat_lower == 'weo':
                self.type = self.WEO
            elif newFormat_lower == 'kml':
                self.type = self.KML
            else:
                raise Exception( 'Format error: format "' + str(newFormat) + '" is not supported.' )
        else:
            raise Exception( 'Formats error: can not initialize object with parameter provided. Incompatible type.' )
        return

    def __str__( self ):
        if self.type == self.JSON:
            local = 'json'
        elif self.type == self.XML:
            local = 'xml'
        elif self.type == self.WEO:
            local = 'weo'
        elif self.type == self.KML:
            local = 'kml'
        else:
            raise Exception( 'Format error: format "' + str(self.type) + '" not supported.' )
        return local

    def __eq__( self, other ):
        if isinstance( other, formats ) == True:
            if self.type == other.type:
                return True
            else:
                return False
        elif isinstance( other, int ) == True:
            if self.type == other:
                return True
            else:
                return False
        elif isinstance( other, str ) == True:
            other_lower = other.lower()
            if self.type == self.JSON and other_lower == 'json':
                return True
            elif self.type == self.XML and other_lower == 'xml':
                return True
            elif self.type == self.WEO and other_lower == 'weo':
                return True
            elif self.type == self.KML and other_lower == 'kml':
                return True
            else:
                return False
        else:
            raise Exception( 'Cannot compare a "format" object against the type provided.' )

    def __ne__( self, other ):
        return not self == other
#format_object_end###############################################################################################################

#HTTP_controller#################################################################################################################
class httpController( object ):
    def getGTLD( self, string ):
        sepOne = string.find('.')
        if sepOne != -1:
            sepTwo = string[sepOne+1:].find('.')
            if sepTwo != -1:
                sepl = string[sepOne+sepTwo+1:].find('/')
                if sepl != -1:
                    return string[sepOne+sepTwo+2:sepOne+sepTwo+1+sepl]
                else:
                    return string[sepOne+sepTwo+2:]
            else:
                return ''
        else:
            return ''

    def success( self, code ):
        if code >= 200 and code <= 206:
            return True
        else:
            return False
     
    def getRequestType( self, string ):
        sep = string.rfind('.')
        if sep == -1:
            return 'application/xml'
        else:
            rtype = string[sep+1:].lower()
            if rtype == 'weo' or rtype == 'kml' or rtype == 'xml':
                return 'application/xml'
            else:
                return 'application/' + str(rtype)
     
    def normalizeDomain( self, string ):
        if string.startswith( 'http://' ):
            string = string[7:]
        elif string.startswith( 'https://' ):
            string = string[8:]
            
        if string.endswith( '/' ):
            return string[:-1]
        else:
            return string
     
    def normalizePath( self, string ):
        if len(string) == 0:
            return ''
        elif string[0] != '/':
            return '/' + string
        else:
            return string    
     
    def handleResponse( self, code, output ):
        if code >= 200 and code <= 206:
            return output
        else:
            return None
     
    def Get( self, domain, path, username, password ):
        path = self.normalizePath( path )
        requestType = self.getRequestType( path )
        credentials = base64.encodestring( '%s:%s' % (username, password) ).replace( '\n', '' )
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = httplib.HTTPSConnection( self.normalizeDomain(domain) )
        connection.request( 'GET', path, None, headers )
        response = connection.getresponse()
        connection.close()
        return response.status, response.read()
     
    def Post( self, domain, path, username, password, content ):
        path = self.normalizePath( path )
        requestType = self.getRequestType( path )
        credentials = base64.encodestring( '%s:%s' % (username, password) ).replace( '\n', '' )
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = httplib.HTTPSConnection( self.normalizeDomain(domain) )
        connection.request( 'POST', path, content, headers )
        response = connection.getresponse()
        connection.close()
        return response.status, response.read()
     
    def Put( self, domain, path, username, password, content ):
        path = self.normalizePath( path )
        requestType = self.getRequestType( path )
        credentials = base64.encodestring( '%s:%s' % (username, password) ).replace( '\n', '' )
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = httplib.HTTPSConnection( self.normalizeDomain(domain) )
        connection.request( 'PUT', path, content, headers )
        response = connection.getresponse()
        connection.close()
        return response.status, response.read()

    def Delete( self, domain, path, username, password, content = '' ):
        path = self.normalizePath( path )
        requestType = self.getRequestType( path )
        credentials = base64.encodestring( '%s:%s' % (username, password) ).replace( '\n', '' )
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = httplib.HTTPSConnection( self.normalizeDomain(domain) )
        connection.request( 'DELETE', path, content, headers )
        response = connection.getresponse()
        connection.close()
        return response.status, response.read()
#HTTP_controller_end#############################################################################################################

#weo_session#####################################################################################################################
class weoSession( object ):
    def __init__( self, newHostname, newUsername, newPassword = '' ):
        self.setHostname( newHostname )
        self.httpC     = httpController()
        self.username  = newUsername
        self.password  = newPassword
        self.connected = False
        self.market    = False
        return

    #_connection_functions#############################
    def setHostname( self, newHostname ):
        self.hostname = newHostname.strip()
        if self.hostname.startswith( 'https://' ) == False and self.hostname.startswith( 'http://' ) == False:
            self.hostname = 'https://' + self.hostname
        self.connected = False
        return
    
    def setUsername( self, newUsername ):
        self.username = newUsername
        self.connected = False
        return

    def setPassword( self, newPassword ):
        self.password = newPassword
        self.connected = False
        return

    def setAPIKey( self, apiKey ):
        self.username = apiKey
        self.password = ''
        self.connected = False
        return

    def connect( self ):
        if self.hostname == None:
            raise Exception( 'Session error: please provide a host address.' )
        if self.username == None:
            raise Exception( 'Session error: please provide a username.' )
        if self.password == None:
            raise Exception( 'Session error: please provide a password.' )

        code, output = self.getLibraryInfo()
        self.connected = self.httpC.success( code )
        return self.connected

    def connectToMarket( self ):
        if self.hostname == None:
            raise Exception( 'Session error: please provide a host address.' )
        if self.username == None:
            raise Exception( 'Session error: please provide the API key.' )
        if self.password == None:
            raise Exception( 'Session error: please provide a password.' )

        self.connected = True
        self.market    = True
        return self.connected
        
    def clear( self ):
        self.username  = None
        self.password  = None
        self.connected = False
        return self
    #_connection_functions_end#########################

    #_utility_functions################################
    def __str__( self ):
        i  = 'Host:      ' + str(self.hostname)  + '\n'
        i += 'Username:  ' + str(self.username)  + '\n'
        i += 'Password:  ' + str(self.password)  + '\n'
        if self.connected == False:
            i += 'Status:    ' + 'Disconnected'
        else:
            i += 'Status:    ' + ('Good' if self.market == False else 'Probably Good\n')
        return i

    if _DEFINE_USING_WEOXML == True:
        def _parseOutput( self, rtype, output ):
            if len(output.strip()) == 0:
                pOutput = output
            elif rtype == 'xml' or rtype == 'weo' or rtype == 'kml':
                pOutput = weoXML.weoXML( output )
            elif rtype == 'json':
                pOutput = json.loads( output )
            else:
                pOutput = output
            return pOutput
    else:
        def _parseOutput( self, rtype, output ):
            if len(output.strip()) == 0:
                pOutput = output
            elif rtype == 'xml' or rtype == 'weo' or rtype == 'kml':
                pOutput = output
            elif rtype == 'json':
                pOutput = json.loads( output )
            else:
                pOutput = output
            return pOutput
    #_utility_functions_end_############################

    #_job_dictionary_util_functions#####################
    def _validateJobDict( self, jobDict ):
        try:
            jobDict['job']
            if jobDict['job']['dataset_token'] == '':
                return False, 'missing value for "dataset_token" field'
            if jobDict['job']['content_license_acceptance'] == '':
                return False, 'missing value for "content_license_id" field'
            if jobDict['job']['parameters']['job_geocrop'] == '':
                return False, 'missing value for "job_geocrop" field'
            if jobDict['job']['parameters']['job_north'] == '':
                return False, 'missing value for "job_north" field'
            if jobDict['job']['parameters']['job_south'] == '':
                return False, 'missing value for "job_south" field'
            if jobDict['job']['parameters']['job_east'] == '':
                return False, 'missing value for "job_east" field'
            if jobDict['job']['parameters']['job_west'] == '':
                return False, 'missing value for "job_west" field'
            if jobDict['job']['parameters']['job_datum_projection'] == '':
                return False, 'missing value for "job_datum_projection" field'
            if jobDict['job']['parameters']['job_file_format'] == '':
                return False, 'missing value for "job_file_format" field'
        except KeyError as missingKey:
            return False, 'critical key ' + str(missingKey) + ' not found in the job object provided'
        return True, ''

    def _jobDictToXML( self, jobDict ):
        request = '<job>'
        request += '<dataset_token>' + jobDict['job']['dataset_token'] + '</dataset_token>'
        request += '<content_license_acceptance>' + jobDict['job']['content_license_acceptance'] + '</content_license_acceptance>'
        if jobDict['job'].has_key('layers') == True:
            request += '<layers>' + jobDict['layers'] + '</layers>'
        request += '<parameters>'
        request += '<job_geocrop>'            + jobDict['job']['parameters']['job_geocrop']            + '</job_geocrop>'
        request += '<job_north>'              + jobDict['job']['parameters']['job_north']              + '</job_north>'
        request += '<job_south>'              + jobDict['job']['parameters']['job_south']              + '</job_south>'
        request += '<job_east>'               + jobDict['job']['parameters']['job_east']               + '</job_east>'
        request += '<job_west>'               + jobDict['job']['parameters']['job_west']               + '</job_west>'
        request += '<job_datum_projection>'   + jobDict['job']['parameters']['job_datum_projection']   + '</job_datum_projection>'
        request += '<job_file_format>'        + jobDict['job']['parameters']['job_file_format']        + '</job_file_format>'
        if jobDict['job']['parameters'].has_key('job_spatial_resolution') == True:
            request += '<job_spatial_resolution>' + jobDict['job']['parameters']['job_spatial_resolution'] + '</job_spatial_resolution>'
        request += '</parameters>'
        request += '</job>'
        return request
    #_job_dictionary_util_functions_end#################

    #Independent#####################################################################################################################
    @staticmethod
    def _getWeoGeoHostMode( string ):
        if string.startswith( 'http://' ):
            string = string[7:]
        elif string.startswith( 'https://' ):
            string = string[8:]
        if string.endswith( '/' ):
            string = string[:-1]
     
        connection = httplib.HTTPConnection( string )
        headers    = dict()
        headers['Content-Type']  = 'xml'
        connection.request( 'GET', '/version.json', None, headers )
        response = connection.getresponse()
        connection.close()
     
        if response.status != 200:
            return None
     
        versionJSON = json.loads( response.read() )
        return versionJSON['mode']
    #Independent_end#################################################################################################################

    #library_info_calls#########################################################################################################
    def getLibraryInfoRaw( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        path = 'library.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output
    
    def getLibraryInfo( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getLibraryInfoRaw( rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    
    def getLibraryUserRaw( self, user, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/library_users/' + str(user) + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getLibraryUser( self, user, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getLibraryUserRaw( user, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def getLibraryUsersRaw( self, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/library_users' + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getLibraryUsers( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getLibraryUsersRaw( rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def createLibraryUserRaw( self, userEmail, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/library_users.' + str(rtype)
        if rtype == 'xml':
            content = '<library_user><email>' + userEmail + '</email></library_user>'
        else:
            content = '{ "library_user" : { "email" : "' + userEmail + '"}}'
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, content )
        return code, output

    def createLibraryUser( self, userEmail, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.createLibraryUserRaw( userEmail, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def deleteLibraryUser( self, userId ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'admin/library_users/' + str(userId)
        code, output = self.httpC.Delete( self.hostname, path, self.username, self.password )
        return code, output

    def updateLibraryUserRaw( self, userId, newRoles, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/library_users/' + str(userId) + '.' + str(rtype)
        if rtype == 'xml':
            content = '<library_user><role_ids>' + str(newRoles) + '</role_ids></library_user>'
        else:
            content = '{ "library_user" : { "role_ids" : "' + str(newRoles) + '"}}'
        code, output = self.httpC.Put( self.hostname, path, self.username, self.password, content )
        return code, output

    def updateLibraryUser( self, userId, newRoles, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.updateLibraryUserRaw( userId, newRoles, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    #library_info_calls_end#####################################################################################################

    #groups_api_calls_##########################################################################################################
    def getGroupsRaw( self, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/groups.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getGroups( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getGroupsRaw( rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def getGroupRaw( self, groupID, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/groups/' + str(groupID) + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getGroup( self, groupID, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getGroupRaw( groupID, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def createGroupRaw( self, groupName, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/groups.' + str(rtype)
        if rtype == 'xml':
            content = '<group><name>' + groupName  + '</name></group>'
        else:
            content = '{ "group" : { "name" : "' + groupName + '"}}'
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, content )
        return code, output

    def createGroup( self, groupName, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.createGroupRaw( groupName, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def updateGroupRaw( self, groupID, newGroupName, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/groups/' + str(groupID) + '.' + str(rtype)
        if rtype == 'xml':
            content = '<group><name>' + newGroupName  + '</name></group>'
        else:
            content = '{ "group" : { "name" : "' + str(newGroupName) + '"}}'
        code, output = self.httpC.Put( self.hostname, path, self.username, self.password, content )
        return code, output

    def updateGroup( self, groupID, newGroupName, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.updateGroupRaw( groupID, newGroupName, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def deleteGroup( self, groupID ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'admin/groups/' + str(groupID)
        code, output = self.httpC.Delete( self.hostname, path, self.username, self.password )
        return code, output
    #groups_api_calls_end#######################################################################################################

    #roles_api_calls_###########################################################################################################
    def getRolesRaw( self, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/roles.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getRoles( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getRolesRaw( rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def getRoleRaw( self, roleID, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/roles/' + str(roleID) + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output
 
    def getRole( self, roleID, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getRoleRaw( roleID, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def createRoleRaw( self, roleName, canAccessAll, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'admin/roles.' + str(rtype)
        if rtype == 'xml':
            content = '<role><name>' + str(roleName)  + '</name><can_access_all>' + str(canAccessAll) + '</can_access_all></role>'
        else:
            content = '{ "role" : { "name" : "' + str(roleName) + '", "can_access_all":"' + str(canAccessAll) + '"}}'
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, content )
        return code, output

    def createRole( self, roleName, canAccessAll, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.createRoleRaw( roleName, canAccessAll, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def updateRoleRaw( self, roleID, newRoleName = None, canAccessAll = None, groupIDs = None, rtype = formats.JSON  ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        if newRoleName is None and canAccessAll is None and groupIDs is None:
            raise Exception( 'Session error: updateRole invoked with nothing to update.' )
        rtype = formats( rtype )
        path = 'admin/roles/' + str(roleID) + '.' + str(rtype)
        if rtype == 'xml':
            content = '<role>'
            if newRoleName is not None:
                content += '<name>' + str(newRoleName)  + '</name>'
            if canAccessAll is not None:
                content += '<can_access_all>' + str(canAccessAll).lower() + '</can_access_all>'
            if groupIDs is not None:
                content += '<group_ids>' + str(groupIDs) + '</group_ids>'
            content += '</role>'
        else:
            content = '{ "role" : {'
            if newRoleName is not None:
                content += '"name":"' + str(newRoleName)  + '",'
            if canAccessAll is not None:
                content += '"can_access_all":"' + str(canAccessAll).lower() + '",'
            if groupIDs is not None:
                content += '"group_ids":"' + str(groupIDs) + '",'
            content = content[:-1] + '} }'
        code, output = self.httpC.Put( self.hostname, path, self.username, self.password, content )
        return code, output

    def updateRole( self, roleID, newRoleName = None, canAccessAll = None, groupIDs = None, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.updateRoleRaw( roleID, newRoleName, canAccessAll, groupIDs, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
 
    def deleteRole( self, roleID ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'admin/roles/' + str(roleID)
        code, output = self.httpC.Delete( self.hostname, path, self.username, self.password )
        return code, output
    #roles_api_calls_end########################################################################################################

    #license_api_calls_#########################################################################################################
    def getLicensesRaw( self, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'licenses' + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getLicenses( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getLicensesRaw( rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
     
    def getLicenseRaw( self, licenseID, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'licenses/' + str(licenseID) +  '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getLicense( self, licenseID, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getLicenseRaw( licenseID, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    #license_api_calls_end######################################################################################################

    #_event_api_calls_##########################################################################################################
    def _createEvent( self, eType, token, status, subject, body, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        if status.lower() not in ['error', 'warning', 'info']:
            raise Exception( 'Session error: event status "' + status + '" not supported.' )
        rtype = formats( rtype )
        if eType == 'dataset':
            path = 'datasets/' + token + '/events.' + str(rtype)
        else:
            path = 'jobs/' + token + '/events.' + str(rtype)
        if rtype == 'json':
            content = { "event" : { "status" : status.lower(), "subject" : subject, "body" : body } }
        else:
            content  = '<event>'
            content += '<status>'  + status.lower() + '</status>'
            content += '<subject>' + subject        + '</subject>'
            content += '<body>'    + body           + '</body>'
            content += '</event>'
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, str(content) )
        return code, output 

    def createDatasetEventRaw( self, token, status, subject, body, rtype = formats.JSON ):
        code, output = self._createEvent( 'dataset', token, status, subject, body, rtype )
        return code, output

    def createDatasetEvent( self, token, status, subject, body, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self._createEvent( 'dataset', token, status, subject, body, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    
    def createJobEventRaw( self, token, status, subject, body, rtype = formats.JSON ):
        code, output = self._createEvent( 'job', token, status, subject, body, rtype )
        return code, output

    def createJobEvent( self, token, status, subject, body, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self._createEvent( 'job', token, status, subject, body, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    
    def getDatasetEventRaw( self, token, eventID, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'datasets/' + token + '/events/' + str(eventID) + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getDatasetEvent( self, token, eventID, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getDatasetEventRaw( token, eventID, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    
    def getJobEventRaw( self, token, eventID, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'jobs/' + token + '/events/' + str(eventID) + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getJobEvent( self, token, eventID, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getJobEventRaw( token, eventID, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output        
    
    def getDatasetEventsRaw( self, token, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'datasets/' + token + '/events' + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getDatasetEvents( self, token, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getDatasetEventsRaw( token, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output        
    
    def getJobEventsRaw( self, token, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'jobs/' + token + '/events' + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getJobEvents( self, token, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getJobEventsRaw( token, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    #_event_api_calls_end_#####################################################################################################

    #_dataset_api_calls_#######################################################################################################
    def getDatasetRaw( self, token, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'datasets/' + token + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getDataset( self, token, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getDatasetRaw( token, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
    
    def getDatasetsRaw( self, rtype = formats.JSON, *filters ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        dFilter = ''
        if len(filters) > 0:
            dFilter = '?'
            for f in filters:
                dFilter += f + '&'
            dFilter = dFilter.rstrip( '&' )
        path = 'datasets.' + str(rtype) + dFilter
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getDatasets( self, rtype = formats.JSON, *filters ):
        rtype = formats( rtype )
        code, output = self.getDatasetsRaw( rtype, *filters )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def updateDatasetRaw( self, token, content, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'datasets/' + token + '.' + str(rtype)
        code, output = self.httpC.Put( self.hostname, path, self.username, self.password, content )
        return code, output

    def updateDataset( self, token, content, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.updateDatasetRaw( token, content, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
     
    def getTokensRaw( self, numberOfTokensToCreate = 1 ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'datasets/tokens?count=' + str(numberOfTokensToCreate)
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, '' )
        return code, output

    def getTokens( self, numberOfTokensToCreate = 1 ):
        code, output = self.getTokensRaw( numberOfTokensToCreate )
        if self.httpC.success( code ) == True:
            output = output.split( '\n')
        return code, output

    def deleteDataset( self, token ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'datasets/' + token + '.weo'
        code, output = self.httpC.Delete( self.hostname, path, self.username, self.password )
        return code, output
    #_dataset_api_call_end_######################################################################################################

    #_job_api_calls_#############################################################################################################
    def getJobRaw( self, token, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'jobs/' + token + '.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getJob( self, token, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getJobRaw( token, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output
     
    def getJobsRaw( self, rtype = formats.JSON, *filters ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        jFilter = ''
        if len(filters) > 0:
            jFilter = '?'
            for f in filters:
                jFilter += f + '&'
            jFilter = jFilter.rstrip( '&' )
        path = 'jobs.' + str(rtype) + jFilter
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getJobs( self, rtype = formats.JSON, *filters ):
        rtype = formats( rtype )
        code, output = self.getJobsRaw( rtype, *filters )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def getUnfulfilledJobsRaw( self, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'jobs/unfulfilled.' + str(rtype)
        code, output = self.httpC.Get( self.hostname, path, self.username, self.password )
        return code, output

    def getUnfulfilledJobs( self, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.getUnfulfilledJobsRaw( rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def generateUploadWeofile( self, token, jobFile ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'jobs/' + str(token) + '/upload_weofile'
        content = '<filename>' + str(jobFile) + '</filename>'
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, content )
        return code, output
     
    def createJobRaw( self, content, rtype = formats.JSON ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        rtype = formats( rtype )
        path = 'jobs.' + str(rtype)

        success, message = self._validateJobDict( content )
        if success == False:
            raise Exception( 'Session error: createJobRaw: ' + message )

        if rtype == 'json':
            request = str(content)
        else:
            request = self._jobDictToXML( content )

        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, request )
        return code, output

    def createJob( self, content, rtype = formats.JSON ):
        rtype = formats( rtype )
        code, output = self.createJobRaw( content, rtype )
        if self.httpC.success( code ) == True:
            output = self._parseOutput( rtype, output )
        return code, output

    def getPrice( self, request ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        path = 'jobs/price.json'
        code, output = self.httpC.Post( self.hostname, path, self.username, self.password, str(request) )
        return code, output
        
    def jobComplete( self, token, rtype = formats(formats.JSON) ):
        if self.connected == False:
            raise Exception( 'Session error: session not connected. Call function "weoSession.connect()" before any API call.' )
        if isinstance(rtype, formats) == False:
            rtype = formats( rtype )
        path = 'jobs/' + token + '/upload_succeeded'
        code, output = self.httpC.Put( self.hostname, path, self.username, self.password, '' )
        return code, output
    #_job_api_calls_end_#########################################################################################################
#weo_session_end#################################################################################################################
