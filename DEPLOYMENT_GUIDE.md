# GitHub 部署指南

## 第一步：创建 Personal Access Token (PAT)

1. 打开 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置：
   - Note: `web-resource-contributor`
   - Expiration: `No expiration` 或 `1 year`
   - 勾选权限：`public_repo`
4. 点击 "Generate token"
5. **立即复制 token**（只显示一次）

---

## 第二步：在 GitHub 创建仓库

1. 打开 https://github.com/new
2. 设置：
   - Owner: `super006`
   - Repository name: `web-resource-contributor`
   - **必须选择 Public**（GitHub Actions 免费额度需要公开仓库）
   - 不要勾选 "Add a README file"
3. 点击 "Create repository"

---

## 第三步：添加 GitHub Secrets

1. 进入刚创建的仓库
2. 点击 "Settings" → 左侧 "Secrets and variables" → "Actions"
3. 点击 "New repository secret"
4. 添加以下 3 个 secrets：

### Secret 1: GITHUB_TOKEN
- Name: `GITHUB_TOKEN`
- Secret: 粘贴第一步的 PAT

### Secret 2: SITES_CONFIG
- Name: `SITES_CONFIG`
- Secret:
```json
{"sites":[{"name":"PNGDEX","url":"https://pngdex.com","description":"No Limit, No Account, Just Free transparent PNGs.","features":["Image Cropper","Image Splitter","Image Compressor","Image Resizer","Image Converter","Rotate Image","Strip EXIF","Watermark Image"],"tags":["png","transparent","free","design","images","tools"]}]}
```

### Secret 3: TARGETS_CONFIG
- Name: `TARGETS_CONFIG`
- Secret:
```json
{"targets":[{"repo":"neutraltone/awesome-stock-resources","category":"PNG Resources","priority":"high"},{"repo":"bradtraversy/design-resources-for-developers","category":"Images","priority":"high"},{"repo":"LisaDziuba/Awesome-Design-Tools","category":"Stock Images","priority":"medium"}]}
```

---

## 第四步：推送代码到 GitHub

在本地项目目录 `E:\project_2026\web-resource-contributor` 执行：

```powershell
# 初始化 git
git init

# 添加所有文件
git add .

# 创建首次提交
git commit -m "Initial commit: Web resource contributor"

# 关联远程仓库（替换 super006 为你的 GitHub 用户名）
git remote add origin https://github.com/super006/web-resource-contributor.git

# 推送到 GitHub
git push -u origin main
```

如果推送失败提示 `main` 分支不存在，执行：
```powershell
git branch -M main
git push -u origin main
```

---

## 第五步：启用 GitHub Actions

1. 打开仓库页面
2. 点击 "Actions" 标签
3. 如果看到 "I understand my workflows, go ahead and enable them"，点击启用
4. 应该看到 workflow "Daily Resource Submission"

---

## 第六步：测试运行

**手动触发测试：**
1. 点击 "Actions" → "Daily Resource Submission"
2. 点击右侧 "Run workflow" → "Run workflow"
3. 等待运行完成（约 1-3 分钟）
4. 检查日志确认是否成功提交 PR

**自动运行：**
- 每天北京时间 10:00（UTC 02:00）自动运行
- 每次最多提交 3 个 PR（避免被封）

---

## 常见问题

### Q: 需要公开仓库吗？
A: 是。GitHub Actions 对私有仓库有免费额度限制（2000 分钟/月），公开仓库无限制。代码公开无风险，敏感信息存储在 Secrets 中。

### Q: 如何添加更多目标仓库？
A: 编辑 `TARGETS_CONFIG` secret，添加更多 repo 条目。

### Q: 如何添加第二个网站？
A: 编辑 `SITES_CONFIG` secret，在 `sites` 数组中添加新对象。

### Q: 提交的 PR 会被接受吗？
A: 取决于目标仓库维护者。高质量资源 + 符合格式 = 更高通过率。

---

## 验证清单

- [ ] PAT 已创建并保存
- [ ] GitHub 仓库 `web-resource-contributor` 已创建（Public）
- [ ] 3 个 Secrets 已添加（GITHUB_TOKEN, SITES_CONFIG, TARGETS_CONFIG）
- [ ] 代码已推送到 GitHub
- [ ] Actions 已启用
- [ ] 手动触发测试成功
- [ ] 检查目标仓库是否有新 PR

完成后，系统每天自动运行。
