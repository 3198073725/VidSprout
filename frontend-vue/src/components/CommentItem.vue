<template>
  <div class="comment-item" :class="{ 'has-reply': hasReplies }">
    <div class="comment-main">
      <img 
        :src="comment.author_thumbnail_url || '/default-avatar.png'" 
        :alt="comment.author_name"
        class="comment-avatar"
      />
      <div class="comment-content">
        <div class="comment-header">
          <span class="comment-author">{{ comment.author_name || '匿名用户' }}</span>
          <span class="comment-date">{{ formatDate(comment.add_date) }}</span>
        </div>
        <div class="comment-text">{{ comment.text }}</div>
        
        <div class="comment-actions">
          <el-button 
            type="text" 
            size="small"
            @click="toggleReplyForm"
          >
            <el-icon><ChatDotRound /></el-icon>
            回复
          </el-button>
          
          <el-button 
            type="text" 
            size="small"
            :class="{ 'is-liked': comment.user_liked }"
            @click="handleLike"
            :loading="likeLoading"
          >
            <el-icon><StarFilled v-if="comment.user_liked" /><Star v-else /></el-icon>
            {{ comment.likes || 0 }}
          </el-button>
          
          <span v-if="comment.reply_count" class="reply-count">
            {{ comment.reply_count }} 条回复
          </span>
        </div>
      </div>
    </div>
    
    <!-- 回复表单 -->
    <div v-if="showReplyForm" class="reply-form">
      <el-input
        v-model="replyText"
        type="textarea"
        :rows="2"
        :placeholder="`回复 @${comment.author_name}...`"
        maxlength="500"
        show-word-limit
      />
      <div class="reply-form-actions">
        <el-button size="small" @click="cancelReply">取消</el-button>
        <el-button 
          type="primary" 
          size="small"
          @click="submitReply"
          :disabled="!replyText.trim()"
          :loading="submitLoading"
        >
          发表回复
        </el-button>
      </div>
    </div>
    
    <!-- 子评论 -->
    <div v-if="hasReplies" class="comment-children">
      <div 
        v-for="child in comment.children" 
        :key="child.uid" 
        class="child-comment"
      >
        <CommentItem
          :comment="child"
          :media-token="mediaToken"
          @reply-created="handleChildReplyCreated"
        />
      </div>
      
      <div v-if="hasMoreReplies" class="load-more-replies">
        <el-button 
          type="text" 
          size="small" 
          @click="loadMoreReplies"
          :loading="loadMoreLoading"
        >
          {{ loadMoreLoading ? '加载中...' : `查看更多回复 (还有 ${(comment.reply_count || 0) - (comment.children?.length || 0)} 条)` }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, StarFilled, ChatDotRound } from '@element-plus/icons-vue'
import type { CommentItem as CommentItemType } from '@/api/types'
import { likeComment, unlikeComment, createMediaComment, listMediaCommentsEnhanced } from '@/api/comments'
import { useAuthStore } from '@/stores/auth'

interface Props {
  comment: CommentItemType
  mediaToken: string
}

interface Emits {
  (e: 'reply-created'): void
  (e: 'like-updated'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const auth = useAuthStore()

const showReplyForm = ref(false)
const replyText = ref('')
const likeLoading = ref(false)
const submitLoading = ref(false)
const loadMoreLoading = ref(false)
const currentRepliesPage = ref(1)
const hasMoreRepliesData = ref(true)

const hasReplies = computed(() => {
  return props.comment.children && props.comment.children.length > 0
})

const hasMoreReplies = computed(() => {
  return hasMoreRepliesData.value && props.comment.reply_count && props.comment.reply_count > (props.comment.children?.length || 0)
})

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 30) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

async function handleLike() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  likeLoading.value = true
  try {
    if (props.comment.user_liked) {
      await unlikeComment(props.comment.uid)
      props.comment.user_liked = false
      props.comment.likes = Math.max(0, (props.comment.likes || 0) - 1)
      ElMessage.success('已取消点赞')
    } else {
      await likeComment(props.comment.uid)
      props.comment.user_liked = true
      props.comment.likes = (props.comment.likes || 0) + 1
      ElMessage.success('点赞成功')
    }
    emit('like-updated')
  } catch (error) {
    console.error('点赞操作失败:', error)
    ElMessage.error('操作失败，请稍后再试')
  } finally {
    likeLoading.value = false
  }
}

