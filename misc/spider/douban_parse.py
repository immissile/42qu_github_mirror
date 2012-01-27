#coding:utf-8

import _env
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from model.douban import douban_feed_new, id_by_douban_feed, douban_user_feed_new,\
DOUBAN_USER_FEED_VOTE_REC, CID_DOUBAN_FEED_TOPIC, CID_DOUBAN_FEED_NOTE,\
user_id_by_douban_url, douban_url_user_new, id_by_douban_url_new ,\
CID_DOUBAN_URL_GROUP, CID_DOUBAN_URL_SITE 

def url_last(url):
    return url.rstrip("/").rsplit("/", 1)[1]

class ParseRec(object):
    cid = None
    
    def func_url(self, title):
        return (None, "") 

    def __call__(self, title, user_id):
        cid = self.cid
        
        func , url = self.func_url(title)
        rid = url_last(url)
        id = id_by_douban_feed(cid, rid)

        if not id and func:
            from douban_like import user_id_list_by_like, URL_LIKE
            yield user_id_list_by_like , URL_LIKE%(cid, rid), cid, rid
            yield func , url
        else:
            douban_user_feed_new(DOUBAN_USER_FEED_VOTE_REC, cid, rid, user_id)
       
class ParseRecTopic(ParseRec):
    cid = CID_DOUBAN_FEED_TOPIC

    def func_url(self, title):
        t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
        url , topic_name = t[1]
        return parse_topic_htm, url

parse_topic = ParseRecTopic()


class ParseRecNote(ParseRec):
    cid = CID_DOUBAN_FEED_NOTE

    def func_url(self, title):
        t = [i.split('">', 1) for i in txt_wrap_by_all('<a href="', '</a>', title)]
        url , note_title = t[1]

        if url.startswith("http://www.douban.com/note/"):
            func = parse_note_people_htm
        elif url.startswith("http://site.douban.com/widget/notes/"):
            func = parse_note_site_htm
        else:
            func = 0
        return func, url

parse_note = ParseRecNote()

 


class ParseHtm(object):
    cid = None

    def htm(self, data):
        return ""

    def user_id(self, data):
        return 0

    def topic_id(self, data):
        return 0

    def title(self, data):
        title = txt_wrap_by("<title>", "</title>", data)
        return title

    def __call__(self, data, url):
        rid = url_last(url)

        title = self.title(data)

        rec_num = txt_wrap_by('<span class="rec-num">', "人</span>", data) or 0
        like_num = txt_wrap_by('<span class="fav-num" data-tid="', '</a>喜欢</span>', data) or 0
        if like_num:
            like_num = txt_wrap_by('<a href="#">', '人', like_num)

        owner_id = self.user_id(data)
        if owner_id:
            _owner_id = user_id_by_douban_url(owner_id)

            if not _owner_id:
                from douban_like import fetch_user 
                yield fetch_user(owner_id)
                _owner_id = douban_url_user_new(owner_id, 0, "") 
            owner_id = _owner_id 
        
        douban_feed_new(
            self.cid, rid, rec_num, like_num, title, 
            self.htm(data)      ,
            owner_id  ,
            self.topic_id(data) 
        )       
        for uid in set(txt_wrap_by_all('href="http://www.douban.com/people/','"',data)):
            uid = uid.rstrip('/')
            from douban_like import fetch_user 
            if uid.isalnum():
                yield fetch_user(uid)

class ParseTopicHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_TOPIC
    def htm(self, data):
        result = [
            txt_wrap_by('<div class="topic-content">', '</div>', data)
        ]
        user_id = self.user_id(data)
        topic_reply =  txt_wrap_by('<ul class="topic-reply">','</ul>',data)
        topic_reply =  txt_wrap_by_all(' <div class="reply-doc">',' class="lnk-reply">回应</a>',topic_reply)
        
        for i in topic_reply:
            owner_id = txt_wrap_by('<div class="bg-img-green">','</h4>',i)
            owner_id = txt_wrap_by('<a href="http://www.douban.com/people/','/">',owner_id)
            if owner_id!=user_id:
                break
            result.append(txt_wrap_by('</div>','<div class="operation_div"',i)) 
                    
        return '\n'.join(result)

    def user_id(self, data):
        line = txt_wrap_by('<div class="user-face">','">',data)
        line = txt_wrap_by('"http://www.douban.com/people/','/',line)
        return line

    def topic_id(self, data):
        line = txt_wrap_by('<div class="aside">','">回',data)
        line = txt_wrap_by('"http://www.douban.com/group/','/',line)
        id = id_by_douban_url_new(CID_DOUBAN_URL_GROUP, line)
        return id
    
    def title(self, data):
        title = txt_wrap_by('<tr><td class="tablelc"></td><td class="tablecc"><strong>标题：</strong>','</td>', data)
        if not title:
            title = txt_wrap_by("<title>", "</title>", data)
        return title

parse_topic_htm = ParseTopicHtm()

class ParseNoteSiteHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_NOTE
    def htm(self, data):
        return txt_wrap_by(' class="note-content"><pre>', "</pre>", data)

    def topic_id(self, data):
        line = txt_wrap_by('<div class="sp-logo">','" ',data)
        line = txt_wrap_by('http://site.douban.com/','/',line) 
        id = id_by_douban_url_new(CID_DOUBAN_URL_SITE, line)
        return id

parse_note_site_htm = ParseNoteSiteHtm()

class ParseNotePeopleHtm(ParseHtm):
    cid = CID_DOUBAN_FEED_NOTE

    def htm(self, data):
        return txt_wrap_by('<pre class="note">', "</pre>", data)

    def user_id(self, data):
        line = txt_wrap_by('<div class="pic">','">',data)
        line = txt_wrap_by('"http://www.douban.com/people/','/',line)
        return line


parse_note_people_htm = ParseNotePeopleHtm()

