---
layout: post
title: "How to write your blog using Octopress + Github"
date: 2015-04-26 14:49:35 +0800
comments: true
categories: markdown, blog
---

## Environment
Mac OS

** STEP 1: Create your github account **    
- Please register your github account    
- Create a repository name called `username.github.io`    

** STEP 2: Install Octopress **    
- Install RVM (Use RVM to install ruby later)     
  
    curl -L https://get.rvm.io | bash -s stable --ruby

- Install ruby and relative stuff

```
    $ rvm install 2.1.4 && rvm use 2.1.4
    $ git clone git://github.com/imathis/octopress.git octopress
    $ cd octopress 
    $ ruby --version
    $ gem install bundler
    $ bundle install
    $ rake install
```
** STEP 3: Deploy to Github **
- Initialize your new github pages    

    $ rake setup_github_pages

  Input your Github page repository you created in step 1    
  Ex: `git@github.com:rickhau/rickhau.github.io.git`   

- Edit `_config.yml`

  tailor this configuration file to your needs

- Deploy to github   
```
    $ rake generate
    $ rake deploy
    $ git add .
    $ git commit -m "Push octopress blog to Thegithub"
    $ git push -u origin source
```
** STEP 4: Write New Post ** 

    $ rake new_post["Your blog post title"]

   Then, it will create a markdown file under `source/_posts`.    
   Please edit this .markdown to write your new article

** STEP 5: Enable your Octopress to support table sytanx **

- Add data-table.css to `source/stylesheets`    
  
  {% gist 1993032 data-table.css %}

  [data-table.css](https://gist.githubusercontent.com/programus/1993032/raw/data-table.css)    

- Add the following informaiton into `source/_include/head.html`    
```
    <link href="/stylesheets/data-table.css" media="screen, projection" rel="stylesheet" type="text/css" />
```
  Like this:    
```
    <head>
      ...
      <script src="{{ root_url }}/javascripts/octopress.js" type="text/javascript"></script>
      <link href="/stylesheets/data-table.css" media="screen, projection" rel="stylesheet" type="text/css" />
      ...
    </head>     
```
** STEP 6: Publish your new post  **

    $ rake generate
    $ rake preview  
    # Check your post preview by `http://localhost:4000`
    # Modify your post until done

- Publish    
```   
    $ rake generate
    $ rake deploy
```

- Commit your source change
```
    $ git add .
    $ git commit -am "Push message you'd like to say"
    $ git push origin source
```


Reference links:    
>- http://samwize.com/2012/09/11/how-to-setup-octopress-on-github-pages    
>- http://samwize.com/2012/09/24/octopress-table-stylesheet    
>- http://octopress.org/docs/deploying/github/    
>- http://zerodie.github.io/blog/2012/01/19/octopress-github-pages    
>- http://shaching.github.io/2014/06/25/how-to-install-octopress-blog-with-github    
>- https://gist.github.com/benbalter/5555251
