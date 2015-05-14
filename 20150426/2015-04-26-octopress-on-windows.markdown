---
layout: post
title: "Octopress on Windows"
date: 2015-04-26 17:18:10 +0800
comments: true
categories: markdown, blog
---
## Environment
Windows 7

### Pre-requisite ###
- This article is to setup my Windows 7 environment to write blog posts    
- Use octopress environment pushed by MacOS
- You have python 2.7 installed on your Windows 7
- Remaining taks on Windows 7:
  * Install RubyInstaller    
  * Clone git repository    
  * Configure and continue the post    


### Configure environment ###

####STEP 1: Install RubyInstaller

- Download and install rubyinstaller.exe

  [rubyinstaller](http://rubyinstaller.org/downloads/)
  
  I picked up ruby-2.1.4(x64) to install   
  
  [2.1.4(x64)](http://dl.bintray.com/oneclick/rubyinstaller/rubyinstaller-2.1.4-x64.exe)   
  
####STEP 2: Install Ruby Development Kit

- Download and install `DevKit-mingw64-64-4.7.2-20130224-1432-sfx`

  I installed Ruby 2.1.4(x64), so the development kit I have to use is:    
  
  [For use with Ruby 2.0 and 2.1 (x64 - 64bits only)](http://dl.bintray.com/oneclick/rubyinstaller/DevKit-mingw64-64-4.7.2-20130224-1432-sfx.exe)
  
  I extract to `C:\Ruby21-Devkit` where my ruby was installed under `C:\Ruby21-x64`    
  
    
####STEP 3: Create ruby config.yml

- Open your windows terminal 

```
   > cd C:\Ruby21-Devkit    
   > ruby dk.rb init
   # This will generate a config.yml
```  

- Edit config.yml to add where you install the ruby

```
    ---
    - C:/Ruby21-x64
```

- Install it

```
    > ruby dk.rb install
```
  
####STEP 4: Update gem

- Run the following command:

```
    > gem update --system
```
 
  Then, you will see the following messages:
  
```
    SSL_connect returned=1 errno=0 state=SSLv3 read server certificate B: certificate verify failed
```

- Solve the SSL issue    

```
    # To get what gem version you have installed
   > gem --version
```

  1) Download RubyGems based on the gem version you have installed. 
  
   Picked up 2.2.x due to my system reports 2.2.2    
   * [2.2.x](https://github.com/rubygems/rubygems/releases/tag/v2.2.3)    
  
   Others:    
   * [1.8.x](https://github.com/rubygems/rubygems/releases/tag/v1.8.30)   
   * [2.0.x](https://github.com/rubygems/rubygems/releases/tag/v2.0.15)
  
  2) Run the following commands:
  
```
    C:\>gem install --local C:\rubygems-update-1.8.30.gem
    C:\>update_rubygems --no-ri --no-rdoc
    C:\>gem uninstall rubygems-update -x
```

  Congratulations! 
  
  3) Now, let's update gem 
  
     gem update --system
    
  Reference link:
  >- [SSL issue](https://gist.github.com/luislavena/f064211759ee0f806c88)

####STEP 5: Clone your git repository

- Please git clone your "source" branch not "master" branch    
  You can configure your github page using "source" as the default branch

```
    > git clone https://github.com/rickhau/rickhau.github.io.git
    > cd rickhau.github.io
    > gem install bundler
    > bundle install
```

  Note:   
  Due to .gitignore, you might miss some files when cloning your project to windows    
  Please copy the entire foloder to your windows    
  

- Preview your existing posts

```
    > rake preview
```

  Go to http://localhost:4000 to browse your old posts

####STEP 6: Write your new post

```
    > rake new_post["Your new post title"]
```

  Go to `source\_posts\` directory to edit your new markdown file for new article.
  

####STEP 7: Configure the UTF-8 encoding

```
    set LC_ALL=zh_TW.UTF-8
    set LANG=zh_TW.UTF-8
```

- Or you can write it in the .bat script to help you set the encoding automatically

```
    @echo off
    set LC_ALL=zh_TW.UTF-8
    set LANG=zh_TW.UTF-8
    rake generate
    rake preview
```

#### Rake Deploy Error due to git rejection

- `rake deploy` error due to git rejection

```bash
    ## Committing: Site updated at 2015-04-26 12:53:26 UTC
    On branch master
    nothing to commit, working directory clean

    ## Pushing generated _deploy website
    Warning: Permanently added 'github.com,xxx.xxx.xxx.xxx' (RSA) to the list of know
    n hosts.
    To git@github.com:rickhau/rickhau.github.io.git
     ! [rejected]        master -> master (non-fast-forward)
    error: failed to push some refs to 'git@github.com:rickhau/rickhau.github.io.git
    '
    hint: Updates were rejected because the tip of your current branch is behind
    hint: its remote counterpart. Integrate the remote changes (e.g.
    hint: 'git pull ...') before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

- Solution:    

  Please find the following section in your `Rakefile`    
  
```ruby
  cd "#{deploy_dir}" do
    system "git add -A"
    message = "Site updated at #{Time.now.utc}"
    puts "\n## Committing: #{message}"
    system "git commit -m \"#{message}\""
    puts "\n## Pushing generated #{deploy_dir} website"  
    Bundler.with_clean_env { system "git push origin #{deploy_branch}" }   #<-- Modify this line
    puts "\n## Github Pages deploy complete"
  end
```

```
    Bundler.with_clean_env { system "git push origin +#{deploy_branch}" }  
    # Add '+' before #{deploy_branch}
```

   Then, re-run `rake deploy`
   
```bash
    ## Pushing generated _deploy website
    Warning: Permanently added 'github.com,xxx.xxx.xxx.xxx' (RSA) to the list of know
    n hosts.
    Counting objects: 80, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (41/41), done.
    Writing objects: 100% (47/47), 4.67 KiB | 0 bytes/s, done.
    Total 47 (delta 23), reused 0 (delta 0)
    To git@github.com:rickhau/rickhau.github.io.git
     + b8e5c0f...80aaf79 master -> master (forced update)

    ## Github Pages deploy complete
    cd -
```

  Now, you can go back to edit `Rakefile` to remove '+' sign.
  
#### Use slash octopress theme

- Run the following commands to overwrite the existing old fashion theme

```
$ cd octopress
$ git clone git://github.com/tommy351/Octopress-Theme-Slash.git .themes/slash
$ rake install['slash']
$ rake generate
```


Links:
>- [在Windows上使用Octopress](http://tonytonyjan.net/2012/03/01/install-octopress-on-windows/)
>- [Windows安裝Octopress新手教學](http://itspg.logdown.com/posts/1701-octopress-on-windows-tutorial)
>- [在Windows上設定Octopress](http://pro.ctlok.com/blog/2012/03/26/windows-install-octopress.html)    
>- [Rake deploy causes git rejection](http://r-c.im/blog/2014/05/02/octopress-deploy-rejected/)

#### HAPPY WRITING!!!! #####