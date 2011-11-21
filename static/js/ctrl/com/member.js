$(function(){
    $('.search_input').focus()
    $('.f_item').toggle(
        function(){ 
            $(this).toggleClass('f_item2')
            $(this).toggleClass('f_item')
        },
        function(){ 
            $(this).toggleClass('f_item2')
            $(this).toggleClass('f_item')
        })
    $('#select_all').click(
        function(){
            if($(this).attr('checked')){
                $('.f_item').attr('class','f_item2')
            } else{
                $('.f_item2').attr('class','f_item')
            }
        }
    )

    $("#follow_form").submit(function(){
        var select_ids = [];

        $('.f_item2').each(function(){
            select_ids.push(this.id)
        })

        $("#follow_id_list").val(select_ids.join(' '))
        
    })

    $('.member_mail:last').live('blur',function(){
        var self = $(this)
        if($.trim(self.val()).length>0){
            self.parent().after(
'<div class="line"><input placeholder="邮箱" name="mail" class="member_mail"><input placeholder="姓名" name="name" class="member_name"></div>'
            )
        }
    })
    $('.member_link:last').live('blur',function(){
        var self = $(this)
        if($.trim(self.val()).length>0){
            self.parent().after(
'<div class="line"><input placeholder="用户网址" name="link" class="member_link"></div>'
            )
        }
    })
    $('.member_mail_short:last').live('blur',function(){
        var self = $(this)
        if($.trim(self.val()).length>0){
            self.parent().after(
'<div class="line"><input placeholder="邮箱" name="mail" class="member_mail_short"><input placeholder="姓名" name="name" class="member_name_short"></div>'
            )
        }
    })


    $('.member_rm_a').click(function(){
        var self = $(this)
        var url = $(this).attr('id').split('-')[0]=='in'?'/member/invite/rm':'/member/rm'
        var id = $(this).attr('id').split('-')[1]
        self.parent().remove()
        $.postJSON(
            url,
            {'id':id}
        ) 
    })
})

