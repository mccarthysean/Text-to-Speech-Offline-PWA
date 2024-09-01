document.getElementById('playButton').addEventListener('click', () => {
  const text = document.getElementById('textInput').value;
  const speech = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(speech);
});

document.getElementById('clearButton').addEventListener('click', () => {
  document.getElementById('textInput').value = '';
});

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  const installButton = document.getElementById('installButton');
  installButton.style.display = 'block';

  installButton.addEventListener('click', () => {
      installButton.style.display = 'none';
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
              console.log('User accepted the install prompt');
          } else {
              console.log('User dismissed the install prompt');
          }
          deferredPrompt = null;
      });
  });
});
