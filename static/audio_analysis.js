// static/audio_analysis.js

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('waveform');
    const ctx = canvas.getContext('2d');
    const frequencies = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140];
    let currentIndex = 0;

    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    let oscillator, analyser, dataArray, bufferLength;

    function playSound(frequency) {
        oscillator = audioContext.createOscillator();
        analyser = audioContext.createAnalyser();
        oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
        oscillator.type = 'sine';

        oscillator.connect(analyser);
        analyser.connect(audioContext.destination);

        analyser.fftSize = 2048;
        bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);

        oscillator.start();
        draw();

        setTimeout(() => {
            stopSound();
            document.getElementById('question').style.display = 'block';
        }, 3000); // Play each sound for 3 seconds
    }

    function stopSound() {
        oscillator.stop();
        document.getElementById('question').style.display = 'none';
    }

    function draw() {
        requestAnimationFrame(draw);

        analyser.getByteTimeDomainData(dataArray);

        ctx.fillStyle = 'rgba(200, 200, 200, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.lineWidth = 2;
        ctx.strokeStyle = '#007bff';

        ctx.beginPath();

        let sliceWidth = canvas.width * 1.0 / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            let v = dataArray[i] / 128.0;
            let y = v * canvas.height / 2;

            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
    }

    window.sendResponse = function(heard) {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/save_analysis", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert("Your response has been recorded!");
                if (currentIndex < frequencies.length - 1) {
                    currentIndex++;
                    playSound(frequencies[currentIndex]);
                } else {
                    alert("Test completed. Thank you!");
                }
            }
        };
        xhr.send(JSON.stringify({ heard: heard, frequency: frequencies[currentIndex] }));
    };

    // Start playing the first sound
    playSound(frequencies[currentIndex]);
});
