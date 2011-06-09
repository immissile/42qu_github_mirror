function init_preview() {
    var imgw,imgh,pic=$('#pic');
    function preview(img, selection) {
        if (!selection.width || !selection.height)
            return;
        
        var scaleX = 96 / selection.width;
        var scaleY = 96 / selection.height;
     
        $('#preview img').css({
            width: Math.round(scaleX * imgw),
            height: Math.round(scaleY * imgh),
            marginLeft: -Math.round(scaleX * selection.x1),
            marginTop: -Math.round(scaleY * selection.y1)
        });
     
        $('#pos').val(selection.x1+'_'+selection.y1+'_'+(selection.x2-selection.x1))
    }
    if($('#pos').length){
        imgw = pic.width();
        imgh = pic.height();
        var _ = $('#pos').attr('value').split('_');
        var pos = _[2]?  { 
            x1: parseInt(_[0]), 
            y1: parseInt(_[1]), 
            x2: parseInt(_[0])+parseInt(_[2]), 
            y2: parseInt(_[1])+parseInt(_[2]) 
        } : {
            x1: imgw>imgh?(imgw-imgh)/2+10:10, 
            x2: imgw>imgh?(imgw+imgh)/2-10:imgw-10, 
            y1: imgw>imgh?10:(imgh-imgw)/2+10, 
            y2: imgw>imgh?imgh-10:(imgh+imgw)/2-10 
        };
        pic.imgAreaSelect(
            $.extend(pos,{
            aspectRatio : '1:1' ,
            onSelectChange : preview,
            onSelectBegin : preview,
            onSelectEnd:preview,
            show:true,
            persistent:true,
            onInit:preview,
            handles:true,
            minHeight:96,
            minWidth:96
            })
        );
    }

    $("#preview_pic").show()
};
