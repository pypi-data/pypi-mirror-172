# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 09:54:00 2022

@author: PP
"""
import requests, json
class Weather:
    def __init__(self, api_key ):
        if api_key:
            
            url= f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={api_key}'
            r=requests.get(url)
            self.data=r.json()
            if self.data['cod']!='200':
                raise ValueError(self.data['message'])
            
        else:
            raise TypeError('API key missing')
