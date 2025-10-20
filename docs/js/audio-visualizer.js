const audioVisualizerSketch = (p) => {
  let mic;
  let fft;
  let canvasParent;
  let startButton;
  let statusMessage;
  let audioActive = false;

  const getParentSize = () => {
    if (!canvasParent) {
      return { width: window.innerWidth, height: window.innerHeight };
    }

    const { clientWidth, clientHeight } = canvasParent;
    return {
      width: clientWidth || window.innerWidth,
      height: clientHeight || Math.max(window.innerHeight * 0.6, 320)
    };
  };

  const setStatus = (message, isError = false) => {
    if (!statusMessage) {
      return;
    }

    statusMessage.textContent = message;
    statusMessage.classList.toggle("visually-hidden", !message);
    statusMessage.classList.toggle("text-danger", isError);
    statusMessage.classList.toggle("text-success", !isError && Boolean(message));
  };

  const handleStartClick = async () => {
    if (audioActive) {
      return;
    }

    try {
      await p.userStartAudio();
      await mic.start();
      audioActive = true;

      if (startButton) {
        startButton.disabled = true;
        startButton.textContent = "Micrófono activado";
      }

      setStatus("Micrófono en uso. ¡Haz sonidos y observa la animación!");
    } catch (error) {
      console.error("No se pudo iniciar el micrófono", error);
      setStatus("No se pudo acceder al micrófono. Revisa los permisos del navegador.", true);
    }
  };

  const wireControls = () => {
    if (!startButton) {
      startButton = document.getElementById("audio-visualizer-start");
    }

    if (!statusMessage) {
      statusMessage = document.getElementById("audio-visualizer-status");
    }

    if (startButton && !startButton.dataset.bound) {
      startButton.dataset.bound = "true";
      startButton.addEventListener("click", handleStartClick);
    }

    setStatus("Haz clic en \"Activar visualizador\" para conceder permiso al micrófono.");
  };

  p.setup = () => {
    canvasParent = document.getElementById("audio-visualizer-canvas");
    const { width, height } = getParentSize();
    p.createCanvas(width, height).parent(canvasParent || document.body);

    mic = new p5.AudioIn();

    fft = new p5.FFT();
    fft.setInput(mic);

    p.noStroke();
    p.colorMode(p.HSB, 360, 100, 100, 100);

    wireControls();
  };

  p.windowResized = () => {
    const { width, height } = getParentSize();
    p.resizeCanvas(width, height);
  };

  p.draw = () => {
    p.background(0, 10);

    if (!audioActive) {
      return;
    }

    const spectrum = fft.analyze();
    const maxSize = Math.min(p.width, p.height) / 5;

    for (let i = 0; i < spectrum.length; i += 10) {
      const frequency = i;
      const amplitude = spectrum[i];
      const hue = p.map(frequency, 0, 255, 180, 360);
      const size = p.map(amplitude, 0, 255, 5, maxSize);

      p.fill(hue, 80, 100, 40);
      p.ellipse(p.random(p.width), p.random(p.height), size);
    }
  };
};

new p5(audioVisualizerSketch);
