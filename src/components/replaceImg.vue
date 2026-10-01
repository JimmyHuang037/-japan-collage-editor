<!--
 * @Author: 秦少卫
 * @Date: 2023-04-06 22:26:57
 * @LastEditors: 秦少卫
 * @LastEditTime: 2024-10-07 17:15:32
 * @Description: 图片替换
-->

<template>
  <div v-if="isOne && type === 'image'" class="attr-item-box">
    <div class="bg-item">
      <Button @click="repleace" type="text" long>{{ $t('repleaceImg') }}</Button>
    </div>
  </div>
</template>

<script setup name="ReplaceImg">
import useSelect from '@/hooks/select';

import { Utils } from '@kuaitu/core';
const { getImgStr, selectFiles, insertImgFile } = Utils;

const update = getCurrentInstance();
// const canvasEditor = inject('canvasEditor');
const { canvasEditor, isOne } = useSelect();
const type = ref('');

// 替换图片
const repleace = async () => {
  const activeObject = canvasEditor.canvas.getActiveObjects()[0];
  if (activeObject && activeObject.type === 'image') {
    // 图片
    const [file] = await selectFiles({ accept: 'image/*', multiple: false });
    if (!file) return;
    const bytes = await file.arrayBuffer();
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    const hash = Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, '0')).join(
      ''
    );
    // 转字符串
    const fileStr = await getImgStr(file);
    // 字符串转El
    const imgEl = await insertImgFile(fileStr);
    const width = activeObject.get('width');
    const height = activeObject.get('height');
    const scaleX = activeObject.get('scaleX');
    const scaleY = activeObject.get('scaleY');
    const center = activeObject.getCenterPoint();
    activeObject.setSrc(imgEl.src, () => {
      const scale = Math.min((width * scaleX) / imgEl.width, (height * scaleY) / imgEl.height);
      activeObject.set({
        scaleX: scale,
        scaleY: scale,
        photoId: '',
        originalName: file.name,
        sourceHash: hash,
      });
      activeObject.setPositionByOrigin(center, 'center', 'center');
      activeObject.setCoords();
      activeObject.set('originSrc', imgEl.src);
      canvasEditor.canvas.renderAll();
      canvasEditor.saveState();
    });
    imgEl.remove();
  }
};

const init = () => {
  const activeObject = canvasEditor.canvas.getActiveObjects()[0];
  if (activeObject) {
    type.value = activeObject.type;
    update?.proxy?.$forceUpdate();
  }
};

onMounted(() => {
  canvasEditor.on('selectOne', init);
});

onBeforeUnmount(() => {
  canvasEditor.off('selectOne', init);
});
</script>
<style lang="less" scoped>
.attr-item-box {
  margin-top: 8px;
}
</style>
