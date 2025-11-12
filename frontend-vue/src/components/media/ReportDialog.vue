<script setup lang="ts">
import { ref, computed } from 'vue'
import { MediaAPI } from '@/api'
import { ElMessage } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'

interface Props {
  modelValue: boolean
  mediaToken: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'reported'): void
}>()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const submitting = ref(false)
const reportForm = ref({
  reason: '',
  details: ''
})

// 举报原因选项
const reportReasons = [
  { value: 'spam', label: '垃圾内容' },
  { value: 'inappropriate', label: '不当内容' },
  { value: 'violence', label: '暴力内容' },
  { value: 'hate_speech', label: '仇恨言论' },
  { value: 'harassment', label: '骚扰或欺凌' },
  { value: 'sexual_content', label: '性相关内容' },
  { value: 'copyright', label: '版权侵犯' },
  { value: 'misinformation', label: '虚假或误导信息' },
  { value: 'illegal', label: '非法内容' },
  { value: 'other', label: '其他原因' }
]

// 重置表单
function resetForm() {
  reportForm.value = {
    reason: '',
    details: ''
  }
}

// 提交举报
async function handleSubmit() {
  if (!reportForm.value.reason) {
    ElMessage.warning('请选择举报原因')
    return
  }
  
  submitting.value = true
  try {
    // 获取举报原因的中文标签
    const reasonLabel = reportReasons.find(r => r.value === reportForm.value.reason)?.label || reportForm.value.reason
    
    // 构造额外信息
    const extraInfo = {
      reason: reasonLabel, // 使用中文标签
      description: reportForm.value.details || ''
    }
    
    console.log('📤 提交举报:', {
      mediaToken: props.mediaToken,
      extraInfo
    })
    
    // 调用举报API，传递额外信息
    await MediaAPI.createUserMediaAction(props.mediaToken, 'report', extraInfo)
    
    console.log('✅ 举报提交成功')
    ElMessage.success('举报已提交，感谢您的反馈！')
    visible.value = false
    resetForm()
    emit('reported')
  } catch (error: any) {
    console.error('❌ 举报失败:', error)
    ElMessage.error(error.message || '举报失败，请稍后再试')
  } finally {
    submitting.value = false
  }
}

// 对话框关闭时重置表单
function handleClose() {
  if (!submitting.value) {
    resetForm()
  }
}
</script>

<template>
  <el-dialog
    v-model="visible"
    title="举报内容"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div class="report-dialog-content">
      <div class="warning-tip">
        <el-icon color="#E6A23C" :size="20"><Warning /></el-icon>
        <span>请谨慎举报，我们会认真审核每一个举报。</span>
      </div>
      
      <el-form :model="reportForm" label-width="80px" label-position="top">
        <el-form-item label="举报原因" required>
          <el-select 
            v-model="reportForm.reason" 
            placeholder="请选择举报原因"
            style="width: 100%"
          >
            <el-option
              v-for="reason in reportReasons"
              :key="reason.value"
              :label="reason.label"
              :value="reason.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="详细说明（选填）">
          <el-input 
            v-model="reportForm.details" 
            type="textarea" 
            :rows="4"
            placeholder="请详细说明举报原因，帮助我们更快处理（选填）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false" :disabled="submitting">
          取消
        </el-button>
        <el-button 
          type="danger" 
          :loading="submitting"
          @click="handleSubmit"
        >
          提交举报
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.report-dialog-content {
  padding: 8px 0;
}

.warning-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fdf6ec;
  border: 1px solid #f5dab1;
  border-radius: 4px;
  margin-bottom: 24px;
  font-size: 14px;
  color: #e6a23c;
}

[data-theme="dark"] .warning-tip {
  background: #2b2111;
  border-color: #4d3b1f;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 表单样式 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--mc-text-primary, #222);
}

[data-theme="dark"] :deep(.el-form-item__label) {
  color: #cccccc;
}

:deep(.el-select),
:deep(.el-textarea) {
  width: 100%;
}
</style>

