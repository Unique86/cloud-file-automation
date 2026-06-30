
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const selectedFiles = document.getElementById("selectedFiles");
async function upload() {
    const action = document.getElementById("actionSelect").value;
    const files = document.getElementById("fileInput").files;
    const status = document.getElementById("status");

    console.log("Selected action:", action);

    if (files.length === 0) {
        status.innerText = "Please select a file";
        return;
    }

    status.innerText = "Uploading & converting...";

    const formData = new FormData();

    if (action === "merge-pdfs") {
        for (const file of files) {
            formData.append("files", file);
        }
    } else {
        formData.append("file", files[0]);
    }

    try {
        let endpoint = "";

        if (action === "image-to-pdf") {
            endpoint = "/image-to-pdf/";
        } else if (action === "pdf-to-docx") {
            endpoint = "/pdf-to-docx/";
        } else if (action === "docx-to-pdf") {
            endpoint = "/docx-to-pdf/";
        } else if (action === "merge-pdfs") {
            endpoint = "/merge-pdfs/";
        } else {
            alert("Feature coming soon");
            return;
        }

        const res = await fetch(endpoint, {
            method: "POST",
            body: formData,
        });

        const data = await res.json();

        status.innerText = data.message || "Done ✅";

        await loadFiles();
    } catch (err) {
        console.error(err);
        status.innerText = "Error occurred ❌";
    }
}

async function loadFiles() {
    const res = await fetch("/files");
    const data = await res.json();

    const container = document.getElementById("fileList");
    container.innerHTML = "";

    data.files.forEach((file) => {
        container.innerHTML += `
            <div class="file">
                <span>${file}</span>
                <a href="/download/${file}" style="color:#3b82f6;">Download</a>
            </div>
        `;
    });
}

dropZone.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    updateSelectedFiles(fileInput.files);
});

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();

    dropZone.classList.remove("dragover");

    fileInput.files = e.dataTransfer.files;

    updateSelectedFiles(fileInput.files);
});

function updateSelectedFiles(files){

    if(files.length === 0){
        selectedFiles.innerText = "No files selected";
        return;
    }

    let names = [];

    for(const file of files){
        names.push(file.name);
    }

    selectedFiles.innerText = names.join(", ");
}
loadFiles();
