<template>
  <div class="save-box">
    <Button @click="save" :loading="busy" data-testid="save-project">保存工程</Button>
    <Button type="primary" @click="canvasEditor.saveImg()" data-testid="export-png">
      导出 PNG
    </Button>
  </div>
</template>
<script setup lang="ts">
import useSelect from '@/hooks/select';
import { Message } from 'view-ui-plus';
import { portableJSON, download, projectState } from '@/travel/local';
const { canvasEditor } = useSelect();
const busy = ref(false);
async function save() {
  busy.value = true;
  try {
    const json = await portableJSON(canvasEditor);
    download(
      new Blob([JSON.stringify(json)], { type: 'application/json' }),
      projectState.name + '.json'
    );
    Message.success('工程已保存，包含完整照片，可重新导入');
  } catch (error: any) {
    Message.error(error.message);
  } finally {
    busy.value = false;
  }
}
</script>
<style scoped>
.save-box {
  display: flex;
  gap: 8px;
  margin-right: 12px;
}
</style>
