/**
 * Scene Renderer
 * 基準解像度 1920x1080 の仮想キャンバス（DOM要素）に対して
 * シーンの背景画像、ハイライト枠、カーソルアニメーション、字幕、コールアウトをレンダリングする
 */
class SceneRenderer {
  constructor(screenEl, settings) {
    this.screenEl = screenEl;
    this.settings = settings || {};
    this.baseWidth = this.settings.baseResolution?.width || 1920;
    this.baseHeight = this.settings.baseResolution?.height || 1080;
    this.imageContainerConfig = this.settings.imageContainer || {
      width: 1536,
      height: 960,
      offsetX: 192,
      offsetY: 40
    };

    this.currentScene = null;
    this.renderedElements = new Map();

    this._setupScreen();
  }

  _setupScreen() {
    this.screenEl.innerHTML = `
      <div class="video-stage" id="videoStage">
        <!-- 背景レイヤー -->
        <div class="stage-bg" id="stageBg"></div>

        <!-- アプリウィンドウ風コンテナ -->
        <div class="app-window-frame" id="appWindowFrame">
          <div class="window-title-bar">
            <span class="window-dot dot-red"></span>
            <span class="window-dot dot-yellow"></span>
            <span class="window-dot dot-green"></span>
            <span class="window-title-text" id="windowTitleText">ek-chat (http://localhost:3000)</span>
          </div>
          <div class="window-content-area">
            <img class="stage-screenshot" id="stageScreenshot" alt="App Screenshot" />
          </div>
        </div>

        <!-- 演出・オーバーレイレイヤー -->
        <div class="stage-overlay" id="stageOverlay"></div>

        <!-- 字幕キャプションレイヤー -->
        <div class="caption-container" id="captionContainer">
          <div class="caption-badge" id="captionBadge">解説</div>
          <div class="caption-text" id="captionText"></div>
        </div>
      </div>
    `;

    this.stageEl = this.screenEl.querySelector('#videoStage');
    this.stageBgEl = this.screenEl.querySelector('#stageBg');
    this.appWindowEl = this.screenEl.querySelector('#appWindowFrame');
    this.screenshotEl = this.screenEl.querySelector('#stageScreenshot');
    this.overlayEl = this.screenEl.querySelector('#stageOverlay');
    this.captionContainerEl = this.screenEl.querySelector('#captionContainer');
    this.captionTextEl = this.screenEl.querySelector('#captionText');
    this.windowTitleTextEl = this.screenEl.querySelector('#windowTitleText');
  }

  /**
   * シーンの切り替え
   */
  loadScene(scene) {
    if (!scene) return;
    this.currentScene = scene;

    // スクリーンショットの更新
    if (scene.image) {
      this.screenshotEl.src = scene.image;
      this.appWindowEl.style.display = 'flex';
    } else {
      this.appWindowEl.style.display = 'none';
    }

    // ウィンドウタイトルの更新
    if (this.windowTitleTextEl) {
      this.windowTitleTextEl.textContent = `ek-chat | ${scene.title || '操作ガイド'}`;
    }

    // オーバーレイをクリア
    this.overlayEl.innerHTML = '';
    this.renderedElements.clear();

    // キャプションをリセット
    this.captionContainerEl.classList.remove('visible');
    this.captionTextEl.textContent = '';
  }

  /**
   * 毎フレームのレンダリング更新（sceneTime: 現在のシーン内の経過時間 ms）
   */
  renderFrame(sceneTime) {
    if (!this.currentScene) return;

    const elements = this.currentScene.elements || [];

    // 1. キャプションの更新
    let activeCaption = null;

    elements.forEach((elem, index) => {
      const elemKey = `elem_${index}`;
      const startTime = elem.startTime || 0;
      const duration = elem.duration || 999999;
      const endTime = startTime + duration;
      const isActive = sceneTime >= startTime && sceneTime < endTime;

      if (elem.type === 'caption') {
        if (isActive) {
          activeCaption = elem;
        }
      } else if (elem.type === 'highlight') {
        this._renderHighlight(elemKey, elem, isActive, sceneTime);
      } else if (elem.type === 'cursor') {
        this._renderCursor(elemKey, elem, isActive, sceneTime);
      } else if (elem.type === 'callout') {
        this._renderCallout(elemKey, elem, isActive, sceneTime);
      }
    });

    if (activeCaption) {
      this.captionTextEl.textContent = activeCaption.text;
      this.captionContainerEl.classList.add('visible');
    } else {
      this.captionContainerEl.classList.remove('visible');
    }
  }

