function autocomplete_tag(id, default_tag_list, idPrefix){
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
                if(ctrl)list.unshift({id:'-'+word,name:word,num:0})
                return list
            },
            propertyToSearch: "name",
            resultsFormatter: function(item){
                if(String(item.id).substring(0,1)=='-'){
                    return '<li class="dropdown_add">添加 '+$('#token-input-tag_id_list').val()+' 标签</li>'
                }
                var num = item.num-0;
                var s=[
                    '<li>',item.name
                ]
                if(num){
                    s.push( 
                        '<span class="drop_follow_num">'+item.num+'人关注</span>'
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
