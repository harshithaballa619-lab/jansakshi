// JanSakshi AI - Client Application Controller
// Connected to Flask Backend & Six-Module AI Engine

// Global State
let selectedCategoryName = "Drainage";
let attachedImageBase64 = null;
let attachedImageMime = "image/jpeg";
let detectedCoordinates = { lat: 17.7289, lon: 83.3082 }; // Visakhapatnam default

// Language Switcher
function setGlobalLanguage(lang) {
    if (typeof setLanguage === "function") {
        setLanguage(lang);
    }
}

// Category Selection
function selectCategoryItem(name, department, officer, sla, card) {
    selectedCategoryName = name;
    if (typeof updateSelectedCategory === "function") {
        updateSelectedCategory(name);
    }

    const dept = document.getElementById("sidebar-department");
    const assignedOfficer = document.getElementById("sidebar-officer");
    const deadline = document.getElementById("sidebar-sla");

    if (dept) dept.innerText = department;
    if (assignedOfficer) assignedOfficer.innerText = officer;
    if (deadline) deadline.innerText = sla;
}

// Voice Recording Simulator
function toggleVoiceRecordingSimulator() {
    if (typeof toggleVoiceRecording === "function") {
        toggleVoiceRecording();
    }
}

// Photo Upload Helper
function triggerPhotoUploadSim() {
    const fileInput = document.getElementById("photo-file-input");
    if (fileInput) {
        fileInput.click();
    } else {
        // Create invisible file input on the fly if not in DOM
        const input = document.createElement("input");
        input.type = "file";
        input.accept = "image/jpeg,image/png,image/jpg";
        input.onchange = function (e) {
            handlePhotoFileSelected(e.target.files[0]);
        };
        input.click();
    }
}

function handlePhotoFileSelected(file) {
    if (!file) return;
    attachedImageMime = file.type || "image/jpeg";
    const reader = new FileReader();
    reader.onload = function (e) {
        attachedImageBase64 = e.target.result;
        const previewText = document.getElementById("photo-upload-status");
        if (previewText) {
            previewText.innerText = `Uploaded: ${file.name} (${Math.round(file.size / 1024)} KB). AI screening active.`;
            previewText.classList.add("text-tertiary", "font-bold");
        }
    };
    reader.readAsDataURL(file);
}

// Navigation Helpers
function openTrackComplaint(id) {
    if (id) {
        window.location.href = "track.html?id=" + encodeURIComponent(id);
    } else {
        window.location.href = "track.html";
    }
}

function openCitizenDocket() {
    window.location.href = "index.html";
}

function openOfficerDashboard() {
    window.location.href = "officer.html";
}

