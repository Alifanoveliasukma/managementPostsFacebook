const apiUrl = "/posts";
let groupsList = [];
let activeGroupDetailId = null;

async function loadGroupsForAssign() {
    const res = await fetch("/groups"); 
    groupsList = await res.json();
}
loadGroupsForAssign();

async function loadPosts(){
  const res = await fetch(apiUrl);
  const data = await res.json();
  const body = document.getElementById("postsBody");
  const total = document.getElementById("totalPosts");
  body.innerHTML = "";
  data.forEach(p => {
    body.innerHTML += `
      <tr>
        <td>${p.title}</td>
        <td>${p.content}</td>
        <td>${p.groups.length ? p.groups.join(", ") : "belum dikaitkan"}</td>
        <td class="actions">
          <button class="btn btn-sm btn-ghost" onclick="editPost(${p.id}, '${p.title}', \`${p.content}\`)">Edit</button>
          <button class="btn btn-sm btn-ghost" onclick="toggleDetail(${p.id})">Detail</button>
          <button class="btn btn-sm btn-danger" onclick="deletePost(${p.id})">Delete</button>
        </td>
      </tr>
    `;
  });
  total.textContent = "Total: " + data.length;
}

async function submitPost(e){
  e.preventDefault();
  const id = document.getElementById("postId").value;

  const formData = new FormData();
  formData.append("title", document.getElementById("title").value);
  formData.append("content", document.getElementById("content").value);

  const method = id ? "PUT" : "POST";
  const url = id ? `${apiUrl}/${id}` : apiUrl;

  try {
        const res = await fetch(url, { method, body: formData });
        const data = await res.json();

        if (!res.ok) {
        alert(data.error || "Id tidak boleh sama!");
        return;
        }

        alert("Pengaturan Post berhasil disimpan!");
        resetPostForm();
        loadPosts();
    } catch (err) {
        alert("Error koneksi ke server!");
        console.error(err);
    }
}

function editPost(id, title, content){
  document.getElementById("formTitle").textContent = "Edit Post";
  document.getElementById("postId").value = id;
  document.getElementById("title").value = title;
  document.getElementById("content").value = content;
}

async function deletePost(id){
  if(confirm("Yakin ingin menghapus post ini?")){
    await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
    loadPosts();
  }
}

function resetPostForm(){
  document.getElementById("formTitle").textContent = "Add Post";
  document.getElementById("postId").value = "";
  document.getElementById("postForm").reset();
}

function filterPosts(){
  const input = document.getElementById("searchInput").value.toLowerCase();
  const rows = document.querySelectorAll("#postsBody tr");
  rows.forEach(r => {
    const text = r.innerText.toLowerCase();
    r.style.display = text.includes(input) ? "" : "none";
  });
}

function openAssignModal(postId){
  document.getElementById("assignPostId").value = postId;
  document.getElementById("assignModal").classList.add("open");
}

function closeAssignModal(){
  document.getElementById("assignModal").classList.remove("open");
}

async function toggleDetail(postId){
  const detailDiv = document.getElementById("postDetail");
  const groupDetailDiv = document.getElementById("groupDetail") || document.createElement('div');
  groupDetailDiv.id = "groupDetail";

  groupDetailDiv.innerHTML = '';
  activeGroupDetailId = null;

  // // pastikan groupsList sudah ada
  // if (!groupsList.length) {
  //   await loadGroupsForAssign();
  // }

  // Ambil data post by ID
  const res = await fetch(`/posts/${postId}`);
  if (!res.ok) {
        alert("Gagal memuat detail post.");
        return;
  }
  const post = await res.json();

  if (!groupsList.length) {
        await loadGroupsForAssign();
  }

  const groupCheckboxes = groupsList.map(g => {
        // Cek apakah post.groups (daftar nama grup) mengandung nama grup ini
        const isAssigned = post.groups.includes(g.name); 
        
        // Tombol Detail Grup
        const detailButton = `<button class="btn btn-sm btn-ghost" onclick="toggleGroupDetail(${g.id})">Detail Grup</button>`;
        
        return `
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
                <label>
                    <input type="checkbox" value="${g.id}" ${isAssigned ? 'checked' : ''}>
                    ${g.name}
                </label>
                ${detailButton}
            </div>
        `;
  }).join("");

  // Render card detail
  detailDiv.innerHTML = `
    <div class="card">
      <h3>Detail Post</h3>
      <p><b>Title:</b> ${post.title}</p>
      <p><b>Content:</b> ${post.content}</p>
      <p><b>Groups:</b> ${post.groups.length ? post.groups.join(", ") : "(belum dikaitkan)"}</p>

      <hr style="margin: 15px 0;" />
      <h4>Kaitkan ke Group</h4>
      <div id="assignGroupsContainer" style="max-height: 200px; overflow-y: auto; padding: 10px; border: 1px solid var(--border-color); border-radius: 4px;">
          ${groupCheckboxes}
      </div>
      <div style="margin-top:15px; display: flex; gap: 10px;">
          <button class="btn btn-primary" onclick="submitAssignDetail(${post.id})">Simpan Kaitkan</button>
      </div>
  </div>
  `;
  if (!document.getElementById("groupDetail")) {
        detailDiv.after(groupDetailDiv);
  }
}

async function submitAssignDetail(postId){
  const selected = Array.from(document.querySelectorAll("#assignGroupsContainer input[type='checkbox']:checked")).map(o => o.value);

  const res = await fetch(`/posts/${postId}/assign`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ group_ids: selected })
  });

  const data = await res.json();
  alert(data.message);
  loadPosts();
  toggleDetail(postId); // refresh detail biar groups update
}

// let groupsList = [];

async function toggleGroupDetail(groupId) {
    const groupDetailDiv = document.getElementById("groupDetail");

    // Jika detail grup yang sama sedang aktif, tutup
    if (activeGroupDetailId === groupId) {
        groupDetailDiv.innerHTML = '';
        activeGroupDetailId = null;
        return;
    }
    
    // Asumsi ada endpoint GET /groups/{id} di backend Flask Anda
    const res = await fetch(`/groups/${groupId}`);
    if (!res.ok) {
        alert("Gagal memuat detail grup.");
        return;
    }
    const group = await res.json();
    
    // Render card detail Grup
    groupDetailDiv.innerHTML = `
        <div class="card" style="margin-top:20px; border-left: 5px solid #007bff;">
            <h3>Detail Group: ${group.name}</h3>
            <p><b>ID:</b> ${group.id}</p>
            <p><b>Deskripsi:</b> ${group.description || "Tidak ada deskripsi."}</p>
            <button class="btn btn-ghost" onclick="toggleGroupDetail(${groupId})">Tutup Detail Grup</button>
        </div>
    `;
    activeGroupDetailId = groupId;
}


// ... (loadGroupsForAssign dan loadPosts di akhir - TETAP) ...

loadPosts();