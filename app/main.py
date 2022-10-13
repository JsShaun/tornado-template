
import web
import udp 


if __name__ == "__main__":
    udp.start() ## Trio异步UDP数据处理
    web.start() ## tornado 服务端