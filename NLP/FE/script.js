document.body.style.backgroundColor = "black"
const text = document.getElementById("judul")
text.style.color = "lightblue"
text.style.fontFamily = "calibri"
text.style.textAlign = "center"


// START CODE

async function uploadAndTranslate() {
    let fileInput = document.getElementById("inputGroupFile04");

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        let uploadResponse = await fetch("http://localhost:8000/upload", { method: "POST", body: formData });
        let uploadResult = await uploadResponse.json();
        if (!uploadResponse.ok) throw new Error(uploadResult.detail);

        let translatedFile;
        let max = 5
        let x = 0
        while(x < max){
            translatedFile = await fetch("http://localhost:8000/translated/"+ uploadResult.filename)
        
            if(translatedFile.ok) break;
            await new Promise(resolve => setTimeout(resolve,10000))
            x++
        }
        if(!translatedFile.ok){
            console.log("gagal bangsatt")
            return
        }
        let blob = await translatedFile.blob();
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = translatedFile;
        document.body.appendChild(a);
        a.click();
        a.remove();
        
        
        
    }catch (error){
        console.log(error);
    }
}
