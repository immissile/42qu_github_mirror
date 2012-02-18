$(function(){
    autocomplete_tag("#search", [], 1)
    function show_placeholder(){
        if(!$('#token-input-search').val().length>0){
            $('.token-input-list').hide()
            $('#search').show()
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
    $('#search').bind('click',function(){
        $(".token-input-list").show()
        $(this).hide()
        if(navigator.userAgent.indexOf("MSIE")>0) { 
            setTimeout(show_token_input,10)
        }else{
            show_token_input()
        }
    })
})

