var audio;

function playSound(clip){
    // clip = '/Users/vpapadop/Documents/GitHub/speaker-similarity/app/website/downloads/parts/output000000000.wav'
    // var audio = new Audio("https://s3.amazonaws.com/audio-experiments/examples/elon_mono.wav")
    // file = 'listen/?s='+clip
    // audio = new Audio(file)
    // audio.play();

    // fetch('/listen', {
    //     method: 'POST',
    //     body: JSON.stringify({source: clip})
    // }).then((res) => {
    //     console.log(res)
    //     // window.location.href ="/"
    // }); 


    fetch('/listen', {
        method: 'POST',
        body: JSON.stringify({source: clip})
    }).then(response => response.blob()).then(blob => {
        let file = new File([blob], clip, {
                    type:"audio/x-wav", lastModified:new Date().getTime()
            });
            // do stuff with `file`
            audio = new Audio(file)
            audio.play()
        }).catch(err => console.error(err));


}