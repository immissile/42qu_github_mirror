$("input[name=name]").focus(function(){
    $('#tag0').attr('checked',true)
}).defaultValue();

function tag(){
    var fancybox = $.fancybox
    fancybox.showActivity();
    $.postJSON("/j/po/tag",function(o){
        var _tag=$("<div><button>保存</button></div>")
        $("#tag").tmpl(o).prependTo(_tag)
        $.fancybox({
            content:_tag.html()
        })
    })
}

rm_tag=_rm("tag_rm","/j/po/tag/rm/")
