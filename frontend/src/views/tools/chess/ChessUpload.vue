<template>
  <div class="chess-upload-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="upload-header">
          <template #title>
            <div class="flex items-center">
              <icon-upload class="mr-2" />
              <span>上传棋谱</span>
            </div>
          </template>
          <p class="text-gray-500">上传棋谱图片，系统将自动识别棋谱内容。</p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="12">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-image class="mr-2" />
              <span>棋谱图片</span>
            </div>
          </template>
          <div class="upload-area">
            <a-upload
              :custom-request="handleUpload"
              :show-file-list="false"
              :accept="'image/*'"
              :disabled="uploadLoading"
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
              <a-option v-for="model in supportedModels" :value="model">{{ model }}</a-option>
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
          <template #title>
            <div class="flex items-center">
              <icon-code-block class="mr-2" />
              <span>棋谱信息</span>
            </div>
          </template>
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
import { useChessStore } from '@/stores/chessStore'
import { useNotification } from '@/composables/useNotification'
import config from '@/config/env'
import {
  IconUpload,
  IconImage,
  IconCodeBlock
} from '@arco-design/web-vue/es/icon'

// 路由
const router = useRouter()

// 状态管理
const chessStore = useChessStore()
const { success, error } = useNotification()

// 加载状态
const loading = computed(() => chessStore.loading)
const uploadLoading = computed(() => chessStore.uploadLoading)
const parseLoading = computed(() => chessStore.parseLoading)

// 图片URL
const imageUrl = ref('')

// 选择的模型
const selectedModel = ref('gpt-4-vision')

// 支持的模型列表
const supportedModels = config.supportedModels

// 表单数据
const form = reactive({
  title: '',
  description: '',
  moves: '',
  difficulty: 'medium',
  tags: [] as string[]
})

// 处理图片上传
const handleUpload = async (options: any) => {
  try {
    const file = options.file
    
    // 验证文件类型
    if (!config.supportedImageFormats.includes(file.type)) {
      error(`不支持的文件类型: ${file.type}，请上传 JPG、PNG 或 GIF 格式的图片`)
      return
    }
    
    // 验证文件大小
    const fileSize = file.size / 1024 / 1024 // 转换为MB
    if (fileSize > config.uploadSizeLimit) {
      error(`文件大小不能超过 ${config.uploadSizeLimit}MB`)
      return
    }
    
    const result = await chessStore.uploadImage(file)
    if (result) {
      imageUrl.value = result.image_url
      success('图片上传成功')
      
      // 如果上传结果中包含自动解析的棋谱步骤
      if (result.moves) {
        form.moves = result.moves
        success('棋谱已自动解析')
      }
    }
  } catch (err) {
    error('图片上传失败')
  }
}

// 解析图片
const parseImage = async () => {
  if (!imageUrl.value) {
    error('请先上传图片')
    return
  }

  try {
    const moves = await chessStore.parseNotation(imageUrl.value, selectedModel.value)
    if (moves) {
      form.moves = moves
    }
  } catch (err) {
    error('解析棋谱失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!form.title || !form.moves) {
    error('请填写必填字段')
    return
  }

  try {
    const result = await chessStore.createNotation({
      title: form.title,
      description: form.description,
      moves: form.moves,
      difficulty: form.difficulty as 'easy' | 'medium' | 'hard',
      tags: form.tags
    })

    if (result) {
      success('棋谱保存成功')
      router.push('/chess/list')
    }
  } catch (err) {
    error('保存棋谱失败')
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
}
</script>

<style scoped>
.chess-upload-container {
  padding: 16px;
}

.upload-header {
  margin-bottom: 16px;
}

.upload-area {
  width: 100%;
}

.upload-trigger {
  width: 100%;
  height: 200px;
  border: 2px dashed var(--color-border-2);
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-trigger:hover {
  border-color: var(--color-primary);
}

.upload-placeholder {
  text-align: center;
  color: var(--color-text-3);
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
</style> 