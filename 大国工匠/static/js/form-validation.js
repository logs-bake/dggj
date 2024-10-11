(function () {
  'use strict'

  var forms = document.querySelectorAll('.needs-validation')
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

// 选择用户头像后显示预览效果
function headSelect(){
    // 获取待上传的文件对象
    let file = document.getElementById('avatar').files[0]
    // 声明一个读取文件对象
    let reader = new FileReader();
    // 开始读取文件内容
    reader.readAsDataURL(file);
    // 读取操作结束时触发
    reader.onloadend = (ev) => {
      // 赋值给图片预览节点的src属性
      document.getElementById("preview").src=ev.target.result
    };
}