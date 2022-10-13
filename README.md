# Tornado
* 这是一个Web异步框架应用模版

# Trio
* 并行I/O同時執行多項操作的 async runtime



# 启动Redis服务
- docker run -itd --name Redis --restart=always -p 6379:6379 redis:alpine


# docker镜像
- docker build -t tornado:web .
### 正式环境
- docker run --name tornado-web -it -p 5016:5016 -p 5016:5016/udp tornado:web python3 -u main.py
### 更新当前运行容器
- docker run --name $(docker rm $(docker stop tornado-web)) -p 5016:5016 -p 5016:5016/udp -d tornado:web python3 -u main.py
### Docker清除未挂载的所有资源
- docker system prune