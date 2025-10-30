<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="(value) => emit('update:visible', value)"
    title="搜索历史"
    width="800px"
  >
    <div class="space-y-4">
      <!-- 筛选器 -->
      <div class="flex items-center justify-between">
        <el-input
          v-model="searchQuery"
          placeholder="搜索关键词..."
          style="width: 300px"
          clearable
        >
          <template #prefix>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </template>
        </el-input>
        
        <el-button @click="loadHistory">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          刷新
        </el-button>
      </div>

      <!-- 历史记录列表 -->
      <div v-if="loading" class="flex justify-center py-8">
        <el-loading />
      </div>
      
      <div v-else-if="filteredHistory.length === 0" class="text-center py-8 text-gray-500">
        暂无搜索历史
      </div>
      
      <div v-else class="space-y-3 max-h-96 overflow-y-auto">
        <div
          v-for="item in filteredHistory"
          :key="item.session_id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors cursor-pointer"
          @click="selectHistory(item)"
        >
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-medium text-lg">{{ item.original_keyword }}</h3>
            <div class="flex items-center space-x-2">
              <el-tag
                :type="getStatusType(item.status)"
                size="small"
              >
                {{ getStatusText(item.status) }}
              </el-tag>
              <span class="text-sm text-gray-500">
                {{ formatDate(item.created_at) }}
              </span>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div class="flex flex-wrap gap-1">
              <el-tag
                v-for="type in item.variant_types"
                :key="type"
                size="small"
                effect="plain"
              >
                {{ getVariantTypeName(type) }}
              </el-tag>
            </div>
            
            <div class="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
                {{ item.total_suggestions }} 个建议词
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <el-button @click="handleClose">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { storeToRefs } from 'pinia'
import { useKeywordStore } from '@/stores/keyword'
import { keywordApi } from '@/utils/api'
import { formatDate } from '@/utils'
import type { SearchHistory } from '@/types/api'

interface Props {
  visible: boolean
}

interface Emits {
  (e: 'update:visible', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Store
const keywordStore = useKeywordStore()
const { searchHistory, variantTypes } = storeToRefs(keywordStore)

// 数据
const loading = ref(false)
const searchQuery = ref('')

// 计算属性
const filteredHistory = computed(() => {
  if (!searchQuery.value) return searchHistory.value
  
  return searchHistory.value.filter(item =>
    item.original_keyword.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法
const getVariantTypeName = (type: string): string => {
  return variantTypes.value[type] || type
}

const getStatusType = (status: string): string => {
  const types: Record<string, string> = {
    pending: 'warning',
    running: 'primary',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string): string => {
  const texts: Record<string, string> = {
    pending: '待处理',
    running: '分析中',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

const loadHistory = async () => {
  loading.value = true
  try {
    const history = await keywordApi.getSearchHistory(20)
    keywordStore.setSearchHistory(history)
  } catch (error) {
    ElMessage.error('加载历史记录失败')
  } finally {
    loading.value = false
  }
}

const selectHistory = async (item: SearchHistory) => {
  if (item.status !== 'completed') {
    ElMessage.warning('该记录尚未完成分析')
    return
  }
  
  try {
    const result = await keywordApi.getSessionResults(item.session_id)
    keywordStore.setCurrentAnalysis(result)
    handleClose()
    ElMessage.success('已加载历史记录')
  } catch (error) {
    ElMessage.error('加载分析结果失败')
  }
}

const handleClose = () => {
  emit('update:visible', false)
}

// 监听弹窗显示状态
watch(
  () => props.visible,
  (newVisible) => {
    if (newVisible) {
      loadHistory()
    }
  }
)
</script>