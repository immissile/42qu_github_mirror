rm = _rm("#reply","/po/reply/rm/")
$(function(){$(".G,.G4").css('position','static')})
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
if(!IE6){
    $(function(){
        var st = $('#sT');
        if(st[0]){
            st.css('position','absolute')
            var top = st.offset().top, win=$(window).scroll(function() {
                if(win.scrollTop() >= top-16){
                    st.css({'position':'fixed',"marginTop":"-56px"})
                }else{
                    st.css({'position':'absolute',"marginTop":"36px"})
                }
            })
        }

    })
}
$(function(){
    if($(window).width()<827){
        $(".sprev,.snext").hide()
        
    }
})

