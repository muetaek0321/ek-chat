/**
 * Timeline Engine
 * requestAnimationFrame を用いて動画の再生時間、シーン進行、シークを管理するクラス
 */
class Timeline {
  constructor(scenario) {
    this.scenario = scenario;
    this.scenes = scenario.scenes || [];
    this.totalDuration = 0;
    this.currentTime = 0; // ms
    this.playbackRate = 1.0;
    this.isPlaying = false;
    this.lastFrameTime = 0;
    this.rafId = null;

    // コールバック関数
    this.onTick = null;
    this.onSceneChange = null;
    this.onStateChange = null;
    this.onEnded = null;

    this.currentSceneIndex = -1;

    // 各シーンの開始時刻・終了時刻を事前計算
    this._computeTimeline();
  }

  _computeTimeline() {
    let accumulated = 0;
    this.sceneRanges = this.scenes.map((scene, index) => {
      const start = accumulated;
      const duration = scene.duration || 5000;
      const end = start + duration;
      accumulated = end;
      return { index, id: scene.id, start, end, duration, scene };
    });
    this.totalDuration = accumulated;
  }

  play() {
    if (this.isPlaying) return;
    if (this.currentTime >= this.totalDuration) {
      this.currentTime = 0;
    }
    this.isPlaying = true;
    this.lastFrameTime = performance.now();
    if (this.onStateChange) this.onStateChange(true);
    this._loop();
  }

  pause() {
    if (!this.isPlaying) return;
    this.isPlaying = false;
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
    if (this.onStateChange) this.onStateChange(false);
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  seek(timeMs) {
    this.currentTime = Math.max(0, Math.min(this.totalDuration, timeMs));
    this._updateCurrentScene(true);
    if (this.onTick) {
      this.onTick(this.currentTime, this.currentSceneIndex, this.getProgress());
    }
    if (this.currentTime >= this.totalDuration) {
      this.pause();
      if (this.onEnded) this.onEnded();
    }
  }

  seekRatio(ratio) {
    this.seek(this.totalDuration * Math.max(0, Math.min(1, ratio)));
  }

  nextScene() {
    const nextIdx = this.currentSceneIndex + 1;
    if (nextIdx < this.sceneRanges.length) {
      this.seek(this.sceneRanges[nextIdx].start);
    }
  }

  prevScene() {
    const curRange = this.sceneRanges[this.currentSceneIndex];
    if (curRange && (this.currentTime - curRange.start) > 1500) {
      // 1.5秒以上経過していれば同じシーンの先頭へ
      this.seek(curRange.start);
    } else {
      const prevIdx = Math.max(0, this.currentSceneIndex - 1);
      this.seek(this.sceneRanges[prevIdx].start);
    }
  }

  restart() {
    this.seek(0);
    this.play();
  }

  setPlaybackRate(rate) {
    this.playbackRate = Math.max(0.25, Math.min(4.0, rate));
  }

  getProgress() {
    return this.totalDuration > 0 ? (this.currentTime / this.totalDuration) : 0;
  }

  getCurrentSceneInfo() {
    const range = this.sceneRanges[this.currentSceneIndex];
    if (!range) return null;
    return {
      index: this.currentSceneIndex,
      scene: range.scene,
      sceneTime: this.currentTime - range.start,
      duration: range.duration
    };
  }

  _updateCurrentScene(forceEvent = false) {
    let newIndex = this.sceneRanges.findIndex(
      range => this.currentTime >= range.start && this.currentTime < range.end
    );
    if (newIndex === -1) {
      if (this.currentTime >= this.totalDuration && this.sceneRanges.length > 0) {
        newIndex = this.sceneRanges.length - 1;
      } else {
        newIndex = 0;
      }
    }

    if (newIndex !== this.currentSceneIndex || forceEvent) {
      this.currentSceneIndex = newIndex;
      if (this.onSceneChange && this.sceneRanges[newIndex]) {
        this.onSceneChange(newIndex, this.sceneRanges[newIndex].scene);
      }
    }
  }

  _loop() {
    if (!this.isPlaying) return;

    const now = performance.now();
    const delta = (now - this.lastFrameTime) * this.playbackRate;
    this.lastFrameTime = now;

    this.currentTime += delta;

    if (this.currentTime >= this.totalDuration) {
      this.currentTime = this.totalDuration;
      this._updateCurrentScene();
      if (this.onTick) {
        this.onTick(this.currentTime, this.currentSceneIndex, 1.0);
      }
      this.pause();
      if (this.onEnded) this.onEnded();
      return;
    }

    this._updateCurrentScene();
    if (this.onTick) {
      this.onTick(this.currentTime, this.currentSceneIndex, this.getProgress());
    }

    this.rafId = requestAnimationFrame(() => this._loop());
  }
}
