var select_id, dep_id
function select_univ(uid){
    var select = $('#'+select_id).val(SCHOOL_UNIVERSITY[uid])
    if(!IE6){
        select.css({'color':'',border:'1px solid #ccc'})
    }
    $('#school_id'+dep_id.substr(3)).val(uid).trigger('change')
    school_department($('#'+dep_id), uid)
    $.fancybox.close()
}

function school_department(dep_node, uid){
    var deps = SCHOOL_UNIVERSITY_DEPARTMENT_ID[parseInt(uid)] || [];
    dep_node.children().remove()
    dep_node.append('<option value="0">选择院系</option>')
    for(var j=0;j<deps.length;j++){
        var i=deps[j]
        dep_node.append('<option value="'+i+'">'+SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[i]+'</option>')
    }
    dep_node.append('<option value="">其它院系</option>')
}


function pop_school(){
    var school_name_builder = function(name){
        return name.replace('大学', '大').replace('科学技术', '科').replace('中国', '中').replace('师范', '师').replace('科技', '科').replace('交通', '交').replace('财经', '财').replace('工业', '工').replace('北京', '北').replace('科学', '科').replace('农业', '农')
    }
    var self=$(this).blur()
    select_id = self.attr('id')
    dep_id = self.attr('id').replace('school_select','dep')
    var fancybox = $.fancybox
    fancybox({
        content:'<div class="school_wrap"><div class="couns">'+get_couns()+'</div><div class="provs">'+get_provs(0)+'</div><div class="search_univ">搜索 <input type="text" id="univ_txt"></div>'+'<div class="univs">'+get_univ_by_prov(0,0)+'</div></div>',
        overlayShow:false // fuck for ie6  , ctrl/i/guide
    })

    $("#univ_txt").focus()
    $('#prov_0').addClass('prov_now')
    $('#coun_0').addClass('coun_now')
    var txt = $('#univ_txt')
    var univs_node = $('.univs')
    txt.keyup(function(){
        var key = school_name_builder(txt.val())
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
                if(school_name_builder(self.html()).indexOf(key)<0){
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
    var sort = [0,7,6,5,1,11,2,8,4,3]
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
        cont += '<li class="univ_li"><a class="univ" id="univ_'+univs[i]['id']+'" href="javascript:select_univ('+univs[i]['id']+");void(0)\">"+univs[i]['name']+'</a></li>'
    }
    return cont+'</ul>'
}
function school(div,data){
     var tmpl = $('#school_tmpl').tmpl(data).appendTo(div),
        year=(new Date()).getFullYear(),
        r =['<option value="">开始时间</option>'],i, uid=uuid()
        sc=tmpl.find(".school"),
        dep_node = tmpl.find(".school_department").attr("id","dep"+uid)
        ;
        tmpl.find(".school_id").attr("id","school_id"+uid)
        sc.focus(function(){
            this.blur()
        }).attr('id',"school_select"+uid).focus(pop_school)

        for(i=year;i+128>year;--i){
            r.push('<option value="'+i+'">'+i+'</option>')
        }
        year = tmpl.find(".school_year").html(r.join(''))
       
        if(data){
            year.val(data.year)
            school_department(dep_node, data.school_id)
            dep_node.val(data.department)
            tmpl.find(".school_degree").val(data.degree)
        }else{
            sc.css({
                'color':"#999",
                "border-color":"#aaa"
            })
        }

        div.find(".rm").show();
        div.find(".rm:last").hide(); 
        tmpl.find('.rm').click(function(){
            tmpl.fadeOut(function(){
                tmpl.remove()
            })
            if(data){
                $.postJSON("/j/school/rm/"+data.id);
            }
        });
}
function load_school(div, data){
    var i=0,j;
    for(;i<data.length;++i){
        j = data[i];
        j = {
            id: j[0],
            school_id: j[1],
            year:j[2],
            degree:j[3],
            department:j[4],
            txt:j[5],
            name: SCHOOL_UNIVERSITY[j[1]]
        }
        school(div, j)
    }
}