if __name__ == "__main__":
    html = """
<!DOCTYPE html>
<html lang="zh-CN" class="ua-windows ua-ff9">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <title>
    你知道各个职业都在做什么吗，很长但很全面（转贴）
</title>
    <script> (function(d){var i=function(b,a,c){var e=new Date,f,a=a||30,c=c||"/";e.setTime(e.getTime()+a*864E5);a="; expires="+e.toGMTString();for(f in b)d.cookie=f+"="+b[f]+a+"; path="+c},j=function(b){b+="=";var a,c,e,f=d.cookie.split(";");for(c=0,e=f.length;c<e;c++)if(a=f[c].replace(/^\s+|\s+$/g,""),a.indexOf(b)==0)return a.substring(b.length,a.length).replace(/\"/g,"");return null},h=d.write,k={"douban.com":1,"douban.fm":1,"google.com":1,"googleapis.com":1,"gmaptiles.co.kr":1,"gstatic.com":1,"google-analytics.com":1, "googleadservices.com":1},l=function(b,a){var c=new Image;c.onload=function(){};c.src="http://www.douban.com/j/except_report?kind=ra022&reason="+encodeURIComponent(b)+"&environment="+encodeURIComponent(a)},g=function(b){try{h.call(d,b)}catch(a){h(b)}},m=/<script.*?src\=["']?([^"'\s>]+)/ig,n=/http:\/\/(.+?)\.([^\/]+).+/i;d.writeln=d.write=function(b){var a=m.exec(b),c;a?(c=n.exec(a[1]))?k[c[2]]?g(b):j("hj")!=="tqs"&&(l(a[1],location.href),i({hj:"tqs"},1),setTimeout(function(){location.replace(location.href)}, 50)):g(b):g(b)}})(document); </script>

    
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="Sun, 6 Mar 2005 01:00:00 GMT">

    
      <link href="http://img3.douban.com/css/packed_douban6772193981.css" rel="stylesheet" type="text/css">
      <link href="http://img3.douban.com/css/separation/packed__all9552936037.css" rel="stylesheet" type="text/css">
    <script >var _head_start = new Date();</script>
    <script src="http://img3.douban.com/js/packed_jquery.min6301986802.js"></script>
    <script src="http://img3.douban.com/js/packed_douban521020567.js"></script>
    <script src="http://img3.douban.com/js/separation/packed__all1312701400.js"></script>
    

    <style type="text/css">
    
        .operation_div .lnk-reply { display:none; }

    .operation_div .lnk-delete-comment { display:none; }
    .operation_div .lnk-report { display:none; }
    .topic-doc { font-size:13px;line-height:1.62; }
    .topic-report { height: 22px; padding: 4px 0; }
    .topic-report a { float:right; display: none; }
    .topic-figure { text-align:center;color:#999;margin-bottom:2px; }
    .topic-figure img { max-width:500px; }
    .topic-figure-title { display:block; font-size:12px; }
    .clearfix {clear: both;}
    .clear {clear: both;}
    .reply-comment { width:90%;position:relative;padding:3px 4px;margin-bottom:5px;background-color:#e8eef2; }
    .reply-comment .lnk-close { position:absolute;right:10px;top:10px;font-weight:800;line-height:1.2;padding:0 2px; }
    .reply-comment .lnk-close:link { color:#999; }
    .reply-comment .lnk-close:hover { background-color:#999;color:#fff; }
    .reply-comment p { width:30em;padding:6px;margin:0; }
    .pubdate { white-space:nowrap;margin-left:10px; }
    .reply-quote { width:30em;padding-left:7px;margin:20px 0;border-left:1px solid;  }
    .topic-reply li { background:#fff; }
    .operation_div { display:none;position:absolute;right:0;bottom:0;  }
    .operation_div a { margin-left:20px;line-height:1.2; }
    .operation_div a:link,
    .operation_div a:visited { color:#aaa; }
    .operation_div a:hover,
    .operation_div a:active { background-color:#aaa;color:#fff; }

</style>
    <script>

$(function(){
    $("#joingroupbtn").click(function(){
        url = "/j/group/" + $(this).attr("name") + "/join";
        $.post_withck(url, {},
            function(sjson){
                var ret = eval("(" + sjson + ")");
                $("#joingroupbtn").hide();
                if (ret.result=="toomany"){
                    $("#replysect").html('<p class="attn" align="right">你已经加入了250个小组，无法再加入更多小组。</p>');
                }else{
                    $("#replysect").html('<br/><h2>你现在加入了这个小组，可以发表回应　· · · · · ·　</h2><div class="txd"><form name="comment_form" method="post" action="add_comment"><div style="display:none;"><input type="hidden" name="ck" value="1hyK"/></div><textarea name="rv_comment" rows="8" cols="54"></textarea><br/><input type="hidden" name="start" value="0"/><input type="submit" value="加上去"/></form></div>');
                }
            });
        return false;
    });

    $("body").delegate(".topic-doc", 'mouseenter mouseleave', function (e) {
        var target = $('.topic-report a');
        switch (e.type) {
        case "mouseenter":
            target.show();
            break;
        case "mouseleave":
            target.hide();
            break;
        }
    });

    $(".topic-reply li").bind('mouseenter mouseleave click', function (e) {
        var comment_user_id = $(this).find(".operation_div").attr("id"),
        can_delete = 0,
        can_report = 0;
        if (comment_user_id == 1262808){
            can_delete = 1;
        }
        if (comment_user_id!=1262808){
            can_report = 1;
        }
        if (can_delete==1){
            $(this).find(".lnk-delete-comment").show();
        }
        if (can_report==1){
            $(this).find(".lnk-report").show();
        }
        switch (e.type) {
        case "mouseenter":
            $(this).find(".operation_div").show();
            break;
        case "mouseleave":
            $(this).find(".operation_div").hide();
            break;
        case "click":
            tar = $(e.target);
            if (tar.hasClass("lnk-report")) {
                e.preventDefault();
                var TXT_CFM_WARN = "确定要举报这条垃圾广告吗？",
                    id = tar.data("id"),
                    type = tar.data("type");

                var result = confirm(TXT_CFM_WARN);

                if (result) {
                    $.post_withck(
                        "/j/misc/report_ad",
                        {
                            id: id,
                            type: type
                        }
                    );
                }
            }
            break;
        }
    });


    $('body').delegate('.reply-comment .lnk-close', 'click', function(e){
      e.preventDefault();
      $(this).parent().remove();
    });

});

</script>

    <link rel="shortcut icon" href="http://img3.douban.com/favicon.ico" type="image/x-icon">
</head>
<body>
  
    <script type="text/javascript">var _body_start = new Date();</script>
    
   

<div class="top-nav">
  <div class="bd">
    






<div class="top-nav-info">
        
        <a href="http://www.douban.com/doumail/">豆邮<em>(43)</em></a>
    <a target="_blank" href="http://www.douban.com/accounts/">张沈鹏的帐号</a>
    <a href="http://www.douban.com/accounts/logout?ck=1hyK">退出</a>
</div>


    <div class="top-nav-items">
        <ul>

                
                    
                    <li class="on">
                    <a href="http://www.douban.com/">豆瓣社区</a>
                    </li>
                
                    
                    <li>
                    <a href="http://book.douban.com/">豆瓣读书</a>
                    </li>
                
                    
                    <li>
                    <a href="http://movie.douban.com/">豆瓣电影</a>

                    </li>
                
                    
                    <li>
                    <a href="http://music.douban.com/">豆瓣音乐</a>
                    </li>
                
                    
                    <li>
                    <a href="http://www.douban.com/location/">豆瓣同城</a>
                    </li>
                
                    
                    <li>

                    <a href="http://douban.fm/" target="_blank">豆瓣FM</a>
                    </li>
                
                    <li class="top-nav-more">
                        <div class="top-nav-more-items">
                            <a href="#more" class="more">更多 <span class="arrow">&nbsp;</span>&nbsp;</a>
                            <ul>
                            
                            <li><a href="http://9.douban.com" target="_blank">九点</a></li>

                            
                            <li><a href="http://alphatown.com" target="_blank">阿尔法城</a></li>
                            </ul>
                        </div>
                    </li>
        </ul>
    </div>
  </div>
</div>
<script>
Do(function(){
    var more = $('.top-nav-more a.more').click(function(e){
      e.preventDefault();
      var el = $(e.currentTarget), p = el.parent();
      p.toggleClass('on');
      return false;
    });
    $('body').click(function(){
      more.parent().removeClass('on');
    });
});

</script>
 

    <div id="wrapper">
        
<div id="header">
    







<div id="db-nav-main" class="site-nav">
    <div class="site-nav-logo">
        <a href="http://www.douban.com"><img src="http://img1.douban.com/pics/nav/lg_main_a10.png" alt="豆瓣"></a>
    </div>

    <div class="bd">
    <div class="nav-srh">

        <form name="ssform" method="get" action="/search">
            <div class="inp">
                <span><input name="search_text" type="text" title="成员、小组、音乐人、主办方" size="22" maxlength="60" value=""/></span>
                <span><input class="bn-srh" type="submit" value="搜索"/></span>
            </div>
        </form>
    </div>
    <script type="text/javascript">
        Do(function(){
            $("form[name=ssform]").submit(function(){
                if($("input[name=search_text]").val()==="成员、小组、音乐人、主办方"){
                    return false;
                }
            })
        })
    </script>

    <div class="site-nav-items nav-logged-in">
     <ul>
      <li><a href="http://www.douban.com/">豆瓣猜</a></li>
      <li><a href="http://www.douban.com/update/">友邻广播</a>
      </li>
      <li><a href="http://www.douban.com/mine/">我的豆瓣</a></li>
      <li><a href="http://www.douban.com/group/">我的小组</a></li>

      <li><a href="http://www.douban.com/site/">我的小站</a></li>
     </ul>
    </div>
    </div>
    <div class="ext"></div>
</div>
<script>
Do(function(){
    $('#db-nav-main .nav-srh form').prettyField();
    $('#db-nav-main .guide .lnk-close').click(function(e) {
      e.preventDefault();
      $.post_withck('/j/accounts/hidetip',{kind:5,show_to_all:'Y'}, function(){});
      $(this).closest('.tips-overly').fadeOut(300);
    });
});
</script>


    

</div>

        
    <div id="content">
    
    <h1>你知道各个职业都在做什么吗，很长但很全面（转贴）</h1>

    <div class="grid-16-8 clearfix">
        
        <div class="article">
    
    <div class="topic-content clearfix">
        <div class="user-face">
            <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>

        </div>
        <div class="topic-doc">
            <h3>
                <span class="color-green">2011-03-08 02:19:11</span>
                <span class="pl20">来自: <a href="http://www.douban.com/people/2485199/">哭蛉</a></span>
            </h3>

            

            <div class="topic-content">

                        
                        <p>职场围城，复杂程度远超婚姻围城。因为婚姻最多分正室还是外遇，而职场却充满了360行之惑（诱惑的惑）。哪一行银子最多？那一行我适合吗？——你可能总是在问，我也是。
<br/>
<br/>所以，写这篇文章，给那些20 plus的人看，因为我30 plus。我很希望，有40 plus的人，能够写这样的文章给我看。
<br/>
<br/>严重备注：本文信息，仅以个人所了解的资讯为准，不具有科研价值。而且，如果你觉得里面的主人公工资都很高，请记住，他们（她们）一律很辛苦、很坚持，很有才。</p>

            </div>


            <div class="topic-opt clearfix">



                &nbsp; &nbsp;


            </div>

                <div class="topic-report">
                    <a class="gact" href="http://www.douban.com/misc/report?type=T&uid=18099270">举报</a>
                </div>


        <div class="sns-bar">
            <div class="sns-bar-rec">
                
                    
    
    <span class="rec" id="Topic-18099270">
        <a href= "#" data-url="http://www.douban.com/group/topic/18099270/" data-desc="" data-title="【你知道各个职业都在做什么吗，很长但很全面（转贴）】职场围城，复杂程度远超婚姻围城。因为婚姻最多分正室还是外遇，而职场却充满了360行之惑（诱惑的惑）。哪一行银子最多？那一行我适合吗？——你可能总是在问，我也是。所以，写这篇文章..." data-pic="" class="bn-sharing ">分享到</a> &nbsp;&nbsp;
    </span>
    <script>
        var cache_url = cache_url || {};
        (function(u){ if(cache_url[u]){ return; } cache_url[u] = true; $.getScript(u); })('http://img3.douban.com/js/lib/packed_sharebutton5215351074.js');
    </script>

                    






    <script type="text/javascript" src="http://img3.douban.com/js/packed_dshare4865807643.js"></script>

<div class="rec-sec">

    <span class="rec">

<a href="http://shuo.douban.com/!service/share?apikey=&amp;name=%E4%BD%A0%E7%9F%A5%E9%81%93%E5%90%84%E4%B8%AA%E8%81%8C%E4%B8%9A%E9%83%BD%E5%9C%A8%E5%81%9A%E4%BB%80%E4%B9%88%E5%90%97%EF%BC%8C%E5%BE%88%E9%95%BF%E4%BD%86%E5%BE%88%E5%85%A8%E9%9D%A2%EF%BC%88%E8%BD%AC%E8%B4%B4%EF%BC%89&amp;image=&amp;redir=http%3A%2F%2Fwww.douban.com%2Fgroup%2Ftopic%2F18099270%2F&amp;href=http%3A%2F%2Fwww.douban.com%2Fgroup%2Ftopic%2F18099270%2F&amp;curl=&amp;type=com.douban.group&amp;properties=%7B%22href%22%3A%22http%3A%5C%2F%5C%2Fwww.douban.com%5C%2Fgroup%5C%2Fyouzhaopin%5C%2F%22%2C%22name%22%3A%22%E5%9C%88%E5%86%85%E6%8B%9B%E8%81%98%EF%BC%88joboto.com%EF%BC%89%22%2C%22uid%22%3A%22youzhaopin%22%7D&amp;desc=%E8%81%8C%E5%9C%BA%E5%9B%B4%E5%9F%8E%EF%BC%8C%E5%A4%8D%E6%9D%82%E7%A8%8B%E5%BA%A6%E8%BF%9C%E8%B6%85%E5%A9%9A%E5%A7%BB%E5%9B%B4%E5%9F%8E%E3%80%82%E5%9B%A0%E4%B8%BA%E5%A9%9A%E5%A7%BB%E6%9C%80%E5%A4%9A%E5%88%86%E6%AD%A3%E5%AE%A4..." share-id="18099270" data-mode="plain" data-name="你知道各个职业都在做什么吗，很长但很全面（转贴）" data-type="com.douban.group" data-desc="职场围城，复杂程度远超婚姻围城。因为婚姻最多分正室还是外遇，而职场却充..." data-href="http://www.douban.com/group/topic/18099270/" data-image="" data-properties="{&quot;href&quot;:&quot;http:\/\/www.douban.com\/group\/youzhaopin\/&quot;,&quot;name&quot;:&quot;圈内招聘（joboto.com）&quot;,&quot;uid&quot;:&quot;youzhaopin&quot;}" data-redir="http://www.douban.com/group/topic/18099270/vote?ck=1hyK" data-text="" data-apikey="" data-curl="" data-count="10" data-object_kind="1013" data-object_id="18099270" data-target_type="rec" data-target_action="0" data-action_props="{&quot;topic_title&quot;:&quot;你知道各个职业都在做什么吗，很长但很全面（转贴）&quot;,&quot;topic_url&quot;:&quot;http:\/\/www.douban.com\/group\/topic\/18099270\/&quot;}" class="lnk-sharing lnk-douban-sharing">推荐</a>
</span>
<span class="rec-num">8181人</span>
</div>

            </div>
            <div class="sns-bar-fav">

                



        <span class="fav-num" data-tid="18099270" data-tkind="1013"><a href="#">9593人</a>喜欢</span>
                <a class="fav-add btn-fav" title="标为喜欢？" href="#" data-tid="18099270" data-tkind="1013">喜欢</a>
        <script>
           (typeof Do === 'function' ? Do : $).call(null, function(){
                if (typeof hasInitFavBtn !== 'undefined') {
                    return;
                }
                hasInitFavBtn = 1;
                $('html').delegate('.btn-fav', 'click', function(e) {
                    e.preventDefault();
                    var self = $(e.currentTarget),
                        hasFav = self.hasClass('fav-cancel') ? 1 : 0,
                        paras = {
                            tid: self.data('tid'),
                            tkind: self.data('tkind'),
                            ck: '1hyK'
                        };

                    if (self.hasClass('stat-processing')) {
                        return;
                    }

                    self.addClass('stat-processing');

                    $.ajax({
                        type: hasFav ? 'delete' : 'post',
                        url: '/j/like',
                        data: paras,
                        success: function (o) {
                            self.removeClass('stat-processing');
                            if (o.r === 0) {
                                if (hasFav) {
                                    self.removeClass('fav-cancel').addClass('fav-add').attr('title', '标为喜欢?');
                                    updateFavNum(self, -1);
                                } else {
                                    self.removeClass('fav-add').addClass('fav-cancel').attr('title', '取消喜欢?');
                                    updateFavNum(self, 1);
                                }
                            }
                        },
                        dataType: 'json'
                    });
                });

                
var api_userlist = 'http://www.douban.com/j/like',
$win = $(window),
updateFavNum = function(node, n) {
  var p = node.parent(), favNum = p.find('.fav-num'), num;
  $('#fav-userlist').hide();
  if (favNum.length === 0) {
    favNum = $(['<span class="fav-num" data-tkind="', node.data('tkind'),'" data-tid="', node.data('tid'),'"><a href="#">0人</a>喜欢</span>'].join(''));
    p.prepend(favNum);
  }

  num = parseInt(favNum.find('a').text(),10) + n;
  if (num === 0) {
    favNum.remove();
    return;
  }
  favNum.find('a').text(num + '人');
},
renderUserList = function(node, da) {
  if (!$.isArray(da)) {
    $('#fav-userlist').hide();
    return;
  }

  var i = 0, o, pos, h, htmlstr = ['<ul>'];
  if (da.length > 0){
      for (; o = da[i++]; ) {
        htmlstr.push([
         '<li>',
         '<a href="http://www.douban.com/people/', o.uid, '" target="_blank" class="pic"><img src="', o.icon_avatar,'" width="24" height="24"></a>',
         '<a href="http://www.douban.com/people/', o.uid, '" target="_blank">', o.screen_name,'</a>',
         '</li>'
        ].join(''));
      }
      htmlstr.push('</ul>');
  } else {
      htmlstr = ['<span>啊哦…喜欢这个的人都不愿意露脸</span>'];
  }


  node.removeClass('arrow-bottom').find('.bd').css({
    height: i > 9 ? 220 : 'auto',
    overflow: i > 9 ? 'auto' : 'hidden'
  }).html(htmlstr.join(''));

  pos = node.offset();
  h = node.height();

  if (pos.top - $win.scrollTop() + h > $win.height() - 40) {
    node.addClass('arrow-bottom').css('top', pos.top - h - 55);
  }
};

$('html').bind('click', function(e) {
  var list = $('#fav-userlist');
  if (list.length === 0 ||
      list.css('display') === 'none' ||
      e.target.tagName === 'A') {
    return;
  }
  if (!$.contains(list[0], e.target)) {
    list.hide();
  }
});

$('html').delegate('.fav-num a', 'click', function(e) {
  e.preventDefault();
  var el = $(e.currentTarget),
  pos = el.offset(),
  params = el.parent().data(),
  dataId = [params.tkind, params.tid].join(''),
  fav_user_list = $('#fav-userlist');

  if (fav_user_list.length === 0) {
    fav_user_list = $([
    '<div id="fav-userlist" class="fav-userlist">',
    '<div class="hd"><a href="" class="btn-close">X</a></div>',
    '<div class="bd">',
    '</div><i class="arrow"></i>',
    '</div>'
    ].join('')).appendTo('body');
    fav_user_list.find('.btn-close').click(function(e){
      e.preventDefault();
      fav_user_list.hide();
    });
  }

  fav_user_list.removeClass('arrow-bottom').
      find('.bd').
      css('height', 'auto').
      html('加载中...');

  fav_user_list.css({
    top: pos.top + 22,
    'margin-left': (function(con){
      return -1 * Math.floor(con.width()/2 - pos.left + con.offset().left) -10;
    })($('#content'))
  }).show();

  $.get(api_userlist,
  {
      tkind: params.tkind,
      tid: params.tid,
      alt: 'xd'
  },
  function(e){
    renderUserList(fav_user_list, e);
  }, 'jsonp');
});

            });
        </script>



            </div>
        </div>

        </div>
    </div>

    
    <ul class="topic-reply">
        

<li class="clearfix" id="211644091">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">

        <div class="bg-img-green">
          <h4> 2011-03-08 02:19:28
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>
            </h4>
        </div>
        <p>一、        一个Marketing职员在做什么？
<br/>
<br/>（1）       帮助研发部门确定研究的方向：你要到不同的城市或者不同的销售场所去抽取一些消费者进行调查，想办法了解某个地区的消费者喜欢什么产品和服务，不喜欢什么，你的调查要非常详细，有时候详细到连消费者自己可能都没有考虑过的问题，比如说：您喜欢的红是亮一些的，还是暗一些的？把消费者的喜好总结起来，就是一个新产品或新服务的概念。
<br/>
<br/>（2）       和广告商合作设计电视广告，选定媒体和播放形式，比如是连续20天每天播放，还是每间隔一天进行播放等等；对于每一种设计你都要找出足够的理由和数据支持。

<br/>
<br/>（3）       设计广告语是最重要的环节，很多广告都是由于精彩的广告语才被记住的，比如“钻石恒久远，一颗永流传”之类的。
<br/>
<br/>（4）       和平面设计商合作设计店内陈列使用的图片，比如化妆品的美女图，新东方的宣传册之类。
<br/>
<br/>（5）       设计店内的陈列方式，怎么样摆放产品才最吸引眼球。
<br/>
<br/>（6）       设计促销的方法，是买一送一，还是大特价，或是赠送钥匙扣之类的小礼品更好呢？
<br/>
<br/>（7）       有些促销计划有可能要先在某些城市或市场做实验性的推广，那么你要选择先在哪些城市实验。
<br/>
<br/>（8）       把自己的方案做成PowerPoint, 和sales做沟通，说服他们接受你设计的广告和促销计划，然后销售部的人才会乐于去和超市或者经销商协调怎么样把我们的产品卖出去。
<br/>
<br/>（9）       多和研发部门和销售部门沟通能够使自己更好地了解他们的想法，也就更容易说服他们。
<br/>
<br/>（10）   做市场的出路当然就是一直做下去，从负责小品牌到负责大品牌，收入和成就感都是相当高的。
<br/>

<br/>（11）   需要特别提醒应届毕业生的是，当你刚刚加入市场部的时候，你可能每天只是负责一些琐碎的小事，比如说，把新产品的海报送到杂货店，或者到零售网点采集销售数据。
<br/>
<br/> 什么样的人适合做Marketing? 
<br/>（1）       天生就是“点子王”，总能想出出人意料的好点子，也就是具有“创造性思维” 。
<br/>
<br/>（2）       做事敢于适当冒险，愿意尝试与众不同的新方法并敢于承担失败的责任。
<br/>
<br/>（3）       有科学的态度和理性的思维，做事比较理智喜欢用客观的分析的眼光和数据说话。逻辑思维能力强，分析问题讲究前因后果，能把复杂问题简单化。
<br/>
<br/>（4）       有远见，很多市场营销活动是不能够短期起效的，你要比其他人看的远、想的早、行动快，并且对未来进行长远的规划，然后按照规划一步一步地实施。
<br/>
<br/> Marketing的人挣多少钱？ 
<br/>每个公司marketing的人收入完全不同，那些marketing作用大于sales的公司，marketing的人收入就明显高一些，比如大家都知道的宝洁。拥有5年以上经验的名企品牌经理，基本工资一般不超过30万，除非是持有股票的，或者是从广告公司吃拿卡要的。那些市场宣传方式相对简单的公司，比如本人服务过的某体育用品公司，中国北区的市场主管也只能止步与10万年薪，切不易加薪。
<br/>
<br/>如果你想从marketing工作中拿到高薪，卖“产品”的公司，无论是吃的、穿的、用的，要比卖“服务”的公司要更适合你，后者比如银行、咨询公司等等。</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644091#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644091" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644091">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211644111">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 02:19:44
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>

            </h4>
        </div>
        <p>二、        一个公关（PR）部的职员做什么？
<br/>
<br/>（1）       做公关是幕后工作，你要把所服务的企业、老板、产品推到镁光灯下，自己却要保持默默无闻，越不留痕迹的公关越好。
<br/>
<br/>（2）       公关工作的一部分是政府公关，也就是说做好公司和政府主管部门的协调沟通，当公司的某个部门要和政府部门搞活动时，你就要去和政府部门联系，协调好时间、地点、人物等等细节。
<br/>
<br/>（3）       公关公共做的另一个部分当然是媒体公关，你需要拓展维护媒体关系，安排采访。一旦有新产品要发布，要做出具体安排：比如邀请哪些媒体、哪些记者到场，安排什么样的接待，新闻稿主要传达的信息是什么。
<br/>
<br/>（4）       一旦某个部门签约了一个大客户，你要在第一时间内为他们宣传这个成功案例，准备统发新闻稿，争取在重要媒体刊登。撰写新闻稿，审核所有公司对外宣传的材料，以保证所有对外宣传的公关口径全部一致。
<br/>
<br/>（5）       危机处理。在企业陷入信任危机时挺身而出，动用一切媒体资源及政府、业界人脉关系重建口碑。
<br/>

<br/>（6）       媒体资源是公关的命脉，真正要理顺和一家报社的媒体关系，要涉及到各方面的人，除了对口记者，还要兼顾编辑、摄影、部门主任甚至是主编。所以说，多积累媒体资源是这一行业的制胜法宝。
<br/>
<br/>（7）       公关人员要养成翻阅报纸的习惯，比较本公司和竞争对手在媒体亮相的次数、好坏，以此总结出这段时间公司存在的公关问题，再对症下药。一般在公司或大型事业单位作公关工作的工作人员每年都必须搜集所有有关报道的剪报、电视录像、视频资料并作总结，所以也要养成“处处留心”的好习惯。
<br/>
<br/>（8）       进了公关这一行，除了在企业里做公关，还可以到专业的公关公司去，比如国内的本土最大的公关公司蓝色光标、美资的奥美公关等。这一行的路并不宽，但是打交道的人都是公司的高层人士，也有机会转到别的部门去。
<br/>
<br/> 什么样的人适合做PR? 
<br/>（1）       做PR的人外表要达到端庄的标准，因为你代表的是公司形象。丑人也莫要伤心，丑人自有丑人的职业和乐趣，新东方就不在乎，丑点反而让学员觉得亲切。
<br/>
<br/>（2）       既然代表公司形象，而且频繁和媒体打交道，口齿清晰是绝对必要的。
<br/>
<br/>（3）       口头表达能力和书面表达能力都是重头戏。公关是沟通上下级、单位与社会的桥梁，所以沟通能力也是最为看重的公关素质。
<br/>
<br/>（4）       和政府部门有关系以及和媒体有关系都将使你更加适合这个职业！公关公司尤其青睐在媒介打拼过的记者和传媒专业的毕业生，正是看中其天然的人脉资源优势。我见过一个做PR的女孩子，原来在市政府宣传办，很容易就跳槽到一间最大的公关公司任职。
<br/>

<br/> PR的人挣多少钱？ 
<br/>想靠做PR发财的，只能到专业的公关公司（很难进，也很辛苦）。如果在公司的公关部做，很难做到高薪。很多外企的女销售，最大的梦想就是等生完孩子、或者体力不支以后，转到HR部门去，图个轻松。当然，钱袋也大大地轻了。
<br/>
<br/>根据某猎头公司的资讯，除非专业公关公司，其它公司和企业公关部的人，即使做到经理，10万年薪者居多，20万者罕见。</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644111#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644111" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644111">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211644138">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 02:20:02
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>
            </h4>
        </div>
        <p>三、       直接和客户打交道的sales是一个什么样的职位？
<br/>
<br/>（比如ABB的机电销售、IBM的小型机销售、用友的ERP销售等、广告公司的业务代表等）
<br/>
<br/>（1）       直接和目标客户打交道的销售职位，不同于日用消费品的销售代表，后者只和超市或批发商打交道。
<br/>
<br/>（2）       做销售，最重要的是客户。你要尽全部的能力找出下列答案：谁是目标客户？谁是决策者？谁会帮你？谁会唱反调？及早发现唱反调的人就有可能挽救一个单子。如果你在IBM做销售，你可能只面对某个特定范围的客户，比如说农业银行系统、制造业的公司、国税局等等，一个单子可能要跟上一两年。

<br/>
<br/>（3）       做销售要善于利用资源，公司的一切都可以为你所用，包括公司的工程师、高层经理甚至CEO。
<br/>
<br/>（4）       职业优点缺点：做销售很自由，不用按时上下班，花钱也比较随便一些。但是必须要承受很大的心理压力，销售定额时时都悬在头上，而且还要应付丢单子的压力，毕竟我们不能每次都赢。
<br/>
<br/>（5）       做销售最好的出路就是在公司里一路上升，做到管理层。一般来说销售做到高层的机会比别人高一些，因为销售是整个公司的生命线；但是即使如此，毕竟能升上去的仍然是少数，所以要注意积累资源，尽量延长自己做销售的职业寿命。其实在一些有技术含量的领域里，一些Top Sales可以靠老朋友和老客户，一直干到退休。我认识的一个在全球最大制药公司的女销售，干了12年销售，现在负责北京的协和医院，每个月的收入都非常可观，当然她也非常痛恨公司像榨汁机一样，销售目标一路飙升! 不过她想好了，既然自己不想往管理方面发展，那么就要接受做销售这个“月有阴晴圆缺”的职业特点，哪天真顶不住销售目标的压力了，大不了换一家小公司养老，反正这十几年，也把家底挣够了。
<br/>
<br/> 什么样的人适合做sales? 
<br/>（1）       不害怕压力！你是否经历过考试越近就越睡不好觉？去面试的前两天就开始变得焦躁？如果是，你很可能不适合。出色的sales，必定有超乎常人的压力承受能力。如果你不具备这个能力，即使勉强做了sales也会食不甘味，寝不安席。
<br/>
<br/>（2）       你会把goal（任务）变成go（去努力）的动力吗？还是会整天抱怨老板黑了心肝给你这么高的goal（意义相当于出租车司机的“份钱”)？如果你是那种正因为有了目标所以才充满动力的人，你适合做sales!
<br/>
<br/>（3）       你有关心人的天赋吗？还是你觉得关心一个不太熟识的人会很肉麻？作为sales，最重要的事情就是快速建立起和目标客户的亲密关系。我认识的一个高级 sales，隔三差五就会发短信给我，天凉就嘱咐我穿暖一点，天热就建议我喝绿豆汤（他是群发的信息，关心人已经成了他的习惯）。如果你不小心得知你一个目标客户的儿子考大学没考好，离本科线差几分，你是会偷偷避开这个霉头，还是会立刻拼命去了解各个学校的大专分数线以及就业情况，然后立即和你的客户一起商量，即使他觉得你有点多此一举？关心人，而且是真诚地长期地关心人，才能打动你的目标客户。
<br/>
<br/>（4）       你是有激情的人吗？做销售需要激情勃发，需要你每天都充满了完成goal的欲望，需要你对签下合同以后的巨大成就感和完成目标以后拿到提成的一刹那充满了激动的渴望，这才会成为一个好销售。
<br/>

<br/>（5）       你是一个有责任感的人吗？好的sales不可能每天都有新客户，你的资源大部分来自于老客户。你的客户生意好了，他才会持续地采购你的设备，所以一个好的 sales会对客户高度负责，把客户的生意当作自己家的生意，把客户的问题当作自己家的问题，这种责任感是top sales的必要素质。
<br/>
<br/> 这类Sales的人挣多少钱？ 
<br/>对钱有极度渴望的人，除了自己做老板，必须去做销售。一来，即便你刚出校门，即便你公司不是一流企业，只要你是有毅力的销售，靠业绩拿年薪10万是非常轻松的。如果你已有5－10年经验，不拿到30万就很差了。如果你是超级销售，你基本就是这个企业的下一个CEO（CEO来自销售的概率是90％啊。）</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644138#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644138" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644138">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211644157">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 02:20:13
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>
            </h4>
        </div>
        <p>四、        一个消费品公司的sales过着什么样的生活？
<br/>
<br/>（1）       新人第一关几乎永远是“跑街”，我本人在柯达公司上班的第一个月，就要负责把长安街以南的北京领土上所有卖柯达胶卷的大小店铺访问一遍，询问销售情况和代理商的供货情况，尽可能摸清是否会有“水货”（走私货）供应上来。柯达公司是相当仁慈的了，允许我们每天来去打的两次，其余路程，可是必须要徒步穿行了；据说有的公司规定必须要坐公交车跑街，一跑可就是一两个月甚至小半年哪！
<br/>
<br/>（2）       日用消费品公司跑街的任务，常常是到各个超市去当“理货员”，把最便宜又促销的产品摆放在最“出脱”的位置，也就是靠近门口的货架、多层货架上靠近视平线的那几层或者店堂内最抢眼的那几个货架。你的货架越黄金，消费者越容易购买你的产品，店方才会多进货并且肯把黄金货架长期让你享用。
<br/>

<br/>（3）       做销售，不论职位高低，总是在不停地被人拒绝，所以绝对不要怕丢“面子”，甚至根本就不要觉得这是丢“面子”的事情；工作就是工作，要和个人的情绪分开才行。
<br/>
<br/>（4）       做销售要学会和三教九流的人打交道，学会见什么人说什么话，对什么样的话题都能聊两句。和三十来岁的超市售货员就要谈子女教育、谈怎么制服腰包里有点小钱的老公；和四十来岁的部门经理可能要聊聊“保鲜”的体会（保持共产党员先进性）；面对素质不高的客户讲的荤笑话，即使你不愿意降低人格随声附和，你也必须面不改色心不跳，无论如何不能流露出鄙视的神情。
<br/>
<br/>（5）       在搞促销的时候销售是最忙的，要说服超市提供黄金位置、配合市场部做堆头搞陈列、应付店方经理要求增加赠品数量等无理要求。
<br/>
<br/>（6）       做销售不只是要出去跑，也要做报表、做销售反馈单、做销售计划、开会等等。
<br/>
<br/>（7）       在日用消费品公司做销售在中国目前还不能算是一个好的终生职业，因为日用消费品的销售技术含量并不高，新人和“老”人做下来的效果差不多，所以很难保证你靠着多年的经验能够一直做下去，尤其是在某些龌龊的公司，销售的goal（定额）见风长，任你长了三头六臂也很难完成，那就很难保证每个月的个人进帐了。所以说，靠出色的业绩进入销售管理层是一个最佳的选择。
<br/>
<br/>（8）       总体来说，我更鼓励大家从事一些有技术含量的销售，那么你的可替代性就非常地小了，技术含量越高，经验也就越值钱。我的一个朋友做轴承销售，日子过得相当舒服。
<br/>
<br/> 这类Sales的人挣多少钱？ 
<br/>消费品公司底层的销售，由于没有技术含量，收入其实并不高。进入管理层以后，只要完成goal，作为经理的收入就可以逾越外企经理人很难逾越的30万年薪了。当然，即便是30万的背后，也有无数的折磨。</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644157#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644157" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644157">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211644183">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 02:20:26
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>

            </h4>
        </div>
        <p>五、        一个管理咨询顾问会过什么样的生活？
<br/>
<br/>（典型公司：波士顿咨询、毕博管理咨询、麦肯锡等）
<br/>
<br/>（1）       所谓管理咨询顾问，就是给对方公司提出管理上的建议。
<br/>
<br/>（2）       管理咨询的案例五花八门，有可能是帮助对方公司设计一个肯定能通过ISO9001认证的一个工作流程；有可能是帮助他们设计整个公司的ERP系统（企业资源管理系统）；或者给某些公司规划未来十年的发展战略。正因为如此，咨询行业也需要学习各种专业的人才，而不是我们通常所设想的一定是MBA毕业。
<br/>
<br/>（3）       咨询行业不可能把你变成一个全才，现实情况是，你更多地会掌握某一个领域的专业知识，比如设计财务管理流程，或者设计计算机管理系统，然后一直围绕着这个老本行干下去，或者到其他的公司从事相关的工作。
<br/>
<br/>（4）       做咨询员是有一条标准职业发展路径的：从咨询公司到MBA，再回到咨询公司然后转到大公司任管理职位。在咨询行业，你的很多客户都是非常优秀的公司，那么你有可能被这个公司看上，跳槽到自己的客户那里去工作。我的一个学长，曾经在全球排名第一的波士顿咨询公司上海办事处工作过五年，他在给一家来中国投资的美国薄膜企业做投资咨询时，获得了该公司总裁的赏识，一下子被任命为中国区的副总经理（时年36岁），年薪高达10万美元。
<br/>

<br/> 什么样的人适合做咨询顾问? 
<br/>（1）       因为要和客户打交道，行为举止让人看着舒服，不要有什么特别让人难以忍受的缺陷。我有一个“面试口语”班的学员朋友，虽然很英俊但眼角长了一颗黑痣，他 MBA毕业以后想进咨询公司任职却屡面屡败，最后还是拿激光扫除了这颗他窃以为的幸运痣，幸运才真正降临到他头上，被一家本地最有名的咨询公司录用了。
<br/>
<br/>（2）       做咨询行业要有自信，尽管你可能是一个刚大学毕业的黄毛丫头，你却要指手划脚，去告诉一个在某个行业里已经摸爬滚打了许多年的老板应该这样做而不是那样做。这种高强度的心理压力需要你良好的心理素质来应付，因为做咨询的人不可能对所有的行业都了如指掌。
<br/>
<br/>（3）       人看上去要有灵气，客户才会信任你；做事细致有条理；讲话清清楚楚、方案层次分明；普通话要标准；好胜但不是野心勃勃，活泼但不张扬，合作但不抢功。
<br/>
<br/>（4）       看问题看得准，能够给出建设性的意见，因为这个行业本身就是给人提出建议的。
<br/>
<br/>（5）       擅长做陈述，很多方案要在会议上以陈述的方法向顾客提出来，所以必须善于在公共场合陈述观点并且能在没有准备的情况下回答现场提问。
<br/>
<br/>（6）       领导才能、量化分析能力是咨询公司最需要的技能。
<br/>
<br/>  管理咨询顾问挣多少钱？ 
<br/>一流管理咨询公司的顾问当然要拿一流的薪水，一般来收，刚入行的人年薪8－10万，一两年做到senior,有10－15万；通常3－5年后能到咨询经理，就差不多25万的薪资。（根据业内TOP的某市场营销分析公司、某地产信息咨询公司、某管理咨询公司的综合薪水所得数字。）至于再网上，那就看是否能在行政级别上有所突破了，因为刚才所说的咨询经理，实际上管理只能很弱，主要是自己干活。当你管理一个比较大的部门的时候（优秀学历加上优秀资历加上人到中年），你就可以至少拿到50万以上了。</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644183#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644183" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644183">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211644210">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 02:20:37
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>

            </h4>
        </div>
        <p>六、         “个人理财”是个什么样的职业？
<br/>
<br/>（1）       顾名思义，“个人理财”就是帮助客户去打理他/她的个人财产，使其得以保值、增值。
<br/>
<br/>（2）       在美国、加拿大等西方国家，有很多自雇（自己雇佣自己，俗称“个体户”）的个人理财咨询师，他们帮助客户合理避税、提供买卖股票、基金、理财产品的咨询服务。
<br/>
<br/>（3）       在中国，目前还很少有提供综合理财服务的“个人理财”顾问，大部分的个人理财顾问，都分别受雇于保险公司、银行、房地产中介、证券公司等机构，他们只对本机构所提供的理财产品和服务提供咨询，而不能为客户提供“一揽子”理财方案。这种“各立门户”式的理财服务，导致很多理财顾问只了解本机构的产品和服务，而对其他行业和机构的产品和服务则不甚了了，而恰恰是这一点，使得很多客户难以信任这些“个人理财”顾问的专业性。
<br/>
<br/>（4）       我们有理由相信，提供综合理财服务的个人理财顾问，即将成为一个新兴职业。即使你是供职于银行的一名理财顾问，你也必须对保险、房地产、股票甚至彩票等其他投资渠道了如指掌，你才可以顺利说服客户购买本机构的产品和服务。
<br/>

<br/>（5）       我建议所有想从事“个人理财”这个职业却又不知从何下手的大学生们，买一本《穷爸爸富爸爸》来读一读，你就会对理财有一些基本的了解。
<br/>
<br/> 什么样的人适合做“个人理财”? 
<br/>（1）       热衷于实现资产增值。
<br/>
<br/>（2）       有很强的财务意识，对数字非常敏感。
<br/>
<br/>（3）       敢于冒险，但是又具有规避风险的意识。
<br/>
<br/>（4）       有极强的说服能力。
<br/>
<br/> 个人理财员挣多少钱？ 
<br/>中国的个人理财员，10个有9个是理财销售，而非理财咨询师。所以，这个行业的起薪很低，即便是渣打等外资银行，底薪也3000以下每月，而且提成并不容易拿到。理财师真正的高薪时代，需要等他们学会帮我们理财才能到来。</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644210#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644210" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644210">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211644226">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 02:20:50
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>

            </h4>
        </div>
        <p>七、        一个审计师在做什么？
<br/>
<br/>（1）       审计是审计机关依法独立检查被审计单位的会计凭证、会计账簿、会计报表以及其他与财政收支、财务收支有关的资料和资产，监督财政收支、财务收支真实、合法和效益的行为。
<br/>
<br/>（2）       顾名思义，审核+计算=审计。审报表、再审报表、查帐、再查帐、盘货等等都是审计人员的日常工作。
<br/>
<br/>（3）       网上有大量关于“四大”会计师事务所的工作介绍，如果读者感兴趣，不妨去拜读一下。
<br/>
<br/> 什么样的人适合做审计? 
<br/>（1）       细致的审计工作并非人人喜欢，能够一做就几十年还能升到合伙人位置的人毕竟是少数，他们不论喜欢不喜欢自己的工作都能做出一流质量，而且还能在重复劳动中找到工作的乐趣。
<br/>

<br/>（2）       你能够在一堆文件中一泡就是一两天吗？你能够长期忍受简单脑力劳动吗？你能够静下心来准备那个通过率极低的CPA考试吗？
<br/>
<br/> 审计师挣多少钱？ 
<br/>起薪大约6千，做到senior或者项目经理大约2万，做到partner以后年薪50万以上，我想这是审计行业公开的秘密了。</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644226#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644226" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644226">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211644256">
    <div class="user-face">
        <a href="http://www.douban.com/people/2485199/"><img class="pil" src="http://img3.douban.com/icon/u2485199-14.jpg" alt="哭蛉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 02:21:09
                <a href="http://www.douban.com/people/2485199/">哭蛉</a>
            </h4>
        </div>
        <p>八、        “人力资源”是个什么样的职业？
<br/>
<br/>（1）       一般人事事务工作包括：录用、退工，四金交纳，个税，薪资计算，考勤管理，人事档案维护，日常考核，招聘等。
<br/>
<br/>（2）       你必须熟悉劳动人事法规，能够起草劳动合同、保密协议和服务期协议等。
<br/>
<br/>（3）       起草各项人事规章，如[员工手册]、[年度考核实施纲要]，并协助进行工作分析并整理职位说明书。

<br/>
<br/>（4）       对薪酬管理制度、福利制度、绩效考核、激励手段等进行开发或者提出建议。
<br/>
<br/>说到人力资源，笔者要补充一段自己的体会，因为我的脑海中不停浮现出06年底课堂上的一幕。当时我们正在讨论“理想职业”这个话题，我的两个学员先后举手发言：
<br/>
<br/>小A：   我学的是酒店管理，但是我想毕业以后做人力资源，我觉得我特别适合与人打交道。
<br/>
<br/>小 B：   我现在的职位是一家制药公司（我们公司是欧洲最大的精细化工公司）的人力资源助理，但是我觉得我快要闷死了，每天的工作都挺无聊的：给员工办理或转移三险（养老/失业/大病）、给员工转入转出档案、把人事相关的文件比如简历整理并存档等等；我原来希望能从事的招聘、绩效考评、员工培训之类的大事情都和我没有什么关系，基本都是经理在操作，我只能打打杂。而且我们那经理都放出口风来了，说她要在这里干一辈子，那我还有什么希望升职呢？而且我觉得即使做到人力资源经理的职位也没什么意思，好像不如销售那样可以整天往出跑……
<br/>
<br/>其实，小B所反映的基本就是人力资源这个行业的真实情况：
<br/>
<br/>（1）       当你还在“助理”这个职位上的时候，你的工作性质更多地是paperwork，是很多事物性的工作，比如考勤，比如办理录用、退工、公积金、准生证明等手续的时候员工要带什么资料，找哪些部门办理等，总之80%的精力都会花在琐碎的事情上。
<br/>
<br/>（2）       作为助理，你很可能没有太多的机会去做你觉得特别“有意义”的事情，比如“阅人无数”，用你的“慧眼”为企业挑选良才；或者开发一个员工没有被挖掘出的能力，让他在某个工作岗位上大放异彩。
<br/>
<br/>（3）       只有坐到了人事部经理（而且是比较大的公司的人事经理）的高位上，才会真正开始与“人”打交道：设计最有效的方式为企业招聘最优质的员工、了解员工的需求并且有技巧地反映给老板、组织最有帮助的培训项目等等。
<br/>

<br/> 什么样的人适合做“人事”? 
<br/>（1）       仪态庄重并且有很强的亲和力。大公司的人事经理可能要和媒体打交道，所以这里的仪态庄重往往也是相貌端庄之意。
<br/>
<br/>（2）       人比较成熟理智，善于观察，善于聆听。
<br/>
<br/>（3）       出语谨慎，不能八卦，但是也不能给人一种敬而远之的感觉。
<br/>
<br/>（4）       能够接受没有太多刺激性、没有什么变化的工作性质。HR工作是细水长流的，你必须接受一个现实，就是你不能指望自己在一夜之间就获得别人的认同和尊重，你所做的东西不是短期的、具体的、量化的；而是间接的、长期的、柔性的。
<br/>
<br/>（5）       无论HR的工作多么重要，它在企业里永远是配角，所以你要接受一个现实，就是在庆祝成功的时候可能提不到你的名字，你也很难获得火箭式的提升。
<br/>
<br/>  HR挣多少钱？ 
<br/>HR的高薪，一律发生在从业至少5甚至10年之后。不做到大公司的总监职位，做HR的薪水很难和销售和市场去比较。但是，一旦做到高层，HR也可能是世界上最好的职位了</p>

        <div class="operation_div" id="2485199">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211644256#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211644256" class="j a_confirm_link lnk-delete-comment" title="真的要删除哭蛉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211644256">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211645420">
    <div class="user-face">
        <a href="http://www.douban.com/people/2201670/"><img class="pil" src="http://img3.douban.com/icon/u2201670-1.jpg" alt="雨天的太阳"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 02:36:41
                <a href="http://www.douban.com/people/2201670/">雨天的太阳</a> (总结：无财无事业无病痛无桃花)
            </h4>

        </div>
        <p>要是早几年看见这些东西，我就不会是现在这种状况了。这些信息很有用</p>

        <div class="operation_div" id="2201670">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211645420#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211645420" class="j a_confirm_link lnk-delete-comment" title="真的要删除雨天的太阳的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211645420">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211645489">
    <div class="user-face">
        <a href="http://www.douban.com/people/wegel/"><img class="pil" src="http://img3.douban.com/icon/u21920664-2.jpg" alt="wegel"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 02:37:41
                <a href="http://www.douban.com/people/wegel/">wegel</a> (人生，太可怕了！)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="21920664">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211645489#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211645489" class="j a_confirm_link lnk-delete-comment" title="真的要删除wegel的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211645489">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211655053">
    <div class="user-face">
        <a href="http://www.douban.com/people/48619193/"><img class="pil" src="http://img3.douban.com/icon/u48619193-2.jpg" alt="红烧肉"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 07:10:17
                <a href="http://www.douban.com/people/48619193/">红烧肉</a>
            </h4>
        </div>
        <p>好啊</p>

        <div class="operation_div" id="48619193">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211655053#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211655053" class="j a_confirm_link lnk-delete-comment" title="真的要删除红烧肉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211655053">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211655120">
    <div class="user-face">
        <a href="http://www.douban.com/people/6400197/"><img class="pil" src="http://img3.douban.com/icon/u6400197-4.jpg" alt="娃娃爱卢卡"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 07:12:06
                <a href="http://www.douban.com/people/6400197/">娃娃爱卢卡</a> (活在自己的世界不想出来透气)
            </h4>

        </div>
        <p>m</p>

        <div class="operation_div" id="6400197">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211655120#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211655120" class="j a_confirm_link lnk-delete-comment" title="真的要删除娃娃爱卢卡的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211655120">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211655162">
    <div class="user-face">
        <a href="http://www.douban.com/people/fanxiaojie/"><img class="pil" src="http://img3.douban.com/icon/u1101469-54.jpg" alt="Sukida"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 07:12:57
                <a href="http://www.douban.com/people/fanxiaojie/">Sukida</a>
            </h4>
        </div>
        <p>马克</p>

        <div class="operation_div" id="1101469">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211655162#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211655162" class="j a_confirm_link lnk-delete-comment" title="真的要删除Sukida的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211655162">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211656062">
    <div class="user-face">
        <a href="http://www.douban.com/people/36555317/"><img class="pil" src="http://img3.douban.com/icon/u36555317-17.jpg" alt="青豆"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 07:32:51
                <a href="http://www.douban.com/people/36555317/">青豆</a> (得不到的永远在骚动)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="36555317">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211656062#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211656062" class="j a_confirm_link lnk-delete-comment" title="真的要删除青豆的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211656062">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211656672">
    <div class="user-face">
        <a href="http://www.douban.com/people/49358474/"><img class="pil" src="http://img3.douban.com/icon/u49358474-8.jpg" alt="鶿。"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 07:43:45
                <a href="http://www.douban.com/people/49358474/">鶿。</a> (做最好的自己。)
            </h4>

        </div>
        <p>说的很好啊</p>

        <div class="operation_div" id="49358474">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211656672#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211656672" class="j a_confirm_link lnk-delete-comment" title="真的要删除鶿。的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211656672">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211657034">
    <div class="user-face">
        <a href="http://www.douban.com/people/eisntobe/"><img class="pil" src="http://img3.douban.com/icon/u31975634-33.jpg" alt="`E.xN_L 皇帝"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 07:49:38
                <a href="http://www.douban.com/people/eisntobe/">`E.xN_L 皇帝</a> (皇帝，在基督的爱里复活吧)
            </h4>
        </div>
        <p>我现在在大专学的是marketing,考本科打算读工商管理。
<br/>
<br/>LZ怎么看？</p>

        <div class="operation_div" id="31975634">

            <a href="http://www.douban.com/group/topic/18099270/?cid=211657034#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211657034" class="j a_confirm_link lnk-delete-comment" title="真的要删除`E.xN_L 皇帝的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211657034">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211658833">

    <div class="user-face">
        <a href="http://www.douban.com/people/4405285/"><img class="pil" src="http://img3.douban.com/icon/u4405285-2.jpg" alt="dongfanghuazhu"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 08:12:20
                <a href="http://www.douban.com/people/4405285/">dongfanghuazhu</a>
            </h4>

        </div>
        <p>m一个。。。</p>

        <div class="operation_div" id="4405285">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211658833#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211658833" class="j a_confirm_link lnk-delete-comment" title="真的要删除dongfanghuazhu的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211658833">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211661764">
    <div class="user-face">
        <a href="http://www.douban.com/people/48707018/"><img class="pil" src="http://img3.douban.com/icon/u48707018-3.jpg" alt="☆＿★嘻樂"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 08:35:57
                <a href="http://www.douban.com/people/48707018/">☆＿★嘻樂</a>
            </h4>
        </div>
        <p>m一下</p>

        <div class="operation_div" id="48707018">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211661764#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211661764" class="j a_confirm_link lnk-delete-comment" title="真的要删除☆＿★嘻樂的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211661764">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211662031">
    <div class="user-face">
        <a href="http://www.douban.com/people/jielau/"><img class="pil" src="http://img3.douban.com/icon/u1552254-1.jpg" alt="正义作战计划"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 08:37:49
                <a href="http://www.douban.com/people/jielau/">正义作战计划</a>
            </h4>
        </div>
        <p>有时间再看

<br/></p>

        <div class="operation_div" id="1552254">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211662031#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211662031" class="j a_confirm_link lnk-delete-comment" title="真的要删除正义作战计划的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211662031">举报广告</a>
        </div>
    </div>

</li>

        

<li class="clearfix" id="211662371">
    <div class="user-face">
        <a href="http://www.douban.com/people/4727834/"><img class="pil" src="http://img3.douban.com/icon/u4727834-6.jpg" alt="Pandora"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 08:40:15
                <a href="http://www.douban.com/people/4727834/">Pandora</a> (上善若水，知行合一。)
            </h4>

        </div>
        <p>M</p>

        <div class="operation_div" id="4727834">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211662371#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211662371" class="j a_confirm_link lnk-delete-comment" title="真的要删除Pandora的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211662371">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211662783">
    <div class="user-face">
        <a href="http://www.douban.com/people/justinsang/"><img class="pil" src="http://img3.douban.com/icon/u4052722-5.jpg" alt="但醉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 08:42:41
                <a href="http://www.douban.com/people/justinsang/">但醉</a> (小A他二大爷)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="4052722">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211662783#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211662783" class="j a_confirm_link lnk-delete-comment" title="真的要删除但醉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211662783">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211664504">
    <div class="user-face">
        <a href="http://www.douban.com/people/1642177/"><img class="pil" src="http://img3.douban.com/icon/u1642177-14.jpg" alt="林薇"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 08:52:54
                <a href="http://www.douban.com/people/1642177/">林薇</a>
            </h4>
        </div>
        <p>希望再多写点</p>

        <div class="operation_div" id="1642177">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211664504#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211664504" class="j a_confirm_link lnk-delete-comment" title="真的要删除林薇的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211664504">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211665987">
    <div class="user-face">
        <a href="http://www.douban.com/people/vajrapan/"><img class="pil" src="http://img3.douban.com/icon/u2616980-6.jpg" alt="阿稚"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:01:39
                <a href="http://www.douban.com/people/vajrapan/">阿稚</a> (近猪者吃。)
            </h4>

        </div>
        <p>LZ辛苦
<br/>深夜党 or 时差党</p>

        <div class="operation_div" id="2616980">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211665987#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211665987" class="j a_confirm_link lnk-delete-comment" title="真的要删除阿稚的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211665987">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211667789">
    <div class="user-face">
        <a href="http://www.douban.com/people/42536289/"><img class="pil" src="http://img3.douban.com/icon/u42536289-2.jpg" alt="慕"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 09:10:28
                <a href="http://www.douban.com/people/42536289/">慕</a>
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="42536289">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211667789#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211667789" class="j a_confirm_link lnk-delete-comment" title="真的要删除慕的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211667789">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211668593">
    <div class="user-face">
        <a href="http://www.douban.com/people/3677230/"><img class="pil" src="http://img3.douban.com/icon/u3677230-9.jpg" alt="Jessica"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:13:57
                <a href="http://www.douban.com/people/3677230/">Jessica</a> (领导才能？！)
            </h4>
        </div>
        <p>继续继续！正看的有味</p>

        <div class="operation_div" id="3677230">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211668593#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211668593" class="j a_confirm_link lnk-delete-comment" title="真的要删除Jessica的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211668593">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211669771">
    <div class="user-face">
        <a href="http://www.douban.com/people/memorymo/"><img class="pil" src="http://img3.douban.com/icon/u46181406-2.jpg" alt="°呜啦"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:19:23
                <a href="http://www.douban.com/people/memorymo/">°呜啦</a> (深深的话要浅浅地说。)
            </h4>

        </div>
        <p>学习学习…</p>

        <div class="operation_div" id="46181406">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211669771#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211669771" class="j a_confirm_link lnk-delete-comment" title="真的要删除°呜啦的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211669771">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211673632">
    <div class="user-face">
        <a href="http://www.douban.com/people/bobby.xiong/"><img class="pil" src="http://img3.douban.com/icon/u1169058-3.jpg" alt="我想我叫熊"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 09:34:26
                <a href="http://www.douban.com/people/bobby.xiong/">我想我叫熊</a> (简单点)
            </h4>
        </div>
        <p>感谢楼主。</p>

        <div class="operation_div" id="1169058">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211673632#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211673632" class="j a_confirm_link lnk-delete-comment" title="真的要删除我想我叫熊的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211673632">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211677124">
    <div class="user-face">
        <a href="http://www.douban.com/people/anitatu/"><img class="pil" src="http://img3.douban.com/icon/u3291284-72.jpg" alt="桥妹"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:47:29
                <a href="http://www.douban.com/people/anitatu/">桥妹</a> (与小日本不共戴天！)
            </h4>
        </div>
        <p>mark 最近想转型</p>

        <div class="operation_div" id="3291284">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211677124#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211677124" class="j a_confirm_link lnk-delete-comment" title="真的要删除桥妹的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211677124">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211677787">
    <div class="user-face">
        <a href="http://www.douban.com/people/muffin_man/"><img class="pil" src="http://img3.douban.com/icon/u36604810-81.jpg" alt="宋过来    ♥"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:49:49
                <a href="http://www.douban.com/people/muffin_man/">宋过来    ♥</a> (守得住，慢慢来。)
            </h4>

        </div>
        <p>没有了么</p>

        <div class="operation_div" id="36604810">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211677787#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211677787" class="j a_confirm_link lnk-delete-comment" title="真的要删除宋过来    ♥的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211677787">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211679558">
    <div class="user-face">
        <a href="http://www.douban.com/people/sasaxi/"><img class="pil" src="http://img3.douban.com/icon/u2085396-11.jpg" alt="萨萨朵"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 09:56:41
                <a href="http://www.douban.com/people/sasaxi/">萨萨朵</a> (看别人不顺眼是自己修养不够)
            </h4>
        </div>
        <p>来长见识。。</p>

        <div class="operation_div" id="2085396">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211679558#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211679558" class="j a_confirm_link lnk-delete-comment" title="真的要删除萨萨朵的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211679558">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211679582">
    <div class="user-face">
        <a href="http://www.douban.com/people/ineedhappiness/"><img class="pil" src="http://img3.douban.com/icon/u4258964-8.jpg" alt="wanderfor"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:56:45
                <a href="http://www.douban.com/people/ineedhappiness/">wanderfor</a> (wander)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="4258964">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211679582#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211679582" class="j a_confirm_link lnk-delete-comment" title="真的要删除wanderfor的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211679582">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211680147">
    <div class="user-face">
        <a href="http://www.douban.com/people/4260200/"><img class="pil" src="http://img3.douban.com/icon/u4260200-32.jpg" alt="听荷"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 09:58:44
                <a href="http://www.douban.com/people/4260200/">听荷</a> (每一念想都是发愿‖愿力不可思议)
            </h4>

        </div>
        <p>马克</p>

        <div class="operation_div" id="4260200">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211680147#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211680147" class="j a_confirm_link lnk-delete-comment" title="真的要删除听荷的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211680147">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211681364">
    <div class="user-face">
        <a href="http://www.douban.com/people/athule/"><img class="pil" src="http://img3.douban.com/icon/u1682295-27.jpg" alt="百里"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:03:01
                <a href="http://www.douban.com/people/athule/">百里</a> (晚来天欲雪，能饮一杯无。)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="1682295">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211681364#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211681364" class="j a_confirm_link lnk-delete-comment" title="真的要删除百里的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211681364">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211683786">
    <div class="user-face">
        <a href="http://www.douban.com/people/doubankaihua/"><img class="pil" src="http://img3.douban.com/icon/u44618741-2.jpg" alt="豆瓣开花"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:11:29
                <a href="http://www.douban.com/people/doubankaihua/">豆瓣开花</a>
            </h4>
        </div>
        <p>马克</p>

        <div class="operation_div" id="44618741">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211683786#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211683786" class="j a_confirm_link lnk-delete-comment" title="真的要删除豆瓣开花的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211683786">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211685552">
    <div class="user-face">
        <a href="http://www.douban.com/people/49572046/"><img class="pil" src="http://img3.douban.com/icon/u49572046-2.jpg" alt="bamboo常青"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:17:27
                <a href="http://www.douban.com/people/49572046/">bamboo常青</a>

            </h4>
        </div>
        <p>大三在读，不想一直在办公室待着，想做销售，又感觉自己不太会和人打交道，目前不知道以后要做什么的来学习</p>

        <div class="operation_div" id="49572046">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211685552#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211685552" class="j a_confirm_link lnk-delete-comment" title="真的要删除bamboo常青的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211685552">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211687596">
    <div class="user-face">
        <a href="http://www.douban.com/people/36787795/"><img class="pil" src="http://img3.douban.com/icon/u36787795-9.jpg" alt="真ture"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:24:22
                <a href="http://www.douban.com/people/36787795/">真ture</a> (坏的开始是成功的一半)
            </h4>
        </div>
        <p>我想从事于广告行业，现在的目标是美编，或网站设计，不知道有否相关的知识，thankyou</p>

        <div class="operation_div" id="36787795">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211687596#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211687596" class="j a_confirm_link lnk-delete-comment" title="真的要删除真ture的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211687596">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211688650">
    <div class="user-face">
        <a href="http://www.douban.com/people/weixilai/"><img class="pil" src="http://img3.douban.com/icon/u4571984-27.jpg" alt="蔚熙来"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:27:57
                <a href="http://www.douban.com/people/weixilai/">蔚熙来</a> (因循不觉韶光换)
            </h4>
        </div>
        <p>马克</p>

        <div class="operation_div" id="4571984">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211688650#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211688650" class="j a_confirm_link lnk-delete-comment" title="真的要删除蔚熙来的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211688650">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211688738">
    <div class="user-face">
        <a href="http://www.douban.com/people/1008392/"><img class="pil" src="http://img3.douban.com/icon/u1008392-3.jpg" alt="1zzzzzzzzzz"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:28:14
                <a href="http://www.douban.com/people/1008392/">1zzzzzzzzzz</a>

            </h4>
        </div>
        <p>这贴不错</p>

        <div class="operation_div" id="1008392">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211688738#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211688738" class="j a_confirm_link lnk-delete-comment" title="真的要删除1zzzzzzzzzz的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211688738">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211689047">
    <div class="user-face">
        <a href="http://www.douban.com/people/13026525/"><img class="pil" src="http://img3.douban.com/icon/u13026525-4.jpg" alt="Vian&amp;Bien"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:29:16
                <a href="http://www.douban.com/people/13026525/">Vian&amp;Bien</a> (一直在行走)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="13026525">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211689047#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211689047" class="j a_confirm_link lnk-delete-comment" title="真的要删除Vian&amp;Bien的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211689047">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211689067">
    <div class="user-face">
        <a href="http://www.douban.com/people/wudan11_08/"><img class="pil" src="http://img3.douban.com/icon/u10439046-6.jpg" alt="酒窝"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:29:18
                <a href="http://www.douban.com/people/wudan11_08/">酒窝</a> (为了遇见…需要坚持！~)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="10439046">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211689067#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211689067" class="j a_confirm_link lnk-delete-comment" title="真的要删除酒窝的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211689067">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211689637">
    <div class="user-face">
        <a href="http://www.douban.com/people/mcgege1022/"><img class="pil" src="http://img3.douban.com/icon/u44033964-2.jpg" alt="作茧自缚"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:31:14
                <a href="http://www.douban.com/people/mcgege1022/">作茧自缚</a> (作茧自缚，永远是为了化蝶的蜕变)
            </h4>

        </div>
        <p>唉~~hr之路蜗牛爬中。。。</p>

        <div class="operation_div" id="44033964">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211689637#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211689637" class="j a_confirm_link lnk-delete-comment" title="真的要删除作茧自缚的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211689637">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211690389">
    <div class="user-face">
        <a href="http://www.douban.com/people/tongdamei/"><img class="pil" src="http://img3.douban.com/icon/u48005270-36.jpg" alt="小舔妞壮壮"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:33:41
                <a href="http://www.douban.com/people/tongdamei/">小舔妞壮壮</a> (媚媚姑娘钱多多)
            </h4>
        </div>
        <p>木有了呀~~谢谢LZ</p>

        <div class="operation_div" id="48005270">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211690389#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211690389" class="j a_confirm_link lnk-delete-comment" title="真的要删除小舔妞壮壮的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211690389">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211690664">
    <div class="user-face">
        <a href="http://www.douban.com/people/ichgoing/"><img class="pil" src="http://img3.douban.com/icon/u2840009-38.jpg" alt="going"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:34:35
                <a href="http://www.douban.com/people/ichgoing/">going</a> (so,work me a little magic)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="2840009">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211690664#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211690664" class="j a_confirm_link lnk-delete-comment" title="真的要删除going的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211690664">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211690773">
    <div class="user-face">
        <a href="http://www.douban.com/people/enid921/"><img class="pil" src="http://img3.douban.com/icon/u4875860-4.jpg" alt="雁过如陌"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:34:57
                <a href="http://www.douban.com/people/enid921/">雁过如陌</a> (rp啊~~~~你在哪里~~~~)
            </h4>

        </div>
        <p>必须马克一个</p>

        <div class="operation_div" id="4875860">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211690773#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211690773" class="j a_confirm_link lnk-delete-comment" title="真的要删除雁过如陌的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211690773">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211692854">
    <div class="user-face">
        <a href="http://www.douban.com/people/lwy107/"><img class="pil" src="http://img3.douban.com/icon/u3252472-14.jpg" alt="葬临生"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:41:46
                <a href="http://www.douban.com/people/lwy107/">葬临生</a> (哈哈哈！我捍卫不了自己的爱情！)
            </h4>
        </div>
        <p>这个东西好。</p>

        <div class="operation_div" id="3252472">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211692854#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211692854" class="j a_confirm_link lnk-delete-comment" title="真的要删除葬临生的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211692854">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211693322">
    <div class="user-face">
        <a href="http://www.douban.com/people/36904120/"><img class="pil" src="http://img3.douban.com/icon/u36904120-7.jpg" alt="碧玺"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:43:20
                <a href="http://www.douban.com/people/36904120/">碧玺</a> (N多奸情，都始于微信。。。)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="36904120">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211693322#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211693322" class="j a_confirm_link lnk-delete-comment" title="真的要删除碧玺的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211693322">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211693430">
    <div class="user-face">
        <a href="http://www.douban.com/people/48316265/"><img class="pil" src="http://img3.douban.com/icon/u48316265-2.jpg" alt="小黄蜂"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:43:41
                <a href="http://www.douban.com/people/48316265/">小黄蜂</a>

            </h4>
        </div>
        <p>mmm</p>

        <div class="operation_div" id="48316265">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211693430#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211693430" class="j a_confirm_link lnk-delete-comment" title="真的要删除小黄蜂的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211693430">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211693553">
    <div class="user-face">
        <a href="http://www.douban.com/people/tippiz/"><img class="pil" src="http://img3.douban.com/icon/u35025178-67.jpg" alt="郑花钱"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:44:03
                <a href="http://www.douban.com/people/tippiz/">郑花钱</a> (强迫病患小二逼~)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="35025178">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211693553#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211693553" class="j a_confirm_link lnk-delete-comment" title="真的要删除郑花钱的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211693553">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211694146">
    <div class="user-face">
        <a href="http://www.douban.com/people/wikichan/"><img class="pil" src="http://img3.douban.com/icon/u1421816-4.jpg" alt="wiki"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:45:57
                <a href="http://www.douban.com/people/wikichan/">wiki</a>
            </h4>
        </div>
        <p>确实全面……技术贴……</p>

        <div class="operation_div" id="1421816">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211694146#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211694146" class="j a_confirm_link lnk-delete-comment" title="真的要删除wiki的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211694146">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211694904">
    <div class="user-face">
        <a href="http://www.douban.com/people/wikichan/"><img class="pil" src="http://img3.douban.com/icon/u1421816-4.jpg" alt="wiki"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:48:15
                <a href="http://www.douban.com/people/wikichan/">wiki</a>

            </h4>
        </div>
        <p>这个可以做提纲，捯饬捯饬出书哎，职场类……</p>

        <div class="operation_div" id="1421816">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211694904#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211694904" class="j a_confirm_link lnk-delete-comment" title="真的要删除wiki的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211694904">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211695038">
    <div class="user-face">
        <a href="http://www.douban.com/people/gangzitou/"><img class="pil" src="http://img3.douban.com/icon/u3511951-53.jpg" alt="火锅"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:48:41
                <a href="http://www.douban.com/people/gangzitou/">火锅</a> (我要完蛋了)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="3511951">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211695038#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211695038" class="j a_confirm_link lnk-delete-comment" title="真的要删除火锅的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211695038">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211695765">
    <div class="user-face">
        <a href="http://www.douban.com/people/hermosa1109/"><img class="pil" src="http://img3.douban.com/icon/u46679498-28.jpg" alt="小喵呜寻真爱！"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:51:01
                <a href="http://www.douban.com/people/hermosa1109/">小喵呜寻真爱！</a> (把最美好的留给最值得的。)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="46679498">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211695765#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211695765" class="j a_confirm_link lnk-delete-comment" title="真的要删除小喵呜寻真爱！的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211695765">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211697775">
    <div class="user-face">
        <a href="http://www.douban.com/people/31787100/"><img class="pil" src="http://img3.douban.com/icon/u31787100-13.jpg" alt="生如夏花"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 10:56:35
                <a href="http://www.douban.com/people/31787100/">生如夏花</a> (要婴儿肌啊混蛋！)
            </h4>

        </div>
        <p>m</p>

        <div class="operation_div" id="31787100">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211697775#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211697775" class="j a_confirm_link lnk-delete-comment" title="真的要删除生如夏花的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211697775">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211698184">
    <div class="user-face">
        <a href="http://www.douban.com/people/tyhuashengmi/"><img class="pil" src="http://img3.douban.com/icon/u37548697-14.jpg" alt="花生米"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 10:57:45
                <a href="http://www.douban.com/people/tyhuashengmi/">花生米</a> (拒绝零食。。。。。。)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="37548697">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211698184#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211698184" class="j a_confirm_link lnk-delete-comment" title="真的要删除花生米的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211698184">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211706054">
    <div class="user-face">
        <a href="http://www.douban.com/people/42905554/"><img class="pil" src="http://img3.douban.com/icon/u42905554-7.jpg" alt="天蓝"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:21:15
                <a href="http://www.douban.com/people/42905554/">天蓝</a> (梦想和现实，总有一些远！)
            </h4>
        </div>
        <p>为嘛跟适合做人事的12345一条也对不上？要不要这么悲催呀嗷嗷嗷、、、</p>

        <div class="operation_div" id="42905554">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211706054#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211706054" class="j a_confirm_link lnk-delete-comment" title="真的要删除天蓝的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211706054">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211707334">
    <div class="user-face">
        <a href="http://www.douban.com/people/1268696/"><img class="pil" src="http://img3.douban.com/icon/u1268696-1.jpg" alt="海豚游啊游"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:25:10
                <a href="http://www.douban.com/people/1268696/">海豚游啊游</a> (不以物喜，不以己悲)
            </h4>

        </div>
        <p>m</p>

        <div class="operation_div" id="1268696">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211707334#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211707334" class="j a_confirm_link lnk-delete-comment" title="真的要删除海豚游啊游的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211707334">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211708674">
    <div class="user-face">
        <a href="http://www.douban.com/people/4679525/"><img class="pil" src="http://img3.douban.com/icon/u4679525-9.jpg" alt="慌谎"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 11:28:54
                <a href="http://www.douban.com/people/4679525/">慌谎</a> (我还真不争气……)
            </h4>
        </div>
        <p>M
<br/></p>

        <div class="operation_div" id="4679525">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211708674#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211708674" class="j a_confirm_link lnk-delete-comment" title="真的要删除慌谎的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211708674">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211710539">
    <div class="user-face">
        <a href="http://www.douban.com/people/47836772/"><img class="pil" src="http://img3.douban.com/icon/u47836772-1.jpg" alt="starting"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:34:27
                <a href="http://www.douban.com/people/47836772/">starting</a>
            </h4>
        </div>
        <p>mark</p>

        <div class="operation_div" id="47836772">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211710539#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211710539" class="j a_confirm_link lnk-delete-comment" title="真的要删除starting的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211710539">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211711764">
    <div class="user-face">
        <a href="http://www.douban.com/people/aurorayeung/"><img class="pil" src="http://img3.douban.com/icon/u2469906-10.jpg" alt="桃絲。"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:38:07
                <a href="http://www.douban.com/people/aurorayeung/">桃絲。</a> (花的姿态。)
            </h4>

        </div>
        <p>呃 正在HR助理位置上慢慢熬...</p>

        <div class="operation_div" id="2469906">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211711764#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211711764" class="j a_confirm_link lnk-delete-comment" title="真的要删除桃絲。的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211711764">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211712065">
    <div class="user-face">
        <a href="http://www.douban.com/people/caroline_wong/"><img class="pil" src="http://img3.douban.com/icon/u11530978-2.jpg" alt="Caroline"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 11:39:08
                <a href="http://www.douban.com/people/caroline_wong/">Caroline</a> (成也萧何，败也萧何。)
            </h4>
        </div>
        <p>此前读过，还是再马克下，经典！</p>

        <div class="operation_div" id="11530978">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211712065#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211712065" class="j a_confirm_link lnk-delete-comment" title="真的要删除Caroline的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211712065">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211712602">
    <div class="user-face">
        <a href="http://www.douban.com/people/3731473/"><img class="pil" src="http://img3.douban.com/icon/u3731473-47.jpg" alt="wen"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:40:52
                <a href="http://www.douban.com/people/3731473/">wen</a>
            </h4>
        </div>
        <p>强力马~好文章</p>

        <div class="operation_div" id="3731473">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211712602#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211712602" class="j a_confirm_link lnk-delete-comment" title="真的要删除wen的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211712602">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211713244">
    <div class="user-face">
        <a href="http://www.douban.com/people/48255113/"><img class="pil" src="http://img3.douban.com/icon/u48255113-2.jpg" alt="废材八嘎"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:42:47
                <a href="http://www.douban.com/people/48255113/">废材八嘎</a>

            </h4>
        </div>
        <p>马克，好多专有名词
<br/>
<br/>插一个
<br/>【3•14特别企划】给属于我们的纪念日，晒出你的幸福
<br/><a href="http://www.mimimama.com/forum/thread-102334-1-1.html" target="_blank" rel="nofollow">http://www.mimimama.<wbr/>com/forum/thread-102<wbr/>334-1-1.html</a> 
<br/> 
<br/></p>

        <div class="operation_div" id="48255113">

            <a href="http://www.douban.com/group/topic/18099270/?cid=211713244#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211713244" class="j a_confirm_link lnk-delete-comment" title="真的要删除废材八嘎的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211713244">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211714910">

    <div class="user-face">
        <a href="http://www.douban.com/people/dollface/"><img class="pil" src="http://img3.douban.com/icon/u2274992-7.jpg" alt="小喷菇"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:48:06
                <a href="http://www.douban.com/people/dollface/">小喷菇</a> (努力坚持着我想要的)
            </h4>

        </div>
        <p>M</p>

        <div class="operation_div" id="2274992">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211714910#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211714910" class="j a_confirm_link lnk-delete-comment" title="真的要删除小喷菇的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211714910">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211715383">
    <div class="user-face">
        <a href="http://www.douban.com/people/msstupid/"><img class="pil" src="http://img3.douban.com/icon/u12817158-20.jpg" alt="花天酒地小闲闲"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 11:49:31
                <a href="http://www.douban.com/people/msstupid/">花天酒地小闲闲</a> (2012的新年愿望是成为白富美！)
            </h4>
        </div>
        <p>这贴特别好！！
<br/>
<br/>希望lz继续保持这种知识分享的风格！！
<br/>
<br/>希望将来有资本加入这一队伍！！</p>

        <div class="operation_div" id="12817158">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211715383#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211715383" class="j a_confirm_link lnk-delete-comment" title="真的要删除花天酒地小闲闲的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211715383">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211717216">
    <div class="user-face">
        <a href="http://www.douban.com/people/solitario/"><img class="pil" src="http://img3.douban.com/icon/u36722229-11.jpg" alt="solitario"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:55:28
                <a href="http://www.douban.com/people/solitario/">solitario</a> (Jesse真是个萌孩子)
            </h4>

        </div>
        <p>好贴啊</p>

        <div class="operation_div" id="36722229">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211717216#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211717216" class="j a_confirm_link lnk-delete-comment" title="真的要删除solitario的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211717216">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211717360">
    <div class="user-face">
        <a href="http://www.douban.com/people/2081983/"><img class="pil" src="http://img3.douban.com/icon/u2081983-1.jpg" alt="呵呵"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 11:55:58
                <a href="http://www.douban.com/people/2081983/">呵呵</a>
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="2081983">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211717360#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211717360" class="j a_confirm_link lnk-delete-comment" title="真的要删除呵呵的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211717360">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211718437">
    <div class="user-face">
        <a href="http://www.douban.com/people/40823778/"><img class="pil" src="http://img3.douban.com/icon/u40823778-2.jpg" alt="飞向幸福"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 11:59:29
                <a href="http://www.douban.com/people/40823778/">飞向幸福</a> (前路漫漫，我依旧坚强)
            </h4>
        </div>
        <p>好，有帮助</p>

        <div class="operation_div" id="40823778">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211718437#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211718437" class="j a_confirm_link lnk-delete-comment" title="真的要删除飞向幸福的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211718437">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211732210">
    <div class="user-face">
        <a href="http://www.douban.com/people/paradoxox/"><img class="pil" src="http://img3.douban.com/icon/u4440088-107.jpg" alt="壳"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 12:47:18
                <a href="http://www.douban.com/people/paradoxox/">壳</a> (我这个人是很三俗的)
            </h4>

        </div>
        <p>M</p>

        <div class="operation_div" id="4440088">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211732210#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211732210" class="j a_confirm_link lnk-delete-comment" title="真的要删除壳的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211732210">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211732229">
    <div class="user-face">
        <a href="http://www.douban.com/people/2330122/"><img class="pil" src="http://img3.douban.com/icon/u2330122-9.jpg" alt="辛欣辛"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 12:47:21
                <a href="http://www.douban.com/people/2330122/">辛欣辛</a> (我不想当笨蛋 我绝对不逞强)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="2330122">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211732229#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211732229" class="j a_confirm_link lnk-delete-comment" title="真的要删除辛欣辛的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211732229">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211732636">
    <div class="user-face">
        <a href="http://www.douban.com/people/bianshajia/"><img class="pil" src="http://img3.douban.com/icon/u2072424-30.jpg" alt="沙加"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 12:48:30
                <a href="http://www.douban.com/people/bianshajia/">沙加</a> (夜已经荒凉)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="2072424">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211732636#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211732636" class="j a_confirm_link lnk-delete-comment" title="真的要删除沙加的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211732636">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211732808">
    <div class="user-face">
        <a href="http://www.douban.com/people/forever2012/"><img class="pil" src="http://img3.douban.com/icon/u38673040-7.jpg" alt="Alisa"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 12:49:02
                <a href="http://www.douban.com/people/forever2012/">Alisa</a> (注会考试开始倒计时了，紧张。)
            </h4>

        </div>
        <p>都很对啊。</p>

        <div class="operation_div" id="38673040">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211732808#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211732808" class="j a_confirm_link lnk-delete-comment" title="真的要删除Alisa的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211732808">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211732997">
    <div class="user-face">
        <a href="http://www.douban.com/people/48190577/"><img class="pil" src="http://img3.douban.com/icon/u48190577-5.jpg" alt="樱花树下"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 12:49:36
                <a href="http://www.douban.com/people/48190577/">樱花树下</a> (再等下一站，只是不再是三年)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="48190577">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211732997#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211732997" class="j a_confirm_link lnk-delete-comment" title="真的要删除樱花树下的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211732997">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211735549">
    <div class="user-face">
        <a href="http://www.douban.com/people/46311214/"><img class="pil" src="http://img3.douban.com/icon/u46311214-2.jpg" alt="渐行渐远"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 12:56:39
                <a href="http://www.douban.com/people/46311214/">渐行渐远</a> (从什么时候开始我不开心了……)
            </h4>
        </div>
        <p>M </p>

        <div class="operation_div" id="46311214">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211735549#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211735549" class="j a_confirm_link lnk-delete-comment" title="真的要删除渐行渐远的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211735549">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211736799">
    <div class="user-face">
        <a href="http://www.douban.com/people/43314393/"><img class="pil" src="http://img3.douban.com/icon/u43314393-2.jpg" alt="小花点"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 13:00:17
                <a href="http://www.douban.com/people/43314393/">小花点</a>

            </h4>
        </div>
        <p>真好啊，M一下。</p>

        <div class="operation_div" id="43314393">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211736799#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211736799" class="j a_confirm_link lnk-delete-comment" title="真的要删除小花点的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211736799">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211751828">
    <div class="user-face">
        <a href="http://www.douban.com/people/2779227/"><img class="pil" src="http://img3.douban.com/icon/u2779227-4.jpg" alt="ulat"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 13:43:39
                <a href="http://www.douban.com/people/2779227/">ulat</a>
            </h4>
        </div>
        <p>感谢分享</p>

        <div class="operation_div" id="2779227">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211751828#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211751828" class="j a_confirm_link lnk-delete-comment" title="真的要删除ulat的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211751828">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211752552">
    <div class="user-face">
        <a href="http://www.douban.com/people/26251335/"><img class="pil" src="http://img3.douban.com/icon/u26251335-4.jpg" alt="cc"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 13:45:38
                <a href="http://www.douban.com/people/26251335/">cc</a>
            </h4>
        </div>
        <p>,,,mmm</p>

        <div class="operation_div" id="26251335">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211752552#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211752552" class="j a_confirm_link lnk-delete-comment" title="真的要删除cc的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211752552">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211756221">
    <div class="user-face">
        <a href="http://www.douban.com/people/36760083/"><img class="pil" src="http://img3.douban.com/icon/u36760083-6.jpg" alt="123木头人"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 13:56:54
                <a href="http://www.douban.com/people/36760083/">123木头人</a> (我要独立)
            </h4>

        </div>
        <p>m'</p>

        <div class="operation_div" id="36760083">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211756221#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211756221" class="j a_confirm_link lnk-delete-comment" title="真的要删除123木头人的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211756221">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211758104">
    <div class="user-face">
        <a href="http://www.douban.com/people/41780231/"><img class="pil" src="http://img3.douban.com/icon/u41780231-3.jpg" alt="小千"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 14:03:11
                <a href="http://www.douban.com/people/41780231/">小千</a>
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="41780231">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211758104#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211758104" class="j a_confirm_link lnk-delete-comment" title="真的要删除小千的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211758104">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211759577">
    <div class="user-face">
        <a href="http://www.douban.com/people/31107952/"><img class="pil" src="http://img3.douban.com/icon/u31107952-3.jpg" alt="9之前"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 14:08:05
                <a href="http://www.douban.com/people/31107952/">9之前</a> (我们彼此陪伴 也各自孤单)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="31107952">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211759577#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211759577" class="j a_confirm_link lnk-delete-comment" title="真的要删除9之前的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211759577">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211759654">
    <div class="user-face">
        <a href="http://www.douban.com/people/38140140/"><img class="pil" src="http://img3.douban.com/icon/u38140140-4.jpg" alt="果茶"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 14:08:20
                <a href="http://www.douban.com/people/38140140/">果茶</a>

            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="38140140">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211759654#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211759654" class="j a_confirm_link lnk-delete-comment" title="真的要删除果茶的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211759654">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211760815">
    <div class="user-face">
        <a href="http://www.douban.com/people/47506687/"><img class="pil" src="http://img3.douban.com/icon/u47506687-18.jpg" alt="就不喜欢吃苹果"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 14:12:01
                <a href="http://www.douban.com/people/47506687/">就不喜欢吃苹果</a> (I want nothing)
            </h4>
        </div>
        <p>嗯，很有用</p>

        <div class="operation_div" id="47506687">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211760815#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211760815" class="j a_confirm_link lnk-delete-comment" title="真的要删除就不喜欢吃苹果的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211760815">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211762159">
    <div class="user-face">
        <a href="http://www.douban.com/people/47168037/"><img class="pil" src="http://img3.douban.com/icon/u47168037-6.jpg" alt="筱筱"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 14:16:30
                <a href="http://www.douban.com/people/47168037/">筱筱</a> (原来我一点也不懂自己.)
            </h4>
        </div>
        <p>M</p>

        <div class="operation_div" id="47168037">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211762159#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211762159" class="j a_confirm_link lnk-delete-comment" title="真的要删除筱筱的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211762159">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211771004">
    <div class="user-face">
        <a href="http://www.douban.com/people/1325564/"><img class="pil" src="http://img3.douban.com/icon/u1325564-5.jpg" alt="白水加冰"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 14:45:19
                <a href="http://www.douban.com/people/1325564/">白水加冰</a>

            </h4>
        </div>
        <p>有意思</p>

        <div class="operation_div" id="1325564">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211771004#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211771004" class="j a_confirm_link lnk-delete-comment" title="真的要删除白水加冰的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211771004">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211823065">
    <div class="user-face">
        <a href="http://www.douban.com/people/1927124/"><img class="pil" src="http://img3.douban.com/icon/u1927124-21.jpg" alt="朱大麦"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 17:18:34
                <a href="http://www.douban.com/people/1927124/">朱大麦</a>
            </h4>
        </div>
        <p>管理咨询顾问平均薪资最高。。。</p>

        <div class="operation_div" id="1927124">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211823065#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211823065" class="j a_confirm_link lnk-delete-comment" title="真的要删除朱大麦的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211823065">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211824352">
    <div class="user-face">
        <a href="http://www.douban.com/people/cherieliu/"><img class="pil" src="http://img3.douban.com/icon/u3821364-47.jpg" alt="fallen"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 17:22:15
                <a href="http://www.douban.com/people/cherieliu/">fallen</a> (On the way)
            </h4>
        </div>
        <p>over了？

<br/>LZ说说外贸吧，还有总经理助理之类的</p>

        <div class="operation_div" id="3821364">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211824352#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211824352" class="j a_confirm_link lnk-delete-comment" title="真的要删除fallen的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211824352">举报广告</a>
        </div>
    </div>

</li>

        

<li class="clearfix" id="211827578">
    <div class="user-face">
        <a href="http://www.douban.com/people/advantage_lucy/"><img class="pil" src="http://img3.douban.com/icon/u36393289-2.jpg" alt="Lucia"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 17:31:35
                <a href="http://www.douban.com/people/advantage_lucy/">Lucia</a> (我不努力，谁给我未来！)
            </h4>

        </div>
        <p>我也想听外贸！</p>

        <div class="operation_div" id="36393289">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211827578#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211827578" class="j a_confirm_link lnk-delete-comment" title="真的要删除Lucia的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211827578">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211827721">
    <div class="user-face">
        <a href="http://www.douban.com/people/2398781/"><img class="pil" src="http://img3.douban.com/icon/u2398781-7.jpg" alt="Folliculina"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 17:32:02
                <a href="http://www.douban.com/people/2398781/">Folliculina</a> (好爱我的小喵喵！)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="2398781">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211827721#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211827721" class="j a_confirm_link lnk-delete-comment" title="真的要删除Folliculina的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211827721">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211827936">
    <div class="user-face">
        <a href="http://www.douban.com/people/47213326/"><img class="pil" src="http://img3.douban.com/icon/u47213326-10.jpg" alt="V"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 17:32:44
                <a href="http://www.douban.com/people/47213326/">V</a> (我应该看劳动合同法)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="47213326">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211827936#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211827936" class="j a_confirm_link lnk-delete-comment" title="真的要删除V的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211827936">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211829613">
    <div class="user-face">
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 17:38:28
                <a href="http://www.douban.com/people/48699302/">lyna003</a>
            </h4>

        </div>
        <p>M</p>

        <div class="operation_div" id="48699302">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211829613#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211829613" class="j a_confirm_link lnk-delete-comment" title="真的要删除lyna003的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211829613">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211829713">
    <div class="user-face">
        <a href="http://www.douban.com/people/lazylover/"><img class="pil" src="http://img3.douban.com/icon/u1466426-12.jpg" alt="最初的茉莉"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 17:38:51
                <a href="http://www.douban.com/people/lazylover/">最初的茉莉</a>
            </h4>
        </div>
        <p>之前看过</p>

        <div class="operation_div" id="1466426">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211829713#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211829713" class="j a_confirm_link lnk-delete-comment" title="真的要删除最初的茉莉的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211829713">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211832870">
    <div class="user-face">
        <a href="http://www.douban.com/people/2103623/"><img class="pil" src="http://img3.douban.com/icon/u2103623-32.jpg" alt="Clover"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 17:50:20
                <a href="http://www.douban.com/people/2103623/">Clover</a> (废柴啊)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="2103623">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211832870#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211832870" class="j a_confirm_link lnk-delete-comment" title="真的要删除Clover的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211832870">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211836125">
    <div class="user-face">
        <a href="http://www.douban.com/people/rhymliu/"><img class="pil" src="http://img3.douban.com/icon/u32255676-66.jpg" alt="简淡"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 18:02:16
                <a href="http://www.douban.com/people/rhymliu/">简淡</a> (万言万当，不如一默。)
            </h4>

        </div>
        <p>说说外贸~~~</p>

        <div class="operation_div" id="32255676">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211836125#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211836125" class="j a_confirm_link lnk-delete-comment" title="真的要删除简淡的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211836125">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211840784">
    <div class="user-face">
        <a href="http://www.douban.com/people/47214550/"><img class="pil" src="http://img3.douban.com/icon/u47214550-1.jpg" alt="Nicolas"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 18:19:57
                <a href="http://www.douban.com/people/47214550/">Nicolas</a> ()
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="47214550">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211840784#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211840784" class="j a_confirm_link lnk-delete-comment" title="真的要删除Nicolas的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211840784">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211875624">
    <div class="user-face">
        <a href="http://www.douban.com/people/38916827/"><img class="pil" src="http://img3.douban.com/icon/u38916827-37.jpg" alt="年轮的寂寞"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 20:15:59
                <a href="http://www.douban.com/people/38916827/">年轮的寂寞</a> (一步步)
            </h4>
        </div>
        <p>m</p>

        <div class="operation_div" id="38916827">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211875624#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211875624" class="j a_confirm_link lnk-delete-comment" title="真的要删除年轮的寂寞的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211875624">举报广告</a>
        </div>
    </div>

</li>

        

<li class="clearfix" id="211879631">
    <div class="user-face">
        <a href="http://www.douban.com/people/woaixixiaoxiao/"><img class="pil" src="http://img3.douban.com/icon/u41651344-5.jpg" alt="-晓晓的肥鹅-"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 20:27:15
                <a href="http://www.douban.com/people/woaixixiaoxiao/">-晓晓的肥鹅-</a> (UUUUUU)
            </h4>

        </div>
        <p>马~~想要看行政部的~楼主加油~~~</p>

        <div class="operation_div" id="41651344">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211879631#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211879631" class="j a_confirm_link lnk-delete-comment" title="真的要删除-晓晓的肥鹅-的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211879631">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211896754">
    <div class="user-face">
        <a href="http://www.douban.com/people/2155525/"><img class="pil" src="http://img3.douban.com/icon/u2155525-4.jpg" alt="左转向右"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 21:11:55
                <a href="http://www.douban.com/people/2155525/">左转向右</a> (流落到城外)
            </h4>
        </div>
        <p>楼主的阐述比较贴切～学习了</p>

        <div class="operation_div" id="2155525">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211896754#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211896754" class="j a_confirm_link lnk-delete-comment" title="真的要删除左转向右的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211896754">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211919339">
    <div class="user-face">
        <a href="http://www.douban.com/people/PaPajudy/"><img class="pil" src="http://img3.douban.com/icon/u1723570-1.jpg" alt="papajudy"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 22:03:49
                <a href="http://www.douban.com/people/PaPajudy/">papajudy</a> (开不了口.....)
            </h4>
        </div>
        <p>果断马克 求更新</p>

        <div class="operation_div" id="1723570">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211919339#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211919339" class="j a_confirm_link lnk-delete-comment" title="真的要删除papajudy的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211919339">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211922686">
    <div class="user-face">
        <a href="http://www.douban.com/people/abcba/"><img class="pil" src="http://img3.douban.com/icon/u39229318-30.jpg" alt="lily"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 22:11:12
                <a href="http://www.douban.com/people/abcba/">lily</a> (豆瓣改版很不错啊....)
            </h4>

        </div>
        <p>谢谢lz   m</p>

        <div class="operation_div" id="39229318">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211922686#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211922686" class="j a_confirm_link lnk-delete-comment" title="真的要删除lily的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211922686">举报广告</a>

        </div>
    </div>
</li>

        

<li class="clearfix" id="211922764">
    <div class="user-face">
        <a href="http://www.douban.com/people/temason/"><img class="pil" src="http://img3.douban.com/icon/u47497164-44.jpg" alt="云吞大战油条"/></a>
    </div>
    <div class="reply-doc">
        <div class="bg-img-green">

          <h4> 2011-03-08 22:11:23
                <a href="http://www.douban.com/people/temason/">云吞大战油条</a> (Chrome app)
            </h4>
        </div>
        <p>啊</p>

        <div class="operation_div" id="47497164">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211922764#last" class="lnk-reply">回应</a>

            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211922764" class="j a_confirm_link lnk-delete-comment" title="真的要删除云吞大战油条的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211922764">举报广告</a>
        </div>
    </div>
</li>

        

<li class="clearfix" id="211922819">
    <div class="user-face">
        <a href="http://www.douban.com/people/temason/"><img class="pil" src="http://img3.douban.com/icon/u47497164-44.jpg" alt="云吞大战油条"/></a>

    </div>
    <div class="reply-doc">
        <div class="bg-img-green">
          <h4> 2011-03-08 22:11:29
                <a href="http://www.douban.com/people/temason/">云吞大战油条</a> (Chrome app)
            </h4>
        </div>
        <p>翻页</p>

        <div class="operation_div" id="47497164">
            <a href="http://www.douban.com/group/topic/18099270/?cid=211922819#last" class="lnk-reply">回应</a>
            <a rel="nofollow" href="http://www.douban.com/group/topic/18099270/remove_comment?cid=211922819" class="j a_confirm_link lnk-delete-comment" title="真的要删除云吞大战油条的发言?">删除</a>
            <a rel="nofollow" class="lnk-report"  href="#" data-type="3004" data-id="211922819">举报广告</a>
        </div>
    </div>
</li>

    </ul>


    
    
    
    
        <div class="paginator">
        <span class="prev">
            &lt;前页
        </span>
        
        

                <span class="thispage">1</span>
                
            <a href="http://www.douban.com/group/topic/18099270/?start=100" >2</a>

        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=200" >3</a>
        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=300" >4</a>
        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=400" >5</a>
        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=500" >6</a>
        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=600" >7</a>
        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=700" >8</a>

        
                
            <a href="http://www.douban.com/group/topic/18099270/?start=800" >9</a>
        
            <span class="break">...</span>
                
            <a href="http://www.douban.com/group/topic/18099270/?start=900" >10</a>
        
            <a href="http://www.douban.com/group/topic/18099270/?start=1000" >11</a>
        
        <span class="next">
            <link rel="next" href="http://www.douban.com/group/topic/18099270/?start=100"/>
            <a href="http://www.douban.com/group/topic/18099270/?start=100" >后页&gt;</a>

        </span>

        </div>




    






</div>
        <div class="aside">
            

    <p class="pl2">&gt; <a href="http://www.douban.com/group/youzhaopin/">回圈内招聘（joboto.com）小组</a></p><br/>

<!-- douban ad begin -->
<div id="google_ads_slot_group_topic_new_top_right" class="mb5"></div>
<div id="google_ads_slot_group_topic_new_top_right2" class="mb20"></div>
<!-- douban ad end -->


        <h2 class="usf">最新话题:</h2>
        <div class="indent">
                <p class="pl ul"><a href="http://www.douban.com/group/topic/26689387/" title="【招聘】美国服饰American Apparel 三里屯店 ！！">【招聘】美国服饰American Apparel 三里屯店 ！！</a> &nbsp;
                <span class ="pl">(穿红戴绿苴苴刘) </p>

                <p class="pl ul"><a href="http://www.douban.com/group/topic/27041035/" title="【求职】【北京】11年北理工毕业，本科，能活下去即可">【求职】【北京】11年北理工毕业，本科，能活下去即可</a> &nbsp;
                <span class ="pl">(Joe) </p>
                <p class="pl ul"><a href="http://www.douban.com/group/topic/26853568/" title="坐标北京，有偿诚聘脚模，拍足部写真">坐标北京，有偿诚聘脚模，拍足部写真</a> &nbsp;
                <span class ="pl">(Steven ) </p>
                <p class="pl ul"><a href="http://www.douban.com/group/topic/26828304/" title="【招@上海】第一弹_招各类设计师_配iMac">【招@上海】第一弹_招各类设计师_配iMac</a> &nbsp;

                <span class ="pl">(左神神) </p>
                <p class="pl ul"><a href="http://www.douban.com/group/topic/26868327/" title="我觉得有必要科普下求职者的权益~">我觉得有必要科普下求职者的权益~</a> &nbsp;
                <span class ="pl">(囧囧无神™) </p>
                <p class="pl ul"><a href="http://www.douban.com/group/topic/23227569/" title="AUY~面试达人！">AUY~面试达人！</a> &nbsp;
                <span class ="pl">(sunflower) </p>

                <p class="pl ul"><a href="http://www.douban.com/group/topic/19893022/" title="{这是日记帖}我是一名新晋医药代表，并且以后还会是医药代表">{这是日记帖}我是一名新晋医药代表，并且以后还会是医...</a> &nbsp;
                <span class ="pl">(米斯兔) </p>
                <p class="pl ul"><a href="http://www.douban.com/group/topic/27071894/" title="我给不了长期饭票，只能给个米果护照，相册为证">我给不了长期饭票，只能给个米果护照，相册为证</a> &nbsp;
                <span class ="pl">(vincenzo) </p>
        </div>

        </div>
        <div class="extra">
            
    
    <span class="gact">&gt; <a href="http://www.douban.com/misc/report?type=T&uid=18099270">举报不良信息</a></span>


        </div>
    </div>
    </div>

        
    <div id="footer">
        
<span id="icp" class="fleft gray-link">
    &copy; 2005－2012 douban.com, all rights reserved
</span>

<span class="fright">
    <a href="http://www.douban.com/about">关于豆瓣</a>
    · <a href="http://www.douban.com/jobs">在豆瓣工作</a>

    · <a href="http://www.douban.com/about?topic=contactus">联系我们</a>
    · <a href="http://www.douban.com/about?policy=disclaimer">免责声明</a>
    
    · <a href="http://www.douban.com/help/">帮助中心</a>
    · <a href="http://www.douban.com/service/">API</a>
    · <a href="http://www.douban.com/mobile/">手机豆瓣</a>

    · <a href="http://www.douban.com/partner/">品牌俱乐部</a>
</span>


    </div>

    </div>
    
    <!-- douban ad begin -->
    

<script type="text/javascript"
        src="http://partner.googleadservices.com/gampad/google_service.js">
</script>

<script type="text/javascript">
    GS_googleAddAdSenseService("ca-pub-6419643701131111");
    GS_googleEnableAllServices();
</script>
<script type="text/javascript">
    GA_googleAddSlot("ca-pub-6419643701131111", "group_topic_new_top_right");
    GA_googleAddSlot("ca-pub-6419643701131111", "group_topic_new_top_right2");
</script>
<script type="text/javascript">
    GA_googleFetchAds();
</script>

    
    




            <script type="text/javascript">
                    GA_googleAddAttr("client", "duijiaodj");
            </script>

        <div id="group_topic_new_top_right" style="display: none;">
            <script type="text/javascript">
                GA_googleFillSlot("group_topic_new_top_right");
            </script>
        </div>

            <script type="text/javascript">
                    GA_googleAddAttr("client", "duijiaodj");
            </script>

        <div id="group_topic_new_top_right2" style="display: none;">
            <script type="text/javascript">
                GA_googleFillSlot("group_topic_new_top_right2");
            </script>
        </div>

    <script type="text/javascript">
        var get = function(id) {
            return document.getElementById(id);
        }

        var move = function(slot) {
            var adslot = get('google_ads_slot_' + slot), ifrm, ad_frame = get('google_ads_iframe_' + slot);
            if (!adslot) {
                return;
            }
            if (ad_frame) {
                ifrm = document.createElement('iframe');
                ifrm.setAttribute('id', 'google_ads_slot_iframe_' + slot);
                ifrm.setAttribute('frameBorder', 0);
                ifrm.setAttribute('scrolling', 'no');
                ifrm.setAttribute('width', ad_frame.getAttribute('width'));
                ifrm.setAttribute('height', ad_frame.getAttribute('height'));
                adslot.appendChild(ifrm);
                ifrm.contentWindow.document.open();
                ifrm.contentWindow.document.write(ad_frame.contentWindow.document.documentElement.innerHTML);
                ifrm.contentWindow.document.close();
                if (slot !== "group_topic_new_top_right"){
                    $('#google_ads_slot_iframe_' + slot).addClass('mb20');
                }
            } else {
                var ad_div = get('google_ads_div_' + slot) || get('google_ads_div_' + slot + '_ad_container');
                if (ad_div) {
                    adslot.appendChild(ad_div);
                    if (slot !== "group_topic_new_top_right" && slot !== "people_photo_right"){
                        ad_div.className += ' mb20';
                    }
                }
            }
        };
        (typeof Do === 'function'? Do : $).call(null, function() {
            setTimeout("move('group_topic_new_top_right')", 0);
            setTimeout("move('group_topic_new_top_right2')", 100);
        });
    </script>
    

    <!-- douban ad end -->


    
    
<script type="text/javascript">
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-7019765-1']);
_gaq.push(['_addOrganic', 'baidu', 'word']);
_gaq.push(['_addOrganic', 'soso', 'w']);
_gaq.push(['_addOrganic', '3721', 'name']);
_gaq.push(['_addOrganic', 'yodao', 'q']);
_gaq.push(['_addOrganic', 'vnet', 'kw']);
_gaq.push(['_addOrganic', 'sogou', 'query']);
_gaq.push(['_addIgnoredOrganic', '豆瓣']);
_gaq.push(['_addIgnoredOrganic', 'douban']);
_gaq.push(['_addIgnoredOrganic', '豆瓣网']);
_gaq.push(['_addIgnoredOrganic', 'www.douban.com']);
_gaq.push(['_setDomainName', '.douban.com']);

_gaq.push(['_trackPageview']);
_gaq.push(['_trackPageLoadTime']);
    _gaq.push(['_setVar', '126']);


(function() {
    var ga = document.createElement('script');
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    ga.setAttribute('async', 'true');
    document.documentElement.firstChild.appendChild(ga);
})();
</script>







    <!-- hogg6-->

<script>var _check_hijack = function () {
            var _sig = "i9gsK/lU", _login = true, bid = get_cookie('bid');
            if (location.protocol != "file:" && (typeof(bid) != "string" && _login || typeof(bid) == "string" && bid.substring(0,8) != _sig)) {
                location.href+=(/\?/.test(location.href)?"&":"?") + "_r=" + Math.random().toString(16).substring(2);
            }};
            if (typeof(Do) != 'undefined') Do(_check_hijack);
            else if (typeof(get_cookie) != 'undefined') _check_hijack();
            </script>



</body>
</html>
"""

    
    print parse_topic_htm.htm(html)
