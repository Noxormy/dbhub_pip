##Installing
Using pip  

    $ pip install dbhub

##Usage
**Get your api key for the database on *website***    

After that include packet in your code:  

    from dbhub import get_database

Create your database:  

     apikey = 'xxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    db = get_atabase(apiKey)
    
Get collection(table) from database:  
    
    collection = db.get_collection(collection_name)

##CRUD
Create new element in collection:
    
    collection.create(element)

Read element in collection:
    
    collection.read(id)

Update element in collection:

    collection.update(id, element)

Delete new element in collection:
    
    collection.delete(id)