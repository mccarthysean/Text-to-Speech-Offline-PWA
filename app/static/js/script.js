const synth = window.speechSynthesis;
const playButton = document.getElementById("playButton");
const clearButton = document.getElementById("clearButton");
const voiceSelect = document.getElementById("voiceSelect");
const rateInput = document.getElementById("rateInput");
const rateOutput = document.getElementById("rateOutput");
let voices = [];

playButton.addEventListener("click", () => {
  const text = document.getElementById("textInput").value;
  const utterThis = new SpeechSynthesisUtterance(text);
  // Set the voice based on the selected option
  utterThis.voice = voices[voiceSelect.value];
  // Set the speech rate based on the input
  utterThis.rate = rateInput.value;
  synth.speak(utterThis);
});

clearButton.addEventListener("click", () => {
  document.getElementById("textInput").value = "";
});

// Update rate value display
rateInput.addEventListener("input", function () {
  rateOutput.textContent = rateInput.value;
});

let deferredPrompt;

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferredPrompt = e;
  const installButton = document.getElementById("installButton");
  installButton.style.display = "block";

  installButton.addEventListener("click", () => {
    installButton.style.display = "none";
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === "accepted") {
        console.log("User accepted the install prompt");
      } else {
        console.log("User dismissed the install prompt");
      }
      deferredPrompt = null;
    });
  });
});

function loadVoices() {
  voices = synth.getVoices();
  let defaultVoiceIndex = 0;

  for (let i = 0; i < voices.length; i++) {
    const option = document.createElement("option");
    option.textContent = `${voices[i].name} (${voices[i].lang})`;
    option.value = i;

    // Check if the voice is "Google UK English Male"
    if (
      voices[i].name === "Google UK English Male" &&
      voices[i].lang === "en-GB"
    ) {
      defaultVoiceIndex = i + 1;
    }

    voiceSelect.appendChild(option);
  }

  // Set the default selected voice to Google UK English Male
  voiceSelect.selectedIndex = defaultVoiceIndex;
}

if (synth.onvoiceschanged !== undefined) {
  synth.onvoiceschanged = loadVoices;
} else {
  loadVoices();
}
