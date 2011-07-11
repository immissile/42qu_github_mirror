(function(){
$("#amount").focus().select()

if(!$.cookie.get('S')){
    function _(){
        var val = $('#alipay_account').val(), mail=$(this);
        if(val.indexOf('@')>0&&$.trim(mail.val())==''){
            mail.val(val).focus().select()
        }
    }
    $("#mail").focus()
    $("#pay").submit(_)
}
})()
