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

/*
    function fav(id){
        var rec_id = $("#rec_id"+id)
        rec_id.addClass("fav_loading");
        callback=function(){
            rec_id.removeClass("fav_loading")
                  .addClass("site_faved")
                  .attr("href","javascript:unfav("+id+")");
        };
        _(id, 2,callback);
    }

    function unfav (id){
        callback=function(){};
        _(id, 0,callback);
        $("#rec_id"+id).removeClass("site_faved");
                       .attr("href","javascript:fav("+id+")");
    }
*/
    $(".buzz_h1").hover(function(){$(this).find("a").show()},function(){$(this).find("a").hide()});
    $(".buzz_w").hover(function(){$(this).find('.bzr').show()},function(){$(this).find(".bzr").hide()});

});

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

