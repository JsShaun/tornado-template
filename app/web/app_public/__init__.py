from .dictionary import DictV
from .visitor import VisitV
from .province import ProvinceV
from .province.city import CityV
from .province.city.county import CountyV
from .room import RoomV
from .roles import RolesV
from .roles.action import ActionV
from .roles.stats import StatsV



RuleList = [
    (r'/dict/',DictV),
    (r"/login/visit/", VisitV),
    (r"/province/", ProvinceV),
    (r"/province/city/", CityV),
    (r'/province/city/county/',CountyV),
    (r'/room/',RoomV),
    (r'/roles/',RolesV),
    (r'/roles/action/',ActionV),
    (r'/roles/stats/',StatsV),
]  
