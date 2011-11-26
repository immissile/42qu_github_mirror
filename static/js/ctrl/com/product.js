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

    auto_add('similar_product_name','<div class="similar_product_wrap"> <input name="similar_product_name" class="similar_product_name" placeholder="产品名称"><input name="similar_product_url" placeholder="相关链接" class="similar_product_url"><a href="javascript:void(0)" class="close_item"></a></div>','similar_product_block','close_item','focus')

    auto_add('product_name','<div class="line"><input name="product_name" class="product_name"><input name="product_about" class="product_about"><input name="product_url" class="product_url"><a href="javascript:void(0)" class="close_item"></a></div>','product_block','close_item','focus')
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