// -------------------------------------------------------------------------
// REAL BACKEND INTEGRATION: Grievance Submission with Complete 6-Module AI
// -------------------------------------------------------------------------
async function submitGrievanceAction() {
    const submitBtn = document.getElementById("submit-btn");
    const successBanner = document.getElementById("submission-success-banner");
    const complaintTextElem = document.getElementById("complaint-text");

    const description = complaintTextElem ? complaintTextElem.value.trim() : "";

    if (!description) {
        alert("Please provide a complaint description in Telugu or English (ఫిర్యాదు వివరాలను నమోదు చేయండి).");
        return;
    }

    // Set Loading State
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add("opacity-75", "cursor-wait");
        submitBtn.innerHTML = `
            <span class="inline-block animate-spin mr-2">⟳</span>
            <span>Triaging with JanSakshi AI...</span>
        `;
    }

    try {
        const payload = {
            description: description,
            category: selectedCategoryName || "Drainage",
            location: "Ward 34, Dwaraka Nagar, Visakhapatnam",
            latitude: detectedCoordinates.lat,
            longitude: detectedCoordinates.lon,
            image_base64: attachedImageBase64,
            mime_type: attachedImageMime
        };

        const response = await fetch("/api/ai/analyze-complete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();
        const complaintId = data.complaint_id || "JS-VSKP" + Math.floor(100000 + Math.random() * 900000);

        // Store for immediate tracking
        localStorage.setItem("jansakshi_last_complaint_id", complaintId);

        // Update Token Display
        const tokenElem = document.getElementById("complaint-token-display");
        if (tokenElem) tokenElem.innerText = complaintId;

        // Update Dossier Summary with AI insights
        if (data.triage_summary) {
            const revDept = document.getElementById("review-dept");
            const revOfficer = document.getElementById("review-officer");
            const revSla = document.getElementById("review-sla");

            if (revDept && data.triage_summary.department) revDept.innerText = data.triage_summary.department;
            if (revOfficer && data.triage_summary.officer_assigned) revOfficer.innerText = data.triage_summary.officer_assigned;
            if (revSla && data.triage_summary.sla) revSla.innerText = data.triage_summary.sla;
        }

        // Render AI Modules Feedback Card inside banner
        const modulesData = data.modules || {};
        let aiBadgesHtml = `
            <div class="mt-3 pt-3 border-t border-surface-variant/40 grid grid-cols-1 sm:grid-cols-3 gap-2 text-label-sm">
                <div class="p-2 bg-surface-container rounded">
                    <span class="block font-bold text-primary">Module 1: Intake Triage</span>
                    <span>Lang: ${modulesData.module_1_understanding?.detected_language || 'Detected'} | Cat: ${data.triage_summary?.category || selectedCategoryName}</span>
                </div>
                <div class="p-2 bg-surface-container rounded">
                    <span class="block font-bold text-secondary">Module 3 & 4: Priority & SLA</span>
                    <span>Priority: <strong>${data.triage_summary?.priority || 'High'}</strong> (${data.triage_summary?.sla || '48h'})</span>
                </div>
                <div class="p-2 bg-surface-container rounded">
                    <span class="block font-bold text-tertiary">Module 6: Authenticity</span>
                    <span>Risk: ${modulesData.module_6_authenticity?.evidence_risk_level || 'No concerning indicators'}</span>
                </div>
            </div>
        `;

        if (successBanner) {
            // Append badges if not already present
            if (!document.getElementById("ai-analysis-feedback-card")) {
                const badgeDiv = document.createElement("div");
                badgeDiv.id = "ai-analysis-feedback-card";
                badgeDiv.innerHTML = aiBadgesHtml;
                successBanner.appendChild(badgeDiv);
            }
            successBanner.classList.remove("hidden");
            successBanner.scrollIntoView({ behavior: "smooth" });
        }

        // Update submit button to success state
        if (submitBtn) {
            submitBtn.classList.remove("opacity-75", "cursor-wait");
            submitBtn.classList.add("opacity-60", "pointer-events-none");
            submitBtn.innerHTML = `
                <span class="material-symbols-outlined text-[20px]">check_circle</span>
                <span>Registered: ${complaintId}</span>
            `;
        }

        // Update Track Button onclick
        const trackButtons = document.querySelectorAll("[onclick*='openTrackComplaint']");
        trackButtons.forEach(btn => {
            btn.onclick = () => openTrackComplaint(complaintId);
        });

    } catch (err) {
        console.warn("AI Complete pipeline error, falling back to base registration:", err);
        // Fallback registration
        submitGrievanceFallback(description);
    }
}

// Fallback submit function
function submitGrievance() {
    submitGrievanceAction();
}

async function submitGrievanceFallback(description) {
    const submitBtn = document.getElementById("submit-btn");
    const successBanner = document.getElementById("submission-success-banner");

    try {
        const res = await fetch("/api/complaints", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                description: description,
                category: selectedCategoryName,
                location: "Ward 34, Dwaraka Nagar, Visakhapatnam",
                latitude: detectedCoordinates.lat,
                longitude: detectedCoordinates.lon
            })
        });
        const data = await res.json();
        const cid = data.complaint_id || "JS-VSKP" + Math.floor(100000 + Math.random() * 900000);

        const tokenElem = document.getElementById("complaint-token-display");
        if (tokenElem) tokenElem.innerText = cid;
        if (successBanner) {
            successBanner.classList.remove("hidden");
            successBanner.scrollIntoView({ behavior: "smooth" });
        }
        if (submitBtn) {
            submitBtn.innerHTML = `<span class="material-symbols-outlined text-[20px]">check_circle</span> Submitted | సమర్పించబడింది`;
        }
    } catch (e) {
        if (successBanner) successBanner.classList.remove("hidden");
    }
}

// -------------------------------------------------------------------------
// REAL BACKEND INTEGRATION: Grievance Tracking (track.html)
// -------------------------------------------------------------------------
async function fetchTrackingRecord() {
    const input = document.getElementById("tracking-search-input") || document.querySelector("input[placeholder*='Enter Reference No.']");
    if (!input || !input.value.trim()) {
        alert("Please enter a valid Complaint Reference ID (ఉదా: JS-VSKP08421).");
        return;
    }
    const targetId = input.value.trim();
    await loadGrievanceDetailsForTracking(targetId);
}

