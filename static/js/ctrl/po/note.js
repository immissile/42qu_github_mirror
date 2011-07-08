$(function(){
    $("#name").focus()
    $("#txt").elastic()
    $("#po_form").submit(function(){
        $("[placeholder]").each(function(){
            if(this.value==this.placeholder){
                this.value='';
            }
        })
    })
})

