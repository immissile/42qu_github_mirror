b1024();
function render_note(data){
    _render_note("#feed_index","#item_list", data)[0].style.borderTop=0;
    $(".com_main,.com_side").show();
}


;$(function(){

    var data = $.parseJSON($("#site_data").html()),
        rec_wrapper=$("#rec_wrapper"),
        site_rec=$("#site_rec");


    if(data&&data.length){
        rec_wrapper.append(site_rec.tmpl(data));
    }

    function fav(id){
        $("#rec_id"+id).addClass("fav_loading");
        callback=function(){
            $("#rec_id"+id).removeClass("fav_loading");
            $("#rec_id"+id).addClass("site_faved");
            $("#rec_id"+id).attr("href","javascript:unfav("+id+")");
        };
        _(id, 2,callback);
    }

    function unfav (id){
        callback=function(){};
        _(id, 0,callback);
        $("#rec_id"+id).removeClass("site_faved");
        $("#rec_id"+id).attr("href","javascript:fav("+id+")");
    }
    $(".buzz_h1").hover(function(){$(this).find("a").show()},function(){$(this).find("a").hide()});
    $(".buzz_w").hover(function(){$(this).find('.bzr').show()},function(){$(this).find(".bzr").hide()});

});

/*
    function readx(){
        var fav=txt_body.find(".fav,.faved")[0];
        $('#fcmx_'+fav.rel).click();
        txt_loading.remove()
        feed_index.show() 
        winj.scrollTop(oldtop)
        oldtop=-1
        if(fav){
            $("#fav"+fav.rel)[0].className = fav.className;
        }
        txt_body.replaceWith(feed_loading)
    }
    function change_txt(){
        self = $(".fav_txt")
        if(self.hasClass('isfaved')){
            self.html("关注");
            self.removeClass('isfaved');
        }else{
            self.html("遗忘");
            self.addClass('isfaved');
        }
    }

    $('.readx').live('click',readx)
    $(".fav_txt").click(
            function(e){
                $(".fav_tag").click();
            });

    $(".fav_tag").click(function(e){change_txt()})
    $(document).bind("keyup",function(e){
        if(e.keyCode == 27 && oldtop>=0){
            readx()
        }
    })

    $('.reado').live('click',function(){
        feed_index.hide();
        var self=$(this), 
            title=self.find('.title').addClass('c9'), 
            id=this.id.slice(5), 
            user=$(this.parentNode).find('.TPH'),
            user_link=user[0].href
            ;
        txt_title.html(title.html());
        feeds.append(txt_loading);
        oldtop=winj.scrollTop();
        winj.scrollTop(scrollTop);
        $.get(
        "/j/po/json/"+id,
        function(r){

            r.id=id
            r.user_name=user.html()
            r.link = user_link+id
            r.time = $.timeago(r.create_time)
            r.fav = $('#fav'+id)[0].className

            txt_body = render_txt.tmpl(r)
            feed_loading.replaceWith(txt_body)
            winj.scrollTop(scrollTop)
        })

        return false; 
    })

    if(!IE6){
        if(main_nav_txt[0]){
            var top = main_nav_txt.offset().top, win=$(window).scroll(function() {
                if(win.scrollTop() >= scrollTop+14){
                    main_nav_txt.css({'position':'fixed',"marginTop":-scrollTop-14})
                }else{
                    main_nav_txt.css({'position':'absolute',"marginTop":"0"})
                }
            })
        }
    }
})();
*/

function click_sets(){
    var html = $('html,body'),
    e = $('.xatagset').blur(),
    pb = $('.pop_block')
    function _() {
        pb.hide()
        html.unbind('click', _)
    }

    if (pb.is(":hidden")) {
        pb.show()
        html.click(_)
        clicked = true;
    } else {
        _()
    }
}


function pop_manage(){
    if(!islogin())return;
    var fancybox = $.fancybox
    fancybox.showActivity()

    state2cn = {
0 : '描述你在该领域的经验 , 审核后将开通管理权限',
5 : '申请被拒 , 请完善自己在该领域的经验后 , 再次申请',
10: '申请已提交 , 等待审批中 ; 你可以修订自己的介绍',
    }
    $.getJSON('/j/tag/manage/apply', function(o){
        fancybox.hideActivity()
        fancybox({
            content:
'<div class="pop_wrap"><div class="pop_title">'+
state2cn[o[0]]+
'</div><textarea id="pop_txt" class="pop_txt"></textarea><a class="pop_submit_a" href="javascript:void(0)">提交</a></div>',
            onComplete:function(){
                var pop_txt = $('#pop_txt')
                pop_txt.focus().val(o[1])
                $('.pop_submit_a').click(function(){
                    var txt = pop_txt.val();
                    if(!txt.length){
                        alert("写几句吧 , 亲 ...")
                        pop_txt.focus()
                    }else{ 
                        fancybox.showActivity()
                        $.postJSON(
                            '/j/tag/manage/apply',
                            { txt:txt },
                            function(){
                                fancybox.hideActivity()
                                fancybox({content:'<p>申请已提交</p><p>请耐心等待</p>'})
                            }
                        )
                    }
                })             
            },
            'overlayShow':false
        })
    })
}
function sns_share(){
    var fancybox = $.fancybox
    fancybox({
        content:'<div class="pop_share"><p class="share_title">分享到 · · ·</p></div>',
        onComplete:function(){
            var url = location.href,
            title = document.title,
            urls = [["http://www.douban.com/recommend/?url=","豆瓣","2"],["http://share.renren.com/share/buttonshare.do?link=","人人","9"],["http://v.t.sina.com.cn/share/share.php?url=","新浪","3"],["http://share.v.t.qq.com/index.php?c=share&a=index&url=","腾讯",8]] 
            for(var i=0;i<urls.length;++i){
                $('.pop_share').append('<a class="share_a" href='+urls[i][0]+url+'&title='+title+' target="_blank"><img src="http://s.realfex.xxx/img/ico/oauth/'+urls[i][2]+'.ico" class="share_img" />'+urls[i][1]+'</a>')
            }
        }
    })
}
