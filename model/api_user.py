from model.zsite import Zsite
from model.motto import motto
from model.zsite_link import url_by_id
from model.txt import txt_get
from model.ico import ico96, ico, ico_url
from model.namecard import namecard_get
from model.follow import follow_count_by_to_id, follow_count_by_from_id
from zkit.earth import place_name

def json_info(user_id):
        user_id = int(user_id)
        user = Zsite.mc_get(user_id)
        namecard = namecard_get(user_id)
        data = {}
        if user:
            data['cid'] = user.cid
            data['user_id'] = user_id
            data['self_intro'] = txt_get(user_id)
            data['name'] = user.name
            data['ico'] = ico_url(user_id) or ''
            data['moto'] = motto.get(user_id)
            data['user_link'] = "http:%s"%user.link
            data['sex'] = namecard.sex
            data['marry'] = namecard.marry
            data['follower_num'] = follow_count_by_to_id(user_id)
            data['following_num'] = follow_count_by_from_id(user_id)
            data['verify_state'] = user.state
            data['pic'] = ico.get(user_id)
            if namecard.pid_now:
                data['place_now_name'] = place_name(namecard.pid_now)
                data['place_now'] = namecard.pid_now
            if namecard.pid_home:
                data['place_home_name'] = place_name(namecard.pid_home)
                data['place_home'] = namecard.pid_home
        return data
