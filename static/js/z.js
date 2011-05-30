$(function(){
    function checkInputStatus(){
            var self=$(this), value=self.find("input").val();
            if(!value||value=="")
            {
                self.removeClass("focused")
                    .removeClass("filled")
                    .addClass("blurred");
            }else{
                self.removeClass("focused")
                    .addClass("filled");
            }
    }

    
    setTimeout(function(){
        $(".register .input-wrapper").focusout(checkInputStatus).change(checkInputStatus).focusin(function() {
            $(this).removeClass("blurred")
                .removeClass("filled")
                .addClass("focused");
        }).each(function(){
            checkInputStatus.apply(this)
        })

    },0)
});

$.postJSON = function(url, data, callback) {
    data = data||{};
    if ( $.isFunction( data ) ) {
        callback = data;
    }
    data._xsrf = cookie.get("_xsrf");
    $.ajax({
        url: url,
        data: data, 
        dataType: "json", 
        type: "POST",
        success: callback 
    });
};

cookie = {
set:function(dict, days, path){
    if(typeof(days)=='string'){
        path=days;
        days=0;
    }
    days = days || 99;
    path = path||'/';
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
    for (var i in dict){
        document.cookie = i+"="+dict[i]+expires+"; path="+path;
    }
},
get:function(name) {
    var e = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(e) == 0) {
            return c.substring(e.length,c.length).replace(/\"/g,'');
        }
    }
    return null;
}
}

_gaq=[['_setAccount', 'UA-23361634-1'],['_trackPageview'],['_trackPageLoadTime']];
(function(){
    var ga = document.createElement('script');
    ga.type = 'text/javascript';
    ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    /*google 百度 统计*/
})()
