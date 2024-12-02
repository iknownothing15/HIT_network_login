# 哈尔滨工业大学 校园网登陆脚本

## 介绍

本项目是一个用于哈尔滨工业大学校园网自动登录的脚本，使用python编写,遵循GPLv3协议。

## 依赖

在运行脚本之前，请确保已安装以下依赖：

- requests
- beautifulsoup4

你可以使用以下命令安装这些依赖：

```sh
pip install requests beautifulsoup4
```

## 使用方法

在运行脚本之前，请在 configure.json 文件中配置你的账号信息和相关 URL：

```
{
    "urls":{
        "login_page": "https://webportal.hit.edu.cn/srun_portal_pc?ac_id=24&srun_wait=1&theme=hit",
        "get_challenge_api": "http://webportal.hit.edu.cn/cgi-bin/get_challenge",
        "login_api": "http://webportal.hit.edu.cn/cgi-bin/srun_portal"
    },
    "account": {
        "username": "your_username",
        "password": "your_password",
        "n" : "200",
        "vtype": "1",
        "acid": "24",
        "enc": "srun_bx1"
    }
}
```

请将 your_username 和 your_password 替换为你的实际用户名和密码。(一般是学号和密码)

在配置好 configure.json 文件后，你可以运行 login.py 脚本来进行登录：

```
python login.py

```
## 脚本说明

### login.py

这个脚本包含一个 Login 类，用于处理登录过程。主要方法包括：

`get_ip()`: 获取用户的 IP 地址。

`get_challenge()`: 获取挑战令牌。

`generate_login_info()`: 生成并加密登录信息。

`send_login_info()`: 发送登录信息。

`resolve_login_response()`: 解析登录响应。

`get_login_response()`: 执行完整的登录流程。

### configure.json

这个文件包含登录所需的配置信息，包括 URL 和账号信息。首次使用时，请确认已经正确填写了账号密码。


## 注意事项

请确保已连接到 HIT-WLAN 。

请确保 configure.json 文件中的配置信息正确无误。

有时会提示登陆失败，但实际已经登陆成功的情况，如果多次失败可以尝试直接打开网页测试是否已经成功登陆。

项目 `encryption` 文件夹来自于项目[BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script) ，没有他们的代码就没有这个项目，感谢他们的恩！情！