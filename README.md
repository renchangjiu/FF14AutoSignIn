#  FF14 国服官网自动签到脚本

*2023年6月2日更新: 盛趣上线了新版积分商城, 原签到 api 已无效, 等我重构.*  
*2022年1月11日更新: 适配新大区`豆豆柴`.*  
*2019年12月20日更新: 适配新大区`猫小胖`.*  
*2019年12月6日更新: 已解决因官网登录参数变化导致无法登录的问题.*  

1.作用  
&nbsp;&nbsp;使用 python 的 requests 库, 实现 FF14 国服官网自动签到, 暂不支持 WeGame 帐号.  
示例:  
![示例](https://raw.githubusercontent.com/renchangjiu/image-bed/master/img/20200315123628.png)

2.安装
  1. 安装 Python 解释器 [Python 官网](https://www.python.org/)
  2. 下载项目源码
  3. 进入项目根目录, 执行命令 `pip -r requirements.txt` 安装依赖库

3.用法
  1. 修改项目根目录下的 `config.py` 文件, 添加登录参数
  2. 进入项目根目录, 执行命令 `python main.py`, 完成签到
