(function ($) {  
var pre,
at_size,at_list

methods={
    getCarePos: function (node, con) {
        var size = [node.offsetWidth, node.offsetHeight],
            dot = $('<em>&nbsp;</em>'),
            node = $(node),
            nodePos = node.offset(),
            pos = {};

        if (!pre) {
            pre = $('<pre></pre>').
                css(this.initPreStyle(node));
            pre.appendTo('body');
        }
        pre.html(con).append(dot);
        pos = dot.position();

        return {
            left: pos.left + nodePos.left + 2,
            top: pos.top + nodePos.top + 21
        };
    },
    initPreStyle:  function (node) {
        return {
            position: 'absolute',
            left: -9999,
            width: node.width() + 'px',
            padding: '8px',
            font: '14px/20px "Helvetica Neue", Helvetica, Arial',
            'word-wrap': 'break-word',
            border: '1px'
        }
    },
    getCursorPosition: function (t) {
       if (document.selection) {
            t.focus();

            var ds = document.selection,
                range = ds.createRange(),
                storedRange = range.duplicate();

            storedRange.moveToElementText(t);
            storedRange.setEndPoint('EndToEnd', range);
            t.selectionStart = storedRange.text.length - range.text.length;
            t.selectionEnd = t.selectionStart + range.text.length;

            return t.selectionStart;
        } else {
            return t.selectionStart;
        }
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
            val = t.value

        // reset value  
         t.value = val.slice(0,p-n)
        // reset cursor
        this.setCursorPosition(t, p - (n < 0 ? 0 : n));
        // for firefox
        firefox = $.browser.mozilla && setTimeout(function () {
            if (t.scrollTop !== s) {
                t.scrollTop = s;
            }
        }, 10);
    },

    insertAfterCursor: function (t, str) {
        var val = t.value,
            self = this; 
                
        // for IE
        if (document.selection) {
            t.focus();
            document.selection.createRange().text = str + ' ';  

           
        } else {
            var obj=t;
            obj.focus();
            if (document.selection) {
                setCursorPosition(obj,pos);
                var sel = document.selection.createRange();
                sel.text = str;
            } else if (typeof obj.selectionStart == 'number' && typeof obj.selectionEnd == 'number') {
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
        };
    },

    moveSelectedItem: function (step) {
        var list = $('#at_list');
        var ats = list.children();
        var onId = list.find('.on').index();
        if (!at_size) { return; }

        onId += step;

        if (onId >= at_size) {
          onId -= at_size;
        }
        if (onId < 0) {
          onId += at_size;
        }
        ats.removeClass('on');
        $(ats[onId]).addClass('on')
    }
};
 

$.fn.pop_at = function(){
    atComplete = function(t,w){
        var onli = $('#at_list').find($('.on'))
        name = onli.find($('.at_name')).text()
        id = onli.find($('.at_name')).attr('id')
        methods.deleteRangeText(t, w.length);
        methods.insertAfterCursor(t,name+'('+id+') ');
        $('#at_list').remove()
    }
    this.bind('keyup',function(e){
        at_list,at_size
        var self = $(this)
        offset = methods.getCursorPosition(self[0])
        var val = self.val()
        lastCharAt = val.substring(0, offset).lastIndexOf('@')
        hasSpace = val.substring(lastCharAt, offset).indexOf(' ')
        if(lastCharAt>=0 && hasSpace<0){
            wordsForSearch = val.substring(lastCharAt + 1, offset);
            var keys = new Array(38,40,13,16,9)
            if($.inArray(e.keyCode,keys)<0){
                $.postJSON(
                    "/j/at/",
                    function(data){
                        html = '<div class="at_list" id="at_list">'
                        if(data.length<0){
                            return;
                        }else{
                        for(i=0;i<data.length;i++){
                            t=data[i]
                            html += '<div class="at_li"><img class="at_img L" src="'+t[3]+'"><span class="at_name" id="'+t[2]+'">'+t[0]+'</span><span class="at_title">'+t[1]+'</span></div>'
                        }}
                        at_list = html+'</div>'
                        at_size = data.length
                    }
                )
                $('#at_list').remove()
                pos = methods.getCarePos(self,val.substring(0,lastCharAt))
                $('body').append(at_list)
                $('#at_list').css(pos)
                $('.at_li').mouseover(function(){$('.at_li').removeClass('on');$(this).addClass('on')})
                $('.at_li').click(function(){atComplete(self[0],wordsForSearch)})
                $("body:not(:.at_li)").click(function(){$('#at_list').remove()})
            }
        } else{$('#at_list').remove()}
    }).bind('keydown',function(e){
        if ($('#at_list')[0]) { 
        switch (e.keyCode) {
            // space
            case 32:
            $('#at_list').remove();
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
}
})(jQuery);
