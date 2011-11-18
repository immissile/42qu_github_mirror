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
            self.parent().append(tip);
            tip.fadeOut(function(){tip.fadeIn()})
            tip.html("此项必填")
        }
    }
    var elem="#name,#motto,#url,#txt"
    if(!$("#pic_id")[0]){
        elem+=",#pic"
    }
    elem=$(elem)
    elem.blur(verify).focus(function(){
        $("#errtip_"+this.id).remove()
    })
    com_new = function(){
        var i=0
        for(;i<elem.length;++i){
            var self=$(elem[i])
            if(empty(self)){
                self.focus()
                $(window).scrollTop(Math.max(self.offset().top-50,0))
                tip(self)
                return false
            }
        }
        if($('#pid')[0] && $('#pid>select[name="city"]').val()==0){
            $('#errtip_addr').html('请填写完整地址')
            return false
        }
        if(!$('#pid')[0] && $('.pid:first>select[name="city"]').val()==0){
            $('#errtip_addr').html('请填写完整地址')
            return false
        }
        $('.pid:last').parent().remove()
        $('input[type="hidden"]').each(function(){
            var self = $(this)
            if(self.attr('name').substr(0,3)=='pid') self.attr('name','pid')
        })
        return true 
    }

    var addr_num = 2
    add_addr = function(){
        var self = $('.add_addr')
        self.before('<div><span id="pid'+addr_num+'" class="pid"></span><script>_("pid'+addr_num+'",0)<\/script><input type="text" class="input addr_input" name="address" /><a href="javascript:close_addr('+addr_num+');void(0)" class="close_addr"></a></div>')
        addr_num++
    }
    close_addr = function(id){
        var fir_id = $('.pid:first').attr('id').substr(3)
        var fir = fir_id.length>0 && !$('#pid')[0]
        if(id==1){
            $('#pid').remove()
            $('.addr_input:first').remove()
            $('.close_addr:first').remove()
            $('.pid:first').parent().css('display','inline')
            $('.pid:first').css('margin-left','-4px')
        } else if(fir){
            $('#pid'+id).parent().remove()
            $('.pid:first').parent().css('display','inline')
            $('.pid:first').css('margin-left','-4px')
        } else{
            $('#pid'+id).parent().remove()
        }
    }
})
