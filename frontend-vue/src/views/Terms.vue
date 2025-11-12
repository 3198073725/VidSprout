<script setup lang="ts">
import { ref } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'

const activeNames = ref(['1'])
const lastUpdated = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
</script>

<template>
  <section class="home-sec terms-page">
    <div class="home-sec-head">
      <div class="home-sec-title">使用条款与服务协议</div>
    </div>

    <!-- 更新时间提示 -->
    <el-alert
      type="info"
      :closable="false"
      show-icon
      class="terms-alert"
    >
      <template #title>
        最后更新时间：{{ lastUpdated }}
      </template>
    </el-alert>

    <el-card class="terms-card">
      <div class="terms-intro">
        <p>
          <el-icon><InfoFilled /></el-icon>
          欢迎使用短视频平台！在使用本平台服务之前，请仔细阅读以下条款和协议。
          使用本平台即表示您同意遵守这些条款。
        </p>
      </div>

      <el-collapse v-model="activeNames" class="terms-collapse">
        <!-- 服务条款 -->
        <el-collapse-item name="1">
          <template #title>
            <h3 class="collapse-title">1. 服务条款</h3>
          </template>
          <div class="terms-content">
            <h4>1.1 服务范围</h4>
            <p>
              本平台为用户提供视频、音频、图片等多媒体内容的上传、管理、分享和浏览服务。
              我们致力于为用户提供安全、稳定、高效的服务体验。
            </p>

            <h4>1.2 账户注册</h4>
            <p>
              用户需要注册账户才能使用完整功能。注册时请提供真实、准确的信息。
              您有责任维护账户安全，不得将账户转让给他人使用。
            </p>

            <h4>1.3 服务变更</h4>
            <p>
              我们保留随时修改、暂停或终止服务的权利，无需事先通知。
              我们会尽力提前通知重大变更，但不承担因服务变更造成的损失。
            </p>

            <h4>1.4 免责声明</h4>
            <p>
              本平台不对用户上传的内容负责。我们不保证服务的连续性、安全性或无错误。
              用户使用本服务的风险由用户自行承担。
            </p>
          </div>
        </el-collapse-item>

        <!-- 隐私政策 -->
        <el-collapse-item name="2">
          <template #title>
            <h3 class="collapse-title">2. 隐私政策</h3>
          </template>
          <div class="terms-content">
            <h4>2.1 信息收集</h4>
            <p>
              我们收集您在注册、使用服务过程中提供的个人信息，包括但不限于：
              用户名、邮箱、头像、上传的媒体内容等。这些信息用于提供和改进服务。
            </p>

            <h4>2.2 信息使用</h4>
            <p>
              我们使用收集的信息来：
            </p>
            <ul>
              <li>提供、维护和改进我们的服务</li>
              <li>个性化用户体验</li>
              <li>发送通知和更新</li>
              <li>防止欺诈和滥用行为</li>
              <li>遵守法律要求</li>
            </ul>

            <h4>2.3 信息共享</h4>
            <p>
              我们不会向第三方出售您的个人信息。在以下情况下，我们可能共享您的信息：
            </p>
            <ul>
              <li>获得您的明确同意</li>
              <li>遵守法律要求或响应法律程序</li>
              <li>保护我们的权利、财产或安全</li>
            </ul>

            <h4>2.4 数据安全</h4>
            <p>
              我们采取适当的技术和组织措施来保护您的个人信息安全，
              包括加密存储、访问控制等。但请注意，没有任何系统是完全安全的。
            </p>
          </div>
        </el-collapse-item>

        <!-- 用户行为规范 -->
        <el-collapse-item name="3">
          <template #title>
            <h3 class="collapse-title">3. 用户行为规范</h3>
          </template>
          <div class="terms-content">
            <h4>3.1 禁止行为</h4>
            <p>使用本平台时，您不得：</p>
            <ul>
              <li>上传违法、有害、威胁、辱骂、骚扰、诽谤等内容</li>
              <li>侵犯他人知识产权、隐私权或其他权利</li>
              <li>传播病毒、恶意代码或其他有害内容</li>
              <li>进行任何形式的网络攻击或破坏行为</li>
              <li>未经授权访问他人账户或系统</li>
              <li>发布虚假信息或进行欺诈活动</li>
              <li>滥用举报功能或其他平台功能</li>
            </ul>

            <h4>3.2 内容审核</h4>
            <p>
              我们保留审核、删除或限制任何违反本条款的内容的权利。
              对于违规用户，我们可能采取警告、限制功能、暂停或终止账户等措施。
            </p>

            <h4>3.3 知识产权</h4>
            <p>
              您上传的内容的知识产权归您所有。但您授予我们在全球范围内、
              免费、非独占的许可，以使用、复制、修改、发布和展示这些内容。
            </p>
          </div>
        </el-collapse-item>

        <!-- 用户权利 -->
        <el-collapse-item name="4">
          <template #title>
            <h3 class="collapse-title">4. 用户权利</h3>
          </template>
          <div class="terms-content">
            <h4>4.1 访问和控制</h4>
            <p>您有权：</p>
            <ul>
              <li>访问和更新您的个人信息</li>
              <li>删除您上传的内容</li>
              <li>请求删除您的账户和数据</li>
              <li>导出您的数据</li>
              <li>选择退出某些数据收集</li>
            </ul>

            <h4>4.2 数据可携带</h4>
            <p>
              您可以随时请求导出您在平台上的数据。我们将以常见的、
              机器可读的格式提供数据。
            </p>

            <h4>4.3 投诉和建议</h4>
            <p>
              如果您对我们的服务或隐私实践有任何疑问或投诉，
              请通过联系页面与我们联系。我们将尽快处理您的请求。
            </p>
          </div>
        </el-collapse-item>

        <!-- 法律责任 -->
        <el-collapse-item name="5">
          <template #title>
            <h3 class="collapse-title">5. 法律责任</h3>
          </template>
          <div class="terms-content">
            <h4>5.1 责任限制</h4>
            <p>
              在法律允许的最大范围内，我们不对以下情况承担责任：
            </p>
            <ul>
              <li>服务中断、延迟或错误</li>
              <li>数据丢失或损坏</li>
              <li>第三方行为造成的损失</li>
              <li>用户违规行为的后果</li>
              <li>不可抗力事件</li>
            </ul>

            <h4>5.2 赔偿</h4>
            <p>
              如果您违反本条款导致我们遭受损失，您同意赔偿我们的损失，
              包括但不限于法律费用、诉讼费用等。
            </p>

            <h4>5.3 适用法律</h4>
            <p>
              本条款受中华人民共和国法律管辖。任何争议应首先通过友好协商解决，
              协商不成的，提交有管辖权的人民法院解决。
            </p>
          </div>
        </el-collapse-item>

        <!-- 条款变更 -->
        <el-collapse-item name="6">
          <template #title>
            <h3 class="collapse-title">6. 条款变更</h3>
          </template>
          <div class="terms-content">
            <h4>6.1 修改权利</h4>
            <p>
              我们保留随时修改本条款的权利。重大变更将通过站内通知、
              邮件或其他方式通知用户。
            </p>

            <h4>6.2 生效时间</h4>
            <p>
              修改后的条款将在发布后立即生效。继续使用服务即表示您接受修改后的条款。
              如果您不同意修改，请停止使用服务。
            </p>

            <h4>6.3 历史版本</h4>
            <p>
              您可以随时查看本条款的历史版本。我们建议您定期查看本页面，
              以了解最新的条款内容。
            </p>
          </div>
        </el-collapse-item>

        <!-- 联系我们 -->
        <el-collapse-item name="7">
          <template #title>
            <h3 class="collapse-title">7. 联系我们</h3>
          </template>
          <div class="terms-content">
            <p>
              如果您对本条款有任何疑问或建议，或需要行使您的权利，
              请通过以下方式联系我们：
            </p>
            <ul>
              <li><strong>邮箱：</strong>legal@mediacms.example.com</li>
              <li><strong>电话：</strong>+86 010-1234-5678</li>
              <li><strong>地址：</strong>中国 北京市 朝阳区 XXX街道 XXX号</li>
              <li><strong>在线：</strong>访问"联系我们"页面提交反馈</li>
            </ul>
            <p class="terms-footer-note">
              我们会在收到您的请求后尽快处理，通常在30个工作日内给予答复。
            </p>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 底部确认 -->
    <el-card class="terms-confirm">
      <p class="confirm-text">
        <el-icon><InfoFilled /></el-icon>
        使用本平台即表示您已阅读、理解并同意遵守以上所有条款和协议。
      </p>
    </el-card>
  </section>
