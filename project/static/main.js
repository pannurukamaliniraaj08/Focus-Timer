let hours = document.querySelector('#hours');
let minutes = document.querySelector('#minutes');
let seconds = document.querySelector('#seconds');
let start = document.querySelector('#start');
let quit = document.querySelector('#quit');
let play_pause = document.querySelector('#play_pause');
let timerDisplay = document.querySelector('#timer-display');
let video = document.querySelector('#timer-video');
let totalSeconds;

let timerInterval = null;
let endTime = null;
let isTimerRunning = false;

function updateDisplay(totalSecs) {
    if (totalSecs < 0) totalSecs = 0;
    let h = Math.floor(totalSecs / 3600).toString().padStart(2, '0');
    let m = Math.floor((totalSecs % 3600) / 60).toString().padStart(2, '0');
    let s = (totalSecs % 60).toString().padStart(2, '0');
    timerDisplay.textContent = `${h}:${m}:${s}`;
}

function tick() {
    let now = Date.now();
    let remainingSeconds = Math.round((endTime - now) / 1000);

    if (remainingSeconds > 0) {
        updateDisplay(remainingSeconds);
    } else {
        // Timer Reached Zero
        clearInterval(timerInterval);
        timerInterval = null;
        isTimerRunning = false;
        video.pause();
        video.currentTime = 0;
        fetch("/get-seconds", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ totalSeconds: totalSeconds })
        })
        .then(response => response.json())
        .then(data => console.log("Saved session:", data));
        localStorage.clear();
        updateDisplay(0);
    }
}

// START BUTTON
start.addEventListener('click', function() {
    if (timerInterval) clearInterval(timerInterval);
    let h = parseInt(hours.value) || 0;
    let m = parseInt(minutes.value) || 0;
    let s = parseInt(seconds.value) || 0;
    totalSeconds = h * 3600 + m * 60 + s;

    if (totalSeconds <= 0) return;

    endTime = Date.now() + (totalSeconds * 1000);
    localStorage.setItem('timerEndTime', endTime);
    localStorage.setItem('isTimerRunning', 'true');

    isTimerRunning = true;
    updateDisplay(totalSeconds);

    video.currentTime = 0;
    video.play().catch(err => console.log("Video playback error:", err));

    timerInterval = setInterval(tick, 1000);
});

// PLAY / PAUSE CHECKBOX
play_pause.addEventListener('change', function() {
    let savedEndTime = localStorage.getItem('timerEndTime');
    if (!savedEndTime) return;

    if (this.checked) {
        // Resume
        let remaining = parseInt(localStorage.getItem('pausedRemainingSeconds') || 0);
        endTime = Date.now() + (remaining * 1000);
        localStorage.setItem('timerEndTime', endTime);
        localStorage.setItem('isTimerRunning', 'true');

        isTimerRunning = true;
        video.play().catch(err => console.log("Video playback error:", err));
        timerInterval = setInterval(tick, 1000);
    } else {
        // Pause
        isTimerRunning = false;
        clearInterval(timerInterval);
        timerInterval = null;

        let remainingSeconds = Math.round((endTime - Date.now()) / 1000);
        localStorage.setItem('pausedRemainingSeconds', remainingSeconds);
        localStorage.setItem('isTimerRunning', 'false');

        video.pause();
    }
});

// QUIT BUTTON
if (quit) {
    quit.addEventListener('click', function() {

        clearInterval(timerInterval);
        timerInterval = null;
        isTimerRunning = false;
        video.pause();

        let isQuit = true;
        const totalSecondsRemaining = Math.max(0, totalSeconds);

        // Incomplete: need to update completed seconds into the database
        let savedEndTime = localStorage.getItem('timerEndTime');
        let elapsedSeconds = 0;
        video.currentTime = 0;

        if (savedEndTime){
            let remainingSeconds = Math.max(0, Math.floor((parseInt(savedEndTime) - Date.now()) / 1000));
            elapsedSeconds = Math.max(0, totalSeconds - remainingSeconds);
        }

        if(elapsedSeconds <= 0){
            localStorage.clear();
            updateDisplay(0);
            return;
        }

        fetch("/get-seconds", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
             totalSeconds: elapsedSeconds,
             savedEndTime: savedEndTime ? parseInt(savedEndTime) : 0,
             isQuit: true
         })
        })
        .then(response => response.json())
        .then(data =>{console.log("Quit saved session:", data);
                        localStorage.clear();
                        updateDisplay(0);
                        location.reload();
                    });
        });
    }
// RESTORE STATE ON REFRESH
function restoreOnReload() {
    let savedEndTime = localStorage.getItem('timerEndTime');
    let savedRunningState = localStorage.getItem('isTimerRunning');

    if (savedEndTime) {
        endTime = parseInt(savedEndTime);
        let remaining = Math.round((endTime - Date.now()) / 1000);

        if (remaining > 0) {
            if (savedRunningState === 'true') {
                isTimerRunning = true;
                play_pause.checked = true;
                video.play().catch(err => console.log(err));
                tick();
                timerInterval = setInterval(tick, 1000);
            } else {
                let pausedRemaining = parseInt(localStorage.getItem('pausedRemainingSeconds') || 0);
                play_pause.checked = false;
                updateDisplay(pausedRemaining);
            }
        } else {
            localStorage.clear();
            updateDisplay(0);
        }
    }
}

restoreOnReload();
