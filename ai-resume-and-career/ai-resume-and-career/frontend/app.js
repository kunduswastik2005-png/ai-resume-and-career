const fileInput = document.getElementById("resumeFile");
const dropzone = document.getElementById("dropzone");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const formError = document.getElementById("formError");
const loading = document.getElementById("loading");

let selectedFile = null;
let resumeText = "";

const PDFJS_VERSION = "3.11.174";
const PDFJS_URL = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${PDFJS_VERSION}/pdf.min.js`;
const PDFJS_WORKER_URL = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${PDFJS_VERSION}/pdf.worker.min.js`;
const MAMMOTH_URL = "https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.8.0/mammoth.browser.min.js";

// Dynamically load a library if it is not already available.
function loadScript(url) {
    return new Promise((resolve, reject) => {
        const existing = [...document.scripts].find(script => script.src === url);

        if (existing) {
            if (existing.dataset.loaded === "true") {
                resolve();
                return;
            }

            existing.addEventListener("load", resolve, { once: true });
            existing.addEventListener("error", reject, { once: true });
            return;
        }

        const script = document.createElement("script");
        script.src = url;
        script.onload = () => {
            script.dataset.loaded = "true";
            resolve();
        };
        script.onerror = () => reject(new Error(`Could not load library: ${url}`));
        document.head.appendChild(script);
    });
}

async function ensurePdfJs() {
    if (!window.pdfjsLib) {
        await loadScript(PDFJS_URL);
    }

    if (!window.pdfjsLib) {
        throw new Error("PDF.js could not be loaded. Check your internet connection and refresh the page.");
    }

    window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER_URL;

    return window.pdfjsLib;
}

async function ensureMammoth() {
    if (!window.mammoth) {
        await loadScript(MAMMOTH_URL);
    }

    if (!window.mammoth) {
        throw new Error("The DOCX extraction library could not be loaded.");
    }

    return window.mammoth;
}

// File selection
fileInput.addEventListener("change", () => {
    acceptFile(fileInput.files[0]);
});

// Drag and drop
["dragenter", "dragover"].forEach(event => {
    dropzone.addEventListener(event, e => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    });
});

["dragleave", "drop"].forEach(event => {
    dropzone.addEventListener(event, e => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
    });
});

dropzone.addEventListener("drop", e => {
    acceptFile(e.dataTransfer.files[0]);
});

function acceptFile(file) {
    formError.textContent = "";

    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["pdf", "docx", "txt"].includes(extension)) {
        return showError("Please upload a PDF, DOCX or TXT file.");
    }

    if (file.size > 5 * 1024 * 1024) {
        return showError("File is larger than 5 MB. Please choose a smaller resume.");
    }

    selectedFile = file;

    fileName.textContent =
        `${file.name} · ${(file.size / 1024).toFixed(0)} KB`;

    analyzeBtn.disabled = false;
}

function showError(message) {
    formError.textContent = message;
}

// Extract PDF text using PDF.js
async function extractPdfText(file) {
    const pdfjs = await ensurePdfJs();

    const buffer = await file.arrayBuffer();
    const data = new Uint8Array(buffer);

    let pdf;

    try {
        pdf = await pdfjs.getDocument({
            data: data
        }).promise;
    } catch (error) {
        console.warn("Normal PDF loading failed. Retrying without worker:", error);

        pdf = await pdfjs.getDocument({
            data: data,
            disableWorker: true,
            isEvalSupported: false
        }).promise;
    }

    const extractedPages = [];

    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
        const page = await pdf.getPage(pageNumber);
        const content = await page.getTextContent();

        const pageText = content.items
            .filter(item => typeof item.str === "string")
            .map(item => item.str)
            .filter(text => text.trim().length > 0)
            .join(" ");

        extractedPages.push(pageText);
    }

    return extractedPages.join("\n");
}

// Extract DOCX text
async function extractDocxText(file) {
    const mammoth = await ensureMammoth();

    const result = await mammoth.extractRawText({
        arrayBuffer: await file.arrayBuffer()
    });

    return result.value || "";
}

