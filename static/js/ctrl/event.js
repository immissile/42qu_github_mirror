function fancybox_txt(tip, action, post, complete, submit) {
	var fancybox = $.fancybox;
	fancybox({
		'content': '<form method="POST" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">　</div><div id="po_pop_main"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns"><span id="po_pop_error"></span><span class="btnw"><button type="submit">确认</button></span></div></form>',
		"onComplete": function() {
			$('.po_pop_tip').text(tip)
			var form = $("#po_pop_form"),
			pop_txt = $('#po_pop_txt').focus(),
			error = $("#po_pop_error");
			complete && complete()
			form.submit(function() {
				var txt = $.trim(pop_txt.val());

				error.hide()
				if (txt.length) {
					submit && submit()
					fancybox.showActivity()
					$.postJSON(
					action, {
						'txt': txt
					},
					post)
				} else {
					error.html('请输入文字').fadeIn()
					pop_txt.focus()
				}

				return false
			})
		},
	})
}

function event_kill() {
	fancybox_txt('解散原因如下 :', "/j/event/kill", function() {
		$.fancybox({
			'content': '活动已解散'
		})
	})
}
function event_notice() {
	fancybox_txt('公告如下 :', "/j/event/notice", function() {
		$.fancybox({
			'content': '发布成功 !'
		})
	})
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
		fancybox_txt('拒绝理由如下 :', '/j/event/check/' + id + '/0', function() {
			$.fancybox.close()
			$('#ndbk' + id).slideUp(500, function() {
				$(this).remove()
			})
		}),
		function() {
			$('#po_pop_txt').val(_txt)
		},
		function() {
			_txt = $('#po_pop_txt').val()
		}
	})
})