</template>

<style scoped>
.terms-page {
  max-width: 1000px;
  margin: 0 auto;
}

.terms-alert {
  margin-bottom: 20px;
}

.terms-card {
  margin-bottom: 20px;
}

.terms-intro {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.terms-intro p {
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  line-height: 1.6;
  color: #606266;
}

.terms-intro .el-icon {
  color: #409eff;
  margin-top: 3px;
  flex-shrink: 0;
}

.terms-collapse {
  border: none;
}

.collapse-title {
  margin: 0;
  font-size: 18px;
  color: #303133;
  font-weight: 600;
}

.terms-content {
  padding: 20px;
  line-height: 1.8;
}

.terms-content h4 {
  margin: 20px 0 12px 0;
  font-size: 16px;
  color: #409eff;
  font-weight: 600;
}

.terms-content h4:first-child {
  margin-top: 0;
}

.terms-content p {
  margin: 0 0 16px 0;
  color: #606266;
  text-align: justify;
}

.terms-content ul {
  margin: 12px 0;
  padding-left: 24px;
}

.terms-content li {
  margin: 8px 0;
  color: #606266;
  line-height: 1.6;
}

.terms-content strong {
  color: #303133;
  font-weight: 600;
}

.terms-footer-note {
  margin-top: 16px !important;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
  color: #909399;
}

.terms-confirm {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.confirm-text {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  justify-content: center;
}

.confirm-text .el-icon {
  font-size: 20px;
}

/* 暗色模式 */
[data-theme="dark"] .terms-alert :deep(.el-alert) {
  background: #262626;
  border-color: #404040;
  color: #cccccc;
}

[data-theme="dark"] .terms-alert :deep(.el-alert__title) {
  color: #4a9eff;
}

[data-theme="dark"] .terms-card :deep(.el-card),
[data-theme="dark"] .terms-confirm :deep(.el-card) {
  background: #1a1a1a !important;
  border-color: #333 !important;
}

[data-theme="dark"] .terms-card :deep(.el-card__body) {
  background: #1a1a1a !important;
}

[data-theme="dark"] .terms-card :deep(.el-card__header) {
  background: #1a1a1a !important;
  border-color: #333 !important;
}

[data-theme="dark"] .terms-intro {
  background: #262626;
  border: 1px solid #333;
}

[data-theme="dark"] .terms-intro p {
  color: #cccccc;
}

[data-theme="dark"] .terms-intro .el-icon {
  color: #4a9eff;
}

[data-theme="dark"] .collapse-title {
  color: #ffffff;
}

[data-theme="dark"] .terms-collapse :deep(.el-collapse-item__header) {
  background: #1a1a1a;
  border-color: #333;
  color: #ffffff;
}

[data-theme="dark"] .terms-collapse :deep(.el-collapse-item__wrap) {
  background: #1a1a1a;
  border-color: #333;
}

[data-theme="dark"] .terms-collapse :deep(.el-collapse-item__content) {
  background: #262626;
}

[data-theme="dark"] .terms-content h4 {
  color: #4a9eff;
}

[data-theme="dark"] .terms-content p,
[data-theme="dark"] .terms-content li {
  color: #cccccc;
}

[data-theme="dark"] .terms-content strong {
  color: #ffffff;
}

[data-theme="dark"] .terms-footer-note {
  background: #1a1a1a;
  border: 1px solid #333;
  color: #999;
}

[data-theme="dark"] .terms-confirm {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

[data-theme="dark"] .terms-confirm :deep(.el-card__body) {
  background: transparent;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .terms-page {
    padding: 12px;
  }

  .collapse-title {
    font-size: 16px;
  }

  .terms-content {
    padding: 16px;
  }

  .terms-content h4 {
    font-size: 15px;
  }

  .confirm-text {
    font-size: 14px;
    text-align: left;
  }
}
</style>
