# 日本旅行拼贴 · 续接入口

更新：2026-10-01，Asia/Shanghai。本文件为当前状态。旧交接归档在 `docs/history/`，其中旧授权阻塞与尚未实施的描述不代表现在。

## 最新视觉细化（2026-10-01）

用户提供抖音旅行拼贴截图，要求按参考细化拼贴。已细化 **04 宇治、08 生日** 两页，继续保留九图的 7+2 结构与原快图 UI。改为错落旋转相框、撕纸故事卡、半透明胶带、植物纸花、手绘音符/蛋糕/箭头；保留 2400×2400 画布、原故事及全部原片。装饰使用 Fabric 原生矢量，独立可编辑。

- `scripts/scrapbook.py` 是新排版源，`build_nine.py` 调用；旧排版与产物完整备份在 `outputs/history/before-reference-refinement-2026-10-01/`。
- 本机 Windows 的 simkai.ttf、Inkfree.ttf 复制到私有 `public/travel/fonts/`，编辑器本地加载“旅行楷体”、TravelHand。新增 CSS、字体列表和打开工程时字体预加载。系统字体不提交、不打入交付 ZIP；其他 Fabric 环境缺字体时可能回退。
- 真实浏览器验收仍通过：独立胶带、换图比例、撤销重做、旋转缩放边界、组合拆组、文字编辑、保存重导入、导出；没有浏览器异常或外部 HTTP 请求。容器构建、修改 TS 的 ESLint、差异空白检查通过；原片字节验证保留。
- 本轮交付目录为 `/home/jimmyhuang/.codex-wsl/Documents/Codex/2026-10-01/files-mentioned-by-the-user-codex/outputs`；含新版成图、内嵌工程、完整九图包，以及 `两张拼贴_成图与可编辑工程.zip`、`两张拼贴预览.jpg`。`package_refinement.py` 生成两页单独交付包。
- 当前编辑器仍为 http://127.0.0.1:3077/，刷新后左侧“九图”打开新版。切换或刷新前仍需手动保存个人修改。

细化版尚待用户视觉审核；未部署、公开或写入 Drive。GitHub 提交/推送状态见下方。

## 当前成果与授权

用户本次要求检查仓库与详细聊天历史，代理筛选并制作 **7 张原图 + 2 张拼贴**，每张继续在原快图 UI 编辑。九图初稿完成；真实浏览器功能验收通过，等待用户视觉反馈，未声称用户已批准审美。

沿用此前“其他同意，go”：WSL/Linux 容器开发、Drive 只读下载、快图必要修改、选片制作和本地交付均已授权，不重复确认。范围不含地图、个人网站、云写入、公开素材、生产部署或朋友圈发布。

独立 Git 根目录 `/home/jimmyhuang/japan-collage-editor`，分支 `codex/japan-collage`，上游基线为 `b3bdcfb0bd6d8f98e7483cf561ac03ba56c0d889`。本地提交状态以 Git 为准，GitHub 备份远程见文末，Gitee 主远程尚未配置；`upstream` 只是开源来源。保留既有未提交文件、`data/pre-clone-unfinished/`；后者未接入当前应用。

## 历史复核与故事

已详细读原始《朋友圈创意编辑整理》（ChatGPT ID `6ab12fba-3fe4-83e8-a73c-a04ea05cb05c`）用户原文、9月21/22日实施会话，以及今日启动/授权会话（Codex ID `01a0f6d2-93d0-72b1-bff3-a4c658d64345`）。核对 AGENTS、旧交接与 `data/reference/HANDOFF.md`；该私有参考文件继续保存九章节故事。

新作品顺序：USJ、奈良、京都、**宇治拼贴**、诹访花火、富士山、东京、**生日与童心拼贴**、镰仓看海。

宇治含京吹巡礼、任天堂、与浙江兄弟和小马三人夜爬大吉山；生日页含哆啦 A 梦咖啡馆、任意门、九个隐藏道具、富士秋千与生日和牛。没有找到可明确对应香港夫妇/上海家庭的合照，不冒认照片。文件名日期不作为核实后的拍摄时间。

## 素材与选片

- 最新 Drive 安全清单 `data/reference/drive-current.json`：1,483 张图片。
- 取得全部预览并看完31张联系表（`outputs/screening/`），无预览失败；再比较33张候选原片，最终18张不同原片入选。
- 本轮新增26张候选原片，本地素材共92张。33候选均通过Drive MD5校验；没有全量下载1,483张原片。
- `data/screening/index.json` 与 `candidates.json` 是安全索引；签名缩略图URL只在下载进程内存，不写入索引、工程或交付包。
- Drive 196组文件MD5相同，保留所有ID，不删除或按同名覆盖，只避免重复入选。
- 原片在 `data/originals/<Drive ID>.jpg`；本地目录 `public/travel/catalog.json`；`public/travel/photos` 相对链接至原片目录。
- 所用18张原片、七张单图、九个内嵌工程的字节校验在 `outputs/draft-nine/source-verification.json`。

## 编辑器实现

保留正式 clone 快图的原入口、布局和左右栏、画布、原生工具；没有另写独立编辑器。

