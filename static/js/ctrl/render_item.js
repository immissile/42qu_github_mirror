$.template(
    'note',
    '<div class="readl c">'+
        '<a rel="${$data[0]}" href="javascript:void(0)" id="fav${$data[0]}" class="fav{{if $data[5]}}ed{{/if}}"></a>'+
        '<div id="reado${$data[0]}" class="reado">'+
            '<span class="reada">'+
                '<span class="title">${$data[1]}</span>'+
                '<span class="rtip">${$data[2]}</span>'+
            '</span>'+
        '</div>'+
        '<div class="zname">'+
            '<a href="#" rel="${$data[3]}" class="TPH" target="_blank">${$data[4]}</a>'+
        '</div>'+
    '</div>'
)


function _render_note(elem, data){
    var result = $.tmpl('note', data)
    result.find('.TPH').each(function(){
        this.href="//"+this.rel+HOST_SUFFIX
    })
    result.appendTo(elem);
}
