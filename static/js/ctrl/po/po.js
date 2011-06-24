rm = _rm("#reply","/po/reply/rm/")
$("#txt_form").elastic_login()

$(".reply_at").live("click", function(){
    var txt=$("#reply_txt").focus(),
        val=txt.val(),
        name=$(this.parentNode).find(".replyer").text(),
        add;
    add =  "@"+name+'('+this.rel+') '
    if(val.length){
        if($.trim(val)==val){
            val+=" "
        }
        val+=add;
    }else val=add;

    txt.val(val)

})
$("#reply_txt").elastic()


