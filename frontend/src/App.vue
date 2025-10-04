<script setup>
import { onMounted } from "vue";
import * as THREE from "three";
import { ARButton } from "three/examples/jsm/webxr/ARButton.js";


let scene, camera, renderer;
let reticle, controller;
let hitTestSource = null;
let hitTestSourceRequested = false;
let cubesAdded = false;

onMounted(() => {
  // Renderer with XR enabled
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.xr.enabled = true;
  document.body.appendChild(renderer.domElement);

  // Scene + Camera
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.01, 20);

  // Light
  const light = new THREE.HemisphereLight(0xffffff, 0xbbbbff, 1);
  light.position.set(0.5, 1, 0.25);
  scene.add(light);

  // Reticle (for hit-test)
  reticle = new THREE.Mesh(
    new THREE.RingGeometry(0.1, 0.11, 32).rotateX(-Math.PI / 2),
    new THREE.MeshBasicMaterial({ color: 0x00ff00 })
  );
  reticle.matrixAutoUpdate = false;
  reticle.visible = false;
  scene.add(reticle);

  // Controller for tapping
  controller = renderer.xr.getController(0);
  controller.addEventListener("select", onSelect);
  scene.add(controller);

  // AR Button
  document.body.appendChild(
    ARButton.createButton(renderer, { requiredFeatures: ["hit-test"] })
  );

  // Start animation
  renderer.setAnimationLoop(renderLoop);
});

// On tap → place cube
function onSelect() {
  if (reticle.visible) {
    const geometry = new THREE.BoxGeometry(0.1, 0.1, 0.1);
    const material = new THREE.MeshPhongMaterial({ color: 0xff0000 });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.setFromMatrixPosition(reticle.matrix);
    scene.add(cube);
  }
}

// Render loop with hit-test
function renderLoop(timestamp, frame) {
  if (frame) {
    const referenceSpace = renderer.xr.getReferenceSpace();
    const session = renderer.xr.getSession();

    if (!hitTestSourceRequested) {
      session.requestReferenceSpace("viewer").then((refSpace) => {
        session.requestHitTestSource({ space: refSpace }).then((source) => {
          hitTestSource = source;
        });
      });
      session.addEventListener("end", () => {
        hitTestSourceRequested = false;
        hitTestSource = null;
      });
      hitTestSourceRequested = true;
    }

    if (!cubesAdded && renderer.xr.isPresenting) {
      // Add several cubes in front of the camera at different positions
      for (let i = 0; i < 6; i++) {
        const geometry = new THREE.BoxGeometry(0.15, 0.15, 0.15);
        const material = new THREE.MeshPhongMaterial({ color: 0xffffff * Math.random() });
        const cube = new THREE.Mesh(geometry, material);
        // Place cubes 0.5-2 meters in front, with some random offset
        const distance = 0.5 + Math.random() * 1.5;
        const angle = (i / 6) * Math.PI * 2;
        cube.position.set(
          Math.cos(angle) * distance,
          0.1 + Math.random() * 0.5,
          -Math.sin(angle) * distance
        );
        scene.add(cube);
      }
      cubesAdded = true;
    }

    if (hitTestSource) {
      const hitTestResults = frame.getHitTestResults(hitTestSource);
      if (hitTestResults.length) {
        const pose = hitTestResults[0].getPose(referenceSpace);
        reticle.visible = true;
        reticle.matrix.fromArray(pose.transform.matrix);
      } else {
        reticle.visible = false;
      }
    }
  }

  renderer.render(scene, camera);
}
</script>

<template>
  <div class="w-screen h-screen bg-black">
    <!-- Three.js canvas gets injected here -->
  </div>
</template>
