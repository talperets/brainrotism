// This is a TypeScript/Vue component for AR with Three.js
import { defineComponent } from 'vue';
import * as THREE from 'three';
import { ARButton } from 'three/examples/jsm/webxr/ARButton.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export default defineComponent({
  name: 'AR',
  setup() {
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;

    const init = () => {
      // Scene
      scene = new THREE.Scene();

      // Camera
      camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.01, 20);

      // Renderer
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.xr.enabled = true;

      // Lights
      const light = new THREE.HemisphereLight(0xffffff, 0xbbbbff, 1);
      light.position.set(0.5, 1, 0.25);
      scene.add(light);

      // Add AR button
      document.body.appendChild(
        ARButton.createButton(renderer, {
          requiredFeatures: ['hit-test']
        })
      );

      // Start rendering
      renderer.setAnimationLoop(render);
    };

    const render = () => {
      renderer.render(scene, camera);
    };

    onMounted(() => {
      init();
    });

    return {};
  }
});