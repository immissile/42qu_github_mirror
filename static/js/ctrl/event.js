
function event_kill(id) {
    fancybox_word(
        '解散原因如下 :',
        '/j/event/kill/' + id,
        '活动已解散'
    )
}
function event_notice(id) {
    fancybox_word(
        '公告如下 :',
        '/j/event/notice/' + id,
        '发布成功 !'
    )
}

$(function() {
	var _txt = $('#_txt').val()

	$('.join_yes').click(function() {
		var box = $(this.parentNode.parentNode)
		if (!box.hasClass('join_y')) {
			box.addClass('join_y')
			var id = this.rel
			$.postJSON('/j/event/check/' + id + '/1')
		}
	})

	$('.join_no').click(function() {
		var id = this.rel
		fancybox_txt(
        '拒绝理由如下 :', 
        '/j/event/check/' + id + '/0', 
		function() {
			$('#po_pop_txt').val(_txt).select()
		},
        function() {
			$.fancybox.close()
			$('#ndbk' + id).slideUp(500, function() {
				$(this).remove()
			})
		},
		function() {
			_txt = $('#po_pop_txt').val()
		})
	})
})
