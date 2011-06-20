from model.zsite import Zsite
from model.motto import motto
from model.zsite_link import url_by_id
from model.txt import txt_get
from model.ico import ico96, ico
from model.namecard import namecard_get
from model.follow import follow_count_by_to_id, follow_count_by_from_id

def json_info(user_id):
        user = Zsite.mc_get(user_id)
        namecard = namecard_get(user_id)
        data = {}
        if user:
            data['user_id'] = user_id
            data['self_intro'] = txt_get(user_id)
            data['name'] = user.name
            data['ico'] = ico96.get(user_id)
            data['moto'] = motto.get(user_id)
            data['user_link'] = url_by_id(user_id)
            data['sex'] = namecard.sex
            data['marry'] = namecard.marry
            data['place_home'] = namecard.pid_home
            data['place_now'] = namecard.pid_now
            data['follower_num'] = follow_count_by_to_id(user_id)
            data['following_num'] = follow_count_by_from_id(user_id)
            data['verify_state'] = user.state
            data['pic'] = ico.get(user_id)
        return data
