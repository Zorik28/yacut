### Project run on local server
1. Install the virtual environment:
```py -m venv venv```
   
   
   Activate:
```. venv/Scripts/activate```

2. Upgrade pip version:
```py -m pip install --upgrade pip```


   Install dependencies from requirements.txt:
```pip install -r requirements.txt```

3. Run shell:
```flask shell```
   
4. Create the table:
```>>> from yacut import db```


```>>> db.create_all()```

5. Run tha YaCut!
```flask run```