// Extract TXT text
async function extractText(file) {
    const extension = file.name.split(".").pop().toLowerCase();

    if (extension === "txt") {
        return await file.text();
    }

    if (extension === "docx") {
        return await extractDocxText(file);
    }

    if (extension === "pdf") {
        return await extractPdfText(file);
    }

    throw new Error("Unsupported file format.");
}

// Analyze resume
analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) {
        return showError("Please select a resume first.");
    }

    formError.textContent = "";
    loading.classList.remove("hidden");
    analyzeBtn.disabled = true;

    try {
        // Extract text
        resumeText = (await extractText(selectedFile)).trim();

        console.log("Selected file:", selectedFile.name);
        console.log("Extracted characters:", resumeText.length);
        console.log("Extracted text:", resumeText.slice(0, 1000));

        if (!resumeText || resumeText.length < 40) {
            throw new Error(
                `Only ${resumeText.length} readable characters were extracted. Try another PDF, DOCX or TXT file.`
            );
        }

        // Match backend maximum length
        if (resumeText.length > 30000) {
            resumeText = resumeText.slice(0, 30000);
        }

        // Send data to FastAPI
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                resumeText: resumeText,
                education: document.getElementById("education").value,
                interests: document.getElementById("interest").value,
                experience: document.getElementById("experience").value
            })
        });

        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error("The server returned an invalid response.");
        }

        if (!response.ok) {
            throw new Error(
                data.error ||
                data.detail ||
                "Resume analysis failed. Please try again."
            );
        }

        renderReport(data);

    } catch (error) {
        console.error("Analysis error:", error);

        showError(
            error.message || "Something went wrong. Please try again."
        );

    } finally {
        loading.classList.add("hidden");
        analyzeBtn.disabled = false;
    }
});

// Validate arrays
function safeArray(value) {
    return Array.isArray(value) ? value : [];
}

// Display report
function renderReport(data) {
    document.getElementById("emptyState").classList.add("hidden");
    document.getElementById("report").classList.remove("hidden");
    document.getElementById("printBtn").disabled = false;

    document.getElementById("profileTitle").textContent =
        data.profileTitle || "Your career profile";

    document.getElementById("profileSummary").textContent =
        data.summary || "Your resume analysis is ready.";

    const score = Math.max(
        0,
        Math.min(100, Number(data.profileStrength) || 0)
    );

    document.getElementById("scoreValue").textContent = score;

    document.getElementById("scoreRing").style.borderColor =
        score >= 75 ? "#73d6b2" :
        score >= 50 ? "#8fa9ff" :
        "#e5b36b";

    fillChips("skillsList", data.skills);
    fillList("gapsList", data.skillGaps);
    fillList("resourcesList", data.learningResources);
    fillList("suggestionsList", data.resumeSuggestions);

    const careers = document.getElementById("careersList");
    careers.innerHTML = "";

    safeArray(data.careerPaths).forEach(item => {
        const card = document.createElement("div");
        card.className = "career-item";

        const title = document.createElement("b");
        title.textContent = item.title || "Career option";

        const description = document.createElement("p");
        description.textContent = item.reason || "";

        const skills = document.createElement("span");
        skills.textContent = item.skillsToLearn
            ? `Focus: ${item.skillsToLearn}`
            : "";

        card.append(title, description, skills);
        careers.appendChild(card);
    });

    document.getElementById("results").scrollIntoView({
        behavior: "smooth"
    });
}

// Display skill chips
function fillChips(id, values) {
    const node = document.getElementById(id);
    node.innerHTML = "";

    safeArray(values).forEach(value => {
        const chip = document.createElement("span");
        chip.className = "chip";
        chip.textContent = value;
        node.appendChild(chip);
    });

    if (!node.children.length) {
        node.textContent = "No specific skills were identified.";
    }
}

// Display recommendation lists
function fillList(id, values) {
    const node = document.getElementById(id);
    node.innerHTML = "";

    safeArray(values).forEach(value => {
        const li = document.createElement("li");
        li.textContent = value;
        node.appendChild(li);
    });

    if (!node.children.length) {
        const li = document.createElement("li");
        li.textContent = "No recommendations available.";
        node.appendChild(li);
    }
}

// Print report
document.getElementById("printBtn").addEventListener("click", () => {
    window.print();
});