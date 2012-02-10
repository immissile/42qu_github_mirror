$(function(){
    $("#tags").tokenInput("http://api"+HOST_SUFFIX+"/po/tag",
        {
            theme: "42qu",
            onResult: function (results) {
                var list = [],i=0,t,ctrl=true
                var word = $('#token-input-tags').val()
                for(;i<results.length;++i){
                    t = results[i]
                    list.push({
                        id:t[0],
                        name:t[2],
                        num:t[1]
                    })
                    if(t[2]==word){
                        ctrl = false
                    }
                }
                if(ctrl)list.unshift({id:'-'+word,name:word,num:0})
                return list
            },
            propertyToSearch: "name",
            resultsFormatter: function(item){
                if(String(item.id).substring(0,1)=='-'){
                    return '<li class="dropdown_add">添加 "'+item.name+'" 标签</li>'
                }
                return '<li>'+item.name+'<span class="drop_follow_num">'+item.num+'人关注</span></li>'
            },
            tokenFormatter: function(item){
                 return '<li class="token-input-token-42qu"><p>'+item.name+'</p></li>'+'<input type="hidden" name="tag_id_list" value='+item.id+' />' 
            }

        })
    var arr = JSON.parse( $('#site_data').text()).tags
    if(arr.length>0){
        for(var i=0;i<arr.length;i++){
            $('#tags').tokenInput("add", {id: arr[i][1], name: arr[i][0]});
        }
    }
});

