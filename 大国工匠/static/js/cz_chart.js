(function () {
    const socket = io('ws://localhost:19999')        // 连接到服务器

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
            let message = { userid:user.userid, username: user.username, avatar: user.avatar,
                            submit_datetime:formattedDate, text: messageText }
            socket.emit('message', message);
            messageInput.value = '';
            append_message(message, 'bg-success', 'text-end')
        }
    });

    // 与服务端建立连接时，发送用户信息
    socket.on('connect', function () {
        socket.emit('user_info', {userid:user.userid, username: user.username, avatar: user.avatar});
    });

    // 监听服务器发送的消息,并将消息添加到聊天信息列表中
    socket.on('welcome', function(info){
        console.log("info = ", info)
        var chatMessages = document.getElementById('chat-messages');  // 获取聊天信息列表的根节点
        var chatDiv = document.createElement('div');  // 动态创建聊天信息的div
        chatDiv.classList.add("py-3")    // 为div元素设置类样式
        chatDiv.classList.add("text-center")    // 为div元素设置类样式
        chatDiv.textContent = info.text
        chatMessages.appendChild(chatDiv);  //将聊天信息div添加到聊天信息列表的根节点中
         var infoDiv = document.getElementById('info');
        // 使用display属性来隐藏信息提示div
        infoDiv.style.display = "none"
    })

    // 监听服务器发送的消息,并将消息添加到聊天信息列表中
    socket.on('message', function(message){
        if(message.userid != user.userid){
            append_message(message, 'bg-light', 'text-start')
        }
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
                <div class="pt-2 ${position}">
                    <span class="fs-4 text-dark p-2 rounded ${background}">${ message.text }</span>
                </div>
            </div>`

        var chatDiv = document.createElement('div');  // 动态创建聊天信息的div
        chatDiv.classList.add("p-0")    // 为div元素设置类样式
        chatDiv.innerHTML = inner
        chatMessages.appendChild(chatDiv);  //将聊天信息div添加到聊天信息列表的根节点中
    }
})()
