- 左侧“九图”打开九个原生 Fabric 工程；“照片”使用本地92张素材，支持勾选替换当前照片。原生元素、图层、导入、预览、撤销重做继续使用。
- `src/travel/local.ts` 负责照片保护、横竖换片、打开与内嵌保存。照片完整等比缩放，禁用裁切、滤镜、翻转、拉伸、图像阴影/描边；旋转和移动时调整至画布内，支持多选和分组。Fabric 保存精度提高至8位。
- `ServersPlugin.ts` 保留 photoId/originalName/sourceHash/name；`GroupPlugin.ts` 组合克隆保留元数据，拆组保留ID。
- 顶部“保存工程”下载含完整原片的JSON，“导出PNG”使用快图原生导出。文件菜单重导入JSON。固定模板使用本地ID路径；下载工程的原片为data:image字节，不依赖Drive临时链接、blob或本地软链接。
- 本地字体/尺寸列表替代默认外部API；移除云上传/登录/模板保存入口与百度统计。验收期间无外部HTTP请求。CSP限制连接、图片与字体来源。
- 字体来自已有仓库，系统字体允许正常回退；字体选择器显示名称，英文缺少的翻译回退中文。
- **切换作品或刷新前手动点击“保存工程”**。左侧始终打开固定初稿，不自动覆盖原工程，不做云同步。

## 产物与复现

私有产物 `outputs/draft-nine/`：images恰好七张原始JPEG、两张2400×2400 PNG；projects九个内嵌原片JSON；sources十八张原片备份；附总览、选片说明、配文与验收报告。

首版交付目录：`/home/jimmyhuang/.codex-wsl/Documents/Codex/2026-10-01/go-on-for-japan-travel-editor/outputs`，保留旧初稿。当前细化版交付目录见上方“最新视觉细化”。均只在本地交付。

制作顺序：`build_nine.py`生成JSON及七张原片直出 → `render_nine.py`真实浏览器点击原生PNG导出，生成拼贴/预览 → `check_travel.py`交互验收 → `package_nine.py <目标目录>`校验与打包。修改布局后重做对应步骤。

验收证据：`outputs/browser-acceptance/report.json` 与 `editor-nine.png`；往返保存样本 `roundtrip.json` 与PNG。旧check_original.py曾覆盖旧upstream-baseline文件，不能作为原版基线证据；以后该脚本存到editor-smoke，业务验收必须用check_travel.py。

## 通过的验收

- 九图与全部预览卡片加载；十八张嵌入原片字节/哈希保留。
- 原生独立胶带拖动、撤销重做，照片布局未改变。
- 横竖图互换、撤销重做，完整等比显示，元数据保留。
- 原生Shift角点缩放、旋转与边界拖动；多选组合、组合缩放与拆组。
- 原生文字编辑、JSON下载、刷新和文件菜单重新导入，文字与照片布局保留。
- 原生PNG导出2400×2400；无浏览器page errors、无外部HTTP请求。
- 容器生产构建通过；现有核心2文件/4测试通过；修改UI的ESLint与git diff --check通过。上游仍有少量警告。

## 当前运行与凭据

编辑器 `japan-collage-editor-1` 保留运行，仅绑定 `127.0.0.1:3077`。使用 `docker compose -f compose.yaml`，不能误用上游docker-compose.yml。依赖已在容器，不重复安装；Node20/pnpm8.4在Linux容器，QA使用 `japan-collage-qa:local` 与宿主只读Chromium缓存。

Drive只读OAuth今日已通过新容器刷新、下载验证。凭据仅在 `/home/jimmyhuang/.config/japan-collage/`，目录700、文件600；不提交、不进前端或镜像。除非实际刷新失败，不重复授权；未承诺永久有效。

## 下一次继续

先读本文件与AGENTS，核对运行和文件。优先根据用户对九图的视觉反馈调整候选与排版。夜爬自拍有原始雾感、和牛原片分辨率较低，继续保留真实原片，不擅自修复或重绘。用户视觉审核尚未完成。

## GitHub 推送（2026-10-01）

用户明确要求提交并推送 GitHub，随后提供 `git@github.com:JimmyHuang037/-japan-collage-editor.git`。实际核对该仓库为空且为公开仓库；按用户指定目标上传代码，私人照片、素材清单、工程产物、系统字体及凭据均被排除。GitHub 是备份，不改变全局 Gitee 优先规则；Gitee 地址仍未提供。

- SSH 实际确认登录 `JimmyHuang037`；远程 `github` 指向上述用户仓库，`upstream` 保留快图来源。
- 提交当前编辑器代码、容器配置、制作/验收脚本及文档，保留上游历史和许可；新增 Python 缓存与本地凭据忽略规则。
- 本轮差异空白检查、待提交文件隐私/凭据检查通过；此前的构建和浏览器验收结果沿用，未重新运行。
- 推送分支 `codex/japan-collage`，不触发上游 main 分支的 gh-pages 发布工作流。推送结果与提交 SHA 以 Git/远端实际状态为准。无生产部署或 Drive 写入，用户视觉审核仍待完成。

推送已成功：实现提交 `21ad467` 已上传 `github/codex/japan-collage` 并设为跟踪分支。容器内旅行代码 ESLint 补充检查通过。首次提交触发上游 Husky 在宿主运行格式化/检查，后续提交通过 HUSKY=0 避免宿主执行；未安装或修改宿主全局 Node/pnpm。记录更新提交随后同步同一分支。
