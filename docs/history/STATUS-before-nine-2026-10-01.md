# 当前状态

当前状态（2026-10-01，优先于下方历史交接）：editor 正在运行，入口 http://127.0.0.1:3077/。Google Drive 只读授权已真实完成，新容器读取 Japan_Travel、刷新令牌交换与原片下载校验均通过。Drive 最新清单 1,483 张图片，本地原片及素材目录 66 张；九图业务仍未完成。本轮仅处理启动和 Drive 授权，未执行全量下载。


2026-09-22 收工交接已写入根目录 `HANDOFF.md`，它是新会话的详细续接入口。按用户“今天先到这里”的要求，已停止编辑器容器；下一次用户要求继续时再启动。新会话先读项目 AGENTS.md 与 HANDOFF.md，不必重复询问背景。

项目已按用户纠正移至 `/home/jimmyhuang/japan-collage-editor`，与 AE、学生管理系统平级；旧 projects 路径不再使用。

用户已批准实施：WSL/Linux 容器开发、Drive 访问、代理制作九图、每张网页可编辑。地图与个人网站展示已排除。

已正式 git clone 官方快图仓库，保留完整 Git 历史。远程名 upstream，URL https://github.com/ikuaitu/vue-fabric-editor.git；开发分支 codex/japan-collage，基线 b3bdcfb0bd6d8f98e7483cf561ac03ba56c0d889。

用户纠正要求：直接改造快图原有界面，不另写独立编辑器。此前未完成的独立界面与辅助代码保存在 `data/pre-clone-unfinished/`，未接入现有应用，不得视为成品。

已核对原始交接与快图快照，复制 65 张原片到本项目；完整旅行选片仍需其余素材。Drive 原有技能配置返回 NOT_AUTHENTICATED，正在等待用户提供 OAuth 客户端路径或完成只读授权。网络可达不代表账号授权成功。rclone 共享客户端按官方说明将于 2026 年停用，不作为持久访问方案。

容器开发镜像及浏览器验收镜像已构建，快图原版依赖安装完成。真实 Chromium 冒烟检查已确认原版画布、左右侧栏可见（`outputs/upstream-baseline/`）；默认外部接口出现 3 个 AxiosError，旅行本地化尚未实施。宇治可编辑工程与九图仍未完成，不能把原版启动当成业务验收。

## 2026-09-28 本机 Docker Desktop 迁移

本机 WSL 原生 Docker Engine 已迁移至 Windows Docker Desktop 4.93.0（WSL 2 backend，Ubuntu-24.04 集成）。镜像和数据卷已恢复并验证；本项目容器已重建、保持未启动（Created），未继续业务开发。启动前先打开 Windows Docker Desktop，原 Compose 入口继续使用。迁移与回退记录：`/home/jimmyhuang/docker/migrations/README.md`。

## 2026-10-01 状态核对（仅查询）

用户询问旅行前端工作台是否卡在 Google Drive 登录。已读取交接并核对：Git 工作区仍保留原有未提交改动；editor 容器状态为 Created，未运行；`/home/jimmyhuang/.config/japan-collage` 仍无凭据文件。Drive 持续访问授权尚未完成的记录未发现变化，本轮未尝试账号 API 验证、未启动容器、未恢复业务开发。现有 65 张本地素材与九图目标沿用此前交接记录。

## 2026-10-01 启动编辑器与修复授权回调

用户明确要求启动容器并修复 Drive 登录。editor 已启动，WSL `http://127.0.0.1:3077/` 返回 HTTP 200；已请求在 Codex 打开该地址（工具返回 queued）。保留运行，未恢复九图或其他业务开发。

Drive 容器 `check` 明确返回尚未授权；技能检查也无 token，常用下载目录未发现客户端 JSON。用户随后要求指导如何创建客户端，当前等待用户在 Google Cloud 创建 Desktop app 并提供下载 JSON 的文件路径；不能标记账号授权完成。

发现原 Drive host-network 回调服务容器运行时，WSL 无法连接 `127.0.0.1:8765`。已改 compose 的 drive 服务为 bridge + `127.0.0.1:8765:8765` 映射；OAuth 仍以 `127.0.0.1` 作为 redirect host，容器监听使用 `bind_addr='0.0.0.0'`。docs/DRIVE-SETUP.md 已更新启动命令，必须运行：

```bash
docker compose -f compose.yaml --profile tools run --rm --service-ports drive auth
```

临时 HTTP 回调探针在 WSL curl 和 Windows PowerShell Invoke-WebRequest 均返回 HTTP 200，探针容器已删除；容器访问 Drive API discovery 返回 HTTP 200，OAuth 脚本语法核验成功。这些核验不等于实际 OAuth 账号授权、刷新或私有文件下载验收。未提交或推送。

下一步：拿到 JSON 路径后验证 Desktop 类型，安全保存到 `/home/jimmyhuang/.config/japan-collage/client.json`（600），开启 auth，提供实际授权链接；用户浏览器批准后，在新容器执行 check 和一张原片下载核验，再检查凭据持久化。

2026-10-01 授权进度：用户截图显示 Japan Collage 项目已创建名为 Japan Collage Desktop 的桌面客户端，客户端密钥处于启用状态。下载目录和项目凭据目录仍未发现客户端 JSON；下一步点击密钥行复制图标右侧的下载箭头下载 JSON。尚未取得文件或完成账号授权；截图不能证明 API 已启用或 Audience 已发布。

2026-10-01 实际 OAuth 授权已启动：用户提供 Desktop 客户端 JSON 并明确要求在 WSL 工作。已验证 Desktop 类型和 Google 标准端点，安全保存到 `/home/jimmyhuang/.config/japan-collage/client.json`（600；目录 700），未输出密钥或放入项目。当前无 token。editor 持续运行；一次性容器 `japan-drive-auth` 已通过 `--service-ports` 启动，正在等待浏览器批准只读 Drive scope，最长 15 分钟。授权 URL 已提供给用户，不写入交接。执行会话 ID 44848；后续先检查进程/token 实际状态，若超时再重启 auth。尚未完成真实账号授权及私有文件读取，未提交推送。

## 2026-10-01 Drive 账号验收完成

用户回复 done 后，原授权进程成功退出并保存包含刷新令牌的 token（权限 600，只读 scope）。新一次性容器独立读取持久凭据，主动完成一次真实刷新令牌交换，再次列出 Japan_Travel，均成功。`sync --limit 1` 更新私有清单为 1,483 张图片并下载 1 张缺少原片；样本 MD5 与 Drive 元数据一致，原有 65 张原片 SHA-256 均保持不变。现有 66 张原片；prepare_assets.py 已成功更新素材目录和 3 张联系表。

非敏感验收报告：`data/reference/drive-auth-verification.json`；私有实时清单：`data/reference/drive-current.json`。凭据仅存在 `/home/jimmyhuang/.config/japan-collage/`，未提交、未进入网页或镜像。auth 和验收一次性容器已退出，editor 保持运行；没有全量同步、业务编辑器改造、九图制作或生产部署。Google Cloud Audience 的发布状态未实测，不能承诺永久授权。

后续若用户要求继续九图任务，可先增量同步全量缺少素材并更新目录，再沿既有快图改造和选片计划继续；已完成的 OAuth 不需要重新创建客户端或重复授权，除非实际刷新失败。
