const apiUrl = "/groups";

async function loadGroups(){
  const res = await fetch(apiUrl);
  const data = await res.json();
  const body = document.getElementById("groupsBody");
  const total = document.getElementById("totalGroups");
  body.innerHTML = "";
  data.forEach(g => {
    body.innerHTML += `
      <tr>
        <td>
            <img src="${g.icon_url}" alt="icon" style="width:24px;height:24px;border-radius:50%;margin-right:6px;">
        </td>
        <td>${g.name}</td>
        <td>${g.fb_group_id}</td>
        <td class="actions">
            <button class="btn btn-sm btn-ghost" onclick="showDetail(\`${g.name}\`,\`${g.fb_group_id}\`,\`${g.description || ''}\`,\`${g.rules || ''}\`, \`${g.icon_url || ''}\`)">Detail</button>
            <button class="btn btn-sm btn-ghost" onclick="editGroup(${g.id}, '${g.name}', '${g.fb_group_id}', '${g.description}', \`${g.rules||''}\`)">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deleteGroup(${g.id})">Delete</button>
        </td>
      </tr>
    `;
  });
  total.textContent = "Total: " + data.length;
}

async function submitForm(e){
  e.preventDefault();
  const id = document.getElementById("groupId").value;

  const formData = new FormData();
  formData.append("name", document.getElementById("name").value);
  formData.append("fb_group_id", document.getElementById("fb_group_id").value);
  formData.append("description", document.getElementById("description").value);
  formData.append("rules", document.getElementById("rules").value);

  const icon_url = document.getElementById("icon_url").files[0]; 
  if (icon_url) {
    formData.append("icon_url", icon_url);
  }
  
const method = id ? "PUT" : "POST";
  const url = id ? `${apiUrl}/${id}` : apiUrl;

  try {
    const res = await fetch(url, { method, body: formData });
    const data = await res.json();

    if (!res.ok) {
      alert(data.error || "Id tidak boleh sama!");
      return;
    }

    alert("Grup berhasil disimpan!");
    resetForm();
    loadGroups();
  } catch (err) {
    alert("Error koneksi ke server!");
    console.error(err);
  }
}

function showDetail(icon_url, name, fb_group_id, description, rules){
  document.getElementById("detailIconUrl").src = icon_url;
  document.getElementById("detailName").textContent = name;
  document.getElementById("detailGroupId").textContent = fb_group_id;
  document.getElementById("detailDescription").textContent = description || "-";
  document.getElementById("detailRules").textContent = rules || "-";
  document.getElementById("detailModal").classList.add("open");
}

function closeDetail(){
  document.getElementById("detailModal").classList.remove("open");
}

function editGroup(id, icon_url, name, fb_group_id, description, rules){
  document.getElementById("formTitle").textContent = "Edit Group";
  document.getElementById("groupId").value = id;
  document.getElementById("icon_url").value = ""; // file input tidak bisa diisi manual
  document.getElementById("name").value = name;
  document.getElementById("fb_group_id").value = fb_group_id;
  document.getElementById("description").value = description;
  document.getElementById("rules").value = rules;

  if (icon_url) {
      document.getElementById("detailIconUrl").src = icon_url;
  }
}

async function deleteGroup(id){
  if(confirm("Yakin ingin menghapus grup ini?")){
      await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
      loadGroups();
  }
}

function resetForm(){
  document.getElementById("formTitle").textContent = "Add Group";
  document.getElementById("groupId").value = "";
  document.getElementById("groupForm").reset();
}

function filterGroups(){
  const input = document.getElementById("searchInput").value.toLowerCase();
  const rows = document.querySelectorAll("#groupsBody tr");
  rows.forEach(r => {
      const text = r.innerText.toLowerCase();
      r.style.display = text.includes(input) ? "" : "none";
  });
}

// panggil saat page load
loadGroups();
