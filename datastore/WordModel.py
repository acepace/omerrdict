from google.appengine.ext import ndb

class WordEntry(ndb.Model):
    '''
        Basic word entry
    '''
    word = ndb.StringProperty(required=True)
    definition = ndb.StringProperty(indexed=False,required=True)
    addDate = ndb.DateTimeProperty(auto_now_add=True)
    
    def put(self):
        '''
            Don't add dup entries
        '''
        currentWord = self.word
        existing = WordEntry.query(WordEntry.word == currentWord).get()
        if existing: #if it exists, check if we're in an update operation, if not, GTFO
            if existing.key != self.key:
                raise ValueError("Definition already exists.")
        return super(WordEntry, self).put() #run the putter