$("input[name=name]").focus(function(){
    $('#tag0').attr('checked',true)
}).defaultValue();

function tag(){
    var fancybox = $.fancybox
    fancybox.showActivity();
    $.postJSON("/j/po/tag",function(o){
        fancybox.hideActivity()
        $.fancybox({
            content:o
        })
    })
}