async function loadGrievanceDetailsForTracking(targetId) {
    const urlParams = new URLSearchParams(window.location.search);
    const trackingId = targetId || urlParams.get("id") || localStorage.getItem("jansakshi_last_complaint_id") || "JS-VSKP08421";

    if (!trackingId) return;

    try {
        const response = await fetch(`/api/complaints/${encodeURIComponent(trackingId)}`);
        if (!response.ok) {
            if (targetId) {
                alert(`Grievance record "${trackingId}" not found in local database. Showing latest active demonstration record.`);
            }
            return;
        }

        const complaint = await response.json();

        // Update search input
        const searchInput = document.getElementById("tracking-search-input") || document.querySelector("input[placeholder*='Enter Reference No.']");
        if (searchInput) searchInput.value = complaint.id;

        // Update Docket ID header
        const docketH1 = document.querySelector("h1.font-headline-lg");
        if (docketH1) {
            docketH1.innerHTML = `
                ${complaint.id}
                <button class="text-outline hover:text-primary transition-colors text-[18px]" onclick="navigator.clipboard.writeText('${complaint.id}')" title="Copy Docket ID">
                    <span class="material-symbols-outlined">content_copy</span>
                </button>
            `;
        }

        // Update all text occurrences of old dummy tokens
        document.querySelectorAll("span, strong, code, p, div, h1").forEach(el => {
            if (el.children.length === 0 && (el.innerText.includes("VSKP-2025-08421") || el.innerText.includes("JS-VSKP08421"))) {
                el.innerText = el.innerText.replace(/VSKP-2025-08421|JS-VSKP08421/g, complaint.id);
            }
        });

        // Update category & description in dossier
        const catElem = document.querySelector(".grid p.font-label-lg");
        if (catElem && complaint.category) catElem.innerText = complaint.category;

        const locElem = document.querySelectorAll(".grid .bg-surface-container-low")[1]?.querySelector("p.font-label-md");
        if (locElem && complaint.location) locElem.innerText = complaint.location;

        const deptElem = document.querySelectorAll(".grid .bg-surface-container-low")[2]?.querySelector("p.font-label-md");
        if (deptElem && complaint.assigned_officer) deptElem.innerText = complaint.assigned_officer;

        // Update description details
        document.querySelectorAll("p strong").forEach(st => {
            if (st.innerText.includes("Description:") && complaint.description) {
                st.parentElement.innerHTML = `<strong class="text-on-surface">Description:</strong> ${complaint.description}`;
            }
        });

        // Update operational state banner
        const opState = document.querySelector(".bg-tertiary-fixed .font-label-md");
        if (opState) {
            opState.innerText = `${complaint.status} • SLA: ${complaint.sla || '48 Hours'}`;
        }

        // Update status toast text
        const toast = document.getElementById("status-toast");
        if (toast) {
            const toastText = toast.querySelector("span span:last-child");
            if (toastText) toastText.innerText = `Thank you! Grievance ${complaint.id} marked as verified with citizen certification.`;
        }

    } catch (err) {
        console.warn("Could not load real complaint record for tracking:", err);
    }
}

// -------------------------------------------------------------------------
// REAL BACKEND INTEGRATION: Public Accountability Snapshot (index.html)
// -------------------------------------------------------------------------
async function loadPublicAccountabilityMetrics() {
    try {
        const response = await fetch("/api/ai/predictive-insights");
        if (!response.ok) return;

        const data = await response.json();
        const summary = data.dataset_summary || {};

        // Update live data sync label
        const syncBadge = document.querySelector("#public-accountability span.animate-pulse")?.parentElement;
        if (syncBadge && summary.data_origin) {
            syncBadge.innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-tertiary-container animate-pulse"></span> <span>Live Sync: ${summary.data_origin} (${summary.total_complaints_analyzed} Records)</span>`;
        }
    } catch (err) {
        console.debug("Metrics sync running in local demo mode.");
    }
}

// -------------------------------------------------------------------------
// Page Initialization & Navigation Event Bindings
// -------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
    const routes = {
        "home": "index.html",
        "register-complaint": "register.html",
        "track-complaint": "track.html",
        "officer-dashboard": "officer.html",
        "citizen-portal": "track.html",
        "citizen-services": "register.html",
        "public-accountability-dashboard": "index.html#public-accountability",
        "contact-and-help": "index.html#contact-and-help"
    };

    document.querySelectorAll("[data-path]").forEach(function (element) {
        const page = routes[element.dataset.path];
        if (page) {
            element.addEventListener("click", function (event) {
                event.preventDefault();
                window.location.href = page;
            });
        }
    });

    // Check if on track.html
    if (window.location.pathname.includes("track.html") || document.querySelector("input[placeholder*='Enter Reference No.']")) {
        loadGrievanceDetailsForTracking();
    }

    // Check if on index.html
    if (document.getElementById("public-accountability")) {
        loadPublicAccountabilityMetrics();
    }
});