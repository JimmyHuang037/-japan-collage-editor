# WSL / 容器持久只读授权

1. Google Cloud 创建个人项目，启用 Google Drive API。
2. Google Auth Platform 配置 Branding / Audience；外部应用测试时加入自己的账号。长期使用应将 OAuth 发布状态设为 In production。仅供个人使用时是否出现未验证提示取决于账号和 Google 政策；不要把生产发布状态当成已完成 Google 验证。
3. Clients 创建 Desktop app，下载 JSON。保存到 `~/.config/japan-collage/client.json`，权限 600；目录权限 700。不要发凭据内容到聊天、不要加入 Git。
4. 在项目目录运行 `docker compose -f compose.yaml --profile tools run --rm --service-ports drive auth`。打开终端输出的授权链接，浏览器回调 `127.0.0.1:8765`；Compose 将回环端口映射到容器中的回调监听器，不依赖 Docker Desktop 的 host networking。`--service-ports` 不可省略，否则一次性容器不会发布回调端口。授权进程最多等待 15 分钟。
5. `docker compose -f compose.yaml --profile tools run --rm drive check` 实际读取目标文件夹。`sync --limit 1` 下载一张核验，再执行 `sync` 增量下载缺少的原片。已存在且内容不同的 ID 停止处理，不覆盖原片。
6. `docker compose -f compose.yaml run --rm editor python scripts/prepare_assets.py` 更新本地素材库和联系表。

仅申请 `https://www.googleapis.com/auth/drive.readonly`。此 scope 可读账号可访问的 Drive 文件，并非 Google 强制的单文件夹权限；程序限制同步 Japan_Travel 目录及其子目录。刷新令牌只存于项目外的 `~/.config/japan-collage/token.json`，运行时挂载，不进入镜像或网页。

脚本使用离线授权、PKCE、本地回调和自动刷新。External + Testing 的 Drive 刷新令牌通常 7 天过期；In production 可免除此测试期限制，但撤销授权、长期不用、账号策略等仍可能使令牌失效。失效时明确要求重新授权，不无止境重试。

官方依据：
- https://developers.google.com/identity/protocols/oauth2/native-app
- https://developers.google.com/identity/protocols/oauth2#expiration
- https://developers.google.com/workspace/drive/api/guides/api-specific-auth

当前状态（2026-10-01）：Desktop 客户端与 token 已安全保存于 WSL 项目外凭据目录，文件权限 600。真实只读授权、新容器读取 Japan_Travel、刷新令牌交换、下载一张缺少原片与 Drive MD5 校验均通过；现有 65 张原片 SHA-256 保持不变，当前本地 66 张。最新云端图片清单 1,483 条，尚未全量下载。此验收不证明 Google Cloud Audience 的发布状态；若仍为 Testing，后续仍受测试期刷新令牌限制。
