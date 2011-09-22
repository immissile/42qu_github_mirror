
function init_say(){
    document.write('<div class="say"><div class="say_txt">今天 ,  想说什么?</div></div> <div class="pop_say"> <textarea class="pop_txt"></textarea> <div class="pop_banner"><a class="pop_submit" href="javascript:post_say();void(0)">发表</a><div class="pop_tip"></div><a class="pop_close" href="javascript:close_pop();void(0)"></a></div></div>')
}

$(function(){
    var say = $('.say')
    var pop_say = $(".pop_say")
    var txt = $('.say_txt')
    var pop_txt = $('.pop_txt')
    var txt_tip = txt.text()
    var  pop_tip = $('.pop_tip') 
    
    can_say = txt_maxlen(pop_txt,pop_tip,142)

    txt.click(function(){
        if(pop_say.is(":hidden")){
            pop_say.show();
            pop_say.css("marginTop",0).css("marginTop",Math.max(txt.offset().top-pop_say.offset().top-98,-62))
            pop_txt.focus()
        }  
    })
    
    close_pop = function (){
        var cont = $('.pop_txt').val()
        pop_say.hide()
        if($.trim(cont)=='') txt.text(txt_tip)
        else txt.text(cont)
    }


    post_say = function (){
        if(!can_say()){
            pop_tip.fadeOut(function(){pop_tip.fadeIn()})
            return false
        }
        var val=pop_txt.val()
        pop_txt.attr('disabled',true)
        pop_tip.replaceWith('<div class="say_loading pop_tip"></div>')
        $('.pop_close,.pop_submit').hide()
        $.postJSON(
            '/j/po/word',
            {
                "txt":val
            },
            function(){
                $('.pop_tip').replaceWith('<div class="pop_ok pop_tip">发表成功</div>')
                var pop_ok = $('.pop_ok')  
                pop_ok.fadeIn(function(){
                    location="/word"
                })
            }
        )
    }
})




function fav(){
    if(!islogin())return;
    fancybox_word(
        '备注 :',
        '/j/fav',
        function(){
            $("#fav_a").text('设置').attr('href','/mark')
        },
        function(){return 1} 
    )
}

function render_site(data){
	var feed_loader = feed_load_maker(
"zsite_id id fav cid rid reply_count create_time name txt txt_more"
    )
	,
    zsite_dict = data[1],
    career_dict = data[2],
    data = data[0],
    i,
    length = data.length,
    result,
    t,
    o,
    r = [],
    z
;

    for (i=0;i < length; ++i) {
        t=feed_loader(data[i])
        t.zsite = z= {}
        o = zsite_dict[t.zsite_id]
        if(o){
            z.name = o[0] 
            z.link = o[1] 
        }
        o = career_dict[t.zsite_id]
        if(o){
            z.unit = o[0]
            z.title = o[1] 
        }

        r.push(t)
    }
    $('#feed').tmpl(r).appendTo("#feeds");
}


