
  <script type="module">
    import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
    import { gsap } from 'https://cdn.jsdelivr.net/npm/gsap@3.12.5/index.js';
    import { ScrollTrigger } from 'https://cdn.jsdelivr.net/npm/gsap@3.12.5/ScrollTrigger.js';

    gsap.registerPlugin(ScrollTrigger);

    const canvas = document.getElementById("webgl");
    const heroContent = document.querySelector(".hero-content");
    const floatingCard = document.querySelector(".floating-card");
    const scrollIndicator = document.querySelector(".scroll-indicator");

    const scene = new THREE.Scene();

    const sizes = {
      width: window.innerWidth,
      height: window.innerHeight
    };

    const camera = new THREE.PerspectiveCamera(45, sizes.width / sizes.height, 0.1, 100);
    scene.add(camera);

    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true
    });

    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    scene.add(ambientLight);

    const directionalLight1 = new THREE.DirectionalLight(0xffffff, 2.2);
    directionalLight1.position.set(4, 5, 6);
    scene.add(directionalLight1);

    const directionalLight2 = new THREE.DirectionalLight(0xff4ecd, 1.8);
    directionalLight2.position.set(-4, -2, 4);
    scene.add(directionalLight2);

    const group = new THREE.Group();
    scene.add(group);

    const mainGeometry = new THREE.TorusKnotGeometry(1.15, 0.34, 220, 32);
    const mainMaterial = new THREE.MeshStandardMaterial({
      color: 0xa855f7,
      metalness: 0.7,
      roughness: 0.18
    });
    const mainMesh = new THREE.Mesh(mainGeometry, mainMaterial);
    group.add(mainMesh);

    const ringGeometry = new THREE.TorusGeometry(2.2, 0.04, 16, 100);
    const ringMaterial = new THREE.MeshStandardMaterial({
      color: 0xff2fb3,
      metalness: 0.8,
      roughness: 0.2
    });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.rotation.x = Math.PI / 2.4;
    group.add(ring);

    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 200;
    const positions = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
      positions[i] = (Math.random() - 0.5) * 14;
    }

    particlesGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

    const particlesMaterial = new THREE.PointsMaterial({
      size: 0.03,
      color: 0xffffff
    });

    const particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    function setScenePosition() {
      const isMobile = window.innerWidth <= 768;

      if (isMobile) {
        camera.position.set(0, 0, 8.4);
        group.position.set(0, 0.4, 0);
        group.scale.set(0.78, 0.78, 0.78);
      } else {
        camera.position.set(0, 0, 7);
        group.position.set(2.8, 0.4, 0);
        group.scale.set(1, 1, 1);
      }
    }

    setScenePosition();

    function createScrollAnimation() {
      ScrollTrigger.getAll().forEach(trigger => trigger.kill());

      const isMobile = window.innerWidth <= 768;

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: ".scroll-scene",
          start: "top top",
          end: "bottom top",
          scrub: 1.1
        }
      });

      tl.to(group.rotation, {
        x: Math.PI * 2.2,
        y: Math.PI * 3.8,
        z: Math.PI * 1.25,
        ease: "none"
      }, 0);

      tl.to(group.position, {
        x: isMobile ? 0 : -5.3,
        y: isMobile ? -0.5 : -1.35,
        ease: "none"
      }, 0);

      tl.to(camera.position, {
        z: isMobile ? 7.1 : 4.2,
        ease: "none"
      }, 0);

      tl.to(ring.rotation, {
        z: Math.PI * 2,
        ease: "none"
      }, 0);

      tl.to(heroContent, {
        x: isMobile ? 0 : -160,
        y: isMobile ? -40 : 0,
        opacity: 0,
        ease: "none"
      }, 0.08);

      tl.to(floatingCard, {
        x: isMobile ? 0 : 140,
        y: isMobile ? 35 : 0,
        opacity: 0,
        ease: "none"
      }, 0.12);

      tl.to(scrollIndicator, {
        opacity: 0,
        y: 30,
        ease: "none"
      }, 0.1);
    }

    createScrollAnimation();

    gsap.to(group.rotation, {
      y: "+=" + Math.PI * 2,
      duration: 8,
      repeat: -1,
      ease: "none"
    });

    gsap.to(particles.rotation, {
      y: Math.PI * 2,
      duration: 20,
      repeat: -1,
      ease: "none"
    });

    const clock = new THREE.Clock();

    function animate() {
      const elapsedTime = clock.getElapsedTime();
      const floatY = Math.sin(elapsedTime * 1.2) * 0.08;

      mainMesh.rotation.x += 0.003;
      mainMesh.rotation.y += 0.004;
      ring.rotation.x += 0.0015;

      const targetY = window.innerWidth <= 768 ? 0.4 + floatY : 0.4 + floatY;
      group.position.y += (targetY - group.position.y) * 0.04;

      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }

    animate();

    window.addEventListener("resize", () => {
      sizes.width = window.innerWidth;
      sizes.height = window.innerHeight;

      camera.aspect = sizes.width / sizes.height;
      camera.updateProjectionMatrix();

      renderer.setSize(sizes.width, sizes.height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      setScenePosition();
      createScrollAnimation();
      ScrollTrigger.refresh();
    });
  </script>