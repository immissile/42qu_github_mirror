function find_value_and_highlight_term(template, value, term) {
        return template.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + RegExp.escape(value) + ")(?![^<>]*>)(?![^&;]+;)", "g"), highlight_term(value, term));
    }

function highlight_term(value, term) {
        return value.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + RegExp.escape(term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<b>$1</b>");
}
 
function add_prefix(idPrefix){
   return {
        tokenList: idPrefix+"-list",
        token: idPrefix+"-token",
        tokenDelete: idPrefix+"-delete-token",
        selectedToken: idPrefix+"-selected-token",
        highlightedToken: idPrefix+"-highlighted-token",
        dropdown: idPrefix+"-dropdown",
        dropdownItem: idPrefix+"-dropdown-item",
        dropdownItem2: idPrefix+"-dropdown-item2",
        selectedDropdownItem: idPrefix+"-selected-dropdown-item",
        inputToken: idPrefix+"-input-token"
    } 
}

function autocomplete_tag(id, default_tag_list, idPrefix){
    idPrefix = idPrefix || "token-input"
    var elem=$(id), t, i, 
        o = {
            onResult: function (results, word) {
                var list = [],
                    i=0, 
                    ctrl=1;
                for(;i<results.length;++i){
                    t = results[i]
                    t = {
                        id:t[0],
                        name:t[2],
                        num:t[1]
                    }
                    if(t.name == word){
                        ctrl = 0 
                        list.unshift(t)
                    }else{
                        list.push(t)
                    }
                }
                if(ctrl)list.unshift({id:'-'+word,name:$('#token-input-'+id.substring(1)).val(),num:0})
                return list
            },
            hintText:'',
            propertyToSearch: "name",
            resultsFormatter: function(item){
                if(String(item.id).substring(0,1)=='-'){
                    return '<li class="dropdown_add">添加 '+htmlescape($('#token-input-'+id.substring(1)).val())+' 标签</li>'
                }
                var num = item.num-0,
                s=[
                    '<li>',item.name
                ]
                if(num){
                    s.push( 
                        '<span class="drop_follow_num">' + item.num + '人关注</span>'
                    )
                }
                s.push('</li>')
                return s.join('') 
            },
            tokenFormatter: function(item){
                 return '<li class="'+idPrefix+'-token"><p>'+htmlescape(item.name)+'&#8204;</p>'+'<input type="hidden" name="tag_id_list" value="'+item.id+'"></li>' 
            },
            animateDropdown: false
        }

    if(idPrefix){
        o.classes=add_prefix(idPrefix)
    }

    elem.tokenInput("http://api"+HOST_SUFFIX+"/tag",o) 
    if(default_tag_list.length){
        for(i=0;i<default_tag_list.length;++i){
            t=default_tag_list[i]
            elem.tokenInput("add", {id: t[1], name: t[0]});
        }
    }
}
function autocomplete_tag_hero(id,idPrefix){
    idPrefix = idPrefix||'token-input'
    var elem=$(id), t, i,
        input,
        o = {
            onReady: function(){
                input = $('#'+idPrefix+'-'+id.substring(1))
                elem.parents('form').submit(function(){
                    elem.val(input.val())
                })
            },
            onResult: function (results,word) {
                var list = [],
                    i=0,
                    ctrl=1; 
                for(;i<results.length;++i){
                    t = results[i]
                    for(var j=0;j<t[1].length;++j){
                        var item = t[1][j]
                        if(word==item[2])ctrl=0;
                        list.push({
                            id:item[0],
                            name:item[2],
                            num:Number(item[1]),
                            alias:item[3],
                            cid:t[0]
                        })
                    }
                }
                if(ctrl)list.unshift({id:0,name:input.val(),num:0,alias:'',cid:0})
                return list
            },
            hintText:'',
            propertyToSearch: "name",
            onAdd: function (item) {
                var href; 
                elem.tokenInput("clear")
                if(item.id==0){
                    href = '/q?q='+encodeURIComponent(item.name)
                }else{
                    href = '//' + item.id + HOST_SUFFIX
                }
                location.href = href 
            },
            resultsFormatter: function(item){
                var num = item.num-0, ctxt, alias=item.alias;
                if(item.id===0){
                    return '<li class="dropdown_add">搜索 '+htmlescape(input.val())+'</li>'
                }

                switch(item.cid){
                    case 1: 
                        ctxt = '个粉丝'
                        style = 'search_hero_li'
                        break
                    case 6:
                        ctxt = '人关注'
                        style = 'search_tag_li'
                        break
               }
                var s=[
                    '<li class="' + style + '">',item.name
                ]
                if(alias){
                    s.push(
                        '<span class="drop_item_alias">'+htmlescape(alias)+"</span>"
                    )
                }
                if(num){
                    s.push( 
                        '<span class="drop_follow_num">' + item.num + ctxt + '</span>'
                    )
                }
                s.push('</li>')
                s = s.join('')
                if(alias){
                    s = find_value_and_highlight_term(s,alias,input.val())
                }
                return s
            },
            animateDropdown: false
        }
    if(idPrefix){
        o.classes=add_prefix(idPrefix)
    }
    elem.tokenInput("http://api"+HOST_SUFFIX+"/tip",o)

    function token_search_decoration(){
        function show_placeholder(){
            if(!input.val().length>0){
                $('.'+idPrefix+'-list').hide()
                elem.show()
                input.unbind('blur')
            }
            if(document.activeElement.id!=idPrefix+'-search'){
                $('.'+idPrefix+'-dropdown').hide()
            }
        }
        function show_token_input(){
            input.focus().blur(show_placeholder).focus(function(){
                if(input.val().length>0)
                $('.'+idPrefix+'-dropdown').show()}
            )
        }
        show_placeholder()
        elem.bind('click',function(){
            $('.'+idPrefix+'-list').show()
            $(this).hide()
            if(navigator.userAgent.indexOf("MSIE")>0) { 
                setTimeout(show_token_input,10)
            }else{
                show_token_input()
            }
        })
        input.focus(function(){
            $(this).css('color','#000')
        }).blur(function(){
            $(this).css('color','#999')
        })
    }
    token_search_decoration()
}


