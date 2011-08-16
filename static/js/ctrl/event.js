(function() {
	var _txt = $('#_txt').val()

	$('a.join_yes').live('click', function() {
		var box = $(this.parentNode.parentNode)
		if (!box.hasClass('join_y')) {
			box.addClass('join_y')
			var id = this.rel
			$.postJSON('/j/event/check/' + id + '/1')
		}
	})

	$('a.join_no').live('click', function() {
		var id = this.rel
		var fancybox = $.fancybox
		fancybox({
			'content': '<form method="POST" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">拒绝理由如下 :</div><div id="po_pop_main"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns"><span id="po_pop_error"></span><span class="btnw"><button type="submit">提交</button></span></div></form>',
			"onComplete": function() {
				var form = $("#po_pop_form"),
                    pop_txt = $('#po_pop_txt').focus().val(_txt),
                    error = $("#po_pop_error");

				form.submit(function() {
					var txt = $.trim(pop_txt.val());
                    
                    error.hide()

					if (txt.length) {
						fancybox.showActivity()
						_txt = txt
						$.postJSON('/j/event/check/' + id + '/0', {
							'txt': txt
						},
						function(data) {
							fancybox.close()
							$('#ndbk' + id).slideUp(500, function() {
								$(this).remove()
							})
						})
					} else {
						error.html('请输入理由').fadeIn()
                        pop_txt.focus()
					}

					return false
				})
			}
		})
	})
})()
