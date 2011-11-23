function product_add(){
    $.fancybox({
        'content':'<form enctype="multipart/form-data" method="POST" action="/product/new" id="popline"><input name="_xsrf" type="hidden"><div class="line"><div>产品名称<input autocomplete="off" value="" class="input" name="product_name" id="pop_name"></div><div>简单描述<input autocomplete="off" class="input" name="product_about" value=""></div><div>相关链接<input class="input" autocomplete="off" name="product_url" value=""></div><div style="margin:7px 0 0 70px"><span class="btnw"><button type="submit">添加产品</button></span></div></div><input type="hidden" name="edit" value="1">','onComplete':function(){

        var pop_name = $('#pop_name').focus()
        $("#popline").submit(function(){
            if(!pop_name.val().length){
                alert("请输入产品名称 !")
                pop_name.focus()
                return false
            }
        }).find("input[name=_xsrf]").val($.cookie.get("_xsrf"))
    }, 
    'overlayShow':false
    })
}
$(function(){
    var pop_add = $("#pop_add")
    if(pop_add[0]){
        pop_add.click(product_add)
    }else{
        $('.product_name:last').live('blur',function(){
            var self = $(this)
            if($.trim($('.line:last').find('input[name="product_name"]').val()).length>0){
                var wrap = self.parent().parent(),
                id = parseInt(wrap.attr('id').substr(4))+1
                wrap.after('<div class="line" id="line'+id+'"> <span class="L"><input name="product_name" class="product_name" value="" autocomplete="off"><input value="" name="product_about" class="product_about" autocomplete="off"><input value="" name="product_url" class="product_url"></span><a href="javascript:close_item('+id+');void(0)" class="close_item"></a></div>')
            }
            self.unbind('blur')
        })
    }
})
function close_item(id){
    $('#line'+id).remove()
}
