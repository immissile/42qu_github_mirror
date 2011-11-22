

JOB_KIND =[[[0, '计算机软件'],
  [1, '计算机硬件'],
  [2, '计算机服务(系统、数据服务，维修)'],
  [3, '通信/电信/网络设备'],
  [4, '通信/电信运营、增值服务'],
  [5, '互联网/电子商务'],
  [6, '网络游戏'],
  [7, '电子技术/半导体/集成电路'],
  [8, '仪器仪表/工业自动化']],
 [[100, '会计/审计'],
  [101, '金融/投资/证券'],
  [102, '银行'],
  [103, '保险']],
 [[200, '贸易/进出口'],
  [201, '批发/零售'],
  [202, '服装/纺织/皮革'],
  [203, '家具/家电/工艺品/玩具/珠宝'],
  [204, '办公用品及设备'],
  [205, '机械/设备/重工'],
  [206, '汽车及零配件']],
 [[300, '制药/生物工程'],
  [301, '医疗/护理/保健/卫生'],
  [302, '医疗设备/器械'],
  [303, '广告'],
  [304, '公关/市场推广/会展'],
  [305, '影视/媒体/艺术'],
  [306, '文字媒体/出版'],
  [307, '印刷/包装/造纸']],
 [[400, '房地产开发'],
  [401, '建筑/建材/工程'],
  [402, '家居/室内设计/装潢'],
  [403, '物业管理/商业中心']],
 [[500, '中介服务'],
  [501, '专业服务(咨询，人力资源)'],
  [502, '外包服务'],
  [503, '检测，认证'],
  [504, '法律'],
  [505, '教育/培训'],
  [506, '学术/科研']],
 [[600, '餐饮业'],
  [601, '酒店/旅游'],
  [602, '娱乐/休闲/体育'],
  [603, '美容/保健'],
  [604, '生活服务']],
 [[700, '交通/运输/物流'], [701, '航天/航空']],
 [[800, '石油/化工/矿产/地质'],
  [801, '采掘业/冶炼'],
  [802, '电力/水利'],
  [803, '原材料和加工']],
 [[900, '政府'], [901, '非盈利机构'], [902, '环保']],
 [[1000, '农业/渔业/林业'],
  [1001, '多元化业务集团公司'],
  [1002, '其他行业']]];

function man_de(){
    var fancybox = $.fancybox
    var cont='<form id="de_form"><div class="pop_hint">管理部门</div>',opts = $('.de_opt')
    opts.each(function(){
        cont += '<div class="pop_de" id="pop_de'+$(this).val()+'"><input type="text" class="pop_de_name" name="pop_de_name" value="'+$(this).text()+'"><input type="hidden" name="pop_de_id" value="'+$(this).val()+'"><a href="javascript:rm_de('+$(this).val()+');void(0)" class="rm_addr"></a></div>'
    })
    cont += '<a href="javascript:man_done();void(0)" class="man_done">保存</a></form>'
    fancybox({content:cont,'hideOnOverlayClick': false})
}
function rm_de(id){
    if(confirm('删除,确定?')){
        $.postJSON(
            '/job/department/rm',
            {'id':id}
        )
        $('#pop_de'+id).remove()
    }
}
function man_done(){
    var pop_des = $('.pop_de'),result='',ctrl=false
    pop_des.each(function(){
        var de = $(this),
        id = de.find('input[name="pop_de_id"]').val(),
        name = $.trim(de.find('.pop_de_name').val())
        if(name==''){
            alert('部门名称不能为空')
            ctrl = true
            return
        }
        result += '<option class="de_opt" value="'+id+'">'+name+'</option>'
    })
    if(ctrl) return
    $.postJSON(
        '/job/department/write',
        $('#de_form').serialize()
    )
    $('#depart').html(result)
    $('#fancybox-close').click()  
}
function add_de_a(){
    val = $('.add_de_txt').val()
    if($.trim(val)==''){
        alert('部门名称不能为空')
        return
    }
    $.postJSON(
        '/job/department/add',
        {'txt':val},
        function(id){
            de = $('#depart')
            de.append('<option class="de_opt" selected value="'+id+'">'+val+'</option>')
            $('#fancybox-close').click()
        }
    )
}
function add_ad_a(){
    var co = $("select[name='country']").val(),
    coun = $("select[name='country']").find("option:selected").text(),
    city = $("select[name='city']").find("option:selected").text(),
    town = $("select[name='town']").find("option:selected").text()
    if(!(coun && city && town && city!="- 请选择 -" && town!="- 请选择 -") && coun=='中国' ){
        alert('请选择完整的城市及县区')
        return
    }
    if(co==1) addr=city+' '+town; else addr=coun;
    num = $('#addr').children().length + 1
    var addr_val = $('#pid').find('input').val()
    $('#addr').append('<div class="address"><input name="addr" value="'+addr_val+'" id="addr'+num+'" type="checkbox" checked><label for="addr'+num+'"> '+addr+'</label><a href="javascript:rm_addr('+num+');void(0)" class="rm_addr"></a></div>')
    $('.add_ad_txt, .add_de_a').remove()
    $('.add_addr').hide()
    $('#add_addr').show()
}
function add_de(){
    var fancybox = $.fancybox
    fancybox({
        'content':'<input type="text" class="input add_de_txt"><a class="add_de_a" href="javascript:add_de_a();void(0)">添加部门</a>',
        'hideOnOverlayClick': false
    })
    $('.add_de_txt').focus()
}
function add_addr(){
    $('#add_addr').hide()
    $('.add_addr').css('display','inline')
    $('.add_addr').after('<a class="c9 add_de_a" href="javascript:add_ad_a();void(0)">添加</a>')
}
function rm_addr(id){
    $('#addr'+id).parent().remove()
};

