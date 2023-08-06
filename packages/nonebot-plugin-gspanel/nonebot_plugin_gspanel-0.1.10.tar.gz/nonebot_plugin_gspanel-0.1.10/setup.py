# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gspanel']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0b1',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0b3']

setup_kwargs = {
    'name': 'nonebot-plugin-gspanel',
    'version': '0.1.10',
    'description': 'Genshin player cards plugin for NoneBot2',
    'long_description': '<h1 align="center">NoneBot Plugin GsPanel</h1></br>\n\n\n<p align="center">🤖 用于展示原神游戏内角色展柜数据的 NoneBot2 插件</p></br>\n\n\n<p align="center">\n  <a href="https://github.com/monsterxcn/nonebot-plugin-gspanel/actions">\n    <img src="https://img.shields.io/github/workflow/status/monsterxcn/nonebot-plugin-gspanel/Build%20distributions?style=flat-square" alt="actions">\n  </a>\n  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot-plugin-gspanel/master/LICENSE">\n    <img src="https://img.shields.io/github/license/monsterxcn/nonebot-plugin-gspanel?style=flat-square" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-gspanel">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-gspanel?style=flat-square" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7.3+-blue?style=flat-square" alt="python"><br />\n</p></br>\n\n\n| ![刻晴](https://user-images.githubusercontent.com/22407052/187607775-61cfa24c-d736-4994-bd16-d211d807ae50.png) | ![琴](https://user-images.githubusercontent.com/22407052/187607799-b503f504-770f-4f80-85c6-9db78d5f849a.png) | ![香菱](https://user-images.githubusercontent.com/22407052/187607839-d29e3962-5bf6-4bf5-912d-2516e16b7643.png) |\n|:--:|:--:|:--:|\n\n\n## 安装方法\n\n\n如果你正在使用 2.0.0.beta1 以上版本 NoneBot，推荐使用以下命令安装：\n\n\n```bash\n# 从 nb_cli 安装\npython3 -m nb plugin install nonebot-plugin-gspanel\n\n# 或从 PyPI 安装\npython3 -m pip install nonebot-plugin-gspanel\n```\n\n\n## 使用须知\n\n\n - 插件的圣遗物评分计算规则、卡片样式均来自 [@yoimiya-kokomi/miao-plugin](https://github.com/yoimiya-kokomi/miao-plugin)。此插件移植后作了以下修改：\n   \n   + 以角色生命值、攻击力、防御力的实际基础值进行词条得分计算，导致固定值的生命值、攻击力、防御力词条评分相较原版有小幅度波动\n   + 于面板数据区域展示圣遗物评分使用的词条权重规则，插件尚未自定义词条权重规则的角色使用默认规则（攻击力 `75`、暴击率 `100`、暴击伤害 `100`）\n   + 于面板数据区域展示角色最高的伤害加成数据，该属性与角色实际伤害属性不一致时区别显示词条权重规则\n   + 对元素属性异常的空之杯进行评分惩罚，扣除该圣遗物总分的 50%（最大扣除比例）\n   \n - 插件返回「暂时无法访问面板数据接口..」可能的原因有：Bot 与 [Enka.Network](https://enka.network/) 的连接不稳定；[Enka.Network](https://enka.network/) 服务器暂时故障等。\n   \n - 插件首次生成某个角色的面板图片时，会尝试从 [Enka.Network](https://enka.network/) 下载该角色的抽卡大图、命座图片、技能图片、圣遗物及武器图片等素材图片，生成面板图片的时间由 Bot 与 [Enka.Network](https://enka.network/) 的连接质量决定。素材图片下载至本地后将不再从远程下载，生成面板图片的时间将大幅缩短。\n   \n - 一般来说，插件安装完成后无需设置环境变量，只需重启 Bot 即可开始使用。你也可以在 Nonebot2 当前使用的 `.env` 文件中添加下表给出的环境变量，对插件进行更多配置。环境变量修改后需要重启 Bot 才能生效。\n   \n   | 环境变量 | 必需 | 默认 | 说明 |\n   |:-------|:----:|:-----|:----|\n   | `gspanel_expire_sec` | 否 | `300` | 面板数据缓存过期秒数 |\n   | `resources_dir` | 否 | `/path/to/bot/data/` | 插件数据缓存目录的父文件夹，包含 `gspanel` 文件夹的上级文件夹路径 |\n   | `resources_mirror` | 否 | `https://enka.network/ui/` | 素材图片下载镜像，需提供 `UI_Talent_S_Nilou_01.png` 形式的图片地址，可选镜像：<br>`https://file.microgg.cn/KimigaiiWuyi/resource/icon/`（小灰灰）<br>`https://api.ambr.top/assets/UI/`（安柏计划） |\n   \n - 插件图片生成采用 [@kexue-z/nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)，若插件自动安装运行 Chromium 所需的额外依赖失败，请参考 [@SK-415/HarukaBot](https://haruka-bot.sk415.icu/faq.html#playwright-%E4%BE%9D%E8%B5%96%E4%B8%8D%E5%85%A8) 给出的以下解决方案：\n   \n   + Ubuntu：`python3 -m playwright install-deps`\n   + CentOS（仅供参考）：`yum install -y atk at-spi2-atk cups-libs libxkbcommon libXcomposite libXdamage libXrandr mesa-libgbm gtk3`\n   + 其他非 Ubuntu 系统：[@microsoft/playwright/issues](https://github.com/microsoft/playwright/issues)\n\n\n## 命令说明\n\n\n插件响应以 `面板` / `评分` / `panel` 开头的消息，下面仅以 `面板` 为例。\n\n\n - `面板绑定100123456`\n   \n   绑定 UID `100123456` 至发送此指令的 QQ，QQ 已被绑定过则会更新绑定的 UID。\n   \n   Bot 管理员可以通过在此指令后附带 `@某人` 或 `2334556789` 的方式将 UID `100123456` 绑定至指定的 QQ。\n   \n - `面板100123456`\n   \n   查找 UID `100123456` 角色展柜中展示的所有角色（文本）。\n   \n   仅发送 `面板` 时将尝试使用发送此指令的 QQ 绑定的 UID；发送 `面板@某人` 时将尝试使用指定 QQ 绑定的 UID。\n   \n - `面板夜兰100123456` / `面板100123456夜兰`\n   \n   查找 UID `100123456` 的夜兰面板（图片）。\n   \n   仅发送 `面板夜兰` 时将尝试使用发送此指令的 QQ 绑定的 UID；发送 `面板夜兰@某人` 时将尝试使用指定 QQ 绑定的 UID。\n\n\n*\\*所有指令都可以用空格将关键词分割开来，如果你喜欢的话。*\n\n\n## 特别鸣谢\n\n\n[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [@yoimiya-kokomi/miao-plugin](https://github.com/yoimiya-kokomi/miao-plugin) | [Enka.Network](https://enka.network/) | [Miniprogram Teyvat Helper](#)\n',
    'author': 'monsterxcn',
    'author_email': 'monsterxcn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/monsterxcn/nonebot-plugin-gspanel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
