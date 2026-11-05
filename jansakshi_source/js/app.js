// JanSakshi AI - Shared JavaScript

// Language switch
function setGlobalLanguage(lang) {
    if (typeof setLanguage === "function") {
        setLanguage(lang);
    }
}

// Category selection
function selectCategoryItem(name, department, officer, sla, card) {
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

// Voice recording button
function toggleVoiceRecordingSimulator() {
    if (typeof toggleVoiceRecording === "function") {
        toggleVoiceRecording();
    }
}

// Photo upload placeholder
function triggerPhotoUploadSim() {
    alert("Photo upload functionality will be connected next.");
}

// Page navigation
function openTrackComplaint(id) {
    if (id) {
        window.location.href =
            "track.html?id=" + encodeURIComponent(id);
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
// JanSakshi AI - Page Navigation

document.addEventListener("DOMContentLoaded", function () {

    const routes = {
        "home": "index.html",
        "register-complaint": "register.html",
        "track-complaint": "track.html",
        "officer-dashboard": "officer.html",
        "citizen-portal": "track.html"
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

});