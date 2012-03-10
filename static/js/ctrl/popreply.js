function popreply(cid, title_html, href, counter){
    if(!counter[0])counter=0;
    var content = $(
        '<div class="fcmpop" id="reply_reply_pop"><a target="_blank" id="reply_name"></a><div id="reply_reply_body" class="reply_reply_loading"></div><textarea></textarea><div class="tr"><span class="btnw"><button type="submit" class="button">回复</button></span></div></div>'
        ),
        cbody = content.find('#reply_reply_body'), 
        t=cbody[0],
        textarea = content.find('textarea'),
        fancybox = $.fancybox,
        button = content.find('button'),
        reply_name=content.find('#reply_name'),
        id = href.split("/")[4].split("#")[0],
        count=true;

        if(counter){
            count=counter.html()
            if(count.length){
                count-=0
            }else{
                count=0
            }
        }
        textarea.ctrl_enter(button.click);
        reply_name.html(title_html).attr('href',href)

    button.click(function(){
        var v=textarea.val(), 
            fancybox=$.fancybox;
        if(!v.length)return;
        textarea.val('')
        fancybox.showActivity();
        post_reply(id, v,function(data){
            fancybox.hideActivity();
            textarea.focus()
            _result(data)
            if(counter){
                count+=1
                counter.html(count)
            }
        })
    })
    function _(data){
        if(data.cid==61){
            reply_name.remove()
        }else{
            reply_name.text(data.name)
        }
        _result(data.result,1)
    }
    function _result(result,i){
        cbody.removeClass('reply_reply_loading').append(render_reply(result,i))
        codesh()
        var height = t.scrollHeight+2, 
            winheight=$(window).height() - 260;

        if(height>winheight){
            height = winheight;
        }else{
            cbody.css("padding","0")
        }

        cbody.css({
            height:height
        })
        if(count===true){ //有count的就从第一个开始显示
            t.scrollTop=t.scrollHeight-t.offsetHeight-5
        }
        fancybox.resize()
    }
    if(!count){
        cbody.css('height',0).removeClass('reply_reply_loading')
    }
    fancybox({
        content:content, 
        onComplete:function(){
            textarea.focus()
            if(count||!counter){ 
                $.getJSON( '/j/po-'+cid+'/json/'+id, _)
            }
        }
    })
}


$(function(){
    $(".bzreply").live("click",function(){
        var self=$(this)
        popreply(
            "reply",
            self.parents('.readpad').find('.readtitle').html(),
            this.href,
            self.find('.count')
        )
        return false
    })
})

function recreply(elem){
    popreply(
        "reply",
        '',
        elem.href
    )
    return false
}
