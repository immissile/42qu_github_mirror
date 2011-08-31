$(function(){

var po_word="po_word", tip='今天 , 你想说什么 ?', po_submit=$('<div class="po_word_submit"><a href="javascript:void(0)" class="po_word_close"></a><span class="po_word_tip"><span>32</span>字</span><a href="javascript:void(0)" class="po_word_submit_a">发布</a></div>'), word=$("#"+po_word).val(tip).blur().focus(function(){
    if(!$.cookie.get('S')){
        login();
        return
    }
    if(!word.hasClass(po_word)){
        word.val('').addClass(po_word);
        po_submit.show()
    }
}).blur(function(){
    var v=word.val();
    if(!v||v==''){
        word.removeClass(po_word).val(tip)
        po_submit.hide()
    }
}).after(po_submit)

po_submit.find('.po_word_submit_a').click(function(){
    var v=word.val();
    $.fancybox.showActivity()
    if(v.length){
        $.post("/po/word",function(){
            location.reload()
        })
    } 
})
po_submit.find('.po_word_close').click(function(){
    word.val('').blur()
})

})
/*
<div style=" "><span style="color: rgb(153, 153, 153); padding: 0pt 0pt 0pt 14px; line-height: 38px;">32字</span>
</div>
*/
