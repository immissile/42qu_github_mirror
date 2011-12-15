WINDOW_WIDTH = document.documentElement.clientWidth;
textarea = $('.say_txt');
change = function(){
    $('.say_type').hide();
    $('#po_ext').show();
    textarea.addClass('saying')
};
calcel = function(){
    $('#po_ext').hide();
    $('.say_type').show();
    textarea.removeClass('saying')
};

tip = $('#txt_tip');
can_say = txt_maxlen(textarea, tip, 142, change,calcel);

$('#po_ext').click(function(){
    $('#po_ext').hide();
    tip.hide();
    $('.say_type').show();
});

