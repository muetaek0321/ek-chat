/**
 * Player Controller
 * プレイヤーUI、タイムライン、シーンレンダラーの統合コントローラー
 */
document.addEventListener('DOMContentLoaded', async () => {
  const videoViewport = document.getElementById('videoViewport');
  const videoScreen = document.getElementById('videoScreen');
  const playBtn = document.getElementById('playBtn');
  const playIcon = document.getElementById('playIcon');
  const pauseIcon = document.getElementById('pauseIcon');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const restartBtn = document.getElementById('restartBtn');
  const progressBar = document.getElementById('progressBar');
  const progressFilled = document.getElementById('progressFilled');
  const progressHover = document.getElementById('progressHover');
  const timeCurrent = document.getElementById('timeCurrent');
  const timeTotal = document.getElementById('timeTotal');
  const sceneIndicator = document.getElementById('sceneIndicator');
  const sceneSelect = document.getElementById('sceneSelect');
  const speedBtn = document.getElementById('speedBtn');
  const fullscreenBtn = document.getElementById('fullscreenBtn');

  // 1. シナリオデータのロード
  let scenario = null;
  try {
    const res = await fetch('data/scenario.json');
    if (res.ok) {
      scenario = await res.json();
    }
  } catch (e) {
    console.warn('Fetch scenario.json failed, falling back to window.SCENARIO_DATA', e);
  }

  if (!scenario && window.SCENARIO_DATA) {
    scenario = window.SCENARIO_DATA;
  }

  if (!scenario) {
    alert('動画シナリオデータの読み込みに失敗しました。');
    return;
  }

  // 2. シーンセレクトボックスの初期化
  scenario.scenes.forEach((sc, idx) => {
    const opt = document.createElement('option');
    opt.value = idx;
    opt.textContent = `${idx + 1}. ${sc.title}`;
    sceneSelect.appendChild(opt);
  });

  // 3. レンダラー & タイムラインの初期化
  const renderer = new SceneRenderer(videoScreen, scenario.settings);
  const timeline = new Timeline(scenario);
  window.timeline = timeline; // デバッグ・検証用公開

  // 時間フォーマット関数 (mm:ss)
  function formatTime(ms) {
    const totalSec = Math.floor(ms / 1000);
    const m = Math.floor(totalSec / 60);
    const s = totalSec % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  timeTotal.textContent = formatTime(timeline.totalDuration);

  // 4. レスポンシブ・スケーリング処理
  function updateScale() {
    const containerW = videoViewport.clientWidth;
    const containerH = videoViewport.clientHeight;
    const baseW = 1920;
    const baseH = 1080;

    const scale = Math.min(containerW / baseW, containerH / baseH);
    videoScreen.style.transform = `scale(${scale})`;
  }

  window.addEventListener('resize', updateScale);
  updateScale();

  // 5. タイムラインのコールバック設定
  timeline.onSceneChange = (index, scene) => {
    renderer.loadScene(scene);
    sceneIndicator.textContent = `Scene ${index + 1}/${scenario.scenes.length}: ${scene.title}`;
    sceneSelect.value = index;
  };

  timeline.onTick = (currentTime, sceneIndex, progress) => {
    progressFilled.style.width = `${progress * 100}%`;
    timeCurrent.textContent = formatTime(currentTime);

    const info = timeline.getCurrentSceneInfo();
    if (info) {
      renderer.renderFrame(info.sceneTime);
    }
  };

  timeline.onStateChange = (isPlaying) => {
    if (isPlaying) {
      playIcon.style.display = 'none';
      pauseIcon.style.display = 'block';
    } else {
      playIcon.style.display = 'block';
      pauseIcon.style.display = 'none';
    }
  };

  timeline.onEnded = () => {
    playIcon.style.display = 'block';
    pauseIcon.style.display = 'none';
  };

  // 初期シーンの読み込みとレンダリング
  if (scenario.scenes.length > 0) {
    timeline._updateCurrentScene(true);
    renderer.renderFrame(0);
  }

  // 6. コントローラーのイベント
  playBtn.addEventListener('click', () => timeline.togglePlay());
  videoScreen.addEventListener('click', () => timeline.togglePlay());

  prevBtn.addEventListener('click', () => timeline.prevScene());
  nextBtn.addEventListener('click', () => timeline.nextScene());
  restartBtn.addEventListener('click', () => timeline.restart());

  sceneSelect.addEventListener('change', (e) => {
    const idx = parseInt(e.target.value, 10);
    if (!isNaN(idx) && timeline.sceneRanges[idx]) {
      timeline.seek(timeline.sceneRanges[idx].start);
    }
  });

  // 再生速度切り替え
  const speeds = [1.0, 1.5, 2.0];
  let speedIdx = 0;
  speedBtn.addEventListener('click', () => {
    speedIdx = (speedIdx + 1) % speeds.length;
    const rate = speeds[speedIdx];
    timeline.setPlaybackRate(rate);
    speedBtn.textContent = `${rate}x`;
  });

  // プログレスバーのシーク操作
  let isDraggingProgress = false;

  function handleSeek(e) {
    const rect = progressBar.getBoundingClientRect();
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    progressFilled.style.width = `${pos * 100}%`;
    timeline.seekRatio(pos);
  }

  progressBar.addEventListener('mousedown', (e) => {
    isDraggingProgress = true;
    handleSeek(e);
  });

  window.addEventListener('mousemove', (e) => {
    if (isDraggingProgress) {
      handleSeek(e);
    }
  });

  window.addEventListener('mouseup', () => {
    isDraggingProgress = false;
  });

  // ホバープレビュー位置
  progressBar.addEventListener('mousemove', (e) => {
    const rect = progressBar.getBoundingClientRect();
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    progressHover.style.width = `${pos * 100}%`;
  });

  // フルスクリーン切り替え
  fullscreenBtn.addEventListener('click', () => {
    const playerWrapper = document.getElementById('playerWrapper');
    if (!document.fullscreenElement) {
      playerWrapper.requestFullscreen().catch(err => console.log(err));
    } else {
      document.exitFullscreen().catch(err => console.log(err));
    }
  });

  document.addEventListener('fullscreenchange', () => {
    setTimeout(updateScale, 100);
  });

  // 7. キーボードショートカット
  window.addEventListener('keydown', (e) => {
    // 入力中の場合は無視
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
      return;
    }

    if (e.code === 'Space') {
      e.preventDefault();
      timeline.togglePlay();
    } else if (e.code === 'ArrowLeft') {
      e.preventDefault();
      timeline.prevScene();
    } else if (e.code === 'ArrowRight') {
      e.preventDefault();
      timeline.nextScene();
    } else if (e.code === 'KeyF') {
      e.preventDefault();
      fullscreenBtn.click();
    } else if (e.code === 'Home') {
      e.preventDefault();
      timeline.restart();
    }
  });
});
