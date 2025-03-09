<template>
  <div class="chess-upload-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="upload-header">
          <div class="upload-header-content">
            <div class="header-title">上传棋谱</div>
            <div class="header-divider"></div>
            <p class="header-subtitle">上传棋谱图片，系统将自动识别棋谱内容</p>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="12">
        <a-card>
          <div class="card-header">
            <div class="header-title">棋谱图片</div>
            <div class="header-divider"></div>
          </div>
          
          <div class="upload-area" @click="triggerFileInput" :class="{ 'is-loading': uploading }">
            <div v-if="uploading" class="loading-spinner"></div>
            <div v-else-if="fileList.length > 0" class="preview-container">
              <img :src="previewUrl" alt="预览图" class="preview-image" />
              <a-button type="primary" status="danger" size="small" class="remove-btn" @click.stop="removeImage">
                <icon-delete />
                删除
              </a-button>
            </div>
            <div v-else class="upload-placeholder">
              <icon-upload size="32" />
              <div class="upload-text">点击或拖拽上传棋谱图片</div>
              <div class="upload-hint">支持 JPG、PNG 格式</div>
            </div>
            <input
              ref="fileInputRef"
              type="file"
              accept="image/jpeg,image/png"
              class="file-input"
              @change="handleFileChange"
            />
          </div>
          <div class="mt-4">
            <a-select v-model="selectedModel" placeholder="选择解析模型" style="width: 100%">
              <a-option value="gpt-4-vision">GPT-4 Vision</a-option>
              <a-option value="gemini-pro-vision">Gemini Pro Vision</a-option>
              <a-option value="claude-3">Claude 3</a-option>
            </a-select>
          </div>
          <div class="mt-4">
            <a-button type="primary" long :loading="parseLoading" :disabled="!previewUrl" @click="parseImage">
              解析棋谱
            </a-button>
          </div>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card>
          <div class="card-header">
            <div class="header-title">棋谱信息</div>
            <div class="header-divider"></div>
          </div>
          
          <a-form :model="form" layout="vertical">
            <a-form-item field="title" label="标题" :rules="[{ required: true, message: '请输入标题' }]">
              <a-input v-model="form.title" placeholder="请输入棋谱标题" allow-clear />
            </a-form-item>
            <a-form-item field="description" label="描述">
              <a-textarea v-model="form.description" placeholder="请输入棋谱描述" allow-clear />
            </a-form-item>
            <a-form-item field="moves" label="棋谱步骤" :rules="[{ required: true, message: '请输入棋谱步骤' }]">
              <a-textarea
                v-model="form.moves"
                placeholder="请输入棋谱步骤，例如：1.e4 e5 2.Nf3 Nc6"
                :auto-size="{ minRows: 5, maxRows: 10 }"
                allow-clear
              />
            </a-form-item>
            <a-form-item field="difficulty" label="难度">
              <a-radio-group v-model="form.difficulty">
                <a-radio value="easy">简单</a-radio>
                <a-radio value="medium">中等</a-radio>
                <a-radio value="hard">困难</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item field="tags" label="标签">
              <a-input-tag v-model="form.tags" placeholder="输入标签后按回车" allow-clear />
            </a-form-item>
            <a-form-item>
              <a-space>
                <a-button type="primary" :loading="loading" @click="handleSubmit">保存棋谱</a-button>
                <a-button @click="resetForm">重置</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </a-card>
      </a-col>
    </a-row>

    <div class="upload-result" v-if="uploadResult">
      <div class="result-title">识别结果</div>
      <div class="result-content">{{ uploadResult }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Message, Modal } from '@arco-design/web-vue'
import {
  IconUpload,
  IconImage,
  IconCodeBlock,
  IconDelete
} from '@arco-design/web-vue/es/icon'
import { post, upload } from '@/utils/http'
import { isLoggedIn } from '@/utils/auth'

// 路由
const router = useRouter()

// 加载状态
const loading = ref(false)
const uploadLoading = ref(false)
const parseLoading = ref(false)

// 图片URL
const previewUrl = ref('')
const fileList = ref<any[]>([])

// 选择的模型
const selectedModel = ref('gpt-4-vision')

// 支持的图片格式
const supportedImageFormats = ['image/jpeg', 'image/png', 'image/jpg']

