$(function(){
    var name=$("#name");

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
        h = Math.max(win.height() - txt.offset().top - 37, 250);
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


    autocomplete_tag('#search', window.TAG_LIST||[]);
    function show_placeholder(){
        if(!$('#token-input-search').val().length>0 && !$('.token-input-token').length>0){
            $('.token-input-list').hide()
            $('#search').val("").show()
            $('#token-input-search').unbind('blur')
        }
        if(document.activeElement.id!='token-input-search'){
            $('.token-input-dropdown').hide()
        }
    }
    function show_token_input(){
        $('#token-input-search').focus().blur(show_placeholder).focus(function(){
            if($('#token-input-search').val().length>0)
            $('.token-input-dropdown').show()}
        )
    }
    show_placeholder()
    function _(){
        $(".token-input-list").show()
        $(this).hide()
        if(navigator.userAgent.indexOf("MSIE")>0) { 
            setTimeout(show_token_input,10)
        }else{
            show_token_input()
        }
    }
    $('#search').bind('click',_).show().click()

    name.focus().select()
})

