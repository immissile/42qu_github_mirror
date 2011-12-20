(function(){
function po_(id, action, name, input, oncomplete){
    var fancybox = $.fancybox;
    fancybox({
        "content":[
        '<form method="POST" enctype="multipart/form-data" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">',
        id?"编辑文本":"发布"+name,
        '</div>',
        '<div id="po_pop_main">',
        id?'':input,
        '<input id="po_pop_name" autocomplete="off" name="name" type="text"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns">',
        id?'<a href="javascript:void(0)"  id="po_pop_rm">删除</a>':'<span id="po_pop_error"></span>',
        '<span class="btnw"><button type="submit">提交</button></span></div><input type="hidden" name="_xsrf" value=""></form>'
        ].join(''),
        hideOnOverlayClick:false,
        "onComplete": function(){
            var form=$("#po_pop_form"),
                po_name=$("#po_pop_name"),
                _xsrf = $.cookie.get("_xsrf");
                
                form.find("input[name=_xsrf]").val(_xsrf)
                
                po_name.attr('placeholder',"请输入"+name+"标题 ..." )
                form.attr(
                    'action',
                    "/po/"+action+(id?("/"+id):"")
                )

                if(id){
                    po_name.val($.trim($('#po_name').text()))
                    $("#po_pop_txt").val($.trim($('#_txt').val()))
                    $("#po_pop_rm").attr('href',"/po/rm/"+id+"?_xsrf="+_xsrf).click(function(){
                        if(!confirm('删除 , 确定 ?')) return false;
                    })
                }

                form.submit(function(){ 
                    var error;
                    name = $.trim(po_name.val())
                    if(name==po_name[0].placeholder){
                        name='';
                    }
                    if(!(name&&name.length)){
                        error = "请输入标题"
                        po_name.focus()
                    }
                    fancybox.showActivity();
                    if(!error){
                        if(!id){
                            error = oncomplete() 
                        }
                    }
                    if(error){
                        fancybox.hideActivity();
                        $("#po_pop_error").html(error).fadeIn()
                        return false
                    }
                })
        }
    })
}

po_video = function(id){
    po_(
        id,
        'video',
        '视频',
        '<input id="po_video" autocomplete="off" placeholder="优酷/土豆/新浪的视频网址 ..." name="video" type="txt">',
        function(){
            var e=$('#po_video'), video=$.trim(e.val()), error;
            if(video&&video.length){
                if(
                    !(
                        /^http:\/\/v\.youku\.com\/v_show\/id_[\w=]+\.html$/.test(video) 
                        || 
                        /^http\:\/\/player\.youku\.com\/player\.php\/sid\/[\w=]+\/v\.swf$/.test(video)
                        ||
                        /^http:\/\/www\.tudou\.com\/programs\/view\/[A-z0-9-_]+\//.test(video)
                        ||
                        /^http:\/\/video\.sina\.com\.cn\/v\/b\/\d+-\d+\.html$/.test(video)
                    )
                ){
                    error = '请输入优酷/土豆/新浪视频网址 , <a href="http://help.42qu.com/po_video.html" target="_blank">点此看帮助</a>';
                }
            }else{
                error = "请输入视频网址"
            }
            if(error){
               e.focus().select()
            }
            return error 
        }
    )
}

po_photo = function(id){
    po_(
        id,
        'photo',
        '图片',
        '<input id="po_photo" type="file" name="photo">',
        function(){
            var error,
                photo=$("#po_photo").val();
                        
                if(photo&&photo.length){
                    if(!/\.(jpg|png|bmp|gif|jpeg)$/.test(photo.toLowerCase())){
                        error = "照片格式有误(仅支持JPG,JPEG,GIF,PNG或BMP)"
                    }
                }else{
                    error = "请选择图片"
                }
            return error
        }
    )
}

po_audio = function(id){
    po_(
        id,
        'audio',
        '声音',
        '<input id="po_audio" type="file" name="audio">',
        function(){
            var error,
                audio=$("#po_audio").val();
                if(audio&&audio.length){
                    if(!/\.(mp3)$/.test(audio.toLowerCase())){
                        error = "仅支持mp3"
                    }
                }else{
                    error = "请选择mp3文件"
                }
            return error
        }
    )
}

po_rec= function(id) {
	var fancybox = $.fancybox;
	fancybox({
        content: '<form id="vote_reply" class="fancyreply"><h3>推荐语</h3><textarea name="txt" style="height:140px" class="txt_ar"></textarea><div class="btns"><span class="rec_tip share_sync"></span><span class="btnw"><button class="btn" type="submit">修改</button></span><span class="syncp"><a href="/po/rm/'+id +'?_xsrf=+'+ $.cookie.get("_xsrf")
+ '">删除</a></span></div></form>',
		onComplete: function() {
			var reply = $("#vote_reply"),
			textarea = reply.find("textarea"),
            text= $(".prebody pre p").text();
            textarea.focus().text(text);
            tip = $('.rec_tip');
            can_say = txt_maxlen(textarea, tip, 142);
			reply.submit(function() {
				var txt = $.trim(textarea.val());
                if(can_say()){
				fancybox.showActivity()
				$.postJSON("/po/rec/" + id, {
					'txt': txt
				},
				function(r) {
                    fancybox.close();
                    location.reload(true);
				})}else{
                    tip.fadeOut(function(){tip.fadeIn()})
                    return false
                }
				return false;
			})
			textarea.focus()
		}
	})
}

})()

 
// Set desired tab- defaults to four space softtab
var tab = "    ";
       
