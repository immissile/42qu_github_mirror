$(function(){
    $('.search_input').focus()
    $('.f_item').toggle(
        function(){ 
            $(this).toggleClass('f_item2')
            $(this).toggleClass('f_item')
        },
        function(){ 
            $(this).toggleClass('f_item2')
            $(this).toggleClass('f_item')
        })
    $('#select_all').click(
        function(){
            if($(this).attr('checked')){
                $('.f_item').attr('class','f_item2')
            } else{
                $('.f_item2').attr('class','f_item')
            }
        }
    )

    $("#follow_form").submit(function(){
        var select_ids = [];

        $('.f_item2').each(function(){
            select_ids.push(this.id)
        })

        $("#follow_id_list").val(select_ids.join(' '))
        
    })
})
