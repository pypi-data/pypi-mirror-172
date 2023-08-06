# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httprunner',
 'httprunner.builtin',
 'httprunner.database',
 'httprunner.ext',
 'httprunner.ext.uploader',
 'httprunner.thrift']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'black>=22.3.0,<23.0.0',
 'jinja2>=3.0.3,<4.0.0',
 'jmespath>=0.9.5,<0.10.0',
 'loguru>=0.4.1,<0.5.0',
 'pydantic>=1.8,<1.9',
 'pytest-html>=3.1.1,<4.0.0',
 'pytest>=7.1.1,<8.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.22.0,<3.0.0',
 'sentry-sdk>=0.14.4,<0.15.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'allure': ['allure-pytest>=2.8.16,<3.0.0'],
 'sql': ['sqlalchemy>=1.4.36,<2.0.0', 'pymysql>=1.0.2,<2.0.0'],
 'thrift': ['cython>=0.29.28,<0.30.0',
            'thriftpy2>=0.4.14,<0.5.0',
            'thrift>=0.16.0,<0.17.0'],
 'upload': ['requests-toolbelt>=0.9.1,<0.10.0', 'filetype>=1.0.7,<2.0.0']}

entry_points = \
{'console_scripts': ['hmake = httprunner.cli:main_make_alias',
                     'hrun = httprunner.cli:main_hrun_alias',
                     'httprunner = httprunner.cli:main']}

