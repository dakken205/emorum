const deleteTargets = document.querySelectorAll("[id^='delete-target']");
for (const target of deleteTargets) {
  target.addEventListener("click", (e) => {
    e.preventDefault();
    const postID = target.id.split("-")[2]; // expect: delete-target-\d+
    deletePost(postID);
  });
}

function deletePost(postId) {
  if (!confirm("本当に削除しますか？")) return;

  fetch(`/posts/${postId}/`, {
    method: "DELETE",
  }).then((res) => {
    res.json().then((data) => {
      if (data.ok) {
        window.location.href = "/";
      } else {
        alert(data.msg);
      }
    });
  });
}
