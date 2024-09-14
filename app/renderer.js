document.getElementById("IG_BTN").addEventListener("click", function () {
  const tf = document.getElementById("IG_TF");
  const scroll = document.getElementById("IG_SCROLL");
  const follower = document.getElementById("IG_FOLLOWER");
  const following = document.getElementById("IG_FOLLOWING");
  const posts = document.getElementById("IG_POSTS");

  window.electronAPI.igFollow(
    tf.value,
    scroll.value,
    follower.value,
    following.value,
    posts.value
  );
});

document.getElementById("LI_BTN").addEventListener("click", function () {
  const keywords = document.getElementById("LI_KEYWORDS");
  const pages = document.getElementById("LI_PAGES");

  window.electronAPI.liConnect(encodeURIComponent(keywords.value), pages.value);
});

document.getElementById("FB_BTN").addEventListener("click", function () {
  const group_id = document.getElementById("FB_GID");
  const scroll = document.getElementById("FB_SCROLL");

  window.electronAPI.fbInvite(group_id.value, scroll.value);
});

document.getElementById("TX_BTN").addEventListener("click", function () {
  window.electronAPI.txFollow();
});

document.getElementById("FB_UF").addEventListener("click", function () {
  window.electronAPI.fbUnfriend();
});
