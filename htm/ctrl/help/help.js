$(function(){
    $("a[href='/']").attr("href","//"+location.hostname.split(".").slice(1).join("."))
})
