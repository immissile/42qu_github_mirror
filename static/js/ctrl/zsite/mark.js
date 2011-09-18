$(function(){
    var mk_tip=$('.mk_tip')
    $(".mk_txt").focus()
    var can = txt_maxlen(
            $(".mk_txt"),
            mk_tip,
            142           
       )
    $('#mk_form').submit(
        function(){
            if(!can()){
             mk_tip.fadeOut(function(){mk_tip.fadeIn()})
            return false
        }
    })
})

