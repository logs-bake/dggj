(function () {
    const socket = io('http://localhost:19999')        // 连接到服务器
//    const socket = io('ws://localhost:19999')        // 连接到服务器
    // 绑定发送按钮的点击事件
    document.getElementById('send').addEventListener('click', function() {
        var messageInput = document.getElementById('message');
        var messageText = messageInput.value;
        var date = new Date()       // 获取当前时间
        var formattedDate = date.toLocaleDateString('zh-CN', {
              year: 'numeric', month: '2-digit', day: '2-digit', hour12: false, hour: '2-digit',
              minute: '2-digit', second: '2-digit'
            });
        if (messageText.trim() !== '') {
            let message = { username: user.username, avatar: user.avatar,
                            submit_datetime:formattedDate, text: messageText }
            socket.emit('message', message);
            messageInput.value = '';
            append_message(message, 'bg-success', 'text-end')
            var infoDiv = document.getElementById('info');
            // 使用display属性来隐藏信息提示div
            infoDiv.style.display = "none"
        }
    });

    // 监听服务器发送的消息,并将消息添加到聊天信息列表中
    socket.on('message', function(message){
        console.log("message=", message)
        append_message(message, 'bg-light', 'text-start')
    })

    // 自定义向聊天信息列表中动态添加聊天信息的方法
    function append_message(message, background, position) {
        var chatMessages = document.getElementById('chat-messages');  // 获取聊天信息列表的根节点
        var fullUrl = window.location.href
        var baseUrl = fullUrl.replace("/chat", "/static")  // 获取用户头像所在路径的根目录地址
        var imgUrl = baseUrl+message.avatar
        //  每条聊天信息的内部页面显示结构示例
        let inner = `
            <div class="p-1 h-100">
                <div class="mt-2 ps-2 ${position}">
                    <img class="rounded" width="24" src="${imgUrl}"/>
                    <span class="icon-title fs-5 fw-bold mx-1">${ message.username }</span>
                    <span class="ms-3">${ message.submit_datetime }</span>
                </div>
                <div class="${position}">
                    <span class="fs-4 text-dark p-2 rounded ${background}">${ message.text }</span>
                </div>
            </div>`

        var chatDiv = document.createElement('div');  // 动态创建聊天信息的div
        chatDiv.classList.add("p-0")    // 为div元素设置类样式
        chatDiv.innerHTML = inner

//        var subDiv = document.createElement('div');  // 动态创建聊天信息的内层div
//        subDiv.classList.add("h-100")    // 为内层div元素设置类样式
//        subDiv.classList.add("p-1")
//
//        var userDiv = document.createElement('div');  // 动态创建显示用户信息的子div
//        userDiv.classList.add("mt-2")  // 为显示用户信息的子div元素设置类样式
//        userDiv.classList.add("ps-2")
//        userDiv.classList.add(position)
//
//        var avatarImg = document.createElement('img');  // 动态创建显示用户头像的img标签
//        avatarImg.classList.add("rounded")    // 为img标签设置类样式
//        avatarImg.width = '24'   // 给img标签的width属性赋值
//        var fullUrl = window.location.href
//        var baseUrl = fullUrl.replace("/chat", "/static")  // 获取用户头像所在路径的根目录地址
//        avatarImg.src = baseUrl+message.avatar  // 给img标签的src属性赋值头像的URL地址
//        userDiv.appendChild(avatarImg)  //将img标签添加到用户信息的子div中
//
//        var titleSpan = document.createElement('span'); // 动态创建显示用户名的span标签
//        titleSpan.classList.add("icon-title")
//        titleSpan.classList.add("fs-5")
//        titleSpan.classList.add("fw-bold")
//        titleSpan.classList.add("mx-1")
//        titleSpan.textContent = message.username  // 给span标签添加用户名文本
//        userDiv.appendChild(titleSpan)  //将显示用户名的span标签添加到用户信息的子div中
//
//        var dateSpan = document.createElement('span');  // 动态创建显示聊天信息提交时间的span标签
//        dateSpan.classList.add("ms-3")
//        dateSpan.textContent = message.submit_datetime   // 给span标签添加字符串表示的聊天信息提交时间
//        userDiv.appendChild(dateSpan)  //将显示聊天信息提交时间的span标签添加到用户信息的子div中
//
//        var msgDiv = document.createElement('div');  // 动态创建显示聊天信息文本的子div
//        msgDiv.classList.add(position) // 为子div元素设置类样式
//
//        var msgSpan = document.createElement('span');  // 动态创建显示聊天信息文本的 span 标签
//        msgSpan.classList.add("fs-4")    // 为span标签设置类样式
//        msgSpan.classList.add("text-dark")
//        msgSpan.classList.add("p-2")
//        msgSpan.classList.add("rounded")
//        msgSpan.classList.add(background)
//        msgSpan.textContent = message.text  // 给span标签添加聊天信息文本
//        msgDiv.appendChild(msgSpan) //将显示聊天信息文本的 span标签添加到用户信息的子div中
//
//        subDiv.appendChild(userDiv);    //将显示用户信息的子div中添加到内层div中
//        subDiv.appendChild(msgDiv);     //将显示聊天信息文本的子div中添加到内层div中
//        chatDiv.appendChild(subDiv);    //将内层div中添加到聊天信息的div中
        chatMessages.appendChild(chatDiv);  //将聊天信息div添加到聊天信息列表的根节点中
    }
})()