function insertTab(evt) {
    var t = evt.target;
    var ss = t.selectionStart;
    var se = t.selectionEnd;
 
    // Tab key - insert tab expansion
    if (evt.keyCode == 9) {
        evt.preventDefault();
               
        // Special case of multi line selection
        if (ss != se && t.value.slice(ss,se).indexOf("n") != -1) {
            // In case selection was not of entire lines (e.g. selection begins in the middle of a line)
            // we ought to tab at the beginning as well as at the start of every following line.
            var pre = t.value.slice(0,ss);
            var sel = t.value.slice(ss,se).replace(/n/g,"n"+tab);
            var post = t.value.slice(se,t.value.length);
            t.value = pre.concat(tab).concat(sel).concat(post);
                   
            t.selectionStart = ss + tab.length;
            t.selectionEnd = se + tab.length;
        }
               
        // "Normal" case (no selection or selection on one line only)
        else {
            t.value = t.value.slice(0,ss).concat(tab).concat(t.value.slice(ss,t.value.length));
            if (ss == se) {
                t.selectionStart = t.selectionEnd = ss + tab.length;
            }
            else {
                t.selectionStart = ss + tab.length;
                t.selectionEnd = se + tab.length;
            }
        }
    }
           
    // Backspace key - delete preceding tab expansion, if exists
   else if (evt.keyCode==8 && t.value.slice(ss - 4,ss) == tab) {
        evt.preventDefault();
               
        t.value = t.value.slice(0,ss - 4).concat(t.value.slice(ss,t.value.length));
        t.selectionStart = t.selectionEnd = ss - tab.length;
    }
           
    // Delete key - delete following tab expansion, if exists
    else if (evt.keyCode==46 && t.value.slice(se,se + 4) == tab) {
        evt.preventDefault();
             
        t.value = t.value.slice(0,ss).concat(t.value.slice(ss + 4,t.value.length));
        t.selectionStart = t.selectionEnd = ss;
    }
    // Left/right arrow keys - move across the tab in one go
    else if (evt.keyCode == 37 && t.value.slice(ss - 4,ss) == tab) {
        evt.preventDefault();
        t.selectionStart = t.selectionEnd = ss - 4;
    }
    else if (evt.keyCode == 39 && t.value.slice(ss,ss + 4) == tab) {
        evt.preventDefault();
        t.selectionStart = t.selectionEnd = ss + 4;
    }
}
 


