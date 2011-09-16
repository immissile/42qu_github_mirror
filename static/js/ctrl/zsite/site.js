
$(function(){
    var say = $('#say'),
    txt = $('#say_txt'),
    after=$('<div class="pop_banner"><a class="pop_submit" href="javascript:void(0)">发表</a><div class="pop_tip"></div><a class="pop_close" href="javascript:close_pop();void(0)"></a></div>'),
    tiptxt='今天 , 想说什么?';

    txt.val(tiptxt).focus(function(){
        if(!say.hasClass('pop_say')){
            say.attr('class','pop_say')
            txt.attr('class','pop_txt').after(after)
            if(txt.val()==tiptxt)txt.val('');
            else txt.select();
        }   
    })
    txt_maxlen(txt,after.find('.pop_tip'),142)

    close_pop = function (){
        say.attr('class','say')
        txt.attr('class','say_txt')
        if($.trim(txt.val())==''){
            txt.val(tiptxt)
        }
        $('.pop_banner').remove()
    }
})
