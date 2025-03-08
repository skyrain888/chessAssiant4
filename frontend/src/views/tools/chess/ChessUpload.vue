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
          
          <div class="upload-area">
            <a-upload
              action="/api/chess/upload"
              :file-list="fileList"
              :limit="1"
              :show-file-list="false"
              :accept="'image/*'"
              :disabled="uploadLoading"
              @before-upload="beforeUpload"
              @success="onUploadSuccess"
              @error="onUploadError"
            >
              <template #upload-button>
                <div class="upload-trigger">
                  <div v-if="!imageUrl" class="upload-placeholder">
                    <icon-upload :style="{ fontSize: '32px' }" />
                    <p class="mt-2">点击或拖拽上传棋谱图片</p>
                    <p class="text-gray-400 text-xs mt-1">支持JPG、PNG格式</p>
                  </div>
                  <div v-else class="upload-preview">
                    <img :src="imageUrl" alt="棋谱图片" class="preview-image" />
                  </div>
                </div>
              </template>
            </a-upload>
          </div>
          <div class="mt-4">
            <a-select v-model="selectedModel" placeholder="选择解析模型" style="width: 100%">
              <a-option value="gpt-4-vision">GPT-4 Vision</a-option>
              <a-option value="gemini-pro-vision">Gemini Pro Vision</a-option>
              <a-option value="claude-3">Claude 3</a-option>
            </a-select>
          </div>
          <div class="mt-4">
            <a-button type="primary" long :loading="parseLoading" :disabled="!imageUrl" @click="parseImage">
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import {
  IconUpload,
  IconImage,
  IconCodeBlock
} from '@arco-design/web-vue/es/icon'
import http from '@/utils/http'

// 路由
const router = useRouter()

// 加载状态
const loading = ref(false)
const uploadLoading = ref(false)
const parseLoading = ref(false)

// 图片URL
const imageUrl = ref('')
const fileList = ref([])

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

// 上传前验证
const beforeUpload = (file: File) => {
  // 验证文件类型
  if (!supportedImageFormats.includes(file.type)) {
    Message.error(`不支持的文件类型: ${file.type}，请上传 JPG 或 PNG 格式的图片`)
    return false
  }
  
  // 验证文件大小
  const fileSize = file.size
  if (fileSize > maxUploadSize) {
    Message.error(`文件大小不能超过 5MB`)
    return false
  }
  
  uploadLoading.value = true
  return true
}

// 上传成功处理
const onUploadSuccess = (result: any) => {
  uploadLoading.value = false
  if (result && result.url) {
    imageUrl.value = result.url
    Message.success('图片上传成功')
    
    // 如果上传结果中包含自动解析的棋谱步骤
    if (result.moves) {
      form.moves = result.moves
      Message.success('棋谱已自动解析')
    }
  }
}

// 上传失败处理
const onUploadError = () => {
  uploadLoading.value = false
  Message.error('图片上传失败')
}

// 解析图片
const parseImage = async () => {
  if (!imageUrl.value) {
    Message.error('请先上传图片')
    return
  }

  try {
    parseLoading.value = true
    const response: any = await http.post('/chess/parse', {
      image_url: imageUrl.value,
      model: selectedModel.value
    })
    
    if (response && response.moves) {
      form.moves = response.moves
      Message.success('棋谱解析成功')
    } else {
      Message.error('棋谱解析失败，请重试')
    }
  } catch (err) {
    console.error('解析棋谱失败:', err)
    Message.error('解析棋谱失败')
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

  try {
    loading.value = true
    const response: any = await http.post('/chess/notation', {
      title: form.title,
      description: form.description,
      moves: form.moves,
      difficulty: form.difficulty,
      tags: form.tags,
      image_url: imageUrl.value
    })

    if (response) {
      Message.success('棋谱保存成功')
      router.push('/chess/list')
    }
  } catch (err) {
    console.error('保存棋谱失败:', err)
    Message.error('保存棋谱失败')
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
  imageUrl.value = ''
  fileList.value = []
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
  margin-bottom: 20px;
}

.upload-trigger {
  width: 100%;
  height: 200px;
  border: 2px dashed var(--color-border-2);
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-trigger:hover {
  border-color: #165dff;
}

.upload-placeholder {
  text-align: center;
  color: #86909c;
}

.upload-preview {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.mt-4 {
  margin-top: 16px;
}

.mt-2 {
  margin-top: 8px;
}

.mt-1 {
  margin-top: 4px;
}

.text-gray-400 {
  color: #c9cdd4;
}

.text-xs {
  font-size: 12px;
}
</style> 