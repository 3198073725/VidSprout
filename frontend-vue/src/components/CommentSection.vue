<template>
  <div class="comment-section">
    <div class="comment-header">
      <h3 class="comment-title">
        评论 
        <span v-if="totalCount" class="comment-count">({{ totalCount }})</span>
      </h3>
      
      <!-- 排序选项 -->
      <div class="comment-sort">
        <el-radio-group v-model="sortBy" size="small" @change="handleSortChange">
          <el-radio-button label="newest">最新</el-radio-button>
          <el-radio-button label="hottest">最热</el-radio-button>
          <el-radio-button label="most_liked">最多点赞</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    
    <!-- 评论表单 -->
    <div class="comment-form-section">
      <div class="comment-form-header">
        <img 
          v-if="auth.profile?.thumbnail_url" 
          :src="auth.profile.thumbnail_url" 
          class="user-avatar"
        />
        <div v-else class="user-avatar-placeholder">
          <el-icon><User /></el-icon>
        </div>
        <span class="user-name">{{ auth.profile?.name || '游客' }}</span>
      </div>
      
      <el-form @submit.prevent="submitComment">
        <el-form-item>
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="4"
            placeholder="分享你的想法..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item>
          <div class="form-actions">
            <el-button 
              type="primary" 
              @click="submitComment"
              :disabled="!newComment.trim() || submitLoading"
              :loading="submitLoading"
            >
              发表评论
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 评论列表 -->
    <div class="comments-list">
      <el-skeleton :loading="loading" animated>
        <template #template>
          <div v-for="n in 3" :key="n" class="comment-skeleton">
            <el-skeleton-item variant="circle" style="width: 40px; height: 40px;" />
            <div style="flex: 1; margin-left: 12px;">
              <el-skeleton-item variant="text" style="width: 30%; margin-bottom: 8px;" />
              <el-skeleton-item variant="text" style="width: 100%;" />
            </div>
          </div>
        </template>
        
        <template #default>
          <el-empty 
            v-if="!comments.length" 
            description="暂无评论，来发表第一条评论吧！"
            :image-size="80"
          />
          
          <div v-else class="comments-container">
            <CommentItem
              v-for="comment in comments"
              :key="comment.uid"
              :comment="comment"
              :media-token="mediaToken"
              @reply-created="handleReplyCreated"
              @like-updated="handleLikeUpdated"
            />
          </div>
        </template>
      </el-skeleton>
    </div>
    
    <!-- 分页 -->
    <div v-if="totalCount > pageSize" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="totalCount"
        layout="prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import CommentItem from './CommentItem.vue'
import type { CommentItem as CommentItemType, Paginated } from '@/api/types'
import { listMediaComments, createMediaComment } from '@/api/comments'
import { useAuthStore } from '@/stores/auth'

interface Props {
  mediaToken: string
}

const props = defineProps<Props>()

const auth = useAuthStore()

// 状态管理
const loading = ref(false)
const submitLoading = ref(false)
const newComment = ref('')
const comments = ref<CommentItemType[]>([])
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const sortBy = ref<'newest' | 'hottest' | 'most_liked'>('newest')

// 计算属性
const hasComments = computed(() => comments.value.length > 0)

// 将扁平的评论列表转换为树形结构
function buildCommentTree(flatComments: CommentItemType[]): CommentItemType[] {
  // 创建一个 Map 用于快速查找
  const commentMap = new Map<string, CommentItemType>()
  const rootComments: CommentItemType[] = []
  
  // 第一遍：创建所有评论的副本并建立索引
  flatComments.forEach(comment => {
    const commentCopy = { ...comment, children: [] }
    commentMap.set(comment.uid, commentCopy)
  })
  
  // 第二遍：建立父子关系
  flatComments.forEach(comment => {
    const commentCopy = commentMap.get(comment.uid)!
    
    if (comment.parent) {
      // 这是一个回复，找到它的父评论
      const parentComment = commentMap.get(comment.parent)
      if (parentComment) {
        if (!parentComment.children) {
          parentComment.children = []
        }
        parentComment.children.push(commentCopy)
      } else {
        // 如果找不到父评论（可能父评论被删除），作为根评论处理
        rootComments.push(commentCopy)
      }
    } else {
      // 这是一级评论
      rootComments.push(commentCopy)
    }
  })
  
  return rootComments
}

// 加载评论列表
async function loadComments() {
  loading.value = true
  try {
    // 调用评论API，传递排序参数
    const response: Paginated<CommentItemType> = await listMediaComments(
      props.mediaToken,
      {
        page: currentPage.value,
        sort: sortBy.value  // 传递排序参数：newest, hottest, most_liked
      }
    )
    
    // 将扁平的评论列表转换为树形结构
    comments.value = buildCommentTree(response.results)
    totalCount.value = response.count
  } catch (error) {
    console.error('加载评论失败:', error)
    ElMessage.error('加载评论失败，请稍后再试')
  } finally {
    loading.value = false
  }
}

// 提交评论
async function submitComment() {
  if (!newComment.value.trim()) return
  
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  submitLoading.value = true
  try {
    await createMediaComment(props.mediaToken, {
      text: newComment.value,
      parent: null
    })
    
    ElMessage.success('评论发表成功')
    newComment.value = ''
    
    // 重新加载评论列表
    await loadComments()
  } catch (error) {
    console.error('发表评讯失败:', error)
    ElMessage.error('发表失败，请稍后再试')
  } finally {
    submitLoading.value = false
  }
}

// 处理排序变化
async function handleSortChange() {
  currentPage.value = 1
  await loadComments()
}

// 处理分页变化
async function handlePageChange(page: number) {
  currentPage.value = page
  await loadComments()
  
  // 滚动到评论区域顶部
  const commentSection = document.querySelector('.comment-section')
  if (commentSection) {
    commentSection.scrollIntoView({ behavior: 'smooth' })
  }
}

// 处理回复创建
function handleReplyCreated() {
  // 重新加载评论列表以更新回复数
  loadComments()
}

// 处理点赞更新
function handleLikeUpdated() {
  // 可以在这里处理点赞数的变化
  console.log('点赞状态更新')
}

// 监听登录状态变化
auth.$subscribe(() => {
  // 用户登录/登出时重新加载评论
  loadComments()
})

onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.comment-section {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-top: 24px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.comment-title {
  font-size: 18px;
  font-weight: 500;
  margin: 0;
}

.comment-count {
  color: #999;
  font-weight: normal;
}

.comment-sort {
  display: flex;
  gap: 8px;
}

.comment-form-section {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.comment-form-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.comments-list {
  min-height: 200px;
}

.comments-container {
  border-top: 1px solid #f0f0f0;
}

.comment-skeleton {
  display: flex;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

@media (max-width: 768px) {
  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .comment-sort {
    align-self: stretch;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .comment-section {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .comment-title {
  color: #ffffff;
}

[data-theme="dark"] .comment-count {
  color: #999;
}

[data-theme="dark"] .comment-form-section {
  background: #2a2a2a;
}

[data-theme="dark"] .user-name {
  color: #ffffff;
}

[data-theme="dark"] .user-avatar-placeholder {
  background: #404040;
  color: #999;
}

[data-theme="dark"] .comments-container {
  border-top-color: #333;
}

[data-theme="dark"] .comment-skeleton {
  border-bottom-color: #333;
}

[data-theme="dark"] .pagination-container {
  border-top-color: #333;
}
</style>