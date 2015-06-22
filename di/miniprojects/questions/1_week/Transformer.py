class Transformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self,):
        pass
        # initialization code

    # def fit(self, X, y=None):
    # 	# fit the transformation ...
    # 	return self




        #Unflat dictionary containing list
    def flattelists(unfldict):
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


    #Flatten dictionary of dictionary
    def flatten(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
                #print dict(items)	 	 
        return dict(items)



    def transform(self, jsonlist):
        lst_dicts = self.unpack_all(self,X)
        cityTransform = self.cityTransform(necessary_columns)
        UnfoldedJson=[flattelists(flatten(jsondict)) for jsondict in jsonlist]
        return UnfoldedJson
