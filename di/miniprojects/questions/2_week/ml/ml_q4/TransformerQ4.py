# -*- coding: utf-8 -*-
from __future__ import unicode_literals
class TransformerQ4(base.BaseEstimator, base.TransformerMixin):
   def __init__(self):
       return
   # initialization code

   def columnSelectJsonTransform(self, jsonlist, list_colnames):
       """ """
       selected_dict = []
       for x in jsonlist:
           selected_dict.append({key:val for key, val in x.items() if key in list_colnames})
       selected_dict_transformed = self.JSONTransform(selected_dict)
       return selected_dict_transformed

   def jsonTransform(self, jsonlist):
       """ """
       UnfoldedJSON=[self.flattelists(self.flatten(jsondict)) for jsondict in jsonlist]
       return UnfoldedJSON


   def flattelists(self, unfldict):
      """Converts a dict with lists in values to a dict in which every list 
       element is converted to a new k:v pair (bool True if it exists)
       IN: A single python dict
       OUT:A single python dict"""
       #unfldict={'categories': ['Doctors', 'Health & Medical'],'attributes_By Appointment Only': True, 'hours_Thursday_close': '17:00'}
      keylist=unfldict.keys()
      flattenlistkey=[]
   
      #Create list -flattenlistkey- of keys each associated to a list
      #[flattenlistkey.append(elem) for elem in unfldict if type(unfldict.get(elem))==list ]
      for elem in unfldict:
          if type(unfldict.get(elem))==list:
              if unfldict.get(elem):
                  flattenlistkey.append(elem)
              else:
                  unfldict[elem]=None
      #print flattenlistkey   
      #go through the list and create a new dictionary unfolding the list
      newdictlist={}
      for keyelem in flattenlistkey: #for each key associated to a list
          listtoflat=unfldict.get(keyelem)#return the list associated to key
          #print listtoflat    
          #create a dictionary with categories_eleminlist
          for elemlist in range(0,len(listtoflat)): #goes through each element  of the list
              newdictlist.update({keyelem+'_'+listtoflat[elemlist]:True})
              
      #Popout elements from the original dataframe containing lists and update with unfolded list dictionary    
      totaldict   =  unfldict.copy()
   
      newlistkeys   = newdictlist.keys()
      newlistvalues = newdictlist.values()
   
      #Eliminate key with list
      [totaldict.pop(keyelem, None) for keyelem in flattenlistkey]
   
      #Updating original dictionary with unfolded list
      [totaldict.update({newlistkeys[addind]:newlistvalues[addind]}) for addind in range(0,len(newlistkeys))]
      #for addind in range(0,len(newlistkeys)):
      #    #print newlistkeys[addind] 
      #    totaldict.update({newlistkeys[addind]: newlistvalues[addind]})
      
      return totaldict                         
   
   def flatten(self, d, parent_key='', sep='_'):
      """Converts a nested dict to a flat dict in which the nested dicts are converted to 
       multi-element lists 
       IN: a python dict with nested dicts
       OUT: a single python dict"""
      items = []
      for k, v in d.items():
          new_key = parent_key + sep + k if parent_key else k
          if isinstance(v, collections.MutableMapping):
              items.extend(self.flatten(v, new_key, sep=sep).items())
          else:
              items.append((new_key, v))
      #print dict(items)        
      return dict(items)