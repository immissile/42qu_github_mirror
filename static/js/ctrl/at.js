

function htmlescape(escaped){
    return escaped.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
}

(function ($) {  
var pre, pre0,at_size, at_list , wordsForSearch, req=0, space_at =/\s+@/, ieselect; 

methods={

    getCarePos: function (node, con, line_height) {
        var size = [node.offsetWidth, node.offsetHeight],
            dot = $('<em>&nbsp;</em>'),
            node = $(node),
            nodePos = node.offset(),
            pos = {};

        if (!pre) {
            pre = $('<pre></pre>').css(this.initPreStyle(node));
            pre.appendTo('body');
            pre0 = pre[0]
        }
        con = htmlescape(con)
        if(pre0.outerHTML){
            con=con.replace(/\r\n/g,"\n").replace(/\n/g,"<br>")
        }
        pre.html(con);
        pre.height(node.height())
        pre.append(dot);
        pos = dot.position();
        if(node.scrollTop()>0){
            pos.top -= node.scrollTop()
        }
        return {
            left: pos.left + nodePos.left + 2,
            top: pos.top + nodePos.top + line_height
        };
    },
    initPreStyle:  function (node) {
        return {
            position: 'absolute',
            left: -9999,
            width: node.width() + 'px',
            padding: '0 4px',
            font: '14px/26px Segoe UI,Tahoma,Verdana,Arial,Helvetica,sans-serif',
            'word-wrap': 'break-word',
            border: '1px',
            overflow: 'auto'
        }
    },
    getCursorPosition: function (t) {
       if(ieselect===undefined){
            ieselect = !t.selectionStart && document.selection
       }
       if (ieselect) {
            t.focus();
            var ds = document.selection,
                range = ds.createRange(),
                storedRange = range.duplicate();
            storedRange.moveToElementText(t);
            storedRange.setEndPoint('EndToEnd', range);
            t.selectionStart = storedRange.text.length - range.text.length;
            t.selectionEnd = t.selectionStart + range.text.length;
            return t.selectionStart;
        } 
        return t.selectionStart;
    },
    setCursorPosition: function (t, p) {
        this.selectRangeText(t, p, p);
    },

    selectRangeText: function (t, s, z) {
        if (document.selection) {
            var range = t.createTextRange();

            range.moveEnd('character', -t.value.length);
            range.moveEnd('character', z);
            range.moveStart('character', s);
            range.select();

        } else {
            t.setSelectionRange(s,z);
            t.focus();
        }
    },
    deleteRangeText: function (t, n) {
        var p = this.getCursorPosition(t),
            s = t.scrollTop,
            val = t.value,
            d,
            l=val.length;
        if(n>=l){
            n=l
        }
        d=p-n;
        // reset value  
        t.value = n > 0 ? val.slice(0, d) + val.slice(p): val.slice(0, p) + val.slice(d);

        // reset cursor
        this.setCursorPosition(t, p - (n < 0 ? 0 : n));
        // for firefox
        firefox = $.browser.mozilla && setTimeout(function () {
            if (t.scrollTop !== s) {
                t.scrollTop = s;
            }
        }, 10)
 
        return val.slice(p , d);
    },

    insertAfterCursor: function (t, str) {
        var val = t.value,
            self = this, 
            obj=t;
            obj.focus();    
        // for IE
        if (document.selection) {            
            document.selection.createRange().text = str
        } else if(typeof obj.selectionStart == 'number' && typeof obj.selectionEnd == 'number') {
            var startPos = obj.selectionStart,
                endPos = obj.selectionEnd,
                cursorPos = startPos,
                tmpStr = obj.value;
                obj.value = tmpStr.substring(0, startPos) + str + tmpStr.substring(endPos, tmpStr.length);
                cursorPos += str.length;
            //obj.selectionStart = obj.selectionEnd = cursorPos;
        } else {
            obj.value += str;
        }    
    },

    moveSelectedItem: function (step) {
        var list = $('#at_list');
        var ats = list.children();
        var onId = list.find('.at_on').index();
        if (!at_size) { return; }

        onId += step;

        if (onId >= at_size) {
          onId -= at_size;
        }
        if (onId < 0) {
          onId += at_size;
        }
        ats.removeClass('at_on');
        $(ats[onId]).addClass('at_on')
    }
};
 


$.fn.pop_at = function(url, line_height){
    if(!islogin())return this;
    line_height = line_height||21

    atComplete = function(t,w){
        var onli = $('#at_list').find($('.at_on')),
            name = onli.find($('.at_name')).text(),
            v=methods.deleteRangeText(t, w.length+1);
        
        methods.insertAfterCursor(t,$.trim(v.charAt(0))+" @"+name+" ");
        
        t.value= t.value.replace(space_at," @")
        $('#at_list').remove()
    }

    function at_list_remove(){
        $('#at_list').remove()
    }
    function at_tip_remove(){
        $('.at_tip').remove()
    }

    $("body").click(function(){
        at_list_remove();at_tip_remove()
    })
    this.bind('keyup',function(e){
        var self = $(this),
            offset = methods.getCursorPosition(self[0]),
            val = self.val(),
            lastCharAt = val.substring(0, offset).lastIndexOf('@'),
            hasSpace=1, tipword;
        at_tip_remove()
        if(lastCharAt>=0){
            tipword = val.substring(lastCharAt, offset)
            hasSpace = Math.max(tipword.indexOf(' '),tipword.indexOf("\n"));
        }
        if(hasSpace<0){
            pos = methods.getCarePos(self,val.substring(0,lastCharAt),line_height)
            if(offset>0 && lastCharAt==offset-1){
                
                at_list_remove()
                $('body').append('<div class="at_tip">@ 我关注的人 ...</div>')
                $('.at_tip').css(pos)
                return;
            }else{
                at_tip_remove()
            }
            wordsForSearch = val.substring(lastCharAt + 1, offset);
            req+=1;
            var keys = [38,40,13,16,9], myreq=req;
            if($.inArray(e.keyCode,keys)<0){
               $.ajax(
                    "//api"+HOST_SUFFIX+url,
                    {
                        cache:true,
                        dataType:"jsonp",
                        data:{
                            "q":$.trim(wordsForSearch)
                        },
                        success: function(data){
                            if(myreq!=req)return;
                            at_list = $('<div class="at_list" id="at_list"/>')
                            if(data.length<=0){
                                return;
                            }
                            for(var i=0;i<data.length;i++){
                                t=data[i]
                                var html = $('<div class="at_li"><img class="at_img L"  src="'+t[3]+'"><div class="L"><span class="at_name"></span><span class="at_title"></span></div></div>')
                                html.find(".at_name").text(t[0]+"("+t[2]+")")
                                html.find(".at_title").text(t[1])
                                at_list.append(html)
                            }
                            at_size = data.length;
                            $('body').append(at_list)
                            at_list.css(pos)
                            at_list.find('.at_li:first').addClass('at_on')
                            $('.at_li').click(function(){atComplete(self[0],wordsForSearch)}).mouseover(function(){$('.at_li').removeClass('at_on');$(this).addClass('at_on')})
                        }
                    }
                )
                            
                at_list_remove()
            }
        } else{
            at_list_remove()
        }
    }).bind('keydown',function(e){
        if ($('#at_list')[0]) { 
        switch (e.keyCode) {
            // space
            case 32:
            at_list_remove()
            break;

            // up
            case 38:
            e.preventDefault();
            methods.moveSelectedItem(-1);
            break;

            // down
            case 40:
            e.preventDefault();
            methods.moveSelectedItem(1);
            break;

            // enter
            case 13:
            e.preventDefault();
            atComplete($(this)[0],wordsForSearch)
            break;

            default:
            break;
        }
    }
    })
    return this
}
})(jQuery);


