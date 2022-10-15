from .import receive_and_send
from afore.utils import new_thread
import trio


@new_thread
def start():
    trio.run(receive_and_send.Task)