// 最大上传大小 (5MB)
const maxUploadSize = 5 * 1024 * 1024

// 表单数据
const form = reactive({
  title: '',
  description: '',
  moves: '',
  difficulty: 'medium',
  tags: [] as string[]
})

// 文件输入引用
const fileInputRef = ref<HTMLInputElement | null>(null)

// 上传状态
const uploading = ref(false)
const uploadResult = ref('')

// 在组件挂载时检查登录状态
onMounted(() => {
  // 检查用户是否已登录，如果未登录，提示用户登录
  if (!isLoggedIn()) {
    Modal.warning({
      title: '需要登录',
      content: '请先登录后再使用此功能',
      okText: '去登录',
      onOk: () => {
        router.push('/auth/login?redirect=' + encodeURIComponent(router.currentRoute.value.fullPath))
      }
    })
  }
})

// 触发文件输入点击
const triggerFileInput = () => {
  if (!uploading.value && fileInputRef.value) {
    fileInputRef.value.click()
  }
}

// 处理文件变化
const handleFileChange = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    
    // 验证文件
    if (!file.type.includes('image/')) {
      Message.error('请上传图片文件')
      return
    }
    
    // 创建预览URL
    previewUrl.value = URL.createObjectURL(file)
    
    // 调用上传函数
    handleCustomUpload({ file })
    
    // 重置input，允许重新选择同一文件
    input.value = ''
  }
}

// 上传文件
const handleCustomUpload = (options: any) => {
  // 验证选项和文件
  if (!options || !options.file) {
    console.error('上传选项或文件不存在', options)
    Message.error('上传文件不存在')
    return () => {}
  }

  const file = options.file
  
  // 验证文件是否为File实例
  if (!(file instanceof File)) {
    console.error('上传的不是有效的文件对象', file)
    Message.error('上传的不是有效的文件对象')
    return () => {}
  }
  
  // 验证文件大小
  if (file.size === 0) {
    console.error('文件大小为0', file)
    Message.error('文件大小为0，请选择有效文件')
    return () => {}
  }

  // 更新文件列表状态
  fileList.value = [{ 
    uid: '1', 
    name: file.name,
    status: 'uploading'
  }]
  
  uploading.value = true
  uploadResult.value = ''

  // 使用http.ts中的upload方法
  upload('/api/chess/upload', file, {
    validateFileType: true,
    fileTypes: supportedImageFormats,
    validateFileSize: true,
    maxSize: maxUploadSize / 1024 / 1024, // 转换为MB
    onUploadProgress: (progressEvent: any) => {
      if (progressEvent.lengthComputable) {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        console.log(`上传进度: ${percent}%`)
      }
    }
  })
    .then((response: any) => {
      console.log('上传成功:', response)
      
      // 更新文件列表状态
      fileList.value = [{ 
        uid: '1', 
        name: file.name,
        status: 'done',
        url: URL.createObjectURL(file)
      }]
      
      // 根据实际接口返回格式处理数据
      if (response && response.code === 200 && response.data && response.data.moves) {
        // 如果返回了标准格式的数据
        uploadResult.value = response.data.moves
        // 同时更新表单中的棋谱步骤
        form.moves = response.data.moves
      } else if (response && response.moves) {
        // 兼容直接返回 moves 字段的格式
        uploadResult.value = response.moves
        form.moves = response.moves
      } else if (response && response.data && response.data.result) {
        // 兼容旧的返回格式
        uploadResult.value = response.data.result
      } else {
        uploadResult.value = '识别成功，但未返回结果数据'
      }
      
      Message.success('上传成功')
    })
    .catch((error: any) => {
      console.error('上传失败:', error)
      handleUploadError(error.message || '上传失败，请稍后重试')
    })
    .finally(() => {
      uploading.value = false
    })

  // 返回中止上传的函数（注意：这里需要实现取消上传的功能）
  return () => {
    // 由于使用了http.ts的upload方法，这里需要调整取消逻辑
    // 目前简化处理，仅重置状态
    uploading.value = false
    fileList.value = []
    Message.info('上传已取消')
  }
}

