const synth = window.speechSynthesis;
const playButton = document.getElementById("playButton");
const clearButton = document.getElementById("clearButton");
const installButton = document.getElementById("installButton");
const installButtonRow = document.getElementById("installButtonRow");
const voiceSelect = document.getElementById("voiceSelect");
const rateInput = document.getElementById("rateInput");
const rateOutput = document.getElementById("rateOutput");
let voices = [];

playButton.addEventListener("click", () => {
  let text = document.getElementById("textInput").value;
  // Check if the text is empty or null
  if (!text) {
    text = "Please enter some text to play";
  }
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

// Function to update rate display and class
function updateRateOutput(rateValue) {
  let rateText = "Medium";
  let rateClass = "text-center";
  rateValue = String(rateValue);

  if (rateValue === "0.7") {
    rateText = "Slow";
    rateClass = "text-left";
  } else if (rateValue === "1.3") {
    rateText = "Fast";
    rateClass = "text-right";
  }

  rateOutput.textContent = rateText;
  rateOutput.className = `form-text ${rateClass}`;

  // Store the preferred rate in local storage
  localStorage.setItem("preferredRate", rateValue);
}

// Set initial rate and store changes
rateInput.value = localStorage.getItem("preferredRate") || "1"; // Default to "1" if no value is stored
updateRateOutput(rateInput.value);

// Update rate value display
rateInput.addEventListener("input", () => {
  updateRateOutput(rateInput.value);
});

// Check if the browser supports the beforeinstallprompt event
let deferredPrompt;
window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installButtonRow.style.display = "";

  installButton.addEventListener("click", () => {
    installButtonRow.style.display = "none";

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

// Load voices and populate the select element
function loadVoices() {
  const voices = synth.getVoices();

  // Remove all existing options
  voiceSelect.innerHTML = "";

  // Set the option as selected if it matches the stored preference
  let defaultVoiceIndex = localStorage.getItem("preferredVoice") || null;

  voices.forEach((voice, i) => {
    const option = document.createElement("option");
    option.textContent = `${voice.name} (${voice.lang})`;
    option.value = i;

    if (defaultVoiceIndex === null) {
      if (
        // Check if the voice is "Google UK English Male"
        voices[i].name === "Google UK English Male" &&
        voices[i].lang === "en-GB"
      ) {
        defaultVoiceIndex = i;
      }
    }

    voiceSelect.appendChild(option);
  });

  // Default to the first voice if no preference is stored
  if (defaultVoiceIndex === null) {
    defaultVoiceIndex = 0;
  }

  // Set the default selected voice to Google UK English Male
  voiceSelect.selectedIndex = defaultVoiceIndex;

  // Store the user's preferred voice when they change it
  voiceSelect.addEventListener("change", () => {
    localStorage.setItem(
      "preferredVoice",
      voiceSelect.selectedIndex
    );
  });
}

// Load voices on page load or when voices change
if (synth.onvoiceschanged !== undefined) {
  synth.onvoiceschanged = loadVoices;
} else {
  loadVoices();
}
