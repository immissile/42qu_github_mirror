var select_id, dep_id
select_univ = function(uid,uname){
    $('#'+select_id).val(uname).css({'color':'',border:''})
    var deps = SCHOOL_UNIVERSITY_DEPARTMENT_ID[parseInt(uid)] || [];
    $('#school_id'+dep_id.substr(3)).val(uid).trigger('change')
    var dep_node = $('#'+dep_id)
    dep_node.children().remove()
    dep_node.append('<option value="">选择院系</option>')
    for(var j=0;j<deps.length;j++){
        var i=deps[j]
        dep_node.append('<option value="'+i+'">'+SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[i]+'</option>')
    }
    dep_node.append('<option value="0">其它院系</option>')
    $.fancybox.close()
}

function pop_school(){
    var self=$(this).blur()
    select_id = self.attr('id')
    dep_id = self.attr('id').replace('school_select','dep')
    var fancybox = $.fancybox
    fancybox({
        content:'<div class="school_wrap"><div class="couns">'+get_couns()+'</div><div class="provs">'+get_provs(0)+'</div><div class="search_univ">搜索 <input type="text" id="univ_txt"></div>'+'<div class="univs">'+get_univ_by_prov(0,0)+'</div></div>'
    })

    $("#univ_txt").focus()
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
    if(!provs)return;
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
    var univs, 
        provs = get_provs(cid)
    if(provs){
        $('.provs').html(provs).show()
        univs = get_univ_by_prov(cid,0)
    }else{
        $('.provs').hide()
        univs = get_univ_by_coun(cid)
    }
    $('.prov_now').removeClass('prov_now')
    $('#prov_0').addClass('prov_now')
    $('.univs').html(univs)
    $("#univ_txt").focus().val('')
}
select_prov = function(cid,pid){
    $('.prov_now').removeClass('prov_now')
    $('#prov_'+pid).addClass('prov_now')
    var univs = get_univ_by_prov(cid,pid)
    $('.univs').html(univs)
    $("#univ_txt").focus().val('')
}

function get_univ_by_coun(cid){
    var univs = allUnivList[cid]['univs']
    return get_univs(univs)
}
function get_univ_by_prov(cid,pid){
    var univs = allUnivList[cid]['provs']
    if(univs){
        return get_univs(univs[pid]['univs'])
    }
}


function get_univs(univs){
    var cont = '<ul class="univ_ul">'
    for(var i=0;i<univs.length;i++){
        cont += '<li class="univ_li"><a class="univ" id="univ_'+univs[i]['id']+'" href="javascript:select_univ('+univs[i]['id']+",'"+univs[i]['name']+"');void(0)\">"+univs[i]['name']+'</a></li>'
    }
    return cont+'</ul>'
}
function school(div){
     var tmpl = $('#school_tmpl').tmpl().appendTo(div),
        year=(new Date()).getFullYear(),r =['<option value="">入学年份</option>'],i, uid=uuid()
        ;

        tmpl.find(".school_id").attr("id","school_id"+uid)
        tmpl.find(".school_department").attr("id","dep"+uid)
        tmpl.find(".school").focus(function(){
            this.blur()
        }).attr('id',"school_select"+uid).focus(pop_school).css({
            'color':"#999",
            "border-color":"#aaa",
        })
        for(i=year;i+128>year;--i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        tmpl.find(".school_year").html(r.join(''))
        div.find(".rm").show();
        div.find(".rm:last").hide(); 
        tmpl.find('.rm').click(function(){
            tmpl.fadeOut(function(){
                tmpl.remove()
            })
            if(id){
                $.postJSON("/j/school/rm/"+id);
            }
        });
}
