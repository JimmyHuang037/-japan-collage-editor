<template>
  <div class="travel-projects">
    <Divider plain orientation="left">日本旅行 · 九图初稿</Divider>
    <p class="hint">7 张原图 / 2 张拼贴。点开一张继续编辑。切换作品前请保存工程。</p>
    <Input v-model="query" placeholder="搜索作品" clearable />
    <button
      v-for="item in filtered"
      :key="item.id"
      class="project-card"
      :data-project="item.id"
      :disabled="projectState.busy"
      @click="open(item)"
    >
      <img :src="item.preview" :alt="item.name" />
      <strong>{{ item.name }}</strong>
      <span>{{ item.kind === 'photo' ? '原图直出' : '故事拼贴' }}</span>
    </button>
  </div>
</template>
<script setup lang="ts">
import useSelect from '@/hooks/select';
import { Message } from 'view-ui-plus';
import { openProject, projectState } from '@/travel/local';
const { canvasEditor } = useSelect();
const items = ref<any[]>([]);
const query = ref('');
const filtered = computed(() => items.value.filter((item) => item.name.includes(query.value)));
async function open(item: any) {
  try {
    const response = await fetch(item.project);
    if (!response.ok) throw new Error('工程读取失败');
    await openProject(canvasEditor, await response.json(), item.name);
  } catch (error: any) {
    Message.error(error.message);
  }
}
onMounted(async () => {
  const response = await fetch('/travel/projects/index.json');
  if (!response.ok) return;
  items.value = await response.json();
  if (items.value.length)
    await open(items.value.find((x) => x.kind === 'composite') || items.value[0]);
});
</script>
<style scoped>
.hint {
  color: #777;
  margin-bottom: 14px;
}
.project-card {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 12px 0;
  background: #f6f7f9;
  border: 1px solid #e5e5e5;
  border-radius: 5px;
  cursor: pointer;
  text-align: left;
}
.project-card img {
  width: 100%;
  height: 155px;
  object-fit: contain;
  background: #eee;
}
.project-card strong {
  display: block;
  margin: 8px 0 3px;
}
.project-card span {
  color: #777;
  font-size: 12px;
}
</style>
