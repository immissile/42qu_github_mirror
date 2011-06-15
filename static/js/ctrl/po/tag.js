$("input[name=name]").focus(function(){
    $('#tag0').attr('checked',true)
}).defaultValue();

function tag(){
    var fancybox = $.fancybox
    fancybox.showActivity();
    $.postJSON("/j/po/tag",function(o){
        var _tag=$('<div><button>保存</button></div>')
        $("#tag").tmpl(o).prependTo(_tag)
        $.fancybox({
            content:'<form id="_tag">'+_tag.html()+'</form>'
        })
        _tag=$("#_tag")
        _tag.find('button').click(function(){
            alert(_tag.serialize())
            return false
        }).find('input[type=text]').attr('autocomplete','off') 
    })
}

rm_tag=_rm(".tag","/j/po/tag/rm/")
