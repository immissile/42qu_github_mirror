$(function(){
    var name=$("#name").focus();

    $("#po_form").submit(function(){
        $("[placeholder]").each(function(){
            if(this.value==this.placeholder){
                this.value='';
            }
        })
        if(name.val()==''){
            alert("没有标题 , 不可以 ...")
            name.focus()
            return false
        }
    })


    var win = $(window),
        txt = $("#txt");
    
    function txtresize() {
        var inpo = $("#po_btn"),
        h = Math.max(win.height() - inpo.height() - txt.offset().top - 50, 250);
        txt.height(h)
    }
    txtresize()
    win.resize(txtresize)

    $("#rm").click(function(){
        if(!confirm("删除 , 确定 ?")){
            return false
        }
    }) 

    $("#txt").bind("keydown",insertTab);
})

$(function(){
    autocomplete_tag('#search', [['减肥',10226353]], 0)
/*    var txt = $('#txt'),txt_height = txt.height()
    $('#token-input-search').focus(function(){
        txt.height(txt_height-250)
    }).blur(function(){
        txt.height(txt_height)
    })
*/
})