function toggleReplyForm() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  showReplyForm.value = !showReplyForm.value
  if (showReplyForm.value) {
    replyText.value = ''
  }
}

function cancelReply() {
  showReplyForm.value = false
  replyText.value = ''
}

async function submitReply() {
  if (!replyText.value.trim()) return
  
  submitLoading.value = true
  try {
    await createMediaComment(props.mediaToken, {
      text: replyText.value,
      parent: props.comment.uid
    })
    
    ElMessage.success('回复发表成功')
    showReplyForm.value = false
    replyText.value = ''
    emit('reply-created')
  } catch (error) {
    console.error('回复发表失败:', error)
    ElMessage.error('发表失败，请稍后再试')
  } finally {
    submitLoading.value = false
  }
}

async function loadMoreReplies() {
  if (loadMoreLoading.value) return
  
  loadMoreLoading.value = true
  try {
    // 加载下一页回复
    const nextPage = currentRepliesPage.value + 1
    const response = await listMediaCommentsEnhanced(props.mediaToken, {
      parent: props.comment.uid,
      page: nextPage,
      page_size: 10
    })
    
    if (response.results && response.results.length > 0) {
      // 确保 children 数组存在
      if (!props.comment.children) {
        props.comment.children = []
      }
      
      // 添加新加载的回复到现有列表
      props.comment.children.push(...response.results)
      currentRepliesPage.value = nextPage
      
      console.log(`✅ 已加载 ${response.results.length} 条回复`)
      
      // 检查是否还有更多
      if (!response.next || response.results.length === 0) {
        hasMoreRepliesData.value = false
      }
    } else {
      hasMoreRepliesData.value = false
      ElMessage.info('没有更多回复了')
    }
  } catch (error) {
    console.error('❌ 加载更多回复失败:', error)
    ElMessage.error('加载失败，请稍后再试')
  } finally {
    loadMoreLoading.value = false
  }
}

function handleChildReplyCreated() {
  emit('reply-created')
}
</script>

<style scoped>
.comment-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-main {
  display: flex;
  gap: 12px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 500;
  color: #333;
}

.comment-date {
  font-size: 12px;
  color: #999;
}

.comment-text {
  color: #333;
  line-height: 1.5;
  word-break: break-word;
}

.comment-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 8px;
}

.reply-count {
  font-size: 12px;
  color: #999;
}

.reply-form {
  margin-top: 12px;
  margin-left: 52px;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
}

.reply-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.comment-children {
  margin-top: 16px;
  margin-left: 52px;
  border-left: 3px solid #e8f4ff;
  padding-left: 20px;
  background: #fafbfc;
  border-radius: 0 8px 8px 0;
  padding: 12px 20px 0 20px;
}

.child-comment {
  padding: 12px 0;
  position: relative;
}

.child-comment::before {
  content: '';
  position: absolute;
  left: -20px;
  top: 24px;
  width: 12px;
  height: 2px;
  background: #e8f4ff;
}

.load-more-replies {
  text-align: center;
  padding: 8px 0;
}

.is-liked {
  color: #409eff !important;
}

.has-reply {
  border-bottom: none;
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .comment-item {
  border-bottom-color: #333;
}

[data-theme="dark"] .comment-author {
  color: #ffffff;
}

[data-theme="dark"] .comment-time {
  color: #888;
}

[data-theme="dark"] .comment-text {
  color: #cccccc;
}

[data-theme="dark"] .comment-actions .action-btn {
  color: #999;
}

[data-theme="dark"] .comment-actions .action-btn:hover {
  color: #4a9eff;
}

[data-theme="dark"] .is-liked {
  color: #4a9eff !important;
}

[data-theme="dark"] .reply-count {
  color: #888;
}

[data-theme="dark"] .reply-form {
  background: #2a2a2a;
}

[data-theme="dark"] .comment-children {
  border-left-color: #404040;
  background: #1f1f1f;
}

[data-theme="dark"] .child-comment::before {
  background: #404040;
}
</style>