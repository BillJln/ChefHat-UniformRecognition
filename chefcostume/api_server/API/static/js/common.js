//返回的是字符串形式的参数，例如：class_id=3&id=2&
function getUrlArgStr(){
    var q=location.search.substr(1);
    var qs=q.split('&');
    var argStr='';
    if(qs){
        for(var i=0;i<qs.length;i++){
            argStr+=qs[i].substring(0,qs[i].indexOf('='))+'='+qs[i].substring(qs[i].indexOf('=')+1)+'&';
        }
    }
    return argStr;
}
//返回的是对象形式的参数
function getUrlArgObject(){
    var args=new Object();
    var query=location.search.substring(1);//获取查询串
    var pairs=query.split(",");//在逗号处断开
    for(var i=0;i<pairs.length;i++){
        var pos=pairs[i].indexOf('=');//查找name=value
        if(pos==-1){//如果没有找到就跳过
            continue;
        }
        var argname=pairs[i].substring(0,pos);//提取name
        var value=pairs[i].substring(pos+1);//提取value
        args[argname]=unescape(value);//存为属性
    }
    return args;//返回对象
}


function getUrlIpStr(){
    var q=location.search.substr(1);
    var qs=q.split(':');
    var argStr=qs[0];

    return argStr;
}
function openmydoc(path)
{
var doc=new ActiveXObject("Word.Application");
doc.visible=true;
doc.Documents.Open(path);
}

function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}


function photoCompress(file,w,objDiv){
            var ready=new FileReader();
            /*开始读取指定的Blob对象或File对象中的内容. 当读取操作完成时,readyState属性的值会成为DONE,如果设置了onloadend事件处理程序,则调用之.同时,result属性中将包含一个data: URL格式的字符串以表示所读取文件的内容.*/
            ready.readAsDataURL(file);
            ready.onload=function(){
                var re=this.result;
                canvasDataURL(re,w,objDiv)
            }
        }
function canvasDataURL(path, obj, callback){
        var img = new Image();
        img.src = path;
        img.onload = function(){
            var that = this;
            // 默认按比例压缩
            var w = that.width,
                h = that.height,
                scale = w / h;
            w = obj.width || w;
            h = obj.height || (w / scale);
            var quality = 0.7;  // 默认图片质量为0.7
            //生成canvas
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            // 创建属性节点
            var anw = document.createAttribute("width");
            anw.nodeValue = w;
            var anh = document.createAttribute("height");
            anh.nodeValue = h;
            canvas.setAttributeNode(anw);
            canvas.setAttributeNode(anh);
            ctx.drawImage(that, 0, 0, w, h);
            // 图像质量
            if(obj.quality && obj.quality <= 1 && obj.quality > 0){
                quality = obj.quality;
            }
            // quality值越小，所绘制出的图像越模糊
            var base64 = canvas.toDataURL('image/jpeg', quality);
            // 回调函数返回base64的值
            callback(base64);
        }
    }