$(function(){
    function empty(self){
        var val=self.val();
        return !val||$.trim(val)==''
    }
    function verify(){
        var self=$(this);
        tip(self)
    }
    function tip(self){
        var id=self[0].id;
        if(empty(self)){
            $("#errtip_"+id).remove()
            var tip=$('<div class="errtip" id="errtip_'+id+'"/>');
            self.after(tip);
            tip.fadeOut(function(){tip.fadeIn()})
            tip.html("此项必填")
        }
    }

    var elem="#title,#txt,#require,#more,#kinds_input"
    elem=$(elem)
    elem.blur(verify).focus(function(){
        $("#errtip_"+this.id).remove()
    })

    function check_tip(name){
        var s = ':checkbox[name='+name+']'
        var cb = $(s)
        var par = $('#'+name)
        if($(s+':checked').length<1){
            $('#errtip_'+name).remove()
            par.after('<div class="errtip" id="errtip_'+name+'">请至少选择一项</div>')
            $(window).scrollTop(Math.max(par.offset().top-50,0))
            var err = $('#errtip_'+name)
            err.fadeOut(function(){err.fadeIn()})
            cb.click(function(){err.remove()})
            return false
        }
        return true
    }

    function money_tip(){
        if(empty($('.salary1')) || empty($('.salary2'))){
            $('#errtip_salary').remove()
            $('#salary').after('<div class="errtip" id="errtip_salary">此项必填</div>')
            var err=$('#errtip_salary')
            err.fadeOut(function(){err.fadeIn()})
            $('.salary1,.salary2').click(function(){err.remove()})
            return false
        }
        if(!$('input[name="addr"]:checked')[0]){
            var err=$('#errtip_addr')
            err.fadeOut(function(){err.fadeIn()})
            $('input[name="addr"], #add_addr').click(function(){err.remove()})
            return false
        }
        return true
    }

    job_new = function (){
        var submit,i=0;
        for(;i<elem.length;++i){
            var self=$(elem[i]);
            if(empty(self)){
                self.focus();
                $(window).scrollTop(Math.max(self.offset().top-50,0))
                tip(self)
                submit = false
                return submit;
            }
        }
        if(!check_tip('addr'))return false;
        if(!check_tip('type'))return false;
        return money_tip()
    }

             
    var kinds_content = '<div class="kinds_banner">选择行业类别 (<span class="limit_tip">最多三项</span>)</div><div class="pop_kinds">'
    for(var i=0;i<JOB_KIND.length;i++){
        var li = JOB_KIND[i]
        kinds_content += i%2==0?'<ul class="bgc1">':'<ul class="bgc2">'
        for(var j=0;j<li.length;j++){
            kinds_content += '<li><label><input type="checkbox" value="'+li[j][0]+'" class="kinds_cb" name="kinds'+li[j][0]+'"></label><span class="kinds_word">'+li[j][1]+'</span></li>'
        }
        kinds_content += '</ul>'
    }
    kinds_content += '<div style="height:10px;"></div></div><button class="kinds_btn" type="button">确 定</button>'


    $('#kinds').click(function(){
        var fancybox = $.fancybox
        fancybox({
            'content':kinds_content,
            'hideOnOverlayClick': false
        })
        if($('#kinds_input').val().length>0){
            var ids = $('#kinds_input').val().split('-')
            for(i=0;i<ids.length;i++){
                $(".kinds_cb[name='kinds"+ids[i]+"']").attr('checked','checked')
                $(".kinds_cb[name='kinds"+ids[i]+"']").parent().parent().find('.kinds_word').addClass('kinds_word_on')
            }
        }
        $('.kinds_word').click(function(){
            if($(this).css('background-color')=='transparent'){
                if($('.kinds_word_on').length>=3){
                    $('.limit_tip').css({'color':'#D10','font-size':'16px'}).fadeOut(function(){$('.limit_tip').fadeIn()})
                    return
                }
                $(this).toggleClass('kinds_word_on')
                $(this).parent().find('input').attr('checked','checked')
            } else{
                $('.limit_tip').css({'color':'#000','font-size':'14px'})
                $(this).toggleClass('kinds_word_on')
                $(this).parent().find('input').removeAttr('checked')
            }
        })

        $('.kinds_cb').click(function(){
            var word = $(this).parent().parent().find('.kinds_word')
            if(word.css('background-color')=='transparent'){
                if($('.kinds_word_on').length>=3){
                    $('.limit_tip').css({'color':'#D10','font-size':'16px'}).fadeOut(function(){$('.limit_tip').fadeIn()})
                    $(this).removeAttr('checked')
                    return
                }
                word.toggleClass('kinds_word_on')
            } else{
                $('.limit_tip').css({'color':'#000','font-size':'14px'})
                word.toggleClass('kinds_word_on')
            }
        })

        $('.kinds_btn').click(function(){
            if($('.kinds_word_on').length<1){
                $('#fancybox-close').click()
                return
            }
            var words = ''
            var ids = []
            $('.kinds_word_on').each(function(){
                words += $(this).text()+' + '
                ids.push($(this).parent().find('.kinds_cb').val())
            })
            //ids = ids.substr(0,words.length-2)
            words = words.substr(0,words.length-2)
            $('#fancybox-close').click()
            $('#kinds').text(words).css({'color':'#000','width':'auto','overflow':'hidden','text-align':'left'})
            $('#kinds_input').val(ids.join('-'))
        })
    })
})
