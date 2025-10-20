const audioVisualizerSketch = (p) => {
  let mic;
  let fft;
  let canvasParent;

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

  p.setup = () => {
    canvasParent = document.getElementById("audio-visualizer-canvas");
    const { width, height } = getParentSize();
    p.createCanvas(width, height).parent(canvasParent || document.body);

    mic = new p5.AudioIn();
    mic.start();

    fft = new p5.FFT();
    fft.setInput(mic);

    p.noStroke();
    p.colorMode(p.HSB, 360, 100, 100, 100);
  };

  p.windowResized = () => {
    const { width, height } = getParentSize();
    p.resizeCanvas(width, height);
  };

  p.draw = () => {
    p.background(0, 10);

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
