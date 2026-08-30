// ---------------------------------------------------------------------------
// Student Management System — frontend logic
// Talks to the FastAPI backend at the same origin (relative URLs), so this
// works whether FastAPI serves this file directly or you open it separately
// and point API_BASE at http://127.0.0.1:8000.
// ---------------------------------------------------------------------------

const API_BASE = "/students/";

// Pagination / filter state
const state = {
  skip: 0,
  limit: 10,
  search: "",
  course: "",
  department: "",
  semester: "",
  total: 0,
};

let deleteTargetId = null;

// --- DOM references ---------------------------------------------------
const tableBody = document.getElementById("studentTableBody");
const totalCountEl = document.getElementById("totalCount");
const shownCountEl = document.getElementById("shownCount");
const messageBanner = document.getElementById("messageBanner");
const pageInfo = document.getElementById("pageInfo");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

const searchInput = document.getElementById("searchInput");
const courseFilter = document.getElementById("courseFilter");
const departmentFilter = document.getElementById("departmentFilter");
const semesterFilter = document.getElementById("semesterFilter");
const clearFiltersBtn = document.getElementById("clearFiltersBtn");

const modalOverlay = document.getElementById("modalOverlay");
const modalTitle = document.getElementById("modalTitle");
const studentForm = document.getElementById("studentForm");
const addBtn = document.getElementById("addBtn");
const modalCloseBtn = document.getElementById("modalCloseBtn");
const cancelBtn = document.getElementById("cancelBtn");

const deleteOverlay = document.getElementById("deleteOverlay");
const deleteCancelBtn = document.getElementById("deleteCancelBtn");
const deleteConfirmBtn = document.getElementById("deleteConfirmBtn");

// --- Helpers ------------------------------------------------------------

function showMessage(text, type = "success") {
  messageBanner.textContent = text;
  messageBanner.className = `message ${type}`;
  messageBanner.classList.remove("hidden");
  window.clearTimeout(showMessage._t);
  showMessage._t = window.setTimeout(() => {
    messageBanner.classList.add("hidden");
  }, 4000);
}

function clearFieldErrors() {
  document.querySelectorAll(".field-error").forEach((el) => (el.textContent = ""));
}

function buildQueryParams() {
  const params = new URLSearchParams();
  params.set("skip", state.skip);
  params.set("limit", state.limit);
  if (state.search) params.set("search", state.search);
  if (state.course) params.set("course", state.course);
  if (state.department) params.set("department", state.department);
  if (state.semester) params.set("semester", state.semester);
  return params.toString();
}

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// --- API calls ------------------------------------------------------------

async function fetchStudents() {
  tableBody.innerHTML = `<tr><td colspan="9" class="empty-state">Loading students…</td></tr>`;
  try {
    const res = await fetch(`${API_BASE}?${buildQueryParams()}`);
    if (!res.ok) throw new Error(`Failed to load students (${res.status})`);
    const data = await res.json();
    state.total = data.total;
    renderTable(data.items);
    renderStats(data);
    renderPagination(data);
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="9" class="empty-state">Could not load students. Is the backend running?</td></tr>`;
    showMessage(err.message || "Something went wrong loading students", "error");
  }
}

async function saveStudent(payload, studentId) {
  const url = studentId ? `${API_BASE}${studentId}` : API_BASE;
  const method = studentId ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const err = new Error(data.detail || "Could not save student");
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data;
}

async function deleteStudentById(id) {
  const res = await fetch(`${API_BASE}${id}`, { method: "DELETE" });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Could not delete student");
  return data;
}

// --- Rendering ------------------------------------------------------------

function renderStats(data) {
  totalCountEl.textContent = data.total;
  shownCountEl.textContent = data.items.length;
}

function renderTable(items) {
  if (!items.length) {
    tableBody.innerHTML = `<tr><td colspan="9" class="empty-state">No students found. Try adjusting your search or filters.</td></tr>`;
    return;
  }

  tableBody.innerHTML = items
    .map(
      (s) => `
      <tr>
        <td>${s.id}</td>
        <td>${escapeHtml(s.name)}</td>
        <td>${s.age}</td>
        <td>${escapeHtml(s.email)}</td>
        <td>${escapeHtml(s.phone || "—")}</td>
        <td>${escapeHtml(s.course)}</td>
        <td>${escapeHtml(s.department || "—")}</td>
        <td>${s.semester ?? "—"}</td>
        <td>
          <div class="row-actions">
            <button class="btn btn-secondary btn-small" onclick="openEditModal(${s.id})">Edit</button>
            <button class="btn btn-danger btn-small" onclick="openDeleteModal(${s.id})">Delete</button>
          </div>
        </td>
      </tr>`
    )
    .join("");
}

function renderPagination(data) {
  const currentPage = Math.floor(state.skip / state.limit) + 1;
  const totalPages = Math.max(1, Math.ceil(data.total / state.limit));
  pageInfo.textContent = `Page ${currentPage} of ${totalPages} (${data.total} total)`;
  prevBtn.disabled = state.skip === 0;
  nextBtn.disabled = state.skip + state.limit >= data.total;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// --- Modal (Add / Edit) ----------------------------------------------------

function openAddModal() {
  studentForm.reset();
  document.getElementById("studentId").value = "";
  modalTitle.textContent = "Add Student";
  clearFieldErrors();
  modalOverlay.classList.remove("hidden");
}

async function openEditModal(id) {
  clearFieldErrors();
  try {
    const res = await fetch(`${API_BASE}${id}`);
    if (!res.ok) throw new Error("Could not load student details");
    const s = await res.json();

    document.getElementById("studentId").value = s.id;
    document.getElementById("name").value = s.name;
    document.getElementById("age").value = s.age;
    document.getElementById("email").value = s.email;
    document.getElementById("phone").value = s.phone || "";
    document.getElementById("course").value = s.course;
    document.getElementById("department").value = s.department || "";
    document.getElementById("semester").value = s.semester ?? "";

    modalTitle.textContent = `Edit Student #${s.id}`;
    modalOverlay.classList.remove("hidden");
  } catch (err) {
    showMessage(err.message, "error");
  }
}

