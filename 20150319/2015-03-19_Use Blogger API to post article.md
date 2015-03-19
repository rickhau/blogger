  
### Use blogger script to post Markdown(.md) to Blogger

#### Virtual Environment
Pre-requisite:
- You need to have Python 2.7 installed on your OS first

- Install and Create your virtual environment
  ```
     $ pip install virtualenv

     Create a virutal environment called py2venv
     $ virtualenv py2venv
     (Note: This will use the default python.exe to create)

     If you'd like to create python 3 environment,
     Please specify the path of python3.exe.
     $ virtualenv -p C:\Python34 py3venv

     Activiate your virtual environment
     On windows:
     $ cd py2venv\Scripts
     $ activate
     On Linux:
     $ source py2venv/bin/activate
  ```
- Exit the virtual environment  
  ` $ deactivate `

> Reference:  
> http://docs.python-guide.org/en/latest/dev/virtualenvs/

#### Install gdata library for Google Blogger API
```
    $ pip install -U gdata
    $ pip install -U gdata-python-client
```

#### Enable your API project
- Go to [Google Developer Console](https://console.developers.google.com/)
- Click **Create Project** button  
    + Enter *Project Name* (Ex: BloggerAPI)  
![html](https://github.com/rickhau/blogger/blob/master/20150319/imgs/01.png)
    + Go to *APIs & auth* --> *Credentials*  
![html](https://github.com/rickhau/blogger/blob/master/20150319/imgs/02.png)
- Click **Create new ClientID**
    + Choose *Installed application* as we are going to create CLI scripts  
![html](https://github.com/rickhau/blogger/blob/master/20150319/imgs/03.png)
	+ Click *Configure consent screen
	  * Choose your gmail
	  * Input your *Product Name* (Ex: Blogger)
	  * Click *Save*
- Click **Create new Key** button
	+ Click *Browser Key*
	+ Click *Create*
- Now, you should be able to see
	+ Client ID for native application
	+ Key for browser application

#### Download the Blogger API script

- I made some change to support command line argument to post html article 
  If the content already exists on blogger, it will not post.

  [blogger.py](https://github.com/rickhau/blogger/blogger.py)

```
    To publish html file to blogger as a new post with title:

      $ blogger --title="This is a new title" --file 2015-3-17.html

    OR

      $ blogger -t="NEW TITLE" -f 2015-3-20.html

      Then, choose 1) to use your gmail account to post the new article(html)
```

> Reference Links:
> - Enable Google Blogger API using your google account  
>   http://wescpy.blogspot.com/2014/11/authorized-google-api-access-from-python.html
> - gdata-python-client library  
    https://developers.google.com/gdata/docs/client-libraries
> - Getting Started  
    https://developers.google.com/gdata/articles/python_client_lib
> - Blogger Python developer guide  
    https://developers.google.com/blogger/docs/1.0/developers_guide_python
