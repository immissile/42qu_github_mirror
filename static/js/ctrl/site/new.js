
$(function(){
    function empty(self){
        var val=self.val();
        return !val||$.trim(val)==''
    }
    function verify(){
        var self=$(this);
        tip(self)
    }
    function tip(self){
        var id=self[0].id;
        if(empty(self)){
            $("#errtip_"+id).remove()
            var tip=$('<div class="errtip" id="errtip_'+id+'"/>');
            self.after(tip);
            tip.fadeOut(function(){tip.fadeIn()})
            tip.html("此项必填")
        }
    }
    var elem="#name,#motto";
    if(!$('input[name=pic_id]')[0]){
        elem+=",#pic"
    }
    elem=$(elem);
    elem.blur(verify).focus(function(){
        $("#errtip_"+this.id).remove()
    })
    site_new = function (){
        var submit,i=0;
        for(;i<elem.length;++i){
            var self=$(elem[i]);
            if(empty(self)){
                self.focus();
                $(window).scrollTop(Math.max(self.offset().top-50,0))
                tip(self)
                submit = false
                break
            }
        }
        return submit;
    }
})
