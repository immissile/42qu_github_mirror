$(function(){
    if(location.pathname=='/'){
        $("a[href='/']").attr("href","//"+location.hostname.split(".").slice(1).join("."))
    }
})
