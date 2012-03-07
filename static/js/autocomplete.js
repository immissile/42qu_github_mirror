function autocomplete_tag(id, default_tag_list, only_search, idPrefix){
    //only_search = (typeof(only_search)=="undefined")?0:only_search
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
                if(ctrl && !only_search)list.unshift({id:'-'+word,name:$('#token-input-'+id.substring(1)).val(),num:0})
                return list
            },
            hintText:only_search?null:'',
            propertyToSearch: "name",
            onAdd: function (item) {
                if(only_search){
                    window.location.href = 
                }
            },
            resultsFormatter: function(item){
                if(String(item.id).substring(0,1)=='-'){
                    return '<li class="dropdown_add">添加 '+$('#token-input-'+id.substring(1)).val()+' 标签</li>'
                }
                var num = item.num-0, ctxt;
                switch(item.cid){
                    case 0:
                        ctxt = '个回答'
                        break
                    case 1:
                        ctxt = '人关注'
                        break
                    case 2:
                        ctxt = '个粉丝'
                        break
                }
                var s=[
                    '<li>',item.name
                ]
                if(num){
                    s.push( 
                        '<span class="drop_follow_num">' + item.num + ctxt + '</span>'
                    )
                }
                s.push('</li>')
                return s.join('') 
            },
            tokenFormatter: function(item){
                 return '<li class="token-input-token"><p>'+item.name+'</p>'+'<input type="hidden" name="tag_id_list" value="'+item.id+'"></li>' 
            },
            animateDropdown: false
        }
    if(idPrefix){
        o.idPrefix = idPrefix
    }
    elem.tokenInput("http://api"+HOST_SUFFIX+"/tag",o)
    
    if(default_tag_list.length){
        for(i=0;i<default_tag_list.length;++i){
            t=default_tag_list[i]
            elem.tokenInput("add", {id: t[1], name: t[0]});
        }
    }
}

function autocomplete_tag_hero(id){
    var elem=$(id), t, i, 
        o = {
            onResult: function (results) {
                var list = [],
                    i=0; 
                for(;i<results.length;++i){
                    t = results[i]
                    for(var j=0;j<t[1].length;++j){
                        var item = t[1][j]
                        list.push({
                            id:item[0],
                            name:item[2],
                            num:Number(item[1]),
                            alias:item[3],
                            cid:t[0]
                        })
                    }
                }
                return list
            },
            hintText:'',
            propertyToSearch: "name",
            onAdd: function (item) {
                elem.tokenInput("clear")
                //TODO 关键词, 注意urlencode
                window.location.href = '//' + HOST
            },
            resultsFormatter: function(item){
                var num = item.num-0, ctxt, alias=item.alias;
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
                        '<span class="drop_item_alias">'+$('<p>').text(alias).html()+"</span>"
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
                    s = find_value_and_highlight_term(s,alias,$('#token-input-search').val())
                }
                return s
            },
            animateDropdown: false
        }
    elem.tokenInput("http://api"+HOST_SUFFIX+"/tip",o)
}

function find_value_and_highlight_term(template, value, term) {
        return template.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + RegExp.escape(value) + ")(?![^<>]*>)(?![^&;]+;)", "g"), highlight_term(value, term));
    }

function highlight_term(value, term) {
        return value.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + RegExp.escape(term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<b>$1</b>");
    }
 

function token_search_decoration(){
    function show_placeholder(){
        if(!$('#token-input-search').val().length>0){
            $('.token-input-list').hide()
            $('#search').show()
            $('#token-input-search').unbind('blur')
        }
        if(document.activeElement.id!='token-input-search'){
            $('.token-input-dropdown').hide()
        }
    }
    function show_token_input(){
        $('#token-input-search').focus().blur(show_placeholder).focus(function(){
            if($('#token-input-search').val().length>0)
            $('.token-input-dropdown').show()}
        )
    }
    show_placeholder()
    $('#search').bind('click',function(){
        $(".token-input-list").show()
        $(this).hide()
        if(navigator.userAgent.indexOf("MSIE")>0) { 
            setTimeout(show_token_input,10)
        }else{
            show_token_input()
        }
    })
    $('#token-input-search').focus(function(){
        $(this).css('color','#000')
    }).blur(function(){
        $(this).css('color','#999')
    })
}

