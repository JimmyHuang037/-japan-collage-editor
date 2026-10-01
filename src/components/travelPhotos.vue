<template>
  <div>
    <Divider plain orientation="left">本地原片</Divider>
    <Input v-model="query" placeholder="搜索原文件名" clearable />
    <Checkbox v-model="replace">替换当前选中的照片</Checkbox>
    <div class="photo-grid">
      <button
        v-for="row in filtered"
        :key="row.id"
        :title="row.originalName"
        :data-photo="row.id"
        @click="add(row)"
      >
        <img :src="row.thumb" :alt="row.originalName" loading="lazy" />
        <small>{{ row.originalName.split('/').pop() }}</small>
      </button>
    </div>
  </div>
</template>
<script setup lang="ts">
import useSelect from '@/hooks/select';
import { Message } from 'view-ui-plus';
import { placePhoto } from '@/travel/local';
const { canvasEditor } = useSelect();
const rows = ref<any[]>([]);
const query = ref('');
const replace = ref(false);
const filtered = computed(() => rows.value.filter((r) => r.originalName.includes(query.value)));
async function add(row: any) {
  if (replace.value && canvasEditor.canvas.getActiveObject()?.type !== 'image') {
    Message.info('先在画布中选中要替换的照片');
    return;
  }
  try {
    await placePhoto(canvasEditor, row, replace.value);
  } catch (error: any) {
    Message.error(error.message);
  }
}
onMounted(async () => {
  rows.value = await (await fetch('/travel/catalog.json')).json();
});
</script>
<style scoped>
.photo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 15px;
}
button {
  background: #f6f7f9;
  border: 0;
  border-radius: 4px;
  padding: 5px;
  cursor: pointer;
  overflow: hidden;
}
img {
  width: 100%;
  height: 120px;
  object-fit: contain;
}
small {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 10px;
}
</style>
