rm = _rm("#reply","/po/reply/rm/")
$("#txt_form").elastic_login()

$(".reply_at").live("click", function(){
    var txt=$("#reply_txt").focus(),
        val=txt.val(),
        id=this.rel,
        aname=$('#reply_name'+id),
        href=aname[0].parentNode.href,
        name=aname.text(),
        add;
    href = href.split("/");
    href = href[href.length-1];
    add =  "@"+name+'('+href+') '
    if(val.length){
        if($.trim(val)==val){
            val+=" "
        }
        val+=add;
    }else val=add;

    txt.val(val)

})