function closeModal() {
  modalOverlay.classList.add("hidden");
}

// --- Delete confirm modal ---------------------------------------------

function openDeleteModal(id) {
  deleteTargetId = id;
  deleteOverlay.classList.remove("hidden");
}

function closeDeleteModal() {
  deleteTargetId = null;
  deleteOverlay.classList.add("hidden");
}

// --- Event handlers ------------------------------------------------------

addBtn.addEventListener("click", openAddModal);
modalCloseBtn.addEventListener("click", closeModal);
cancelBtn.addEventListener("click", closeModal);
modalOverlay.addEventListener("click", (e) => {
  if (e.target === modalOverlay) closeModal();
});

deleteCancelBtn.addEventListener("click", closeDeleteModal);
deleteOverlay.addEventListener("click", (e) => {
  if (e.target === deleteOverlay) closeDeleteModal();
});

deleteConfirmBtn.addEventListener("click", async () => {
  if (deleteTargetId == null) return;
  try {
    await deleteStudentById(deleteTargetId);
    showMessage("Student deleted successfully", "success");
    closeDeleteModal();
    fetchStudents();
  } catch (err) {
    showMessage(err.message, "error");
    closeDeleteModal();
  }
});

studentForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearFieldErrors();

  const studentId = document.getElementById("studentId").value || null;

  const payload = {
    name: document.getElementById("name").value.trim(),
    age: Number(document.getElementById("age").value),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim() || null,
    course: document.getElementById("course").value.trim(),
    department: document.getElementById("department").value.trim() || null,
    semester: document.getElementById("semester").value
      ? Number(document.getElementById("semester").value)
      : null,
  };

  const submitBtn = document.getElementById("submitBtn");
  submitBtn.disabled = true;
  submitBtn.textContent = "Saving…";

  try {
    await saveStudent(payload, studentId);
    showMessage(
      studentId ? "Student updated successfully" : "Student added successfully",
      "success"
    );
    closeModal();
    fetchStudents();
  } catch (err) {
    if (err.status === 422 && err.data?.detail) {
      // FastAPI validation errors: show under the right field when possible
      const details = Array.isArray(err.data.detail) ? err.data.detail : [];
      details.forEach((d) => {
        const field = d.loc?.[d.loc.length - 1];
        const el = document.getElementById(`err-${field}`);
        if (el) el.textContent = d.msg;
      });
      if (!details.length) showMessage(err.message, "error");
    } else {
      showMessage(err.message, "error");
    }
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Save Student";
  }
});

// --- Search & filters ---------------------------------------------------

const debouncedSearch = debounce(() => {
  state.search = searchInput.value.trim();
  state.skip = 0;
  fetchStudents();
}, 350);

searchInput.addEventListener("input", debouncedSearch);

[courseFilter, departmentFilter, semesterFilter].forEach((el) => {
  el.addEventListener(
    "input",
    debounce(() => {
      state.course = courseFilter.value.trim();
      state.department = departmentFilter.value.trim();
      state.semester = semesterFilter.value.trim();
      state.skip = 0;
      fetchStudents();
    }, 350)
  );
});

clearFiltersBtn.addEventListener("click", () => {
  searchInput.value = "";
  courseFilter.value = "";
  departmentFilter.value = "";
  semesterFilter.value = "";
  state.search = state.course = state.department = state.semester = "";
  state.skip = 0;
  fetchStudents();
});

// --- Pagination controls ---------------------------------------------

prevBtn.addEventListener("click", () => {
  state.skip = Math.max(0, state.skip - state.limit);
  fetchStudents();
});

nextBtn.addEventListener("click", () => {
  if (state.skip + state.limit < state.total) {
    state.skip += state.limit;
    fetchStudents();
  }
});

// --- Init ------------------------------------------------------------

fetchStudents();
