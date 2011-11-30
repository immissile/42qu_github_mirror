function school_college(id,dep_id){
    $('#'+id).click(pop_school)
    select_univ = function(uid,uname){
        $.fancybox.showActivity()
        $.getScript("http://realfex.com/"+uid+".js",function(){
            $('#'+id).val(uname)
            var deps = depList['deps']
            $('#univ_id'+dep_id.substr(3)).val(uid)
            var dep_node = $('#'+dep_id)
            dep_node.children().remove()
            dep_node.append('<option value="">选择院系</option>')
            for(var i=0;i<deps.length;i++){
                dep_node.append('<option value='+deps[i]['id']+'>'+deps[i]['name']+'</option>')
            }
            $.fancybox.close()
        });
    }
}
function pop_school(){
    var fancybox = $.fancybox
    fancybox({
        content:'<div class="school_wrap"><div class="couns">'+get_couns()+'</div><div class="provs">'+get_provs(0)+'</div><div class="search_univ">搜索 <input type="text" id="univ_txt"></div>'+'<div class="univs">'+get_univ_by_prov(0,0)+'</div></div>'
    })
    $('#prov_0').addClass('prov_now')
    $('#coun_0').addClass('coun_now')
    var txt = $('#univ_txt')
    var univs_node = $('.univs')
    txt.keyup(function(){
        var key = txt.val()
        if(key==''){
            var cid = $('.coun_now').attr('id').substr(5)
            if($('.prov_now')[0]){
                var pid = $('.prov_now').attr('id').substr(5)
                select_prov(cid,pid)
            } else{
                select_coun(cid)
            }
        } else{
            univs_node.find('.univ').each(function(){
                var self = $(this)
                if(self.html().indexOf(key)<0){
                    self.parent().hide()
                }else{
                    self.parent().show()
                }
            })
        }
    })
}
function get_couns(){
    var cont = '<ul class="coun_ul">'
    var sort = [0,7,6,5,1,2,8,4,3]
    for(var j=0;j<9;j++){
        var i = sort[j]
        cont += '<li class="coun_li"><a class="coun" id="coun_'+i+'" href="javascript:select_coun('+i+');void(0)">'+allUnivList[i]['name']+'</a></li>'
    }
    for(var i=9;i<allUnivList.length;i++){
        cont += '<li class="coun_li"><a class="coun" id="coun_'+i+'" href="javascript:select_coun('+i+');void(0)">'+allUnivList[i]['name']+'</a></li>'
    }
    return cont+'</ul>'
}
function get_provs(cid){
    var provs = allUnivList[cid]['provs']
    var cont = '<ul class="prov_ul">'
    if(provs.length>0){
        for(var i=0;i<provs.length;i++){
            var pid = (parseInt(provs[i]['id'])-1)
            cont += '<li class="prov_li"><a class="prov" id="prov_'+pid+'"href="javascript:select_prov('+cid+','+pid+');void(0)">'+provs[i]['name']+'</a></li>'
        }
    }
    return cont+'</ul>'
}
select_coun = function(cid){
    $('.coun_now').removeClass('coun_now')
    $('#coun_'+cid).addClass('coun_now')
    var provs = get_provs(cid)
    var univs = ''
    $('.provs').html(provs)
    $('.prov_now').removeClass('prov_now')
    $('#prov_0').addClass('prov_now')
    if(provs!='<ul class="prov_ul"></ul>'){
        univs = get_univ_by_prov(cid,0)
    } else{
        univs = get_univ_by_coun(cid)
    }
    $('.univs').html(univs)
}
select_prov = function(cid,pid){
    $('.prov_now').removeClass('prov_now')
    $('#prov_'+pid).addClass('prov_now')
    var univs = get_univ_by_prov(cid,pid)
    $('.univs').html(univs)
}

function get_univ_by_coun(cid){
    var univs = allUnivList[cid]['univs']
    return get_univs(univs)
}
function get_univ_by_prov(cid,pid){
    var univs = allUnivList[cid]['provs'][pid]['univs']
    return get_univs(univs)
}
function get_univs(univs){
    var cont = '<ul class="univ_ul">'
    for(var i=0;i<univs.length;i++){
        cont += '<li class="univ_li"><a class="univ" id="univ_'+univs[i]['id']+'" href="javascript:select_univ('+univs[i]['id']+",'"+univs[i]['name']+"');void(0)\">"+univs[i]['name']+'</a></li>'
    }
    return cont+'</ul>'
}
