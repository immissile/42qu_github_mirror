$(function(){
    $('.info_txt').focus(function(){
        var self = $(this)
        self.css('height','120px')
        self.elastic()
        var word = self.attr('placeholder')
        if(!self.prev().find('.place_hint')[0]){
            self.prev().append('<span class="place_hint">'+word+'</span>')
        }
    }).blur(function(){
        var self = $(this)
        self.css('height','28px')
        self.prev().find('.place_hint').remove()
    })
    var tip = $('.txt_bio_tip')
    txt_maxlen($('#txt_bio'),tip,142)

    $('.product_similar_name:last').live('blur',function(){
        var self = $(this)
        if($.trim(self.val()).length>0){
            var wrap = self.parent(),
            id = parseInt(self.parent().attr('id').substr(11))+1
            wrap.after('<div class="product_similar_wrap" id="product_similar_wrap'+id+'"><input name="product_similar_name" class="product_similar_name" autocomplete="off" placeholder="产品名称"><input placeholder="相关链接" name="product_similar_url" class="product_similar_url"><a href="javascript:close_item('+id+');void(0)" class="close_ot_item"></a></div>')
        }
        self.unbind('blur')
    })

    close_item = function(id){
        $('#product_similar_wrap'+id).remove()
    }

    function empty(self){
        var val=self.val();
        return !val||$.trim(val)==''
    }

    var elem="#txt_bio,#txt_plan,#txt_hope"
    elem=$(elem)

    $('form:first').submit(function(){
        for(var i=0;i<elem.length;++i){
            var self=$(elem[i]);
            if(empty(self)){
                self.focus();
                $(window).scrollTop(Math.max(self.offset().top-50,0))
                var hint = self.prev().find('.place_hint')
                hint.text('此项必填').css('color','red').fadeOut(function(){hint.fadeIn()})
                return false
            }
        }
        if(cnenlen($('#txt_bio').val())>142){
            var tip = $('.txt_bio_tip')
            $(window).scrollTop(Math.max(tip.offset().top-50,0))
            tip.fadeOut(function(){tip.fadeIn()})
            return false
        }
        return true
    })
})

function add_pic(){
    $('.add_pic').before('<div class="files"><input class="file" name="pic" type="file" size=35><input class="file" name="pic" type="file" size=35></div>')
}
