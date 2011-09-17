function fancybox_txt(tip, action, complete, post,  submit) {
	var fancybox = $.fancybox;
	fancybox({
		'content': '<form method="POST" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">　</div><div id="po_pop_main"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns"><span id="po_pop_error"></span><span class="btnw"><button type="submit">确认</button></span></div></form>',
		"onComplete": function() {
			$('.po_pop_tip').text(tip)
			var form = $('#po_pop_form'),
			pop_txt = $('#po_pop_txt').focus(),
			error = $('#po_pop_error');
            if(complete){
                complete = complete()           
            } 
            form.submit(function() {
                if(complete&&!complete()){
                    error.hide().fadeIn();
                    return false
                }
				var txt = $.trim(pop_txt.val());
				error.hide();


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

function fancybox_word(title, path, finish){ 
	fancybox_txt(
        title, path,
        function(){
            return txt_maxlen(
                $("#po_pop_txt"), $('#po_pop_error'),  142
            )
        },
        function() {
		$.fancybox({
			'content': finish 
		})	
    })
}
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
