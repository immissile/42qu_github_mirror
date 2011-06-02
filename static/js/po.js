rm = _rm("reply","/po/reply/rm/")

$(function(){
    $("#txt").elastic().focus(function(){
        if(!cookie.get('S')){
            login()
        }
    })
})
