import { fabric } from 'fabric';
import { reactive } from 'vue';

export const projectState = reactive({ name: '日本旅行', busy: false });
const walk = (object: any, fn: (o: any) => void) => {
  fn(object);
  (object.objects || object._objects || []).forEach((o: any) => walk(o, fn));
};
const hasPhoto = (object: any): boolean =>
  object.type === 'image' || (object._objects || []).some(hasPhoto);

// Apply to imported documents, native controls, groups, undo/redo and exports.
export function protectPhotos(editor: any) {
  fabric.Object.NUM_FRACTION_DIGITS = 8;
  const canvas = editor.canvas;
  canvas.uniformScaling = true;
  const normalize = () => {
    const workspace = editor.getWorkspase();
    if (!workspace) return;
    const active = canvas.getActiveObject();
    const roots = canvas.getObjects().filter((o: any) => o.group?.type !== 'activeSelection');
    if (active?.type === 'activeSelection') roots.push(active);
    roots.forEach((root: any) => {
      if (!hasPhoto(root)) return;
      walk(root, (o) => {
        if (!hasPhoto(o)) return;
        const scale = Math.max(0.0001, Math.min(Math.abs(o.scaleX || 1), Math.abs(o.scaleY || 1)));
        o.set({
          scaleX: scale,
          scaleY: scale,
          skewX: 0,
          skewY: 0,
          flipX: false,
          flipY: false,
          clipPath: undefined,
          lockSkewingX: true,
          lockSkewingY: true,
          lockScalingFlip: true,
          opacity: 1,
          shadow: null,
        });
        o.setControlsVisibility({ ml: false, mr: false, mt: false, mb: false });
        if (o.type === 'image') {
          const element = o.getElement();
          o.set({
            cropX: 0,
            cropY: 0,
            width: element.naturalWidth || element.width,
            height: element.naturalHeight || element.height,
            filters: [],
            opacity: 1,
            strokeWidth: 0,
            shadow: null,
          });
          if (o._filteredEl) {
            o._filteredEl = undefined;
            o._element = o._originalElement;
          }
        }
        o.setCoords();
      });
      let bounds = root.getBoundingRect(true, true);
      const fit = Math.min(1, workspace.width / bounds.width, workspace.height / bounds.height);
      if (fit < 1) {
        root.set({ scaleX: root.scaleX * fit, scaleY: root.scaleY * fit });
        root.setCoords();
        bounds = root.getBoundingRect(true, true);
      }
      root.set({
        left:
          root.left +
          Math.max(workspace.left - bounds.left, 0) -
          Math.max(bounds.left + bounds.width - workspace.left - workspace.width, 0),
        top:
          root.top +
          Math.max(workspace.top - bounds.top, 0) -
          Math.max(bounds.top + bounds.height - workspace.top - workspace.height, 0),
      });
      root.setCoords();
    });
  };
  canvas.on('before:render', normalize);
  const originalLoad = editor.loadJSON.bind(editor);
  editor.loadJSON = async (input: any, callback?: () => void) => {
    const json = typeof input === 'string' ? JSON.parse(input) : input;
    if (json.backgroundImage || json.overlayImage) throw new Error('请将照片作为独立图层导入');
    walk(json, (o) => {
      if (o.type !== 'image') return;
      const src = o.src || '';
      const local =
        src.startsWith('/travel/photos/') || /^data:image\/(jpeg|png|webp);base64,/.test(src);
      if (!local) throw new Error('请使用本地原片或已打包的旅行工程');
      o.filters = [];
      o.resizeFilter = null;
      o.clipPath = undefined;
      o.cropX = 0;
      o.cropY = 0;
      o.flipX = false;
      o.flipY = false;
    });
    return originalLoad(json, () => {
      normalize();
      callback?.();
    });
  };
  return normalize;
}

export async function openProject(editor: any, project: any, name = '日本旅行') {
  projectState.busy = true;
  try {
    await Promise.all([
      document.fonts.load('16px "旅行楷体"'),
      document.fonts.load('16px "TravelHand"'),
    ]);
    await document.fonts.ready;
    await new Promise<void>((resolve, reject) => {
      editor.loadJSON(project, resolve).catch(reject);
    });
    projectState.name = name;
    editor.clearAndSaveState();
    editor.canvas.discardActiveObject();
    editor.auto();
  } finally {
    projectState.busy = false;
  }
}

export function download(blob: Blob, name: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function portableJSON(editor: any) {
  const json = editor.getJson();
  const images: any[] = [];
  walk(json, (o) => {
    if (o.type === 'image') images.push(o);
  });
  for (const image of images) {
    if (image.src.startsWith('data:')) continue;
    const response = await fetch(image.src);
    if (!response.ok) throw new Error('原片读取失败');
    const blob = await response.blob();
    image.src = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
  return json;
}

export function placePhoto(editor: any, row: any, replace = false) {
  return new Promise<void>((resolve, reject) => {
    const current = replace ? editor.canvas.getActiveObject() : null;
    const metadata = { photoId: row.id, originalName: row.originalName, sourceHash: row.sha256 };
    fabric.Image.fromURL(
      row.src,
      (image) => {
        if (!image.getElement()) {
          reject(new Error('原片读取失败'));
          return;
        }
        if (current?.type === 'image') {
          const center = current.getCenterPoint();
          const scale = Math.min(
            current.getScaledWidth() / image.width!,
            current.getScaledHeight() / image.height!
          );
          current.setElement(image.getElement());
          current.set({
            ...metadata,
            id: current.id,
            angle: current.angle,
            scaleX: scale,
            scaleY: scale,
          });
          current.setPositionByOrigin(center, 'center', 'center');
          current.setCoords();
        } else {
          image.set(metadata);
          const workspace = editor.getWorkspase();
          const scale = Math.min(
            (workspace.width * 0.55) / image.width!,
            (workspace.height * 0.55) / image.height!
          );
          image.set({ scaleX: scale, scaleY: scale });
          editor.addBaseType(image, { center: true });
        }
        editor.canvas.renderAll();
        editor.saveState();
        resolve();
      },
      { crossOrigin: 'anonymous' }
    );
  });
}
