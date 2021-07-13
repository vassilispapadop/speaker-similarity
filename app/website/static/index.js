function playSound(clip){
    // clip = '/Users/vpapadop/Documents/GitHub/speaker-similarity/app/website/downloads/parts/output000000000.wav'
    var audio = new Audio(clip);
    audio.play();
    // fetch('/delete-note', {
    //     method: 'POST',
    //     body: JSON.stringify({noteId: noteId})
    // }).then((_res) => {
    //     window.location.href ="/"
    // }); 
}