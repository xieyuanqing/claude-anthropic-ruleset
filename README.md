# Claude Anthropic Rule Set

可分享、可维护的 Claude / Anthropic 分流规则集，目标是把 Claude Code、Claude 网页版、Anthropic 控制台、认证、CDN、监控上报、第三方 widget 和 Anthropic IP 段尽量打包成一个规则链接。

规则来源基础：<https://ip.net.coffee/claude/site.html>

## 直接使用

把下面链接填到代理客户端的 **Rule Set / 规则集 URL** 输入框里：

```text
https://raw.githubusercontent.com/<OWNER>/<REPO>/main/rule-set/claude-full.json
```

如果你的客户端使用分流规则条件，可以把这个规则集绑定到你希望 Claude 使用的代理策略组。

> 发布到 GitHub 后，把 `<OWNER>/<REPO>` 替换成实际仓库路径即可。例如：`https://raw.githubusercontent.com/xieyuanqing/claude-anthropic-ruleset/main/rule-set/claude-full.json`。

## 当前覆盖内容

- Anthropic / Claude 核心域名
- Claude MCP 相关域名
- Claude 用户内容与附件域名
- Anthropic CDN / 静态资源
- Auth0 登录认证、Ghost 内容站
- Sentry、Statsig、Datadog、Sift 等监控 / 风控 / 功能开关域名
- Intercom、Fathom 等客服和统计 widget
- Anthropic IPv4 / IPv6 段

## 重要说明

### 为什么不用只内置 `geosite:anthropic`

当前上游 `geosite:anthropic` 覆盖较少，主要包含：

```text
anthropic.com
clau.de
claude.ai
claude.com
claudemcpclient.com
claudeusercontent.com
servd-anthropic-website.b-cdn.net
```

它没有覆盖这份完整规则里的部分内容，例如：

- `claudemcpcontent.com`
- `anthropic.auth0.com`
- `anthropic-com.ghost.io`
- `anthropic.com.cdn.cloudflare.net`
- `browser-intake-us5-datadoghq.com`
- `statsigapi.net`
- `intercom.io` / `intercomcdn.com`
- `cdn.usefathom.com`
- Datadog / Sift 关键词 fallback
- Anthropic IP 段 fallback

因此如果你想让 Claude 相关流量尽量统一走同一个出口，建议使用本仓库的完整规则集。

### JSON 规则集和 ASN / NTP

`rule-set/claude-full.json` 是 sing-box source-format JSON 规则集，适合直接作为 URL 导入。这个格式本身不表达 ASN 和 `geosite:category-ntp`，所以：

- `AS399358` 保留在 `source/claude-full.yaml` 和 `rule-set/claude-full.list` 中，供支持 ASN 的客户端单独配置。
- NTP/UDP 规则建议在客户端里单独配置到同一个代理出口，例如 `geosite:category-ntp`。

## 维护方式

修改源文件：

```bash
source/claude-full.yaml
```

重新生成：

```bash
python3 scripts/generate.py
python3 scripts/validate.py
```

生成文件：

- `rule-set/claude-full.json`：直接导入用的 sing-box JSON 规则集
- `rule-set/claude-full.list`：便于人工查看或给 Clash/Mihomo 类客户端改写的文本规则

## 文件结构

```text
.
├── source/claude-full.yaml       # 人类维护的规则源
├── rule-set/claude-full.json     # 直接导入的规则集链接目标
├── rule-set/claude-full.list     # 文本规则参考
├── scripts/generate.py           # 从源文件生成规则集
├── scripts/validate.py           # 校验关键规则是否存在
└── .github/workflows/validate.yml
```

## License

MIT
