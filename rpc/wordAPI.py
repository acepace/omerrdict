import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from datastore.WordModel import WordEntry


class Entry(messages.Message):
    '''
        Word, definition.
    '''
    word = messages.StringField(1,required=True)
    definition = messages.StringField(2)


class WordCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Entry, 1, repeated=True)



@endpoints.api(name='wordAPI', version='v1')
class WordAPIApi(remote.Service):
    '''
        Quick interface to add/remove/list words.
    '''
    
    @endpoints.method(  message_types.VoidMessage,WordCollection,
                        path='listWords',http_method='GET',
                        name='listWords')
    def listWords(self,request):
        allWords = WordEntry.query()
        wordCount = allWords.count()
        words = allWords.fetch(wordCount)
        items = WordCollection(items = [Entry(word=x.word,definition=x.definition) for x in words])
        return items

    @endpoints.method(  Entry,message_types.VoidMessage,
                        path='addWord',http_method='POST',
                        name='AddWord')
    def addWord(self,request):
        '''
            Add an entry to the DB
        '''
        try:
            newWord = WordEntry()
            newWord.word = request.word
            newWord.definition = request.definition 
            newWord.put()
            return message_types.VoidMessage()
        except ValueError as e:
            raise endpoints.NotFoundException("Invalid data. %s" % e)
        
    @endpoints.method(  Entry,message_types.VoidMessage,
                        path='deleteWord',http_method='POST',
                        name='DeleteWord')
    def deleteWord(self,request):
        '''
            removes according to WordEntry.word and not the definition text. (well, duh)
        '''
        existing = WordEntry.query(WordEntry.word == request.word).get()
        if existing:
            existing.key.delete()
        return message_types.VoidMessage()
    
    @endpoints.method(  Entry,message_types.VoidMessage,
                        path='modifyWord',http_method='POST',
                        name='modifyWord')
    def modifyWord(self,request):
        '''
            Implemented as a delete, add.
            Mostly because the coder was lazy.
        '''
        self.deleteWord(request)
        self.addWord(request)
        return message_types.VoidMessage()
        
    