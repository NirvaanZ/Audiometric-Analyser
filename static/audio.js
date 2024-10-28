// static/audio.js

document.addEventListener('DOMContentLoaded', function () {
    const audio = document.getElementById('audio');
    const canvas = document.getElementById('waveform');
    const ctx = canvas.getContext('2d');

    let audioContext;
    let analyser;
    let dataArray;
    let bufferLength;

    audio.addEventListener('play', function () {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaElementSource(audio);
        analyser = audioContext.createAnalyser();
        source.connect(analyser);
        analyser.connect(audioContext.destination);

        analyser.fftSize = 2048;
        bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);

        draw();
    });

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
            }
        };
        xhr.send(JSON.stringify({ heard: heard }));
    };
});
