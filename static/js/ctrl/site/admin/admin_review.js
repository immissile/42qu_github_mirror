    var before = '<div class="pop_reason"><div class="pop_banner"><a href="javascript:void(0);" class="pop_submit">确定</a><a href="javascript:close_pop();void(0)" class="pop_close"></a><div class="txt_dis">原因如下</div></div><textarea class="pop_txt"></textarea></div>'

$(function(){
    var re_cont
    function pop_reason(){
        var links = $('.refuse,.refused,.pass,.passed')
        links.unbind('click')
        $(this).before(before)
        var txt =  $(this).parent().find($('.pop_txt'))
        txt.val(re_cont).focus()
        $('.pop_submit').click(txt_submit)
    }

    function pass_ck(){
        $(this).attr('class','passed')
        var left_re = $(this).parent().find($('.refused'))
        if(left_re[0]) left_re.attr('class','refuse c9').bind('click',pop_reason)

    }

    function bind_all(){
       $('.refuse').click(pop_reason)
        $('.pass').click(pass_ck)
    }
    
    bind_all()

    close_pop = function(){
        $('.pop_reason').remove()
        bind_all()
    }
    function txt_submit(){
        var right_re = $(this).parent().parent().parent().find($('.passed'))
        var left_re = $(this).parent().parent().parent().find($('.refuse'))
        $.postJSON(
            '/j/po/word',
            {
                "txt":$('.pop_txt').val()
            },
            function(){
                re_cont = $('.pop_txt').val()
                $('.pop_reason').remove()
                if(right_re[0]) right_re.attr('class','pass c9')
                if(left_re[0]) left_re.attr('class','refused')
                bind_all()
            }
        )
    }
})
