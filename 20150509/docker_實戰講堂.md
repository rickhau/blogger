## Docker 實戰講堂筆記(2015-05-09)
==================

### Target Project    

- Codebase@Github -- Web Hook --> DockerHub(Registry)    

  Commit any change, trigger DockerHub    

### Docker

- Containerization   
  In most cases, a dockerized app acts as a normal native process within the host OS.   

- Dockerized app   
  a. EXPOSE ports  
  b. data VOLUME  
  c. daemon off  
  PS. Not every app can be dockerized, you have to meet above pre-requisites.   

- Docker can NOT runa cross platform directly   
  a. Linux kernel(> 3.10) --> Linux container --> Docker engine      
  &nbsp;&nbsp;(x86-64)    
  b.   Arch Linux         --> Linux container --> Docker engine      
  &nbsp;&nbsp;(ARM, Raspberry Pi)    
  c. Windows Server(> 2016?) --> Windows Container --> Docker Engine   
  &nbsp;&nbsp;(x86-64)    
  ![StackImg](http://william-yeh.github.io/docker-workshop/slides/img/dockerized-app.png)
  
- Static structure vs. Dynamic Behavior  
  a. EXE vs Process   
  b. Class vs Object  
  c. Image vs. Container (Docker)   

- Vagrant Command
  a. vagrant ssh `<machine name>`     
  b. vagrant up `<machine name>`   
  c. vagrant status   
  d. vagrant halt `<machine name>`    
  e. vagrant destroy `<machine name>`  

- Docker Hub (Pull images)  
  a. docker pull busybox  
  b. docker pull redies  
  c. docker pull ubuntu  

- Docker command   
  a. docker images     
  b. docker ps  
  c. docker images --tree    
  d. **docker build .**        # `.` means current directory  
     **docker build `-t` IMAGE_NAME .**  
     **docker build `-t` IMAGE_NAME:TAG .**  
  e. docker run `IMAGE NAME or IMAGE ID(at least 4 digits)` /bin/walk-tree/go /  
  f. docker stop `<image id or name>`  
  g. docker rm `<image id or name>`  
  h. docker run -d `<image id or name>`    # `-d` means daemonized or background  
     (Return a `container id`)  
  i. docker logs `<image id or name>`  
  j. docker inspect `<image id or name>`  
  k. docker rmi `<image id or name>`   # remove image  
  l. docker run --name some-nginx \  
     **-v** `/some/content:/usr/share/nginx/html:ro` `-d nginx`  
     `-v` means Data Volume(VM directory) for docker app nginx use
  
  **Image Naming:**  
  a. docker tag `image_id` `image_name`:`TAG`  
     - docker tag 5c62 myredis  
     - docker tag 5c62 myredis:2.8.19  
     - 
  **Container Naming: (You can not re-name after execution)**  
  a. docker run **--name** `CONTAINER_NAME` `IMAGE_ID_or_NAME`  
  b. docker kill `CONTAINER_NAME` to remove container  
  
  **Process injection**  
  a. docker **exec** `CONTAINER_NAME` cat /etc/os-release   
  
  **Interactive tty**   
  b. docker **exec** **-it** `CONTAINER_NAME` bash  
  
- VM command to check process
  * `ps faux` to check which pid of redis-server is docker  

- Performance  
  * Performance Comparison of Virtual Machines and Linux Containers  
    [Slides](http://www.slideshare.net/BodenRussell/performance-characteristics-of-traditional-v-ms-vs-docker-containers-dockercon14)  
    [Video](https://www.youtube.com/watch?v=JHqM_5X3MBU&feature=youtu.be)  
    [Paper](http://domino.research.ibm.com/library/CyberDig.nsf/papers/0929052195DD819C85257D2300681E7B/$File/rc25482.pdf)  
  * Docker Tips And Tricks  
    [Slides](http://www.slideshare.net/jpetazzo/docker-tips-and-tricks-at-the-docker-beijing-meetup)
    
  
- Docker Images
  a. ID(as 64-character hash)  
  b. Official repo   
     * [Ubuntu](https://registry.hub.docker.com/_/ubuntu/)  
  c. User-created images   
     * docker pull youraccount/usercreateimage  
     * docker pull youraccount/usercreateimage:tags
  d. Commerical image service  
     * docker pull quay.io/ACCOUNT/IMAGE  
  e. Self-hosted private registry
     * docker pull IP:PORT/ACCOUNT/IMAGE  

- Docker Stack
  * Install different VMs(Ubuntu, CentOS,..etc) on top of Vagrant
  * Manipulate your docker images on different VMs(Ubuntu, CentOS, ..etc)
  * Docker resides on top of one VM, so all docker images use the same kernel 

- Major difference between Virtual Machine and Docker
  * Virtual Machine has **Linux kernel**, root filesystem, Libs,...
  * Docker does not have ~~Linux kernel~~ but root filesystem, Libs,...

- GitHub hooks DockerHub  
  * Github  
    Add Service (Docker)
  * DockerHub  
    a. Settings -> Linked Account (Github)  
    b. View Profile -> Add repository  -> Automated build  
       --> Select the Github project repository  
       --> Naming your Repository Name for your Docker (Default: Github name)  

- Container's network settings
  * [Docker Networking Model](http://blog.daocloud.io/docker-source-code-analysis-part7-first/)

  * Bridge Mode - Isolated Network (Need to query the Docker IP)  
  
  ```
     $ docker run -d redis
     4abcdef....
     $ docker inspect 4abc | grep IPAddress
   OR
     $ C_IP=$(docker inspect  \
       --format '{{ .NetworkSettings.IPAddress }}'  \
       CONTAINER_ID_OR_NAME)
  ```  
  ![Image](http://blog.daocloud.io/wp-content/uploads/2015/01/Docker_Topology.jpg)
  
  * Host Mode - Skip Bridge
  
  ```
     $ docker run -d   \
       --net=host  \
       IMAGE_ID_OR_NAME
  ```  
      ![Docker](http://blog.daocloud.io/wp-content/uploads/2015/01/Docker_Network_host.jpg)
      
  * Port-mapping  

```
   $ docker run -d   -p 10080:3000   IMAGE_ID_OR_NAME
```
  
- Docker Compose
  * Use YAML(docker-compose.yml)  
  ```  
      app:
        build: .
        ports: 
          - "10080:3000"
  ```
  
  Same as the following Docker CLI
  
  ```
     $ docker build .
     $ docker run [-d] -p 10080:3000 IMAGE_ID_OR_NAME
  ```
  * Run `docker-compose` to read .yml w/o remembering all the docker CLI commands  
  
  ```
    Foreground:
    $ docker-compose up
    Background: 
    $ docker-compose up -d
  ```
  * [Python Dockerfile](http://william-yeh.github.io/docker-workshop/slides/build-pl.html#65)

#### Container Linking (IMPORTANT)

- Traditional Software <==> Dockerized Software  
  
  ![CombinationImg](http://william-yeh.github.io/docker-workshop/slides/img/redis-scenario-all.png)
  
  * Dockerized Client --> Dockerized Server, How??  
    - Dockerized redis-server   
    
    ```
      $ docker run -d --name redis1 redis:2.8.19
    ```  
    
    - Dockerized client  
      
      **--link** `target-name:alias`  
      
    ```
      $ docker run -it --link redis1:redis busybox
                                     ^^^^^
                                     alias(environment variable)
    ```
    
      You can get the dockerized server from   
      1) **env** (environment variable)   
      2) **cat /etc/hosts**  
      
 Note: As long as you keep alias w/o change, you can link to any target server names.
 
 ```
  $ docker run -it          \
    --link redisXXX:redis \
    redis:2.8.19          \
    \
    client
```

#### Avoid Daemonized Yourself

- Docker will daemonized by default, No need to daemonized again  
  You do not need to do ~~-d~~ by yourself.  


### APPENDIX / REFERENCE
- [Docker Slides](http://william-yeh.github.io/docker-workshop/slides/index.html#1)
- [Docker Registry](https://registry.hub.docker.com/)
- [Docker Gitbook](http://philipzheng.gitbooks.io/docker_practice/)
- [Docker command](http://philipzheng.gitbooks.io/docker_practice/content/appendix_command/README.html)
- [Dockerfile reference](https://docs.docker.com/reference/builder/)
- [Quest for minimal Docker images](http://william-yeh.github.io/docker-mini/#1)
- [Docker Host tools](https://github.com/William-Yeh/docker-host-tools/)  
- Presentation
  * [技術簡報好用工具](https://ihower.tw/blog/archives/8075)  
  * [Presentation Mouse effect](http://boinx.com/mousepose/overview/)  
  * [KB/Mouse on Screen effect](http://apple.stackexchange.com/questions/52618/how-can-i-show-typing-keyboard-in-record-screen)  