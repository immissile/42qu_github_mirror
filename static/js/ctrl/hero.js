function click_sets(){
    var html = $('html,body'),
    e = $('.xatagset').blur(),
    pb = $('.pop_block')
    function _() {
        pb.hide()
        html.unbind('click', _)
    }

    if (pb.is(":hidden")) {
        pb.show()
        html.click(_)
        clicked = true;
    } else {
        _()
    }
}