// 解析图片
const parseImage = async () => {
  if (!previewUrl.value) {
    Message.error('请先上传图片')
    return
  }
  
  // 检查用户是否已登录
  const token = localStorage.getItem('token')
  console.log('当前登录状态:', isLoggedIn(), '令牌:', token ? '已存在' : '不存在')
  
  if (!isLoggedIn()) {
    Modal.warning({
      title: '需要登录',
      content: '请先登录后再使用解析功能',
      okText: '去登录',
      onOk: () => {
        router.push('/auth/login?redirect=' + encodeURIComponent(router.currentRoute.value.fullPath))
      }
    })
    return
  }

  try {
    parseLoading.value = true
    
    // 获取当前选择的文件
    const currentFile = fileList.value[0]
    if (!currentFile) {
      Message.error('文件不存在，请重新上传')
      return
    }
    
    console.log('开始解析棋谱，当前文件:', currentFile)
    
    // 创建FormData对象
    const formData = new FormData()
    
    let file = null
    
    // 从fileInputRef中获取实际的文件对象
    if (fileInputRef.value && fileInputRef.value.files && fileInputRef.value.files.length > 0) {
      file = fileInputRef.value.files[0]
      console.log('从fileInputRef获取到文件:', file.name, file.type, file.size)
    } else {
      // 如果无法从input获取文件，尝试从URL获取
      try {
        console.log('尝试从URL获取文件:', previewUrl.value)
        const response = await fetch(previewUrl.value)
        const blob = await response.blob()
        file = new File([blob], currentFile.name || 'image.png', { type: blob.type })
        console.log('从URL创建文件成功:', file.name, file.type, file.size)
      } catch (error) {
        console.error('无法获取图片文件:', error)
        Message.error('无法获取图片文件，请重新上传')
        return
      }
    }
    
    // 添加文件到FormData
    formData.append('file', file)
    
    // 添加模型参数
    formData.append('model', selectedModel.value)
    
    console.log('发送解析请求，模型:', selectedModel.value)
    
    // 使用axios直接发送请求，确保包含Authorization头
    const token = localStorage.getItem('token')
    console.log('发送请求前的令牌:', token ? '已存在' : '不存在')
    
    // 直接使用axios发送请求，确保正确设置Authorization头
    const axios = (await import('axios')).default
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
    
    console.log('使用axios直接发送请求到:', `${apiBaseUrl}/api/chess/parse`)
    console.log('Authorization头:', `Bearer ${token}`)
    
    const axiosResponse = await axios.post(`${apiBaseUrl}/api/chess/parse`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('axios响应状态:', axiosResponse.status)
    console.log('axios响应头:', axiosResponse.headers)
    console.log('axios响应数据:', axiosResponse.data)
    
    const response = axiosResponse.data
    
    // 根据实际接口返回格式处理数据
    if (response && response.code === 200 && response.data && response.data.moves) {
      // 设置棋谱步骤
      form.moves = response.data.moves
      // 同时设置识别结果，显示在界面上
      uploadResult.value = response.data.moves
      Message.success('棋谱解析成功')
    } else if (response && response.moves) {
      // 直接返回moves字段的格式
      form.moves = response.moves
      uploadResult.value = response.moves
      Message.success('棋谱解析成功')
    } else {
      console.error('解析响应格式不正确:', response)
      Message.error('棋谱解析失败，请重试')
    }
  } catch (err: any) {
    console.error('解析棋谱失败:', err)
    // 显示更详细的错误信息
    if (err.response) {
      console.error('错误响应状态码:', err.response.status)
      console.error('错误响应数据:', err.response.data)
      console.error('错误响应头:', err.response.headers)
      
      // 如果是401错误，提示用户登录
      if (err.response.status === 401) {
        Modal.warning({
          title: '登录已过期',
          content: '您的登录已过期，请重新登录',
          okText: '去登录',
          onOk: () => {
            // 清除过期的令牌
            localStorage.removeItem('token')
            localStorage.removeItem('refreshToken')
            router.push('/auth/login?redirect=' + encodeURIComponent(router.currentRoute.value.fullPath))
          }
        })
      } else if (err.response.status === 422) {
        // 422错误可能是请求格式问题，而不是登录问题
        console.error('请求验证失败，详细信息:', err.response.data)
        Message.error(`请求验证失败: ${err.response.data?.message || '请检查上传的文件格式和大小'}`)
      } else {
        Message.error(`解析棋谱失败: ${err.response.data?.message || err.message || '未知错误'}`)
      }
    } else if (err.request) {
      console.error('请求错误:', err.request)
      Message.error('网络请求失败，请检查网络连接')
    } else {
      Message.error(`解析棋谱失败: ${err.message || '未知错误'}`)
    }
  } finally {
    parseLoading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!form.title || !form.moves) {
    Message.error('请填写必填字段')
    return
  }
  
  // 检查用户是否已登录
  if (!isLoggedIn()) {
    Modal.warning({
      title: '需要登录',
      content: '请先登录后再保存棋谱',
      okText: '去登录',
      onOk: () => {
        router.push('/auth/login?redirect=' + encodeURIComponent(router.currentRoute.value.fullPath))
      }
    })
    return
  }

  try {
    loading.value = true
    const response: any = await post('/api/chess/notations', {
      title: form.title,
      description: form.description,
      moves: form.moves,
      difficulty: form.difficulty,
      tags: form.tags,
      image_url: previewUrl.value
    })

    if (response) {
      Message.success('棋谱保存成功')
      router.push('/chess/list')
    }
  } catch (err: any) {
    console.error('保存棋谱失败:', err)
    
    // 显示更详细的错误信息
    if (err.response) {
      console.error('错误响应:', err.response.status, err.response.data)
      
      // 如果是401或422错误，提示用户登录
      if (err.response.status === 401 || err.response.status === 422) {
        Modal.warning({
          title: '需要登录',
          content: '请先登录后再保存棋谱',
          okText: '去登录',
          onOk: () => {
            router.push('/auth/login?redirect=' + encodeURIComponent(router.currentRoute.value.fullPath))
          }
        })
      } else {
        Message.error(`保存棋谱失败: ${err.response.data?.message || err.message || '未知错误'}`)
      }
    } else if (err.request) {
      console.error('请求错误:', err.request)
      Message.error('网络请求失败，请检查网络连接')
    } else {
      Message.error(`保存棋谱失败: ${err.message || '未知错误'}`)
    }
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.title = ''
  form.description = ''
  form.moves = ''
  form.difficulty = 'medium'
  form.tags = []
  previewUrl.value = ''
  fileList.value = []
  uploadResult.value = ''
}

// 删除图片
const removeImage = (e: Event) => {
  e.stopPropagation()
  fileList.value = []
  uploadResult.value = ''
  previewUrl.value = ''
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
}

const handleUploadError = (message: string) => {
  uploading.value = false
  fileList.value = [{ 
    uid: '1', 
    name: fileList.value[0]?.name || '未知文件',
    status: 'error'
  }]
  Message.error(message)
}
</script>

<style scoped>
.chess-upload-container {
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.upload-header {
  margin-bottom: 16px;
}

.upload-header-content {
  text-align: center;
  padding: 8px 0;
}

.card-header {
  text-align: center;
  margin-bottom: 24px;
}

.header-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d2129;
  margin-bottom: 12px;
}

.header-divider {
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #165dff, #4080ff);
  margin: 0 auto 12px;
  border-radius: 2px;
}

.header-subtitle {
  color: #86909c;
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}

.upload-area {
  width: 100%;
  height: 200px;
  border: 2px dashed #c9cdd4;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  background-color: #f7f8fa;
  overflow: hidden;
}

.upload-area:hover {
  border-color: #165dff;
  background-color: rgba(22, 93, 255, 0.05);
}

.upload-area.is-loading {
  cursor: wait;
  pointer-events: none;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #86909c;
}

.upload-text {
  margin-top: 12px;
  font-size: 16px;
  color: #4e5969;
}

.upload-hint {
  margin-top: 8px;
  font-size: 13px;
  color: #86909c;
}

.file-input {
  display: none;
}

.preview-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.remove-btn {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.upload-result {
  margin-top: 24px;
  padding: 16px;
  border-radius: 8px;
  background-color: #f7f8fa;
  border: 1px solid #e5e6eb;
}

.result-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 12px;
  color: #1d2129;
}

.result-content {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: #ffffff;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #e5e6eb;
  max-height: 300px;
  overflow-y: auto;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
  border: 4px solid rgba(22, 93, 255, 0.2);
  border-top: 4px solid #165dff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 