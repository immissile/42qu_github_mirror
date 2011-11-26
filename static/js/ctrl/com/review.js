$(function(){
    $('.review_cb:checked').parent().parent().addClass('selected')
    $('.review_cb').change(function(){
        var self = $(this)
        var id = self.attr('id').substr(3)
        $('#review_'+id).toggleClass('selected')
        $.postJSON('/j/review/show/'+(this.checked?"new":"rm")+"/"+id)
    })

auto_add('member_mail','<div class="line"><input name="mail" class="member_mail" placeholder="邮箱"><input name="name" class="member_name" placeholder="姓名"></div>','mail_block','','blur')
    $('.invite_link').mouseover(function(){$(this).select()})

auto_add('admin_member_mail','<div class="line"><input class="admin_member_mail" name="mail" placeholder="邮箱"><input  class="admin_member_name" name="name" placeholder="姓名"></div>','mate_mail','','blur')

auto_add('admin_friend_mail','<div class="line"><input class="admin_friend_mail" name="mail" placeholder="邮箱"><input  class="admin_friend_name" name="name" placeholder="姓名"></div>','friend_mail','','blur')

})
