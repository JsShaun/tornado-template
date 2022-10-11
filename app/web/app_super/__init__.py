from .user.login import LoginV
from .user.register import RegisterV




RuleList = [
    (r"/user/login/", LoginV),
    (r"/user/register/", RegisterV),
]  




