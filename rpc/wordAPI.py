import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from datetime import datetime

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
    
class DTfield(messages.Message):
    '''
        I hate my day. So I'm just copying a datetime class.
    '''
    year = messages.IntegerField(1,required=True)
    month = messages.IntegerField(2,required=True)
    day = messages.IntegerField(3,required=True)
    hour = messages.IntegerField(4,required=True)
    minute = messages.IntegerField(5,required=True)
    

@endpoints.api(name='wordAPI', version='v1')
class WordAPIApi(remote.Service):
    '''
        Quick interface to add/remove/list words.
    '''
    
    @endpoints.method(  message_types.VoidMessage,WordCollection,
                        path='listWords',http_method='GET',
                        name='listWords')
    def listWords(self,request):
        '''
            Returns all the words/definitions in the DB.
            Horribly inefficient.
        '''
        allWords = WordEntry.query()
        wordCount = allWords.count()
        words = allWords.fetch(wordCount)
        items = WordCollection(items = [Entry(word=x.word,definition=x.definition) for x in words])
        return items

        
    @endpoints.method(  DTfield,WordCollection,
                        path='listWordsByDate',http_method='GET',
                        name='listWordsByDate')
    def listWordsByDate(self,request):
        '''
            Returns request by date filter.
        '''
        requestedRange = datetime(   year=request.year,month=request.month,
                                    day=request.day,hour=request.hour,
                                    minute=request.minute)
        allWords = WordEntry.query(WordEntry.addDate > requestedRange)
        words = allWords.fetch(5000)
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
        
   
        
    