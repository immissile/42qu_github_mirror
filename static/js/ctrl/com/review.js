$(function(){
    $('selected').find('review_cb').attr('checked','checked')
    $('.review_cb').click(function(){
        var self = $(this)
        var id = self.attr('id').substr(3)
        $('#review_'+id).toggleClass('selected')
        $.postJSON(
            'url',
            {
                'id':id
            }
        )
    })

    $('.member_mail:last').live('blur',function(){
        var self = $(this)
        if($.trim($('.line:last').find('input[name="mail"]').val()).length>0){
            var wrap = self.parent()
            wrap.after('<div class="line"><input name="mail" class="member_mail" placeholder="好友邮箱"><input name="name" class="member_name" placeholder="好友姓名"></div>')
        }
    })
    $('.invite_link').mouseover(function(){$(this).select()})


})
