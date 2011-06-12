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
        success: function(data, textStatus, jqXHR){
            if(data.login){
                login()
            }else if(callback){
                callback(data, textStatus, jqXHR)
            }
        }
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

function script(src,callback){
    src = src.split(" ")
    var r=[],i=0;
    for(;i<src.length;++i){
        r.push($.getScript(src[i]))
    }
    $.when(r).then(function(){
        callback&&callback()
    });    

}

(function(){
var BUFFER={}
render = function (id, view, partials, send_fun){
    var html;
    if(!(id in BUFFER)){
         BUFFER[id] = $("#"+id).html() 
    }
    html = BUFFER[id]
    return $.mustache(html, view, partials, send_fun)
}

})()

