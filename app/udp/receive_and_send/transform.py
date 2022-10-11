from model.buffer import Buf
import trio


async def receiver(sock,receive_channel):
    """监听UDP服务"""
    print("启动监听UDP服务")
    while 1:
        data,(ip,port) = await sock.recvfrom(1024)
        buf = Buf(ip,port,data)
        await receive_channel.upload(buf)

async def sender(sock,send_channel,check_queue):
    """UDP发送"""
    print("启动UDP发送")
    async for buf in send_channel.down():
        # print("发送源数据：",buf.to_msg())
        await sock.sendto(buf.data,(buf.ip,buf.port))

async def checker(sock,check_queue):
    """确认发送"""
    while 1:
        await trio.sleep(1)        
        for _ in range(check_queue.qsize()):
            buf = check_queue.down()
            if buf:
                # print("重新发送数据",buf)
                # print("当前md5集合",check_queue.md5_dict)
                await sock.sendto(buf.data,(buf.ip,buf.port))

        
        else:
            await trio.sleep(1)















    