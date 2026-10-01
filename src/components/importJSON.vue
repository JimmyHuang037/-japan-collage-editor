<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2024-05-31 16:58:12
 * @Description: 导入JSON文件
-->

<template>
  <div style="display: inline-block">
    <Dropdown @on-click="clickHandler">
      <a href="javascript:void(0)">
        {{ $t('importFiles.file') }}
        <Icon type="ios-arrow-down"></Icon>
      </a>
      <template #list>
        <DropdownMenu>
          <DropdownItem name="createDesign">
            {{ $t('importFiles.createDesign.title') }}
          </DropdownItem>
          <DropdownItem name="importFiles">{{ $t('importFiles.importFiles') }}</DropdownItem>
        </DropdownMenu>
      </template>
    </Dropdown>

    <!-- 创建设计 -->
    <modalSzie
      :title="$t('importFiles.createDesign.title')"
      ref="modalSizeRef"
      @set="customSizeCreate"
    ></modalSzie>
  </div>
</template>

<script name="ImportJson" setup>
import useSelect from '@/hooks/select';
import { Utils } from '@kuaitu/core';
import { openProject, projectState } from '@/travel/local';
import { Message } from 'view-ui-plus';
import modalSzie from '@/components/common/modalSzie';

const { canvasEditor } = useSelect();
const modalSizeRef = ref(null);

const clickHandler = (type) => {
  const handleMap = {
    // 导入文件
    importFiles: async () => {
      const files = await Utils.selectFiles({ accept: '.json', multiple: false });
      if (!files?.length) return;
      try {
        await openProject(
          canvasEditor,
          JSON.parse(await files[0].text()),
          files[0].name.replace(/\.json$/, '')
        );
      } catch (error) {
        Message.error(error.message || '工程导入失败');
      }
    },
    createDesign,
  };
  handleMap[type]?.();
};

const createDesign = () => {
  modalSizeRef.value.showSetSize();
};

const customSizeCreate = async (w, h) => {
  canvasEditor.clear();
  canvasEditor.setSize(w, h);
  canvasEditor.clearAndSaveState();
  projectState.name = '新旅行作品';
  Message.success('创建成功');
};
</script>
<style scoped lang="less">
h3 {
  margin-bottom: 10px;
}
.divider {
  margin-top: 0;
}
</style>
