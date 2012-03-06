rm = _rm("#reply","/po/rm/reply/")
$(function(){
    $(".G,.G4").css('position','static')

    $("#reply_txt").ctrl_enter( function(){$("#txt_form").submit()});
})
$("#txt_form").elastic_login().submit(function(){
        var textarea=$(this).find('textarea'),
            v=textarea.val(),
            fancybox=$.fancybox;
        if(!v.length)return;
        textarea.val('')

        fancybox.showActivity();
 
        post_reply(PO_ID, v,function(data){
            textarea.focus();
            fancybox.hideActivity();

            var reply_list =  $("#reply_list").show();
            reply_list.find(".fcmi:last").css('borderBottom','1px dotted #ccc')
            reply_list.append(render_reply(data)).find(".fcmi:last").css(
                'border','0'
            )
        })
    return false
})
$(function(){
    if(islogin()&&$('#txt_form')[0]){
        $("#reply_txt").pop_at("/j/at/reply/"+$('#txt_form').attr('action').split('/')[3],27)
        $("#reply_txt").elastic()
    }
})


/*
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
*/

$(function(){
    var style1 = {'position':'fixed',"marginTop":"-56px"},style2 = {'position':'absolute',"marginTop":"36px"}
  
    scroll_to_fixed('#sT',-16,'-56px','36px')
})

$(function(){
    codesh()
    if($(window).width()<827){
        $(".sprev,.snext").hide()
        
    }
});

(function(){

    var INPUT_FOCUS;
    
    $(document).keyup(function (e) {
        if (!INPUT_FOCUS && !(e.ctrlKey || e.shiftKey || e.altKey) ) {
            var id
            switch (e.keyCode) {
                case 37://←
                id="sprev"
                break
                case 39://→
                id="snext"
                break
            }
            if(id){
                id = $('.'+id)[0]
                if(id){
                    location = id.href
                }
            }
        }
    })
    
    function input_ban () {
        $('input, textarea').live('focus',function () {
            INPUT_FOCUS = this
        }).live('blur',function () {
            INPUT_FOCUS = null
        })
    }
    $(input_ban)
    $(document).ajaxComplete(input_ban)
    
    $.postJSON(
        "/j/po/reply/json/"+PO_ID, 
        function(data){
var reply_list =  $("#reply_list");
if(data.length){
    reply_list.append(render_reply(data)).find(".fcmi:last").css('border','0')
}else{
    reply_list.hide()
}
        }
    )

})();
