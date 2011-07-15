$(function(){
    $("#name").focus()
    $("#po_form").submit(function(){
        $("[placeholder]").each(function(){
            if(this.value==this.placeholder){
                this.value='';
            }
        })
    })


    var win = $(window),
        txt = $("#txt");
    
    function txtresize() {
        var inpo = $("#po_btn"),
        h = Math.max(win.height() - inpo.height() - txt.offset().top - 50, 250);
        txt.focus().height(h)
    }
    txtresize()
    win.resize(txtresize)




})

