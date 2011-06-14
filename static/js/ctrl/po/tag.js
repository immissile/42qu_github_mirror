$("input[name=name]").focus(function(){
    $('#tag0').attr('checked',true)
}).defaultValue();

function tag(){
    var fancybox = $.fancybox
    fancybox.showActivity();
    $.postJSON("/j/po/tag",function(o){
        var _tag=$("#_tag")
        $("#tag").tmpl(o).prependTo(_tag)
        $.fancybox({
            content:_tag.html()
        })
    })
}
