import requests
import time
from followeraudit import config
from followeraudit.FauditException import FauditException

class FauditAPIclient:

    def __init__(self,apikey=None,session=False):
        """ Initializes Followeraudit client object for access Followeraudit APIs """
        
        """
        :param api_key: your API key.
        :type api_key:  string
        :param session: Default value for this argument is None but if you're making several requests to the same host, 
                        the underlying TCP connection will be reused, which can result in a significant performance increase. 
                        Please make sure call session.close() after execute all calls to free up resource.   
        :type session: requests.Session
        """
        self.apikey=apikey
        if not self.apikey:
            raise FauditException("Please provide your private API Key")

        if session is True:
            self.request_method = session
        else:
            self.request_method = requests

        """Default value for maximum retries and retry delay is zero """
        self.max_retries = 0
        self.retry_delay = 0

        """Default proxies value is none"""
        self.proxies = None

        """set request timeout"""
        self.request_timeout = config.DEFAULT_REQUEST_TIMEOUT
    
    def set_retries( self, max_retries=0, retry_delay = 0):
        """ API maximum retry and delay when getting 500 error """
        
        """
        :param max_retries: Your maximum retries when server responding with 500 internal error, Default value for this augument is zero.
        :type max_retries:  integer 
        :param retry_delay: Delay(in seconds) between retries when server responding with 500 error, Default value for this augument 
                            is zero seconds.
        :type retry_delay:  integer
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def set_request_timeout( self, request_timeout = config.DEFAULT_REQUEST_TIMEOUT):
        """ API maximum timeout for the request """
        
        """
        :param request_timeout: How many seconds to wait for the client to make a connection and/or send a response.
        :type request_timeout:  integer 
        """
        self.request_timeout = request_timeout

    def set_api_proxies( self, proxies):
        """ Configure Proxie dictionary """
        
        """
        :param proxies: A dictionary of the protocol to the proxy url ( ex.{ "https" : "https://1.1.1.1:80"}).
        :type proxies:  dictionary 
        """
        self.proxies = proxies
    

    def __post(self,headers,form_data,url):
        if self.proxies is None:
            return self.request_method.post(url=url,headers=headers,data=form_data,timeout=self.request_timeout)
        else:
            return self.request_method.post(url=url,headers=headers,data=form_data,proxies=self.proxies,timeout=self.request_timeout)

    def __MaxRetries(self,headers,form_data,url):
        while (self.max_retries):
            time.sleep(self.retry_delay)
            response = self.__post(headers=headers,form_data=form_data,url=url)
            if response.status_code != 500:
                break
            self.max_retries-=1
        return response
    
    def __checkfor_user_tid(self,username,twitterid):
        if not username and not twitterid:
            raise FauditException('Please provide either username or Twitter Id')
        if username and twitterid:
            raise FauditException('Please provide only one, i.e (either username or Twitter-ID)')
        return True

    
    def newaudit(self,username=None,twitterid=None,refresh=0):
        """ Sending POST request to the followeaudit newaudit api"""
        
        """
        :param username: pass your desired username (ex. username='user1')
        :type username: string
        :param twitterid: pass your desired twitterid (ex. twitterid='12345' or twitterid=12345)
        :type twitterid: string or int
        :param refresh: pass refresh = 1 if you wnat to genrate a new audit score of a user  
        :type lang: int
        :return: server response in JSON object 
        """

        if refresh == True or refresh == 1:
            refresh = 1
        else:
            refresh =0

        if self.__checkfor_user_tid(username=username,twitterid=twitterid):
            headers={'bearer-token':self.apikey}
            form_data={'username':username,
                        'twitter_id':twitterid,
                        'refresh':refresh
                        }
            url=config.AUDIT_URL

            response=self.__post(headers=headers,form_data=form_data,url=url)
            
            if response.status_code == 500:
                response=self.__MaxRetries(headers=headers,form_data=form_data,url=url)

            if response.status_code != 200:
                raise FauditException(response.json())

            return response.json()

    def bulkaudit(self,username=None,twitterid=None,refresh=0):
        """ Sending POST request to the followeaudit bulkaudit api"""
        
        """
        :param username: pass your desired username in "," seprated string or in list (ex. username='user1,user2,user3' or username=['user1','user2','user3'])
        :type username: string or list 
        :param twitterid: pass your desired twitterid in "," seprated string or in list (ex. twitterid='1234,5678,12387,54321' or twitterid=[1234,3214,5674,3214])
        :type twitterid: string or int or list
        :param refresh: pass refresh = 1 if you wnat to genrate a new audit score of a users
        :type lang: int
        :return: server response in JSON object 
        """
        if refresh == True or refresh == 1:
            refresh = 1
        else:
            refresh =0
        if self.__checkfor_user_tid(username=username,twitterid=twitterid):
            if isinstance(username,str) or isinstance(twitterid,str):
                headers={'bearer-token':self.apikey}
                form_data={'username':username,
                            'twitter_id':twitterid,
                            'refresh':refresh
                            }
                url=config.BULK_AUDIT_URL
                response=self.__post(headers=headers,form_data=form_data,url=url)
                if response.status_code == 500:
                    response=self.__MaxRetries(headers=headers,form_data=form_data,url=url)
                if response.status_code != 200:
                    raise FauditException(response.json())
                return response.json()
            else:
                if username:
                    if (isinstance(username,list)):
                        username_str=''
                        for user in username:
                            username_str+=user+','

                        username_str=username_str.strip(',')
                        headers={'bearer-token':self.apikey}
                        form_data={'username':username_str,
                                    'twitter_id':twitterid,
                                    'refresh':refresh
                                    }
                        url=config.BULK_AUDIT_URL
                        response=self.__post(headers=headers,form_data=form_data,url=url)
            
                        if response.status_code == 500:
                            response=self.__MaxRetries(headers=headers,form_data=form_data,url=url)

                        if response.status_code != 200:
                            raise FauditException(response.json())

                        return response.json()
                    else:
                        raise FauditException('Please provide username in string with "," seprated or in list')
                if twitterid:
                    if (isinstance(twitterid,list)):
                        twitter_str=''
                        for id in twitterid:
                            id=str(id)
                            twitter_str+=id+','
                        twitter_str=twitter_str.strip(',')
                        headers={'bearer-token':self.apikey}
                        form_data={'username':username,
                                    'twitter_id':twitter_str,
                                    'refresh':refresh
                                    }
                        url=config.BULK_AUDIT_URL
                        response=self.__post(headers=headers,form_data=form_data,url=url)
            
                        if response.status_code == 500:
                            response=self.__MaxRetries(headers=headers,form_data=form_data,url=url)

                        if response.status_code != 200:
                            raise FauditException(response.json())

                        return response.json()
                    else:
                        raise FauditException('Please provide Twitter-ID in string with "," seprated or in list')

    def auditstatus(self,audit_id):
        """ Sending POST request to the followeaudit getaudit api"""
        
        """
        :param audit_id: pass your desired audit_id to get current status of you audit status (ex. audit_id='your audit_id')
        :type audit_id: string 
        :return: server response in JSON object 
        """
        if audit_id:
            headers={'bearer-token':self.apikey}
            form_data={'audit_id':audit_id}
            url=config.AUDIT_STATUS_URL
            
            response=self.__post(headers=headers,form_data=form_data,url=url)
            if response.status_code == 500:
                response=self.__MaxRetries(headers=headers,form_data=form_data,url=url)

            if response.status_code != 200:
                raise FauditException(response.json())

            return response.json()

        else:
            raise FauditException('Please provide a valid process-id to view status of your audit')