$("input[name=name]").focus(function(){
    $('#tag0').attr('checked',true)
})

function tag(){
    var fancybox = $.fancybox
    fancybox.showActivity();
    $.postJSON("/j/po/tag",function(o){
        var _tag=$('<div><span class="btnw"><button type="submit">保存</button></span></div>')
        $("#tag").tmpl(o).prependTo(_tag)
        fancybox({
            content:'<form id="_tag"><div class="tag">'+_tag.html()+'</div></form>'
        })
        _tag=$("#_tag").submit(function(){
            fancybox.showActivity() 
            $.postJSON("/j/po/tag/edit",_tag.serialize(),function(){location.reload()});
            return false
        })
    })
}

rm_tag=_rm(".tag","/j/po/tag/rm/")

