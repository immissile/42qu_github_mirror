$(function(){
    function checkInputStatus(){
            var self=$(this), value=self.find("input").val();
            if(!value||value=="")
            {
                self.removeClass("focused")
                    .removeClass("filled")
                    .addClass("blurred");
            }else{
                self.removeClass("focused")
                    .addClass("filled");
            }
    }

    
    setTimeout(function(){
        $(".register .input-wrapper").focusout(checkInputStatus).change(checkInputStatus).focusin(function() {
            $(this).removeClass("blurred")
                .removeClass("filled")
                .addClass("focused");
        }).each(function(){
            checkInputStatus.apply(this)
        })

    },0)
});

