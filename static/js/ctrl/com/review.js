$(function(){
    $('selected').find('review_cb').attr('checked','checked')
    $('.review_cb').click(function(){
        var self = $(this)
        var id = self.attr('id').substr(3)
        $('#review_'+id).toggleClass('selected')
        $.postJSON(
            'url',
            {
                'id':id
            }
        )
    })
})