setup_kwargs = {
    'name': 'httprunner',
    'version': '4.3.0',
    'description': 'One-stop solution for HTTP(S) testing.',
    'long_description': '# HttpRunner\n\n[![Github Actions](https://github.com/httprunner/httprunner/actions/workflows/unittest.yml/badge.svg)](https://github.com/httprunner/httprunner/actions)\n[![codecov](https://codecov.io/gh/httprunner/httprunner/branch/master/graph/badge.svg)](https://codecov.io/gh/httprunner/httprunner)\n[![Go Reference](https://pkg.go.dev/badge/github.com/httprunner/httprunner.svg)](https://pkg.go.dev/github.com/httprunner/httprunner)\n[![downloads](https://pepy.tech/badge/httprunner)](https://pepy.tech/project/httprunner)\n[![pypi version](https://img.shields.io/pypi/v/httprunner.svg)](https://pypi.python.org/pypi/httprunner)\n[![pyversions](https://img.shields.io/pypi/pyversions/httprunner.svg)](https://pypi.python.org/pypi/httprunner)\n[![TesterHome](https://img.shields.io/badge/TTF-TesterHome-2955C5.svg)](https://testerhome.com/github_statistics)\n\n`HttpRunner` 是一个开源的 API 测试工具，支持 HTTP(S)/HTTP2/WebSocket/RPC 等网络协议，涵盖接口测试、性能测试、数字体验监测等测试类型。简单易用，功能强大，具有丰富的插件化机制和高度的可扩展能力。\n\n> HttpRunner [用户调研问卷][survey] 持续收集中，我们将基于用户反馈动态调整产品特性和需求优先级。\n\n![flow chart](https://httprunner.com/image/hrp-flow.jpg)\n\n[版本发布日志] | [English]\n\n## 设计理念\n\n相比于其它 API 测试工具，HttpRunner 最大的不同在于设计理念。\n\n- 约定大于配置：测试用例是标准结构化的，格式统一，方便协作和维护\n- 标准开放：基于开放的标准，支持与 [HAR]/Postman/Swagger/Curl/JMeter 等工具对接，轻松实现用例生成和转换\n- 一次投入多维复用：一套脚本可同时支持接口自动化测试、性能测试、数字体验监测等多种 API 测试需求\n- 融入最佳工程实践：不仅仅是一款测试工具，在功能中融入最佳工程实践，实现面向网络协议的一站式测试解决方案\n\n## 核心特性\n\n- 网络协议：完整支持 HTTP(S)/HTTP2/WebSocket，可扩展支持 TCP/UDP/RPC 等更多协议\n- 多格式可选：测试用例支持 YAML/JSON/go test/pytest 格式，并且支持格式互相转换\n- 双执行引擎：同时支持 golang/python 两个执行引擎，兼具 go 的高性能和 [pytest] 的丰富生态\n- 录制 & 生成：可使用 [HAR]/Postman/Swagger/curl 等生成测试用例；基于链式调用的方法提示也可快速编写测试用例\n- 复杂场景：基于 variables/extract/validate/hooks 机制可以方便地创建任意复杂的测试场景\n- 插件化机制：内置丰富的函数库，同时可以基于主流编程语言（go/python/java）编写自定义函数轻松实现更多能力\n- 性能测试：无需额外工作即可实现压力测试；单机可轻松支撑 `1w+` VUM，结合分布式负载能力可实现海量发压\n- 网络性能采集：在场景化接口测试的基础上，可额外采集网络链路性能指标（DNS 解析、TCP 连接、SSL 握手、网络传输等）\n- 一键部署：采用二进制命令行工具分发，无需环境依赖，一条命令即可在 macOS/Linux/Windows 快速完成安装部署\n\n## 用户声音\n\n基于 252 份调研问卷的统计结果，HttpRunner 用户的整体满意度评分 `4.3/5`，最喜欢的特性包括：\n\n- 简单易用：测试用例支持 YAML/JSON 标准化格式，可通过录制的方式快速生成用例，上手简单，使用方便\n- 功能强大：支持灵活的自定义函数和 hook 机制，参数变量、数据驱动、结果断言等机制一应俱全，轻松适应各种复杂场景\n- 设计理念：测试用例组织支持分层设计，格式统一，易于实现测试用例的维护和复用\n\n更多内容详见 [HttpRunner 首轮用户调研报告（2022.02）][user-survey-report]\n\n## 一键部署\n\nHttpRunner 二进制命令行工具已上传至阿里云 OSS，在系统终端中执行如下命令可完成安装部署。\n\n```bash\n$ bash -c "$(curl -ksSL https://httprunner.com/script/install.sh)"\n```\n\n安装成功后，你将获得一个 `hrp` 命令行工具，执行 `hrp -h` 即可查看到参数帮助说明。\n\n```text\n$ hrp -h\n\n██╗  ██╗████████╗████████╗██████╗ ██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗███████╗██████╗\n██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗██╔══██╗██║   ██║████╗  ██║████╗  ██║██╔════╝██╔══██╗\n███████║   ██║      ██║   ██████╔╝██████╔╝██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝\n██╔══██║   ██║      ██║   ██╔═══╝ ██╔══██╗██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗\n██║  ██║   ██║      ██║   ██║     ██║  ██║╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║  ██║\n╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝\n\nHttpRunner is an open source API testing tool that supports HTTP(S)/HTTP2/WebSocket/RPC\nnetwork protocols, covering API testing, performance testing and digital experience\nmonitoring (DEM) test types. Enjoy! ✨ 🚀 ✨\n\nLicense: Apache-2.0\nWebsite: https://httprunner.com\nGithub: https://github.com/httprunner/httprunner\nCopyright 2017 debugtalk\n\nUsage:\n  hrp [command]\n\nAvailable Commands:\n  boom         run load test with boomer\n  build        build plugin for testing\n  completion   generate the autocompletion script for the specified shell\n  convert      convert to JSON/YAML/gotest/pytest testcases\n  help         Help about any command\n  pytest       run API test with pytest\n  run          run API test with go engine\n  startproject create a scaffold project\n  wiki         visit https://httprunner.com\n\nFlags:\n  -h, --help               help for hrp\n      --log-json           set log to json format\n  -l, --log-level string   set log level (default "INFO")\n      --venv string        specify python3 venv path\n  -v, --version            version for hrp\n\nUse "hrp [command] --help" for more information about a command.\n```\n\n## 用户案例\n\n<a href="https://httprunner.com/docs/cases/dji-ibg"><img src="https://httprunner.com/image/logo/dji.jpeg" title="大疆 - 基于 HttpRunner 构建完整的自动化测试体系" width="60"></a>\n<a href="https://httprunner.com/docs/cases/youmi"><img src="https://httprunner.com/image/logo/youmi.png" title="有米科技 - 基于 HttpRunner 建设自动化测试平台" width="60"></a>\n<a href="https://httprunner.com/docs/cases/umcare"><img src="https://httprunner.com/image/logo/umcare.png" title="通用环球医疗 - 使用 HttpRunner 实践接口自动化测试" width="100"></a>\n<a href="https://httprunner.com/docs/cases/mihoyo"><img src="https://httprunner.com/image/logo/miHoYo.png" title="米哈游 - 基于 HttpRunner 搭建接口自动化测试体系" width="100"></a>\n\n## 赞助商\n\n### 金牌赞助商\n\n[<img src="https://httprunner.com/image/hogwarts.jpeg" alt="霍格沃兹测试开发学社" width="400">](https://ceshiren.com/)\n\n> [霍格沃兹测试开发学社](http://qrcode.testing-studio.com/f?from=httprunner&url=https://ceshiren.com)是业界领先的测试开发技术高端教育品牌，隶属于[测吧（北京）科技有限公司](http://qrcode.testing-studio.com/f?from=httprunner&url=https://www.testing-studio.com) 。学院课程由一线大厂测试经理与资深测试开发专家参与研发，实战驱动。课程涵盖 web/app 自动化测试、接口测试、性能测试、安全测试、持续集成/持续交付/DevOps，测试左移&右移、精准测试、测试平台开发、测试管理等内容，帮助测试工程师实现测试开发技术转型。通过优秀的学社制度（奖学金、内推返学费、行业竞赛等多种方式）来实现学员、学社及用人企业的三方共赢。\n\n> [进入测试开发技术能力测评!](http://qrcode.testing-studio.com/f?from=httprunner&url=https://ceshiren.com/t/topic/14940)\n\n### 开源服务赞助商\n\n[<img src="https://httprunner.com/image/sentry-logo-black.svg" alt="Sentry" width="150">](https://sentry.io/_/open-source/)\n\nHttpRunner is in Sentry Sponsored plan.\n\n## Subscribe\n\n关注 HttpRunner 的微信公众号，第一时间获得最新资讯。\n\n<img src="https://httprunner.com/image/qrcode.png" alt="HttpRunner" width="400">\n\n如果你期望加入 HttpRunner 用户群，请看这里：[HttpRunner v4 用户交流群，它来啦！](https://httprunner.com/blog/join-chat-group)\n\n[HttpRunner]: https://github.com/httprunner/httprunner\n[boomer]: https://github.com/myzhan/boomer\n[locust]: https://github.com/locustio/locust\n[jmespath]: https://jmespath.org/\n[allure]: https://docs.qameta.io/allure/\n[HAR]: https://en.wikipedia.org/wiki/HAR_(file_format)\n[hashicorp plugin]: https://github.com/hashicorp/go-plugin\n[go plugin]: https://pkg.go.dev/plugin\n[版本发布日志]: docs/CHANGELOG.md\n[pushgateway]: https://github.com/prometheus/pushgateway\n[survey]: https://wj.qq.com/s2/9699514/0d19/\n[user-survey-report]: https://httprunner.com/blog/user-survey-report/\n[English]: README.en.md\n[pytest]: https://docs.pytest.org/\n',
    'author': 'debugtalk',
    'author_email': 'debugtalk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://httprunner.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