  /**
   * ハイライト枠の描画・更新
   */
  _renderHighlight(key, elem, isActive, sceneTime) {
    let el = this.renderedElements.get(key);

    if (!isActive) {
      if (el) {
        el.classList.remove('active');
        setTimeout(() => {
          if (el && !el.classList.contains('active') && el.parentElement) {
            el.parentElement.removeChild(el);
            this.renderedElements.delete(key);
          }
        }, 200);
      }
      return;
    }

    if (!el) {
      el = document.createElement('div');
      el.className = 'anim-highlight';
      el.id = key;

      if (elem.label) {
        const labelEl = document.createElement('div');
        labelEl.className = 'highlight-label';
        labelEl.textContent = elem.label;
        if (elem.color) {
          labelEl.style.backgroundColor = elem.color;
        }
        el.appendChild(labelEl);
      }

      this.overlayEl.appendChild(el);
      this.renderedElements.set(key, el);
    }

    // スタイル適用
    el.style.left = `${elem.x}px`;
    el.style.top = `${elem.y}px`;
    el.style.width = `${elem.width}px`;
    el.style.height = `${elem.height}px`;
    if (elem.color) {
      el.style.borderColor = elem.color;
      el.style.boxShadow = `0 0 20px ${elem.color}66, inset 0 0 15px ${elem.color}33`;
    }

    // フェードイン適用
    requestAnimationFrame(() => {
      el.classList.add('active');
    });
  }

  /**
   * マウスカーソルとクリックアニメーションの描画・更新
   */
  _renderCursor(key, elem, isActive, sceneTime) {
    let el = this.renderedElements.get(key);

    if (!isActive) {
      if (el) {
        el.remove();
        this.renderedElements.delete(key);
      }
      return;
    }

    if (!el) {
      el = document.createElement('div');
      el.className = 'anim-cursor-container';
      el.innerHTML = `
        <svg class="anim-cursor-svg" viewBox="0 0 24 24" fill="none">
          <path d="M5.5 3.2L18.8 13.5L12.5 14.8L16.2 21.2L13.4 22.8L9.7 16.4L5.5 19.8V3.2Z" fill="#1e293b" stroke="#ffffff" stroke-width="1.8" stroke-linejoin="round"/>
        </svg>
        <div class="cursor-ripple"></div>
      `;
      this.overlayEl.appendChild(el);
      this.renderedElements.set(key, el);
    }

    // 移動補間計算
    const startT = elem.startTime || 0;
    const moveT = elem.moveTime || 1000;
    const progress = Math.min(1.0, Math.max(0.0, (sceneTime - startT) / moveT));
    // easeOutCubic イージング
    const ease = 1 - Math.pow(1 - progress, 3);

    const currentX = elem.startX + (elem.endX - elem.startX) * ease;
    const currentY = elem.startY + (elem.endY - elem.startY) * ease;

    el.style.transform = `translate(${currentX}px, ${currentY}px)`;

    // クリック判定
    const rippleEl = el.querySelector('.cursor-ripple');
    const clickT = elem.clickTime || (startT + moveT + 300);
    const clickDuration = 600;

    if (sceneTime >= clickT && sceneTime < (clickT + clickDuration)) {
      rippleEl.classList.add('animate-click');
      el.classList.add('cursor-clicked');
    } else {
      rippleEl.classList.remove('animate-click');
      el.classList.remove('cursor-clicked');
    }
  }

  /**
   * コールアウト（補足吹き出しカード）の描画・更新
   */
  _renderCallout(key, elem, isActive, sceneTime) {
    let el = this.renderedElements.get(key);

    if (!isActive) {
      if (el) {
        el.classList.remove('active');
        setTimeout(() => {
          if (el && !el.classList.contains('active') && el.parentElement) {
            el.parentElement.removeChild(el);
            this.renderedElements.delete(key);
          }
        }, 200);
      }
      return;
    }

    if (!el) {
      el = document.createElement('div');
      el.className = 'anim-callout';

      let innerHtml = '';
      if (elem.title) {
        innerHtml += `<div class="callout-header"><span class="callout-icon">💡</span> <span class="callout-title">${elem.title}</span></div>`;
      }
      innerHtml += `<div class="callout-body">${elem.text.replace(/\n/g, '<br>')}</div>`;
      el.innerHTML = innerHtml;

      this.overlayEl.appendChild(el);
      this.renderedElements.set(key, el);
    }

    el.style.left = `${elem.x}px`;
    el.style.top = `${elem.y}px`;

    requestAnimationFrame(() => {
      el.classList.add('active');
    });
  }
}
