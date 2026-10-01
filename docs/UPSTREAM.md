# 快图上游与开发入口

本项目通过实际 `git clone https://github.com/ikuaitu/vue-fabric-editor.git` 创建，保留完整历史。

项目位置：`/home/jimmyhuang/japan-collage-editor`，与 AE 和学生管理系统平级。

- 上游远程：`upstream`，只作为开源来源，不作为用户项目的发布目标。
- 固定基线：`b3bdcfb0bd6d8f98e7483cf561ac03ba56c0d889`。
- 开发分支：`codex/japan-collage`。
- 继续使用上游 `src/main.ts`、`src/views/home/`、`src/components/` 和 `packages/core/`；不另建应用入口。
- 上游根目录 Dockerfile 用于发布镜像；本地开发环境单独使用 `dev/Dockerfile` 和 `compose.yaml`。
- GitHub 备份远程 `github`：https://github.com/JimmyHuang037/-japan-collage-editor ，用户指定的公开代码仓库。私人素材/产物/凭据均不上传，Gitee 主远程尚未提供。

容器命令必须显式指定 Compose 文件，避免与上游 docker-compose.yml 混淆：

```bash
docker compose -f compose.yaml build editor
docker compose -f compose.yaml run --rm editor pnpm install --registry=https://registry.npmjs.org
docker compose -f compose.yaml up -d editor
```

仅绑定 WSL 回环地址 `127.0.0.1:3077`。宿主 Node/pnpm 不变。
