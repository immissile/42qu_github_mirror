(function(){
    var mail=$("#mail");
    if(mail.val()==''){
        mail.focus();
    }else{
        $('#password').focus();
    }

    var zsite_list=$("#zsite_list");

    zsite_ico_list = function(ico_list){
        var t=ico_list.pop();
        ico_list.push(t);
    }


})()
